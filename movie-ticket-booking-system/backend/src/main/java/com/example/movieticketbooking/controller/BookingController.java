package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.BookingRequest;
import com.example.movieticketbooking.dto.BookingResponse;
import com.example.movieticketbooking.security.UserPrincipal;
import com.example.movieticketbooking.service.BookingService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/bookings")
@CrossOrigin(origins = "*")
public class BookingController {

    private final BookingService bookingService;

    public BookingController(BookingService bookingService) {
        this.bookingService = bookingService;
    }

    @PostMapping
    public ResponseEntity<ApiResponse<BookingResponse>> createBooking(@AuthenticationPrincipal UserPrincipal currentUser,
                                                                      @Valid @RequestBody BookingRequest request) {
        BookingResponse response = bookingService.createBooking(currentUser.getId(), request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok("Booking confirmed successfully", response));
    }

    @GetMapping("/my")
    public ResponseEntity<ApiResponse<List<BookingResponse>>> getMyBookings(@AuthenticationPrincipal UserPrincipal currentUser) {
        List<BookingResponse> bookings = bookingService.getBookingsByUser(currentUser.getId());
        return ResponseEntity.ok(ApiResponse.ok("User bookings retrieved successfully", bookings));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<BookingResponse>> getBookingById(@PathVariable Long id) {
        BookingResponse response = bookingService.getBookingById(id);
        return ResponseEntity.ok(ApiResponse.ok("Booking details retrieved", response));
    }

    @GetMapping("/number/{bookingNumber}")
    public ResponseEntity<ApiResponse<BookingResponse>> getBookingByNumber(@PathVariable String bookingNumber) {
        BookingResponse response = bookingService.getBookingByNumber(bookingNumber);
        return ResponseEntity.ok(ApiResponse.ok("Booking details retrieved", response));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse<BookingResponse>> cancelBooking(@AuthenticationPrincipal UserPrincipal currentUser,
                                                                      @PathVariable Long id,
                                                                      @RequestParam(required = false) String reason) {
        BookingResponse cancelled = bookingService.cancelBooking(id, currentUser.getId(), reason);
        return ResponseEntity.ok(ApiResponse.ok("Booking cancelled successfully", cancelled));
    }
}
