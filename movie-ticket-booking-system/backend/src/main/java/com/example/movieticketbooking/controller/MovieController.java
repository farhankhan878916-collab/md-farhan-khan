package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.MovieDto;
import com.example.movieticketbooking.service.MovieService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/movies")
@CrossOrigin(origins = "*")
public class MovieController {

    private final MovieService movieService;

    public MovieController(MovieService movieService) {
        this.movieService = movieService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<MovieDto>>> getAllMovies() {
        return ResponseEntity.ok(ApiResponse.ok("Movies retrieved successfully", movieService.getAllActiveMovies()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<MovieDto>> getMovieById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.ok("Movie retrieved successfully", movieService.getMovieById(id)));
    }

    @GetMapping("/genre/{genre}")
    public ResponseEntity<ApiResponse<List<MovieDto>>> getMoviesByGenre(@PathVariable String genre) {
        return ResponseEntity.ok(ApiResponse.ok("Movies retrieved by genre", movieService.searchByGenre(genre)));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<MovieDto>> createMovie(@Valid @RequestBody MovieDto movieDto) {
        MovieDto created = movieService.createMovie(movieDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok("Movie created successfully", created));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<MovieDto>> updateMovie(@PathVariable Long id, @Valid @RequestBody MovieDto movieDto) {
        MovieDto updated = movieService.updateMovie(id, movieDto);
        return ResponseEntity.ok(ApiResponse.ok("Movie updated successfully", updated));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> deleteMovie(@PathVariable Long id) {
        movieService.deleteMovie(id);
        return ResponseEntity.ok(ApiResponse.ok("Movie deleted successfully", null));
    }
}
