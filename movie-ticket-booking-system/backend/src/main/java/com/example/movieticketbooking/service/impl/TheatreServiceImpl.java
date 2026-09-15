package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.TheatreDto;
import com.example.movieticketbooking.entity.Theatre;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.repository.TheatreRepository;
import com.example.movieticketbooking.service.TheatreService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class TheatreServiceImpl implements TheatreService {

    private final TheatreRepository theatreRepository;

    public TheatreServiceImpl(TheatreRepository theatreRepository) {
        this.theatreRepository = theatreRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<TheatreDto> getAllActiveTheatres() {
        return theatreRepository.findByActiveTrue().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public TheatreDto getTheatreById(Long id) {
        return mapToDto(findEntityById(id));
    }

    @Override
    @Transactional(readOnly = true)
    public Theatre findEntityById(Long id) {
        return theatreRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Theatre not found with id: " + id));
    }

    @Override
    @Transactional
    public TheatreDto createTheatre(TheatreDto dto) {
        Theatre theatre = new Theatre(
                dto.getName(),
                dto.getAddress(),
                dto.getCity(),
                dto.getState(),
                dto.getZipCode(),
                dto.getTotalScreens() != null ? dto.getTotalScreens() : 1
        );
        theatre.setActive(dto.isActive());
        return mapToDto(theatreRepository.save(theatre));
    }

    @Override
    @Transactional
    public TheatreDto updateTheatre(Long id, TheatreDto dto) {
        Theatre theatre = findEntityById(id);
        theatre.setName(dto.getName());
        theatre.setAddress(dto.getAddress());
        theatre.setCity(dto.getCity());
        theatre.setState(dto.getState());
        theatre.setZipCode(dto.getZipCode());
        theatre.setTotalScreens(dto.getTotalScreens());
        theatre.setActive(dto.isActive());
        return mapToDto(theatreRepository.save(theatre));
    }

    @Override
    @Transactional
    public void deleteTheatre(Long id) {
        Theatre theatre = findEntityById(id);
        theatre.setActive(false);
        theatreRepository.save(theatre);
    }

    private TheatreDto mapToDto(Theatre t) {
        return new TheatreDto(
                t.getId(),
                t.getName(),
                t.getAddress(),
                t.getCity(),
                t.getState(),
                t.getZipCode(),
                t.getTotalScreens(),
                t.isActive()
        );
    }
}
