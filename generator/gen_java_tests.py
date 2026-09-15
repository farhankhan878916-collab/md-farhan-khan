import os

BASE_DIR = "movie-ticket-booking-system"
SRC_TEST = os.path.join(BASE_DIR, "backend", "src", "test", "java", "com", "example", "movieticketbooking")

def write_file(subpath, content):
    full_path = os.path.join(SRC_TEST, subpath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {full_path}")

def generate_tests():
    # Application Context Test
    write_file("MovieTicketBookingApplicationTests.java", """package com.example.movieticketbooking;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("h2")
class MovieTicketBookingApplicationTests {

    @Test
    void contextLoads() {
        // Verifies complete Spring Boot application context loads cleanly
    }
}
""")

    # BookingServiceConcurrencyTest.java (CRUCIAL: Concurrent double-booking test!)
    write_file("service/BookingServiceConcurrencyTest.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.BookingRequest;
import com.example.movieticketbooking.dto.BookingResponse;
import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.entity.*;
import com.example.movieticketbooking.exception.SeatAlreadyBookedException;
import com.example.movieticketbooking.repository.*;
import com.example.movieticketbooking.service.impl.BookingServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class BookingServiceConcurrencyTest {

    @Mock
    private BookingRepository bookingRepository;

    @Mock
    private BookingSeatRepository bookingSeatRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private ShowRepository showRepository;

    @Mock
    private SeatRepository seatRepository;

    @Mock
    private MovieRepository movieRepository;

    @Mock
    private TheatreRepository theatreRepository;

    @Mock
    private SeatRecommendationService seatRecommendationService;

    @Mock
    private PaymentService paymentService;

    @InjectMocks
    private BookingServiceImpl bookingService;

    private Customer userA;
    private Customer userB;
    private Show show;
    private Seat seatA5;

    @BeforeEach
    void setUp() {
        userA = new Customer("userA", "usera@cinema.com", "pass123", "User A", "111");
        userA.setId(1L);

        userB = new Customer("userB", "userb@cinema.com", "pass123", "User B", "222");
        userB.setId(2L);

        Movie movie = new Movie("Inception", "Sci-Fi", "Action", 148, "English", null, null, 8.8);
        movie.setId(10L);

        Theatre theatre = new Theatre("Grand Cineplex", "123 Main St", "NYC", "NY", "10001", 1);
        theatre.setId(20L);

        Screen screen = new Screen("Screen 1", 5, 8, theatre);
        screen.setId(30L);

        show = new Show(movie, screen, LocalDateTime.now().plusHours(2), LocalDateTime.now().plusHours(5), new BigDecimal("15.00"));
        show.setId(100L);

        seatA5 = new Seat("A", 5, SeatType.REGULAR, screen);
        seatA5.setId(505L);
    }

    @Test
    @DisplayName("DOUBLE BOOKING TEST: Two concurrent requests attempting to book seat A5 simultaneously; only one succeeds and one receives 409 Conflict exception")
    void testConcurrentSeatBookingConflict() throws InterruptedException {
        int numberOfThreads = 2;
        ExecutorService executorService = Executors.newFixedThreadPool(numberOfThreads);
        CountDownLatch latch = new CountDownLatch(1);

        AtomicInteger successCount = new AtomicInteger(0);
        AtomicInteger conflictCount = new AtomicInteger(0);

        when(userRepository.findById(1L)).thenReturn(Optional.of(userA));
        when(userRepository.findById(2L)).thenReturn(Optional.of(userB));
        when(showRepository.findById(100L)).thenReturn(Optional.of(show));
        when(seatRepository.findAllById(Collections.singletonList(505L))).thenReturn(Collections.singletonList(seatA5));
        when(seatRepository.findById(505L)).thenReturn(Optional.of(seatA5));

        // State tracker for booked status
        Set<Long> bookedSeats = Collections.synchronizedSet(new HashSet<>());

        when(bookingSeatRepository.findByShowIdAndSeatIdAndStatus(eq(100L), eq(505L), eq(BookingStatus.CONFIRMED)))
                .thenAnswer(invocation -> {
                    if (bookedSeats.contains(505L)) {
                        return Optional.of(new BookingSeat());
                    }
                    return Optional.empty();
                });

        when(bookingRepository.save(any(Booking.class))).thenAnswer(invocation -> {
            Booking b = invocation.getArgument(0);
            b.setId(999L);
            bookedSeats.add(505L);
            return b;
        });

        SeatDto recommendedSeat = new SeatDto(504L, "A", 4, "REGULAR", new BigDecimal("15.00"), "AVAILABLE");
        when(seatRecommendationService.findNearestAvailableSeat(eq(100L), eq(505L)))
                .thenReturn(Optional.of(recommendedSeat));

        when(paymentService.processInitialPayment(any(), any(), any()))
                .thenReturn(new Payment(new Booking(), new BigDecimal("15.00"), PaymentMethod.CARD, PaymentStatus.SUCCESS, "TXN-123"));

        BookingRequest requestA = new BookingRequest(100L, Collections.singletonList(505L), "CARD");
        BookingRequest requestB = new BookingRequest(100L, Collections.singletonList(505L), "CARD");

        // Submit concurrent booking attempts
        executorService.submit(() -> {
            try {
                latch.await();
                BookingResponse res = bookingService.createBooking(1L, requestA);
                assertNotNull(res);
                successCount.incrementAndGet();
            } catch (SeatAlreadyBookedException ex) {
                conflictCount.incrementAndGet();
            } catch (Exception e) {
                fail("Unexpected exception: " + e.getMessage());
            }
        });

        executorService.submit(() -> {
            try {
                latch.await();
                BookingResponse res = bookingService.createBooking(2L, requestB);
                assertNotNull(res);
                successCount.incrementAndGet();
            } catch (SeatAlreadyBookedException ex) {
                conflictCount.incrementAndGet();
            } catch (Exception e) {
                fail("Unexpected exception: " + e.getMessage());
            }
        });

        // Trigger both threads simultaneously
        latch.countDown();
        executorService.shutdown();
        boolean finished = executorService.awaitTermination(5, TimeUnit.SECONDS);

        assertTrue(finished, "Threads should terminate within 5 seconds");
        assertEquals(1, successCount.get(), "Exactly ONE user must successfully book seat A5");
        assertEquals(1, conflictCount.get(), "The concurrent conflicting request MUST receive SeatAlreadyBookedException (HTTP 409)");
    }
}
""")

    # SeatRecommendationServiceTest.java
    write_file("service/SeatRecommendationServiceTest.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.service.impl.SeatRecommendationServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class SeatRecommendationServiceTest {

    @Mock
    private SeatService seatService;

    @InjectMocks
    private SeatRecommendationServiceImpl seatRecommendationService;

    private List<SeatDto> seatLayout;

    @BeforeEach
    void setUp() {
        seatLayout = new ArrayList<>();
        String[] rows = {"A", "B", "C", "D", "E"};
        long id = 1;

        for (String row : rows) {
            for (int col = 1; col <= 8; col++) {
                SeatDto seat = new SeatDto(id++, row, col, "REGULAR", new BigDecimal("12.00"), "AVAILABLE");
                seatLayout.add(seat);
            }
        }
    }

    @Test
    @DisplayName("VACANT SEAT RECOMMENDATION TEST: When user requests C5 and it is BOOKED, system finds nearest vacant seat (C4 or C6)")
    void testNearestVacantSeatRecommendation() {
        Long showId = 100L;
        Long targetSeatId = null;

        // Mark C5 as BOOKED
        for (SeatDto seat : seatLayout) {
            if ("C5".equals(seat.getSeatIdentifier())) {
                seat.setStatus("BOOKED");
                targetSeatId = seat.getId();
            }
        }

        assertNotNull(targetSeatId);
        when(seatService.getSeatLayoutForShow(showId)).thenReturn(seatLayout);

        Optional<SeatDto> nearest = seatRecommendationService.findNearestAvailableSeat(showId, targetSeatId);

        assertTrue(nearest.isPresent(), "A nearest available seat must be found");
        SeatDto recommended = nearest.get();
        assertEquals("AVAILABLE", recommended.getStatus());

        // Nearest should be either C4 or C6 (distance = 1 column in same row)
        assertTrue("C4".equals(recommended.getSeatIdentifier()) || "C6".equals(recommended.getSeatIdentifier()),
                "Recommended seat should be adjacent seat C4 or C6, but was: " + recommended.getSeatIdentifier());
    }

    @Test
    @DisplayName("VACANT SEAT RECOMMENDATION TEST: When C5, C4, C6 are all booked, recommends next closest seat in adjacent row or row C")
    void testRecommendationWhenImmediateNeighborsBooked() {
        Long showId = 100L;
        Long targetSeatId = null;

        for (SeatDto seat : seatLayout) {
            if ("C5".equals(seat.getSeatIdentifier())) {
                seat.setStatus("BOOKED");
                targetSeatId = seat.getId();
            } else if ("C4".equals(seat.getSeatIdentifier()) || "C6".equals(seat.getSeatIdentifier())) {
                seat.setStatus("BOOKED");
            }
        }

        assertNotNull(targetSeatId);
        when(seatService.getSeatLayoutForShow(showId)).thenReturn(seatLayout);

        Optional<SeatDto> nearest = seatRecommendationService.findNearestAvailableSeat(showId, targetSeatId);

        assertTrue(nearest.isPresent());
        SeatDto recommended = nearest.get();
        assertEquals("AVAILABLE", recommended.getStatus());
        assertNotEquals("C5", recommended.getSeatIdentifier());
        assertNotEquals("C4", recommended.getSeatIdentifier());
        assertNotEquals("C6", recommended.getSeatIdentifier());
    }
}
""")

    # MovieServiceTest.java
    write_file("service/MovieServiceTest.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.MovieDto;
import com.example.movieticketbooking.entity.Movie;
import com.example.movieticketbooking.repository.MovieRepository;
import com.example.movieticketbooking.service.impl.MovieServiceImpl;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class MovieServiceTest {

    @Mock
    private MovieRepository movieRepository;

    @InjectMocks
    private MovieServiceImpl movieService;

    @Test
    @DisplayName("MOVIE SERVICE TEST: Get all active movies successfully")
    void testGetAllActiveMovies() {
        Movie m1 = new Movie("Interstellar", "Space exploration", "Sci-Fi", 169, "English", LocalDate.of(2014, 11, 7), "url1", 8.7);
        m1.setId(1L);

        Movie m2 = new Movie("Avengers", "Marvel superhero epic", "Action", 181, "English", LocalDate.of(2019, 4, 26), "url2", 8.4);
        m2.setId(2L);

        when(movieRepository.findByActiveTrue()).thenReturn(Arrays.asList(m1, m2));

        List<MovieDto> result = movieService.getAllActiveMovies();

        assertEquals(2, result.size());
        assertEquals("Interstellar", result.get(0).getTitle());
        assertEquals("Avengers", result.get(1).getTitle());
    }

    @Test
    @DisplayName("MOVIE SERVICE TEST: Create movie successfully")
    void testCreateMovie() {
        MovieDto dto = new MovieDto(null, "Dangal", "Wrestling drama", "Drama", 161, "Hindi", LocalDate.of(2016, 12, 23), "url3", 8.3, true);
        Movie saved = new Movie("Dangal", "Wrestling drama", "Drama", 161, "Hindi", LocalDate.of(2016, 12, 23), "url3", 8.3);
        saved.setId(10L);

        when(movieRepository.save(any(Movie.class))).thenReturn(saved);

        MovieDto created = movieService.createMovie(dto);

        assertNotNull(created);
        assertEquals(10L, created.getId());
        assertEquals("Dangal", created.getTitle());
    }
}
""")

if __name__ == "__main__":
    generate_tests()
