import os

BASE_DIR = "movie-ticket-booking-system"
SRC_JAVA = os.path.join(BASE_DIR, "backend", "src", "main", "java", "com", "example", "movieticketbooking")

def write_file(subpath, content):
    full_path = os.path.join(SRC_JAVA, subpath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {full_path}")

def generate_repositories():
    # UserRepository.java
    write_file("repository/UserRepository.java", """package com.example.movieticketbooking.repository;

import com.example.movieticketbooking.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
    Optional<User> findByEmail(String email);
    Boolean existsByUsername(String username);
    Boolean existsByEmail(String email);
}
""")

    # MovieRepository.java
    write_file("repository/MovieRepository.java", """package com.example.movieticketbooking.repository;

import com.example.movieticketbooking.entity.Movie;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MovieRepository extends JpaRepository<Movie, Long> {
    List<Movie> findByActiveTrue();
    List<Movie> findByGenreIgnoreCaseAndActiveTrue(String genre);
    List<Movie> findByLanguageIgnoreCaseAndActiveTrue(String language);
}
""")

    # TheatreRepository.java
    write_file("repository/TheatreRepository.java", """package com.example.movieticketbooking.repository;

import com.example.movieticketbooking.entity.Theatre;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TheatreRepository extends JpaRepository<Theatre, Long> {
    List<Theatre> findByActiveTrue();
    List<Theatre> findByCityIgnoreCaseAndActiveTrue(String city);
}
""")

    # ScreenRepository.java
    write_file("repository/ScreenRepository.java", """package com.example.movieticketbooking.repository;

import com.example.movieticketbooking.entity.Screen;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ScreenRepository extends JpaRepository<Screen, Long> {
    List<Screen> findByTheatreId(Long theatreId);
}
""")

    # SeatRepository.java
    write_file("repository/SeatRepository.java", """package com.example.movieticketbooking.repository;

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
""")

    # ShowRepository.java
    write_file("repository/ShowRepository.java", """package com.example.movieticketbooking.repository;

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
""")

    # BookingRepository.java
    write_file("repository/BookingRepository.java", """package com.example.movieticketbooking.repository;

import com.example.movieticketbooking.entity.Booking;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

@Repository
public interface BookingRepository extends JpaRepository<Booking, Long> {
    List<Booking> findByUserIdOrderByCreatedAtDesc(Long userId);
    Optional<Booking> findByBookingNumber(String bookingNumber);
    List<Booking> findByShowId(Long showId);

    @Query("SELECT COALESCE(SUM(b.totalAmount), 0) FROM Booking b WHERE b.status = 'CONFIRMED'")
    BigDecimal calculateTotalRevenue();
}
""")

    # BookingSeatRepository.java (CRUCIAL FOR DOUBLE BOOKING DETECTION)
    write_file("repository/BookingSeatRepository.java", """package com.example.movieticketbooking.repository;

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
""")

    # PaymentRepository.java
    write_file("repository/PaymentRepository.java", """package com.example.movieticketbooking.repository;

import com.example.movieticketbooking.entity.Payment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PaymentRepository extends JpaRepository<Payment, Long> {
    Optional<Payment> findByBookingId(Long bookingId);
    Optional<Payment> findByTransactionId(String transactionId);
}
""")

if __name__ == "__main__":
    generate_repositories()
