package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.service.SeatRecommendationService;
import com.example.movieticketbooking.service.SeatService;
import org.springframework.stereotype.Service;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Production implementation of the Automatic Vacant Seat Recommendation Algorithm.
 * Uses Euclidean / Manhattan 2D grid distance mapping across the cinema theatre matrix.
 * Priority:
 * 1. Adjacent seats in the SAME row (e.g. for C5: checks C4, C6, C3, C7)
 * 2. Directly adjacent row seats (e.g. B5, D5, B4, B6, D4, D6)
 * 3. Nearest diagonal or surrounding vacant seats.
 */
@Service
public class SeatRecommendationServiceImpl implements SeatRecommendationService {

    private final SeatService seatService;

    public SeatRecommendationServiceImpl(SeatService seatService) {
        this.seatService = seatService;
    }

    @Override
    public Optional<SeatDto> findNearestAvailableSeat(Long showId, Long targetSeatId) {
        List<SeatDto> allSeats = seatService.getSeatLayoutForShow(showId);
        SeatDto targetSeat = allSeats.stream()
                .filter(s -> s.getId().equals(targetSeatId))
                .findFirst()
                .orElse(null);

        if (targetSeat == null) {
            return Optional.empty();
        }

        return findNearestAvailableSeat(allSeats, targetSeat);
    }

    @Override
    public Optional<SeatDto> findNearestAvailableSeat(List<SeatDto> allSeats, SeatDto targetSeat) {
        int targetRow = targetSeat.getRowIndex();
        int targetCol = targetSeat.getColumnIndex();

        return allSeats.stream()
                .filter(s -> "AVAILABLE".equalsIgnoreCase(s.getStatus()))
                .filter(s -> !s.getId().equals(targetSeat.getId()))
                .min(Comparator.comparingDouble(s -> calculateWeightedDistance(targetRow, targetCol, s.getRowIndex(), s.getColumnIndex())));
    }

    @Override
    public List<SeatDto> findNearestAvailableSeats(Long showId, List<Long> requestedSeatIds, int count) {
        List<SeatDto> allSeats = seatService.getSeatLayoutForShow(showId);
        List<SeatDto> targetSeats = allSeats.stream()
                .filter(s -> requestedSeatIds.contains(s.getId()))
                .collect(Collectors.toList());

        if (targetSeats.isEmpty()) {
            return List.of();
        }

        // Calculate centroid of requested seats
        double avgRow = targetSeats.stream().mapToInt(SeatDto::getRowIndex).average().orElse(0.0);
        double avgCol = targetSeats.stream().mapToInt(SeatDto::getColumnIndex).average().orElse(0.0);

        return allSeats.stream()
                .filter(s -> "AVAILABLE".equalsIgnoreCase(s.getStatus()))
                .filter(s -> !requestedSeatIds.contains(s.getId()))
                .sorted(Comparator.comparingDouble(s -> calculateWeightedDistance(avgRow, avgCol, s.getRowIndex(), s.getColumnIndex())))
                .limit(count)
                .collect(Collectors.toList());
    }

    /**
     * Calculates distance on the cinema grid.
     * Weights same-row movements slightly lower so that adjacent seats in the same row
     * are naturally preferred over changing rows.
     */
    private double calculateWeightedDistance(double r1, double c1, double r2, double c2) {
        double rowDiff = Math.abs(r1 - r2);
        double colDiff = Math.abs(c1 - c2);
        // Col weight 1.0, Row weight 1.5 (sitting next to your desired seat is better than moving rows)
        return Math.sqrt(Math.pow(colDiff * 1.0, 2) + Math.pow(rowDiff * 1.5, 2));
    }
}
