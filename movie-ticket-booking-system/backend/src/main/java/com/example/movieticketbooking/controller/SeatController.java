package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.service.SeatRecommendationService;
import com.example.movieticketbooking.service.SeatService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/shows/{showId}/seats")
@CrossOrigin(origins = "*")
public class SeatController {

    private final SeatService seatService;
    private final SeatRecommendationService seatRecommendationService;

    public SeatController(SeatService seatService, SeatRecommendationService seatRecommendationService) {
        this.seatService = seatService;
        this.seatRecommendationService = seatRecommendationService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<SeatDto>>> getSeatsForShow(@PathVariable Long showId) {
        List<SeatDto> seatLayout = seatService.getSeatLayoutForShow(showId);
        return ResponseEntity.ok(ApiResponse.ok("Seat layout retrieved successfully", seatLayout));
    }

    @GetMapping("/recommend")
    public ResponseEntity<ApiResponse<SeatDto>> getRecommendedSeat(@PathVariable Long showId,
                                                                   @RequestParam Long targetSeatId) {
        SeatDto recommended = seatRecommendationService.findNearestAvailableSeat(showId, targetSeatId)
                .orElse(null);
        return ResponseEntity.ok(ApiResponse.ok("Recommended seat retrieved", recommended));
    }
}
