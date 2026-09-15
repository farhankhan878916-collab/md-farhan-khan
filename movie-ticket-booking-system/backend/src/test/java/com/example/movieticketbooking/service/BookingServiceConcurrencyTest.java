package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.BookingRequest;
import com.example.movieticketbooking.dto.BookingResponse;
import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.entity.*;
import com.example.movieticketbooking.exception.SeatAlreadyBookedException;
import com.example.movieticketbooking.repository.*;
import com.example.movieticketbooking.service.impl.BookingServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class BookingServiceConcurrencyTest {

    @Mock
    private BookingRepository bookingRepository;

    @Mock
    private BookingSeatRepository bookingSeatRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private ShowRepository showRepository;

    @Mock
    private SeatRepository seatRepository;

    @Mock
    private MovieRepository movieRepository;

    @Mock
    private TheatreRepository theatreRepository;

    @Mock
    private SeatRecommendationService seatRecommendationService;

    @Mock
    private PaymentService paymentService;

    @InjectMocks
    private BookingServiceImpl bookingService;

    private Customer userA;
    private Customer userB;
    private Show show;
    private Seat seatA5;

    @BeforeEach
    void setUp() {
        userA = new Customer("userA", "usera@cinema.com", "pass123", "User A", "111");
        userA.setId(1L);

        userB = new Customer("userB", "userb@cinema.com", "pass123", "User B", "222");
        userB.setId(2L);

        Movie movie = new Movie("Inception", "Sci-Fi", "Action", 148, "English", null, null, 8.8);
        movie.setId(10L);

        Theatre theatre = new Theatre("Grand Cineplex", "123 Main St", "NYC", "NY", "10001", 1);
        theatre.setId(20L);

        Screen screen = new Screen("Screen 1", 5, 8, theatre);
        screen.setId(30L);

        show = new Show(movie, screen, LocalDateTime.now().plusHours(2), LocalDateTime.now().plusHours(5), new BigDecimal("15.00"));
        show.setId(100L);

        seatA5 = new Seat("A", 5, SeatType.REGULAR, screen);
        seatA5.setId(505L);
    }

    @Test
    @DisplayName("DOUBLE BOOKING TEST: Two concurrent requests attempting to book seat A5 simultaneously; only one succeeds and one receives 409 Conflict exception")
    void testConcurrentSeatBookingConflict() throws InterruptedException {
        int numberOfThreads = 2;
        ExecutorService executorService = Executors.newFixedThreadPool(numberOfThreads);
        CountDownLatch latch = new CountDownLatch(1);

        AtomicInteger successCount = new AtomicInteger(0);
        AtomicInteger conflictCount = new AtomicInteger(0);

        when(userRepository.findById(1L)).thenReturn(Optional.of(userA));
        when(userRepository.findById(2L)).thenReturn(Optional.of(userB));
        when(showRepository.findById(100L)).thenReturn(Optional.of(show));
        when(seatRepository.findAllById(Collections.singletonList(505L))).thenReturn(Collections.singletonList(seatA5));
        when(seatRepository.findById(505L)).thenReturn(Optional.of(seatA5));

        // State tracker for booked status
        Set<Long> bookedSeats = Collections.synchronizedSet(new HashSet<>());

        when(bookingSeatRepository.findByShowIdAndSeatIdAndStatus(eq(100L), eq(505L), eq(BookingStatus.CONFIRMED)))
                .thenAnswer(invocation -> {
                    if (bookedSeats.contains(505L)) {
                        return Optional.of(new BookingSeat());
                    }
                    return Optional.empty();
                });

        when(bookingRepository.save(any(Booking.class))).thenAnswer(invocation -> {
            Booking b = invocation.getArgument(0);
            b.setId(999L);
            bookedSeats.add(505L);
            return b;
        });

        SeatDto recommendedSeat = new SeatDto(504L, "A", 4, "REGULAR", new BigDecimal("15.00"), "AVAILABLE");
        when(seatRecommendationService.findNearestAvailableSeat(eq(100L), eq(505L)))
                .thenReturn(Optional.of(recommendedSeat));

        when(paymentService.processInitialPayment(any(), any(), any()))
                .thenReturn(new Payment(new Booking(), new BigDecimal("15.00"), PaymentMethod.CARD, PaymentStatus.SUCCESS, "TXN-123"));

        BookingRequest requestA = new BookingRequest(100L, Collections.singletonList(505L), "CARD");
        BookingRequest requestB = new BookingRequest(100L, Collections.singletonList(505L), "CARD");

        // Submit concurrent booking attempts
        executorService.submit(() -> {
            try {
                latch.await();
                BookingResponse res = bookingService.createBooking(1L, requestA);
                assertNotNull(res);
                successCount.incrementAndGet();
            } catch (SeatAlreadyBookedException ex) {
                conflictCount.incrementAndGet();
            } catch (Exception e) {
                fail("Unexpected exception: " + e.getMessage());
            }
        });

        executorService.submit(() -> {
            try {
                latch.await();
                BookingResponse res = bookingService.createBooking(2L, requestB);
                assertNotNull(res);
                successCount.incrementAndGet();
            } catch (SeatAlreadyBookedException ex) {
                conflictCount.incrementAndGet();
            } catch (Exception e) {
                fail("Unexpected exception: " + e.getMessage());
            }
        });

        // Trigger both threads simultaneously
        latch.countDown();
        executorService.shutdown();
        boolean finished = executorService.awaitTermination(5, TimeUnit.SECONDS);

        assertTrue(finished, "Threads should terminate within 5 seconds");
        assertEquals(1, successCount.get(), "Exactly ONE user must successfully book seat A5");
        assertEquals(1, conflictCount.get(), "The concurrent conflicting request MUST receive SeatAlreadyBookedException (HTTP 409)");
    }
}
