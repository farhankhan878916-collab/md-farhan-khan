package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.entity.BookingStatus;
import com.example.movieticketbooking.entity.Seat;
import com.example.movieticketbooking.entity.Show;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.repository.BookingSeatRepository;
import com.example.movieticketbooking.repository.SeatRepository;
import com.example.movieticketbooking.service.SeatService;
import com.example.movieticketbooking.service.ShowService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
public class SeatServiceImpl implements SeatService {

    private final SeatRepository seatRepository;
    private final ShowService showService;
    private final BookingSeatRepository bookingSeatRepository;

    public SeatServiceImpl(SeatRepository seatRepository, ShowService showService, BookingSeatRepository bookingSeatRepository) {
        this.seatRepository = seatRepository;
        this.showService = showService;
        this.bookingSeatRepository = bookingSeatRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<SeatDto> getSeatLayoutForShow(Long showId) {
        Show show = showService.findEntityById(showId);
        Long screenId = show.getScreen().getId();

        // 1. Fetch all seats for the screen
        List<Seat> screenSeats = seatRepository.findByScreenIdOrderByRowNameAscSeatNumberAsc(screenId);

        // 2. Fetch all booked seat IDs for this show
        List<Long> bookedSeatIds = bookingSeatRepository.findBookedSeatIdsByShowId(showId, BookingStatus.CONFIRMED);
        Set<Long> bookedSet = new HashSet<>(bookedSeatIds);

        BigDecimal basePrice = show.getBasePrice();

        return screenSeats.stream().map(seat -> {
            boolean isBooked = bookedSet.contains(seat.getId());
            String status = isBooked ? "BOOKED" : "AVAILABLE";
            BigDecimal calculatedPrice = basePrice.multiply(BigDecimal.valueOf(seat.getSeatType().getMultiplier()));

            SeatDto dto = new SeatDto(
                    seat.getId(),
                    seat.getRowName(),
                    seat.getSeatNumber(),
                    seat.getSeatType().name(),
                    calculatedPrice,
                    status
            );
            return dto;
        }).collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public Seat findEntityById(Long id) {
        return seatRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Seat not found with id: " + id));
    }

    @Override
    @Transactional(readOnly = true)
    public List<Seat> findEntitiesByIds(List<Long> seatIds) {
        List<Seat> seats = seatRepository.findAllById(seatIds);
        if (seats.size() != seatIds.size()) {
            throw new ResourceNotFoundException("One or more requested seats could not be found");
        }
        return seats;
    }
}
