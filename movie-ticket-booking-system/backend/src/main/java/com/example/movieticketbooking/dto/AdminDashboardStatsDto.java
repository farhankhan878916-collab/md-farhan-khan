package com.example.movieticketbooking.dto;

import java.math.BigDecimal;

public class AdminDashboardStatsDto {
    private long totalUsers;
    private long totalMovies;
    private long totalTheatres;
    private long totalShows;
    private long totalBookings;
    private BigDecimal totalRevenue;
    private long availableSeats;
    private long bookedSeats;

    public AdminDashboardStatsDto() {}

    public AdminDashboardStatsDto(long totalUsers, long totalMovies, long totalTheatres, long totalShows, long totalBookings, BigDecimal totalRevenue, long availableSeats, long bookedSeats) {
        this.totalUsers = totalUsers;
        this.totalMovies = totalMovies;
        this.totalTheatres = totalTheatres;
        this.totalShows = totalShows;
        this.totalBookings = totalBookings;
        this.totalRevenue = totalRevenue != null ? totalRevenue : BigDecimal.ZERO;
        this.availableSeats = availableSeats;
        this.bookedSeats = bookedSeats;
    }

    public long getTotalUsers() {
        return totalUsers;
    }

    public void setTotalUsers(long totalUsers) {
        this.totalUsers = totalUsers;
    }

    public long getTotalMovies() {
        return totalMovies;
    }

    public void setTotalMovies(long totalMovies) {
        this.totalMovies = totalMovies;
    }

    public long getTotalTheatres() {
        return totalTheatres;
    }

    public void setTotalTheatres(long totalTheatres) {
        this.totalTheatres = totalTheatres;
    }

    public long getTotalShows() {
        return totalShows;
    }

    public void setTotalShows(long totalShows) {
        this.totalShows = totalShows;
    }

    public long getTotalBookings() {
        return totalBookings;
    }

    public void setTotalBookings(long totalBookings) {
        this.totalBookings = totalBookings;
    }

    public BigDecimal getTotalRevenue() {
        return totalRevenue;
    }

    public void setTotalRevenue(BigDecimal totalRevenue) {
        this.totalRevenue = totalRevenue;
    }

    public long getAvailableSeats() {
        return availableSeats;
    }

    public void setAvailableSeats(long availableSeats) {
        this.availableSeats = availableSeats;
    }

    public long getBookedSeats() {
        return bookedSeats;
    }

    public void setBookedSeats(long bookedSeats) {
        this.bookedSeats = bookedSeats;
    }
}
