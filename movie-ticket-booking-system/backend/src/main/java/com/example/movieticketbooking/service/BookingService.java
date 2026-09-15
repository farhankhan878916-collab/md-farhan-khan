package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.AdminDashboardStatsDto;
import com.example.movieticketbooking.dto.BookingRequest;
import com.example.movieticketbooking.dto.BookingResponse;

import java.util.List;

public interface BookingService {
    BookingResponse createBooking(Long userId, BookingRequest bookingRequest);
    BookingResponse getBookingById(Long bookingId);
    BookingResponse getBookingByNumber(String bookingNumber);
    List<BookingResponse> getBookingsByUser(Long userId);
    List<BookingResponse> getAllBookings();
    BookingResponse cancelBooking(Long bookingId, Long userId, String reason);
    AdminDashboardStatsDto getAdminDashboardStats();
}
