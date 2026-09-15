package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.ShowDto;
import com.example.movieticketbooking.entity.Show;

import java.util.List;

public interface ShowService {
    List<ShowDto> getUpcomingShowsByMovie(Long movieId);
    List<ShowDto> getShowsByMovieAndTheatre(Long movieId, Long theatreId);
    List<ShowDto> getAllShows();
    ShowDto getShowById(Long id);
    Show findEntityById(Long id);
    ShowDto createShow(ShowDto showDto);
    void cancelShow(Long id);
}
