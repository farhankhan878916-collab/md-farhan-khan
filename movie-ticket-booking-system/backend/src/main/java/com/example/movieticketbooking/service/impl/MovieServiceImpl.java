package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.MovieDto;
import com.example.movieticketbooking.entity.Movie;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.repository.MovieRepository;
import com.example.movieticketbooking.service.MovieService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class MovieServiceImpl implements MovieService {

    private final MovieRepository movieRepository;

    public MovieServiceImpl(MovieRepository movieRepository) {
        this.movieRepository = movieRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<MovieDto> getAllActiveMovies() {
        return movieRepository.findByActiveTrue().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<MovieDto> getAllMoviesAdmin() {
        return movieRepository.findAll().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public MovieDto getMovieById(Long id) {
        return mapToDto(findEntityById(id));
    }

    @Override
    @Transactional(readOnly = true)
    public Movie findEntityById(Long id) {
        return movieRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Movie not found with id: " + id));
    }

    @Override
    @Transactional
    public MovieDto createMovie(MovieDto dto) {
        Movie movie = new Movie(
                dto.getTitle(),
                dto.getDescription(),
                dto.getGenre(),
                dto.getDurationMinutes(),
                dto.getLanguage(),
                dto.getReleaseDate(),
                dto.getPosterUrl(),
                dto.getRating() != null ? dto.getRating() : 8.0
        );
        movie.setActive(dto.isActive());
        Movie saved = movieRepository.save(movie);
        return mapToDto(saved);
    }

    @Override
    @Transactional
    public MovieDto updateMovie(Long id, MovieDto dto) {
        Movie movie = findEntityById(id);
        movie.setTitle(dto.getTitle());
        movie.setDescription(dto.getDescription());
        movie.setGenre(dto.getGenre());
        movie.setDurationMinutes(dto.getDurationMinutes());
        movie.setLanguage(dto.getLanguage());
        movie.setReleaseDate(dto.getReleaseDate());
        if (dto.getPosterUrl() != null && !dto.getPosterUrl().isEmpty()) {
            movie.setPosterUrl(dto.getPosterUrl());
        }
        if (dto.getRating() != null) {
            movie.setRating(dto.getRating());
        }
        movie.setActive(dto.isActive());

        Movie updated = movieRepository.save(movie);
        return mapToDto(updated);
    }

    @Override
    @Transactional
    public void deleteMovie(Long id) {
        Movie movie = findEntityById(id);
        movie.setActive(false);
        movieRepository.save(movie);
    }

    @Override
    @Transactional(readOnly = true)
    public List<MovieDto> searchByGenre(String genre) {
        return movieRepository.findByGenreIgnoreCaseAndActiveTrue(genre).stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    private MovieDto mapToDto(Movie m) {
        return new MovieDto(
                m.getId(),
                m.getTitle(),
                m.getDescription(),
                m.getGenre(),
                m.getDurationMinutes(),
                m.getLanguage(),
                m.getReleaseDate(),
                m.getPosterUrl(),
                m.getRating(),
                m.isActive()
        );
    }
}
