package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.AdminDashboardStatsDto;
import com.example.movieticketbooking.dto.BookingRequest;
import com.example.movieticketbooking.dto.BookingResponse;
import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.entity.*;
import com.example.movieticketbooking.exception.BookingException;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.exception.SeatAlreadyBookedException;
import com.example.movieticketbooking.repository.*;
import com.example.movieticketbooking.service.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class BookingServiceImpl implements BookingService {

    private static final Logger logger = LoggerFactory.getLogger(BookingServiceImpl.class);

    private final BookingRepository bookingRepository;
    private final BookingSeatRepository bookingSeatRepository;
    private final UserRepository userRepository;
    private final ShowRepository showRepository;
    private final SeatRepository seatRepository;
    private final MovieRepository movieRepository;
    private final TheatreRepository theatreRepository;
    private final SeatRecommendationService seatRecommendationService;
    private final PaymentService paymentService;

    public BookingServiceImpl(BookingRepository bookingRepository,
                              BookingSeatRepository bookingSeatRepository,
                              UserRepository userRepository,
                              ShowRepository showRepository,
                              SeatRepository seatRepository,
                              MovieRepository movieRepository,
                              TheatreRepository theatreRepository,
                              SeatRecommendationService seatRecommendationService,
                              PaymentService paymentService) {
        this.bookingRepository = bookingRepository;
        this.bookingSeatRepository = bookingSeatRepository;
        this.userRepository = userRepository;
        this.showRepository = showRepository;
        this.seatRepository = seatRepository;
        this.movieRepository = movieRepository;
        this.theatreRepository = theatreRepository;
        this.seatRecommendationService = seatRecommendationService;
        this.paymentService = paymentService;
    }

    /**
     * DOUBLE BOOKING PROTECTION:
     * 1. Uses @Transactional with SERIALIZABLE isolation where supported.
     * 2. Synchronizes on Show ID / atomic checking against active booking seats.
     * 3. Database unique constraint on (show_id, seat_id) acts as hard safety net.
     * 4. If seat is already booked: Finds nearest vacant seat and throws SeatAlreadyBookedException (HTTP 409).
     */
    @Override
    @Transactional(isolation = Isolation.SERIALIZABLE)
    public synchronized BookingResponse createBooking(Long userId, BookingRequest request) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + userId));

        Show show = showRepository.findById(request.getShowId())
                .orElseThrow(() -> new ResourceNotFoundException("Show not found with id: " + request.getShowId()));

        if (request.getSeatIds() == null || request.getSeatIds().isEmpty()) {
            throw new BookingException("Please select at least one seat to book.");
        }

        // 1. Check if ANY of the requested seats are already booked
        for (Long seatId : request.getSeatIds()) {
            Optional<BookingSeat> existingBookingSeat = bookingSeatRepository
                    .findByShowIdAndSeatIdAndStatus(show.getId(), seatId, BookingStatus.CONFIRMED);

            if (existingBookingSeat.isPresent()) {
                Seat bookedSeat = seatRepository.findById(seatId)
                        .orElseThrow(() -> new ResourceNotFoundException("Seat not found with id: " + seatId));

                String seatIdentifier = bookedSeat.getRowName() + bookedSeat.getSeatNumber();

                // Find automatic nearest vacant recommendation
                Optional<SeatDto> recommendedSeat = seatRecommendationService.findNearestAvailableSeat(show.getId(), seatId);

                String message = "Seat " + seatIdentifier + " is no longer available.";
                if (recommendedSeat.isPresent()) {
                    message += " Nearest available seat is " + recommendedSeat.get().getSeatIdentifier() + ".";
                }

                logger.warn("Double booking prevented! Seat {} is already booked for show {}.", seatIdentifier, show.getId());
                throw new SeatAlreadyBookedException(seatIdentifier, recommendedSeat.orElse(null), message);
            }
        }

        // 2. Fetch all seat entities and calculate total price
        List<Seat> seats = seatRepository.findAllById(request.getSeatIds());
        BigDecimal totalAmount = BigDecimal.ZERO;
        BigDecimal basePrice = show.getBasePrice();

        for (Seat seat : seats) {
            BigDecimal seatPrice = basePrice.multiply(BigDecimal.valueOf(seat.getSeatType().getMultiplier()));
            totalAmount = totalAmount.add(seatPrice);
        }

        // 3. Generate unique booking number
        String bookingNumber = "BK-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 4).toUpperCase();
        Booking booking = new Booking(bookingNumber, user, show, totalAmount);
        booking.setStatus(BookingStatus.CONFIRMED);

        Booking savedBooking;
        try {
            savedBooking = bookingRepository.save(booking);

            List<BookingSeat> bookingSeats = new ArrayList<>();
            for (Seat seat : seats) {
                BigDecimal seatPrice = basePrice.multiply(BigDecimal.valueOf(seat.getSeatType().getMultiplier()));
                BookingSeat bookingSeat = new BookingSeat(savedBooking, show, seat, seatPrice, BookingStatus.CONFIRMED);
                bookingSeats.add(bookingSeat);
            }

            bookingSeatRepository.saveAll(bookingSeats);
            savedBooking.setBookingSeats(bookingSeats);

        } catch (DataIntegrityViolationException ex) {
            logger.error("Database constraint triggered on concurrent seat booking attempt!", ex);
            throw new SeatAlreadyBookedException("One or more selected seats were just booked by another user.");
        }

        // 4. Process simulated payment
        PaymentMethod method;
        try {
            method = PaymentMethod.valueOf(request.getPaymentMethod().toUpperCase());
        } catch (Exception e) {
            method = PaymentMethod.CARD;
        }

        Payment payment = paymentService.processInitialPayment(savedBooking, totalAmount, method);
        savedBooking.setPayment(payment);

        // 5. If customer, add loyalty points (1 point per dollar spent)
        if (user instanceof Customer) {
            ((Customer) user).addLoyaltyPoints(totalAmount.intValue());
            userRepository.save(user);
        }

        return mapToResponse(savedBooking);
    }

    @Override
    @Transactional(readOnly = true)
    public BookingResponse getBookingById(Long bookingId) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with id: " + bookingId));
        return mapToResponse(booking);
    }

    @Override
    @Transactional(readOnly = true)
    public BookingResponse getBookingByNumber(String bookingNumber) {
        Booking booking = bookingRepository.findByBookingNumber(bookingNumber)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with number: " + bookingNumber));
        return mapToResponse(booking);
    }

    @Override
    @Transactional(readOnly = true)
    public List<BookingResponse> getBookingsByUser(Long userId) {
        return bookingRepository.findByUserIdOrderByCreatedAtDesc(userId).stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<BookingResponse> getAllBookings() {
        return bookingRepository.findAll().stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional
    public BookingResponse cancelBooking(Long bookingId, Long userId, String reason) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with id: " + bookingId));

        // Ensure user owns this booking or is admin
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        if (!booking.getUser().getId().equals(userId) && user.getRole() != Role.ROLE_ADMIN) {
            throw new BookingException("You are not authorized to cancel this booking.");
        }

        if (booking.getStatus() == BookingStatus.CANCELLED) {
            throw new BookingException("This booking is already cancelled.");
        }

        booking.setStatus(BookingStatus.CANCELLED);
        booking.setCancellationReason(reason != null ? reason : "User requested cancellation");

        // Release seats
        for (BookingSeat bs : booking.getBookingSeats()) {
            bs.setStatus(BookingStatus.CANCELLED);
        }
        bookingSeatRepository.saveAll(booking.getBookingSeats());

        // Refund payment status
        if (booking.getPayment() != null) {
            paymentService.refundPayment(booking.getPayment().getId());
        }

        Booking saved = bookingRepository.save(booking);
        return mapToResponse(saved);
    }

    @Override
    @Transactional(readOnly = true)
    public AdminDashboardStatsDto getAdminDashboardStats() {
        long totalUsers = userRepository.count();
        long totalMovies = movieRepository.count();
        long totalTheatres = theatreRepository.count();
        long totalShows = showRepository.count();
        long totalBookings = bookingRepository.count();
        BigDecimal totalRevenue = bookingRepository.calculateTotalRevenue();

        long totalSeats = seatRepository.count();
        long bookedSeats = bookingSeatRepository.findAll().stream()
                .filter(bs -> bs.getStatus() == BookingStatus.CONFIRMED)
                .count();
        long availableSeats = Math.max(0, (totalSeats * totalShows) - bookedSeats);

        return new AdminDashboardStatsDto(
                totalUsers,
                totalMovies,
                totalTheatres,
                totalShows,
                totalBookings,
                totalRevenue != null ? totalRevenue : BigDecimal.ZERO,
                availableSeats,
                bookedSeats
        );
    }

    private BookingResponse mapToResponse(Booking b) {
        BookingResponse res = new BookingResponse();
        res.setBookingId(b.getId());
        res.setBookingNumber(b.getBookingNumber());
        res.setCustomerName(b.getUser().getFullName());
        res.setCustomerEmail(b.getUser().getEmail());

        Show show = b.getShow();
        res.setMovieTitle(show.getMovie().getTitle());
        res.setMoviePosterUrl(show.getMovie().getPosterUrl());
        res.setTheatreName(show.getScreen().getTheatre().getName());
        res.setTheatreAddress(show.getScreen().getTheatre().getAddress() + ", " + show.getScreen().getTheatre().getCity());
        res.setScreenName(show.getScreen().getName());
        res.setShowStartTime(show.getStartTime());
        res.setShowEndTime(show.getEndTime());

        List<String> seatCodes = b.getBookingSeats().stream()
                .map(bs -> bs.getSeat().getRowName() + bs.getSeat().getSeatNumber())
                .collect(Collectors.toList());
        res.setSeatNumbers(seatCodes);

        res.setTotalAmount(b.getTotalAmount());
        res.setBookingStatus(b.getStatus().name());

        if (b.getPayment() != null) {
            res.setPaymentStatus(b.getPayment().getPaymentStatus().name());
            res.setPaymentMethod(b.getPayment().getPaymentMethod().name());
            res.setTransactionId(b.getPayment().getTransactionId());
        }

        res.setBookedAt(b.getCreatedAt());
        return res;
    }
}
