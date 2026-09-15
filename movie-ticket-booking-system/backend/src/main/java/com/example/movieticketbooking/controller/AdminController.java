package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.AdminDashboardStatsDto;
import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.BookingResponse;
import com.example.movieticketbooking.dto.UserDto;
import com.example.movieticketbooking.service.BookingService;
import com.example.movieticketbooking.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/admin")
@PreAuthorize("hasRole('ADMIN')")
@CrossOrigin(origins = "*")
public class AdminController {

    private final BookingService bookingService;
    private final UserService userService;

    public AdminController(BookingService bookingService, UserService userService) {
        this.bookingService = bookingService;
        this.userService = userService;
    }

    @GetMapping("/dashboard")
    public ResponseEntity<ApiResponse<AdminDashboardStatsDto>> getDashboardStats() {
        AdminDashboardStatsDto stats = bookingService.getAdminDashboardStats();
        return ResponseEntity.ok(ApiResponse.ok("Admin stats retrieved successfully", stats));
    }

    @GetMapping("/users")
    public ResponseEntity<ApiResponse<List<UserDto>>> getAllUsers() {
        return ResponseEntity.ok(ApiResponse.ok("Users retrieved successfully", userService.getAllUsers()));
    }

    @PutMapping("/users/{id}/toggle-status")
    public ResponseEntity<ApiResponse<Void>> toggleUserStatus(@PathVariable Long id) {
        userService.toggleUserStatus(id);
        return ResponseEntity.ok(ApiResponse.ok("User status updated successfully", null));
    }

    @GetMapping("/bookings")
    public ResponseEntity<ApiResponse<List<BookingResponse>>> getAllBookings() {
        return ResponseEntity.ok(ApiResponse.ok("All bookings retrieved successfully", bookingService.getAllBookings()));
    }
}
