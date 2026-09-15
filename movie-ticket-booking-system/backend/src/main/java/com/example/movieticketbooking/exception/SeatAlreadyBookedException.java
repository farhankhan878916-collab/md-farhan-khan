package com.example.movieticketbooking.exception;

import com.example.movieticketbooking.dto.SeatDto;

public class SeatAlreadyBookedException extends RuntimeException {
    private final String seatIdentifier;
    private final SeatDto recommendedSeat;

    public SeatAlreadyBookedException(String message) {
        super(message);
        this.seatIdentifier = null;
        this.recommendedSeat = null;
    }

    public SeatAlreadyBookedException(String seatIdentifier, SeatDto recommendedSeat, String message) {
        super(message);
        this.seatIdentifier = seatIdentifier;
        this.recommendedSeat = recommendedSeat;
    }

    public String getSeatIdentifier() {
        return seatIdentifier;
    }

    public SeatDto getRecommendedSeat() {
        return recommendedSeat;
    }
}
