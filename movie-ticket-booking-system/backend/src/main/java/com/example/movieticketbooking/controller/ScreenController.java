package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.ScreenDto;
import com.example.movieticketbooking.service.ScreenService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/screens")
@CrossOrigin(origins = "*")
public class ScreenController {

    private final ScreenService screenService;

    public ScreenController(ScreenService screenService) {
        this.screenService = screenService;
    }

    @GetMapping("/theatre/{theatreId}")
    public ResponseEntity<ApiResponse<List<ScreenDto>>> getScreensByTheatre(@PathVariable Long theatreId) {
        return ResponseEntity.ok(ApiResponse.ok("Screens retrieved successfully", screenService.getScreensByTheatre(theatreId)));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<ScreenDto>> getScreenById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.ok("Screen retrieved successfully", screenService.getScreenById(id)));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<ScreenDto>> createScreen(@Valid @RequestBody ScreenDto screenDto) {
        ScreenDto created = screenService.createScreen(screenDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok("Screen created successfully", created));
    }
}
