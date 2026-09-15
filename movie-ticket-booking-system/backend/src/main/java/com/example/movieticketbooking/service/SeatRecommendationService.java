package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.SeatDto;

import java.util.List;
import java.util.Optional;

public interface SeatRecommendationService {
    Optional<SeatDto> findNearestAvailableSeat(Long showId, Long targetSeatId);
    Optional<SeatDto> findNearestAvailableSeat(List<SeatDto> allSeats, SeatDto targetSeat);
    List<SeatDto> findNearestAvailableSeats(Long showId, List<Long> requestedSeatIds, int count);
}
