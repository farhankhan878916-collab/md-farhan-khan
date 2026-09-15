package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.MovieDto;
import com.example.movieticketbooking.entity.Movie;

import java.util.List;

public interface MovieService {
    List<MovieDto> getAllActiveMovies();
    List<MovieDto> getAllMoviesAdmin();
    MovieDto getMovieById(Long id);
    Movie findEntityById(Long id);
    MovieDto createMovie(MovieDto movieDto);
    MovieDto updateMovie(Long id, MovieDto movieDto);
    void deleteMovie(Long id);
    List<MovieDto> searchByGenre(String genre);
}
