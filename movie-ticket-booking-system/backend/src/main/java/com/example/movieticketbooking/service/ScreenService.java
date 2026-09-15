package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.ScreenDto;
import com.example.movieticketbooking.entity.Screen;

import java.util.List;

public interface ScreenService {
    List<ScreenDto> getScreensByTheatre(Long theatreId);
    ScreenDto getScreenById(Long id);
    Screen findEntityById(Long id);
    ScreenDto createScreen(ScreenDto screenDto);
}
