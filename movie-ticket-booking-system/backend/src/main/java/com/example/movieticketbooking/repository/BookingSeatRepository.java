package com.example.movieticketbooking.repository;

import com.example.movieticketbooking.entity.BookingSeat;
import com.example.movieticketbooking.entity.BookingStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface BookingSeatRepository extends JpaRepository<BookingSeat, Long> {

    @Query("SELECT bs FROM BookingSeat bs WHERE bs.show.id = :showId AND bs.seat.id = :seatId AND bs.status = :status")
    Optional<BookingSeat> findByShowIdAndSeatIdAndStatus(@Param("showId") Long showId,
                                                        @Param("seatId") Long seatId,
                                                        @Param("status") BookingStatus status);

    @Query("SELECT bs.seat.id FROM BookingSeat bs WHERE bs.show.id = :showId AND bs.status = :status")
    List<Long> findBookedSeatIdsByShowId(@Param("showId") Long showId, @Param("status") BookingStatus status);

    List<BookingSeat> findByShowId(Long showId);
}
