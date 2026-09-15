package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.MovieDto;
import com.example.movieticketbooking.entity.Movie;
import com.example.movieticketbooking.repository.MovieRepository;
import com.example.movieticketbooking.service.impl.MovieServiceImpl;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class MovieServiceTest {

    @Mock
    private MovieRepository movieRepository;

    @InjectMocks
    private MovieServiceImpl movieService;

    @Test
    @DisplayName("MOVIE SERVICE TEST: Get all active movies successfully")
    void testGetAllActiveMovies() {
        Movie m1 = new Movie("Interstellar", "Space exploration", "Sci-Fi", 169, "English", LocalDate.of(2014, 11, 7), "url1", 8.7);
        m1.setId(1L);

        Movie m2 = new Movie("Avengers", "Marvel superhero epic", "Action", 181, "English", LocalDate.of(2019, 4, 26), "url2", 8.4);
        m2.setId(2L);

        when(movieRepository.findByActiveTrue()).thenReturn(Arrays.asList(m1, m2));

        List<MovieDto> result = movieService.getAllActiveMovies();

        assertEquals(2, result.size());
        assertEquals("Interstellar", result.get(0).getTitle());
        assertEquals("Avengers", result.get(1).getTitle());
    }

    @Test
    @DisplayName("MOVIE SERVICE TEST: Create movie successfully")
    void testCreateMovie() {
        MovieDto dto = new MovieDto(null, "Dangal", "Wrestling drama", "Drama", 161, "Hindi", LocalDate.of(2016, 12, 23), "url3", 8.3, true);
        Movie saved = new Movie("Dangal", "Wrestling drama", "Drama", 161, "Hindi", LocalDate.of(2016, 12, 23), "url3", 8.3);
        saved.setId(10L);

        when(movieRepository.save(any(Movie.class))).thenReturn(saved);

        MovieDto created = movieService.createMovie(dto);

        assertNotNull(created);
        assertEquals(10L, created.getId());
        assertEquals("Dangal", created.getTitle());
    }
}
