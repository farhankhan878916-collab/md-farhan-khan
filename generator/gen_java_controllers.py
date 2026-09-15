import os

BASE_DIR = "movie-ticket-booking-system"
SRC_JAVA = os.path.join(BASE_DIR, "backend", "src", "main", "java", "com", "example", "movieticketbooking")

def write_file(subpath, content):
    full_path = os.path.join(SRC_JAVA, subpath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {full_path}")

def generate_controllers():
    # AuthController.java
    write_file("controller/AuthController.java", """package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.AuthRequest;
import com.example.movieticketbooking.dto.AuthResponse;
import com.example.movieticketbooking.dto.RegisterRequest;
import com.example.movieticketbooking.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<AuthResponse>> login(@Valid @RequestBody AuthRequest authRequest) {
        AuthResponse response = authService.login(authRequest);
        return ResponseEntity.ok(ApiResponse.ok("User logged in successfully", response));
    }

    @PostMapping("/register")
    public ResponseEntity<ApiResponse<AuthResponse>> register(@Valid @RequestBody RegisterRequest registerRequest) {
        AuthResponse response = authService.register(registerRequest);
        return ResponseEntity.ok(ApiResponse.ok("User registered successfully", response));
    }
}
""")

    # MovieController.java
    write_file("controller/MovieController.java", """package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.MovieDto;
import com.example.movieticketbooking.service.MovieService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/movies")
@CrossOrigin(origins = "*")
public class MovieController {

    private final MovieService movieService;

    public MovieController(MovieService movieService) {
        this.movieService = movieService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<MovieDto>>> getAllMovies() {
        return ResponseEntity.ok(ApiResponse.ok("Movies retrieved successfully", movieService.getAllActiveMovies()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<MovieDto>> getMovieById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.ok("Movie retrieved successfully", movieService.getMovieById(id)));
    }

    @GetMapping("/genre/{genre}")
    public ResponseEntity<ApiResponse<List<MovieDto>>> getMoviesByGenre(@PathVariable String genre) {
        return ResponseEntity.ok(ApiResponse.ok("Movies retrieved by genre", movieService.searchByGenre(genre)));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<MovieDto>> createMovie(@Valid @RequestBody MovieDto movieDto) {
        MovieDto created = movieService.createMovie(movieDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok("Movie created successfully", created));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<MovieDto>> updateMovie(@PathVariable Long id, @Valid @RequestBody MovieDto movieDto) {
        MovieDto updated = movieService.updateMovie(id, movieDto);
        return ResponseEntity.ok(ApiResponse.ok("Movie updated successfully", updated));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> deleteMovie(@PathVariable Long id) {
        movieService.deleteMovie(id);
        return ResponseEntity.ok(ApiResponse.ok("Movie deleted successfully", null));
    }
}
""")

    # TheatreController.java
    write_file("controller/TheatreController.java", """package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.TheatreDto;
import com.example.movieticketbooking.service.TheatreService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/theatres")
@CrossOrigin(origins = "*")
public class TheatreController {

    private final TheatreService theatreService;

    public TheatreController(TheatreService theatreService) {
        this.theatreService = theatreService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<TheatreDto>>> getAllTheatres() {
        return ResponseEntity.ok(ApiResponse.ok("Theatres retrieved successfully", theatreService.getAllActiveTheatres()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<TheatreDto>> getTheatreById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.ok("Theatre retrieved successfully", theatreService.getTheatreById(id)));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<TheatreDto>> createTheatre(@Valid @RequestBody TheatreDto theatreDto) {
        TheatreDto created = theatreService.createTheatre(theatreDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok("Theatre created successfully", created));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<TheatreDto>> updateTheatre(@PathVariable Long id, @Valid @RequestBody TheatreDto theatreDto) {
        TheatreDto updated = theatreService.updateTheatre(id, theatreDto);
        return ResponseEntity.ok(ApiResponse.ok("Theatre updated successfully", updated));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> deleteTheatre(@PathVariable Long id) {
        theatreService.deleteTheatre(id);
        return ResponseEntity.ok(ApiResponse.ok("Theatre deleted successfully", null));
    }
}
""")

    # ScreenController.java
    write_file("controller/ScreenController.java", """package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.ScreenDto;
import com.example.movieticketbooking.service.ScreenService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/screens")
@CrossOrigin(origins = "*")
public class ScreenController {

    private final ScreenService screenService;

    public ScreenController(ScreenService screenService) {
        this.screenService = screenService;
    }

    @GetMapping("/theatre/{theatreId}")
    public ResponseEntity<ApiResponse<List<ScreenDto>>> getScreensByTheatre(@PathVariable Long theatreId) {
        return ResponseEntity.ok(ApiResponse.ok("Screens retrieved successfully", screenService.getScreensByTheatre(theatreId)));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<ScreenDto>> getScreenById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.ok("Screen retrieved successfully", screenService.getScreenById(id)));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<ScreenDto>> createScreen(@Valid @RequestBody ScreenDto screenDto) {
        ScreenDto created = screenService.createScreen(screenDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok("Screen created successfully", created));
    }
}
""")

    # ShowController.java
    write_file("controller/ShowController.java", """package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.ShowDto;
import com.example.movieticketbooking.service.ShowService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/shows")
@CrossOrigin(origins = "*")
public class ShowController {

    private final ShowService showService;

    public ShowController(ShowService showService) {
        this.showService = showService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<ShowDto>>> getAllShows() {
        return ResponseEntity.ok(ApiResponse.ok("Shows retrieved successfully", showService.getAllShows()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<ShowDto>> getShowById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.ok("Show retrieved successfully", showService.getShowById(id)));
    }

    @GetMapping("/movie/{movieId}")
    public ResponseEntity<ApiResponse<List<ShowDto>>> getUpcomingShowsByMovie(@PathVariable Long movieId) {
        return ResponseEntity.ok(ApiResponse.ok("Shows retrieved for movie", showService.getUpcomingShowsByMovie(movieId)));
    }

    @GetMapping("/movie/{movieId}/theatre/{theatreId}")
    public ResponseEntity<ApiResponse<List<ShowDto>>> getShowsByMovieAndTheatre(@PathVariable Long movieId, @PathVariable Long theatreId) {
        return ResponseEntity.ok(ApiResponse.ok("Shows retrieved for movie and theatre", showService.getShowsByMovieAndTheatre(movieId, theatreId)));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<ShowDto>> createShow(@Valid @RequestBody ShowDto showDto) {
        ShowDto created = showService.createShow(showDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok("Show created successfully", created));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> cancelShow(@PathVariable Long id) {
        showService.cancelShow(id);
        return ResponseEntity.ok(ApiResponse.ok("Show cancelled successfully", null));
    }
}
""")

    # SeatController.java
    write_file("controller/SeatController.java", """package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.service.SeatRecommendationService;
import com.example.movieticketbooking.service.SeatService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/shows/{showId}/seats")
@CrossOrigin(origins = "*")
public class SeatController {

    private final SeatService seatService;
    private final SeatRecommendationService seatRecommendationService;

    public SeatController(SeatService seatService, SeatRecommendationService seatRecommendationService) {
        this.seatService = seatService;
        this.seatRecommendationService = seatRecommendationService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<SeatDto>>> getSeatsForShow(@PathVariable Long showId) {
        List<SeatDto> seatLayout = seatService.getSeatLayoutForShow(showId);
        return ResponseEntity.ok(ApiResponse.ok("Seat layout retrieved successfully", seatLayout));
    }

    @GetMapping("/recommend")
    public ResponseEntity<ApiResponse<SeatDto>> getRecommendedSeat(@PathVariable Long showId,
                                                                   @RequestParam Long targetSeatId) {
        SeatDto recommended = seatRecommendationService.findNearestAvailableSeat(showId, targetSeatId)
                .orElse(null);
        return ResponseEntity.ok(ApiResponse.ok("Recommended seat retrieved", recommended));
    }
}
""")

    # BookingController.java
    write_file("controller/BookingController.java", """package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.BookingRequest;
import com.example.movieticketbooking.dto.BookingResponse;
import com.example.movieticketbooking.security.UserPrincipal;
import com.example.movieticketbooking.service.BookingService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/bookings")
@CrossOrigin(origins = "*")
public class BookingController {

    private final BookingService bookingService;

    public BookingController(BookingService bookingService) {
        this.bookingService = bookingService;
    }

    @PostMapping
    public ResponseEntity<ApiResponse<BookingResponse>> createBooking(@AuthenticationPrincipal UserPrincipal currentUser,
                                                                      @Valid @RequestBody BookingRequest request) {
        BookingResponse response = bookingService.createBooking(currentUser.getId(), request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok("Booking confirmed successfully", response));
    }

    @GetMapping("/my")
    public ResponseEntity<ApiResponse<List<BookingResponse>>> getMyBookings(@AuthenticationPrincipal UserPrincipal currentUser) {
        List<BookingResponse> bookings = bookingService.getBookingsByUser(currentUser.getId());
        return ResponseEntity.ok(ApiResponse.ok("User bookings retrieved successfully", bookings));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<BookingResponse>> getBookingById(@PathVariable Long id) {
        BookingResponse response = bookingService.getBookingById(id);
        return ResponseEntity.ok(ApiResponse.ok("Booking details retrieved", response));
    }

    @GetMapping("/number/{bookingNumber}")
    public ResponseEntity<ApiResponse<BookingResponse>> getBookingByNumber(@PathVariable String bookingNumber) {
        BookingResponse response = bookingService.getBookingByNumber(bookingNumber);
        return ResponseEntity.ok(ApiResponse.ok("Booking details retrieved", response));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse<BookingResponse>> cancelBooking(@AuthenticationPrincipal UserPrincipal currentUser,
                                                                      @PathVariable Long id,
                                                                      @RequestParam(required = false) String reason) {
        BookingResponse cancelled = bookingService.cancelBooking(id, currentUser.getId(), reason);
        return ResponseEntity.ok(ApiResponse.ok("Booking cancelled successfully", cancelled));
    }
}
""")

    # PaymentController.java
    write_file("controller/PaymentController.java", """package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.PaymentRequest;
import com.example.movieticketbooking.dto.PaymentResponse;
import com.example.movieticketbooking.service.PaymentService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/payments")
@CrossOrigin(origins = "*")
public class PaymentController {

    private final PaymentService paymentService;

    public PaymentController(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    @PostMapping("/process")
    public ResponseEntity<ApiResponse<PaymentResponse>> processPayment(@Valid @RequestBody PaymentRequest request) {
        PaymentResponse response = paymentService.processPayment(request);
        return ResponseEntity.ok(ApiResponse.ok("Payment processed successfully", response));
    }

    @GetMapping("/booking/{bookingId}")
    public ResponseEntity<ApiResponse<PaymentResponse>> getPaymentByBooking(@PathVariable Long bookingId) {
        PaymentResponse response = paymentService.getPaymentByBookingId(bookingId);
        return ResponseEntity.ok(ApiResponse.ok("Payment details retrieved", response));
    }
}
""")

    # AdminController.java
    write_file("controller/AdminController.java", """package com.example.movieticketbooking.controller;

import com.example.movieticketbooking.dto.AdminDashboardStatsDto;
import com.example.movieticketbooking.dto.ApiResponse;
import com.example.movieticketbooking.dto.BookingResponse;
import com.example.movieticketbooking.dto.UserDto;
import com.example.movieticketbooking.service.BookingService;
import com.example.movieticketbooking.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/admin")
@PreAuthorize("hasRole('ADMIN')")
@CrossOrigin(origins = "*")
public class AdminController {

    private final BookingService bookingService;
    private final UserService userService;

    public AdminController(BookingService bookingService, UserService userService) {
        this.bookingService = bookingService;
        this.userService = userService;
    }

    @GetMapping("/dashboard")
    public ResponseEntity<ApiResponse<AdminDashboardStatsDto>> getDashboardStats() {
        AdminDashboardStatsDto stats = bookingService.getAdminDashboardStats();
        return ResponseEntity.ok(ApiResponse.ok("Admin stats retrieved successfully", stats));
    }

    @GetMapping("/users")
    public ResponseEntity<ApiResponse<List<UserDto>>> getAllUsers() {
        return ResponseEntity.ok(ApiResponse.ok("Users retrieved successfully", userService.getAllUsers()));
    }

    @PutMapping("/users/{id}/toggle-status")
    public ResponseEntity<ApiResponse<Void>> toggleUserStatus(@PathVariable Long id) {
        userService.toggleUserStatus(id);
        return ResponseEntity.ok(ApiResponse.ok("User status updated successfully", null));
    }

    @GetMapping("/bookings")
    public ResponseEntity<ApiResponse<List<BookingResponse>>> getAllBookings() {
        return ResponseEntity.ok(ApiResponse.ok("All bookings retrieved successfully", bookingService.getAllBookings()));
    }
}
""")

if __name__ == "__main__":
    generate_controllers()
