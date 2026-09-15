package com.example.movieticketbooking.entity;

public enum SeatType {
    REGULAR(1.0),
    PREMIUM(1.5),
    VIP(2.0);

    private final double multiplier;

    SeatType(double multiplier) {
        this.multiplier = multiplier;
    }

    public double getMultiplier() {
        return multiplier;
    }
}
