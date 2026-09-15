package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.ShowDto;
import com.example.movieticketbooking.service.ShowService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/shows")
@CrossOrigin(origins = "*")
public class ShowController {

    private final ShowService showService;

    public ShowController(ShowService showService) {
        this.showService = showService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<ShowDto>>> getAllShows() {
        return ResponseEntity.ok(ApiResponse.ok("Shows retrieved successfully", showService.getAllShows()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<ShowDto>> getShowById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.ok("Show retrieved successfully", showService.getShowById(id)));
    }

    @GetMapping("/movie/{movieId}")
    public ResponseEntity<ApiResponse<List<ShowDto>>> getUpcomingShowsByMovie(@PathVariable Long movieId) {
        return ResponseEntity.ok(ApiResponse.ok("Shows retrieved for movie", showService.getUpcomingShowsByMovie(movieId)));
    }

    @GetMapping("/movie/{movieId}/theatre/{theatreId}")
    public ResponseEntity<ApiResponse<List<ShowDto>>> getShowsByMovieAndTheatre(@PathVariable Long movieId, @PathVariable Long theatreId) {
        return ResponseEntity.ok(ApiResponse.ok("Shows retrieved for movie and theatre", showService.getShowsByMovieAndTheatre(movieId, theatreId)));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<ShowDto>> createShow(@Valid @RequestBody ShowDto showDto) {
        ShowDto created = showService.createShow(showDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok("Show created successfully", created));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> cancelShow(@PathVariable Long id) {
        showService.cancelShow(id);
        return ResponseEntity.ok(ApiResponse.ok("Show cancelled successfully", null));
    }
}
