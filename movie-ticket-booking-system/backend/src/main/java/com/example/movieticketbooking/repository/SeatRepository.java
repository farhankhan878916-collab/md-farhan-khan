package com.example.movieticketbooking.repository;

import com.example.movieticketbooking.entity.Seat;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface SeatRepository extends JpaRepository<Seat, Long> {
    List<Seat> findByScreenIdOrderByRowNameAscSeatNumberAsc(Long screenId);
    Optional<Seat> findByScreenIdAndRowNameAndSeatNumber(Long screenId, String rowName, Integer seatNumber);
}
