package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.TheatreDto;
import com.example.movieticketbooking.service.TheatreService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/theatres")
@CrossOrigin(origins = "*")
public class TheatreController {

    private final TheatreService theatreService;

    public TheatreController(TheatreService theatreService) {
        this.theatreService = theatreService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<TheatreDto>>> getAllTheatres() {
        return ResponseEntity.ok(ApiResponse.ok("Theatres retrieved successfully", theatreService.getAllActiveTheatres()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<TheatreDto>> getTheatreById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.ok("Theatre retrieved successfully", theatreService.getTheatreById(id)));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<TheatreDto>> createTheatre(@Valid @RequestBody TheatreDto theatreDto) {
        TheatreDto created = theatreService.createTheatre(theatreDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok("Theatre created successfully", created));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<TheatreDto>> updateTheatre(@PathVariable Long id, @Valid @RequestBody TheatreDto theatreDto) {
        TheatreDto updated = theatreService.updateTheatre(id, theatreDto);
        return ResponseEntity.ok(ApiResponse.ok("Theatre updated successfully", updated));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> deleteTheatre(@PathVariable Long id) {
        theatreService.deleteTheatre(id);
        return ResponseEntity.ok(ApiResponse.ok("Theatre deleted successfully", null));
    }
}
