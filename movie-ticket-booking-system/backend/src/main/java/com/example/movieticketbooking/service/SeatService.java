package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.entity.Seat;

import java.util.List;

public interface SeatService {
    List<SeatDto> getSeatLayoutForShow(Long showId);
    Seat findEntityById(Long id);
    List<Seat> findEntitiesByIds(List<Long> seatIds);
}
