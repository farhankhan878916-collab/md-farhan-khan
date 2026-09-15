package com.example.movieticketbooking.repository;

import com.example.movieticketbooking.entity.Show;
import com.example.movieticketbooking.entity.ShowStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface ShowRepository extends JpaRepository<Show, Long> {
    List<Show> findByMovieIdAndStatus(Long movieId, ShowStatus status);
    List<Show> findByScreenId(Long screenId);

    @Query("SELECT s FROM Show s WHERE s.movie.id = :movieId AND s.screen.theatre.id = :theatreId AND s.status = :status AND s.startTime >= :now ORDER BY s.startTime ASC")
    List<Show> findActiveShowsByMovieAndTheatre(@Param("movieId") Long movieId,
                                               @Param("theatreId") Long theatreId,
                                               @Param("status") ShowStatus status,
                                               @Param("now") LocalDateTime now);

    @Query("SELECT s FROM Show s WHERE s.movie.id = :movieId AND s.status = :status AND s.startTime >= :now ORDER BY s.startTime ASC")
    List<Show> findUpcomingShowsByMovie(@Param("movieId") Long movieId,
                                       @Param("status") ShowStatus status,
                                       @Param("now") LocalDateTime now);
}
