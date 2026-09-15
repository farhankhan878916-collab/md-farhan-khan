package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.ScreenDto;
import com.example.movieticketbooking.entity.Screen;
import com.example.movieticketbooking.entity.Seat;
import com.example.movieticketbooking.entity.SeatType;
import com.example.movieticketbooking.entity.Theatre;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.repository.ScreenRepository;
import com.example.movieticketbooking.repository.SeatRepository;
import com.example.movieticketbooking.service.ScreenService;
import com.example.movieticketbooking.service.TheatreService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ScreenServiceImpl implements ScreenService {

    private final ScreenRepository screenRepository;
    private final TheatreService theatreService;
    private final SeatRepository seatRepository;

    public ScreenServiceImpl(ScreenRepository screenRepository, TheatreService theatreService, SeatRepository seatRepository) {
        this.screenRepository = screenRepository;
        this.theatreService = theatreService;
        this.seatRepository = seatRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<ScreenDto> getScreensByTheatre(Long theatreId) {
        return screenRepository.findByTheatreId(theatreId).stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public ScreenDto getScreenById(Long id) {
        return mapToDto(findEntityById(id));
    }

    @Override
    @Transactional(readOnly = true)
    public Screen findEntityById(Long id) {
        return screenRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Screen not found with id: " + id));
    }

    @Override
    @Transactional
    public ScreenDto createScreen(ScreenDto dto) {
        Theatre theatre = theatreService.findEntityById(dto.getTheatreId());
        int rows = dto.getTotalRows() != null ? dto.getTotalRows() : 5;
        int cols = dto.getTotalColumns() != null ? dto.getTotalColumns() : 8;

        Screen screen = new Screen(dto.getName(), rows, cols, theatre);
        Screen saved = screenRepository.save(screen);

        // Generate seats automatically
        List<Seat> seats = new ArrayList<>();
        char rowChar = 'A';
        for (int r = 0; r < rows; r++) {
            String rowName = String.valueOf((char) (rowChar + r));
            SeatType type = r == (rows - 1) ? SeatType.VIP : (r >= rows - 3 ? SeatType.PREMIUM : SeatType.REGULAR);
            for (int c = 1; c <= cols; c++) {
                seats.add(new Seat(rowName, c, type, saved));
            }
        }
        seatRepository.saveAll(seats);

        return mapToDto(saved);
    }

    private ScreenDto mapToDto(Screen s) {
        return new ScreenDto(
                s.getId(),
                s.getName(),
                s.getTotalRows(),
                s.getTotalColumns(),
                s.getTheatre().getId(),
                s.getTheatre().getName()
        );
    }
}
