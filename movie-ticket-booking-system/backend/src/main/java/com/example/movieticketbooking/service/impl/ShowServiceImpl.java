package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.ShowDto;
import com.example.movieticketbooking.entity.Movie;
import com.example.movieticketbooking.entity.Screen;
import com.example.movieticketbooking.entity.Show;
import com.example.movieticketbooking.entity.ShowStatus;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.repository.ShowRepository;
import com.example.movieticketbooking.service.MovieService;
import com.example.movieticketbooking.service.ScreenService;
import com.example.movieticketbooking.service.ShowService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ShowServiceImpl implements ShowService {

    private final ShowRepository showRepository;
    private final MovieService movieService;
    private final ScreenService screenService;

    public ShowServiceImpl(ShowRepository showRepository, MovieService movieService, ScreenService screenService) {
        this.showRepository = showRepository;
        this.movieService = movieService;
        this.screenService = screenService;
    }

    @Override
    @Transactional(readOnly = true)
    public List<ShowDto> getUpcomingShowsByMovie(Long movieId) {
        return showRepository.findByMovieIdAndStatus(movieId, ShowStatus.SCHEDULED).stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<ShowDto> getShowsByMovieAndTheatre(Long movieId, Long theatreId) {
        return showRepository.findActiveShowsByMovieAndTheatre(movieId, theatreId, ShowStatus.SCHEDULED, LocalDateTime.now()).stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<ShowDto> getAllShows() {
        return showRepository.findAll().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public ShowDto getShowById(Long id) {
        return mapToDto(findEntityById(id));
    }

    @Override
    @Transactional(readOnly = true)
    public Show findEntityById(Long id) {
        return showRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Show not found with id: " + id));
    }

    @Override
    @Transactional
    public ShowDto createShow(ShowDto dto) {
        Movie movie = movieService.findEntityById(dto.getMovieId());
        Screen screen = screenService.findEntityById(dto.getScreenId());

        LocalDateTime start = dto.getStartTime();
        LocalDateTime end = dto.getEndTime() != null ? dto.getEndTime() : start.plusMinutes(movie.getDurationMinutes() + 30);

        Show show = new Show(movie, screen, start, end, dto.getBasePrice());
        Show saved = showRepository.save(show);
        return mapToDto(saved);
    }

    @Override
    @Transactional
    public void cancelShow(Long id) {
        Show show = findEntityById(id);
        show.setStatus(ShowStatus.CANCELLED);
        showRepository.save(show);
    }

    private ShowDto mapToDto(Show s) {
        ShowDto dto = new ShowDto();
        dto.setId(s.getId());
        dto.setMovieId(s.getMovie().getId());
        dto.setMovieTitle(s.getMovie().getTitle());
        dto.setMoviePosterUrl(s.getMovie().getPosterUrl());
        dto.setScreenId(s.getScreen().getId());
        dto.setScreenName(s.getScreen().getName());
        dto.setTheatreId(s.getScreen().getTheatre().getId());
        dto.setTheatreName(s.getScreen().getTheatre().getName());
        dto.setTheatreCity(s.getScreen().getTheatre().getCity());
        dto.setStartTime(s.getStartTime());
        dto.setEndTime(s.getEndTime());
        dto.setBasePrice(s.getBasePrice());
        dto.setStatus(s.getStatus().name());
        return dto;
    }
}
