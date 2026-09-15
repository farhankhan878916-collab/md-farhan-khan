package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.TheatreDto;
import com.example.movieticketbooking.entity.Theatre;

import java.util.List;

public interface TheatreService {
    List<TheatreDto> getAllActiveTheatres();
    TheatreDto getTheatreById(Long id);
    Theatre findEntityById(Long id);
    TheatreDto createTheatre(TheatreDto theatreDto);
    TheatreDto updateTheatre(Long id, TheatreDto theatreDto);
    void deleteTheatre(Long id);
}
