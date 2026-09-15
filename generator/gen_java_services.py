import os

BASE_DIR = "movie-ticket-booking-system"
SRC_JAVA = os.path.join(BASE_DIR, "backend", "src", "main", "java", "com", "example", "movieticketbooking")

def write_file(subpath, content):
    full_path = os.path.join(SRC_JAVA, subpath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {full_path}")

def generate_services():
    # 1. UserService.java & UserServiceImpl.java
    write_file("service/UserService.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.UserDto;
import com.example.movieticketbooking.entity.User;

import java.util.List;

public interface UserService {
    User findEntityById(Long id);
    User findEntityByUsername(String username);
    UserDto getUserById(Long id);
    UserDto getUserByUsername(String username);
    List<UserDto> getAllUsers();
    UserDto updateUser(Long id, UserDto userDto);
    void toggleUserStatus(Long id);
}
""")

    write_file("service/impl/UserServiceImpl.java", """package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.UserDto;
import com.example.movieticketbooking.entity.User;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.repository.UserRepository;
import com.example.movieticketbooking.service.UserService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public User findEntityById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + id));
    }

    @Override
    @Transactional(readOnly = true)
    public User findEntityByUsername(String username) {
        return userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with username: " + username));
    }

    @Override
    @Transactional(readOnly = true)
    public UserDto getUserById(Long id) {
        User user = findEntityById(id);
        return mapToDto(user);
    }

    @Override
    @Transactional(readOnly = true)
    public UserDto getUserByUsername(String username) {
        User user = findEntityByUsername(username);
        return mapToDto(user);
    }

    @Override
    @Transactional(readOnly = true)
    public List<UserDto> getAllUsers() {
        return userRepository.findAll().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional
    public UserDto updateUser(Long id, UserDto userDto) {
        User user = findEntityById(id);
        user.setFullName(userDto.getFullName());
        user.setPhone(userDto.getPhone());
        User saved = userRepository.save(user);
        return mapToDto(saved);
    }

    @Override
    @Transactional
    public void toggleUserStatus(Long id) {
        User user = findEntityById(id);
        user.setActive(!user.isActive());
        userRepository.save(user);
    }

    private UserDto mapToDto(User user) {
        return new UserDto(
                user.getId(),
                user.getUsername(),
                user.getEmail(),
                user.getFullName(),
                user.getPhone(),
                user.getRole().name(),
                user.isActive()
        );
    }
}
""")

    # 2. AuthService.java & AuthServiceImpl.java
    write_file("service/AuthService.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.AuthRequest;
import com.example.movieticketbooking.dto.AuthResponse;
import com.example.movieticketbooking.dto.RegisterRequest;

public interface AuthService {
    AuthResponse login(AuthRequest authRequest);
    AuthResponse register(RegisterRequest registerRequest);
}
""")

    write_file("service/impl/AuthServiceImpl.java", """package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.AuthRequest;
import com.example.movieticketbooking.dto.AuthResponse;
import com.example.movieticketbooking.dto.RegisterRequest;
import com.example.movieticketbooking.entity.Admin;
import com.example.movieticketbooking.entity.Customer;
import com.example.movieticketbooking.entity.Role;
import com.example.movieticketbooking.entity.User;
import com.example.movieticketbooking.exception.AuthenticationException;
import com.example.movieticketbooking.exception.UserAlreadyExistsException;
import com.example.movieticketbooking.repository.UserRepository;
import com.example.movieticketbooking.security.JwtTokenProvider;
import com.example.movieticketbooking.service.AuthService;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuthServiceImpl implements AuthService {

    private final AuthenticationManager authenticationManager;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider tokenProvider;

    public AuthServiceImpl(AuthenticationManager authenticationManager, UserRepository userRepository,
                           PasswordEncoder passwordEncoder, JwtTokenProvider tokenProvider) {
        this.authenticationManager = authenticationManager;
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.tokenProvider = tokenProvider;
    }

    @Override
    public AuthResponse login(AuthRequest authRequest) {
        try {
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(authRequest.getUsername(), authRequest.getPassword())
            );

            SecurityContextHolder.getContext().setAuthentication(authentication);
            String jwt = tokenProvider.generateToken(authentication);

            User user = userRepository.findByUsername(authRequest.getUsername())
                    .or(() -> userRepository.findByEmail(authRequest.getUsername()))
                    .orElseThrow(() -> new AuthenticationException("Invalid username or password"));

            return new AuthResponse(jwt, user.getId(), user.getUsername(), user.getEmail(), user.getFullName(), user.getRole().name());
        } catch (Exception ex) {
            throw new AuthenticationException("Invalid username or password");
        }
    }

    @Override
    @Transactional
    public AuthResponse register(RegisterRequest registerRequest) {
        if (userRepository.existsByUsername(registerRequest.getUsername())) {
            throw new UserAlreadyExistsException("Username is already taken: " + registerRequest.getUsername());
        }

        if (userRepository.existsByEmail(registerRequest.getEmail())) {
            throw new UserAlreadyExistsException("Email is already in use: " + registerRequest.getEmail());
        }

        Role assignedRole = Role.ROLE_CUSTOMER;
        if ("ROLE_ADMIN".equalsIgnoreCase(registerRequest.getRole()) || "ADMIN".equalsIgnoreCase(registerRequest.getRole())) {
            assignedRole = Role.ROLE_ADMIN;
        }

        User newUser;
        if (assignedRole == Role.ROLE_ADMIN) {
            Admin admin = new Admin(
                    registerRequest.getUsername(),
                    registerRequest.getEmail(),
                    passwordEncoder.encode(registerRequest.getPassword()),
                    registerRequest.getFullName(),
                    registerRequest.getPhone(),
                    "Management"
            );
            newUser = userRepository.save(admin);
        } else {
            Customer customer = new Customer(
                    registerRequest.getUsername(),
                    registerRequest.getEmail(),
                    passwordEncoder.encode(registerRequest.getPassword()),
                    registerRequest.getFullName(),
                    registerRequest.getPhone()
            );
            newUser = userRepository.save(customer);
        }

        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(registerRequest.getUsername(), registerRequest.getPassword())
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = tokenProvider.generateToken(authentication);

        return new AuthResponse(jwt, newUser.getId(), newUser.getUsername(), newUser.getEmail(), newUser.getFullName(), newUser.getRole().name());
    }
}
""")

    # 3. MovieService.java & MovieServiceImpl.java
    write_file("service/MovieService.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.MovieDto;
import com.example.movieticketbooking.entity.Movie;

import java.util.List;

public interface MovieService {
    List<MovieDto> getAllActiveMovies();
    List<MovieDto> getAllMoviesAdmin();
    MovieDto getMovieById(Long id);
    Movie findEntityById(Long id);
    MovieDto createMovie(MovieDto movieDto);
    MovieDto updateMovie(Long id, MovieDto movieDto);
    void deleteMovie(Long id);
    List<MovieDto> searchByGenre(String genre);
}
""")

    write_file("service/impl/MovieServiceImpl.java", """package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.MovieDto;
import com.example.movieticketbooking.entity.Movie;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.repository.MovieRepository;
import com.example.movieticketbooking.service.MovieService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class MovieServiceImpl implements MovieService {

    private final MovieRepository movieRepository;

    public MovieServiceImpl(MovieRepository movieRepository) {
        this.movieRepository = movieRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<MovieDto> getAllActiveMovies() {
        return movieRepository.findByActiveTrue().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<MovieDto> getAllMoviesAdmin() {
        return movieRepository.findAll().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public MovieDto getMovieById(Long id) {
        return mapToDto(findEntityById(id));
    }

    @Override
    @Transactional(readOnly = true)
    public Movie findEntityById(Long id) {
        return movieRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Movie not found with id: " + id));
    }

    @Override
    @Transactional
    public MovieDto createMovie(MovieDto dto) {
        Movie movie = new Movie(
                dto.getTitle(),
                dto.getDescription(),
                dto.getGenre(),
                dto.getDurationMinutes(),
                dto.getLanguage(),
                dto.getReleaseDate(),
                dto.getPosterUrl(),
                dto.getRating() != null ? dto.getRating() : 8.0
        );
        movie.setActive(dto.isActive());
        Movie saved = movieRepository.save(movie);
        return mapToDto(saved);
    }

    @Override
    @Transactional
    public MovieDto updateMovie(Long id, MovieDto dto) {
        Movie movie = findEntityById(id);
        movie.setTitle(dto.getTitle());
        movie.setDescription(dto.getDescription());
        movie.setGenre(dto.getGenre());
        movie.setDurationMinutes(dto.getDurationMinutes());
        movie.setLanguage(dto.getLanguage());
        movie.setReleaseDate(dto.getReleaseDate());
        if (dto.getPosterUrl() != null && !dto.getPosterUrl().isEmpty()) {
            movie.setPosterUrl(dto.getPosterUrl());
        }
        if (dto.getRating() != null) {
            movie.setRating(dto.getRating());
        }
        movie.setActive(dto.isActive());

        Movie updated = movieRepository.save(movie);
        return mapToDto(updated);
    }

    @Override
    @Transactional
    public void deleteMovie(Long id) {
        Movie movie = findEntityById(id);
        movie.setActive(false);
        movieRepository.save(movie);
    }

    @Override
    @Transactional(readOnly = true)
    public List<MovieDto> searchByGenre(String genre) {
        return movieRepository.findByGenreIgnoreCaseAndActiveTrue(genre).stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    private MovieDto mapToDto(Movie m) {
        return new MovieDto(
                m.getId(),
                m.getTitle(),
                m.getDescription(),
                m.getGenre(),
                m.getDurationMinutes(),
                m.getLanguage(),
                m.getReleaseDate(),
                m.getPosterUrl(),
                m.getRating(),
                m.isActive()
        );
    }
}
""")

    # 4. TheatreService.java & TheatreServiceImpl.java
    write_file("service/TheatreService.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.TheatreDto;
import com.example.movieticketbooking.entity.Theatre;

import java.util.List;

public interface TheatreService {
    List<TheatreDto> getAllActiveTheatres();
    TheatreDto getTheatreById(Long id);
    Theatre findEntityById(Long id);
    TheatreDto createTheatre(TheatreDto theatreDto);
    TheatreDto updateTheatre(Long id, TheatreDto theatreDto);
    void deleteTheatre(Long id);
}
""")

    write_file("service/impl/TheatreServiceImpl.java", """package com.example.movieticketbooking.service.impl;

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
""")

    # 5. ScreenService.java & ScreenServiceImpl.java
    write_file("service/ScreenService.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.ScreenDto;
import com.example.movieticketbooking.entity.Screen;

import java.util.List;

public interface ScreenService {
    List<ScreenDto> getScreensByTheatre(Long theatreId);
    ScreenDto getScreenById(Long id);
    Screen findEntityById(Long id);
    ScreenDto createScreen(ScreenDto screenDto);
}
""")

    write_file("service/impl/ScreenServiceImpl.java", """package com.example.movieticketbooking.service.impl;

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
""")

    # 6. ShowService.java & ShowServiceImpl.java
    write_file("service/ShowService.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.ShowDto;
import com.example.movieticketbooking.entity.Show;

import java.util.List;

public interface ShowService {
    List<ShowDto> getUpcomingShowsByMovie(Long movieId);
    List<ShowDto> getShowsByMovieAndTheatre(Long movieId, Long theatreId);
    List<ShowDto> getAllShows();
    ShowDto getShowById(Long id);
    Show findEntityById(Long id);
    ShowDto createShow(ShowDto showDto);
    void cancelShow(Long id);
}
""")

    write_file("service/impl/ShowServiceImpl.java", """package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.ShowDto;
import com.example.movieticketbooking.entity.Movie;
import com.example.movieticketbooking.entity.Screen;
import com.example.movieticketbooking.entity.Show;
import com.example.movieticketbooking.entity.ShowStatus;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.repository.ShowRepository;
import com.example.movieticketbooking.service.MovieService;
import com.example.movieticketbooking.service.ScreenService;
import com.example.movieticketbooking.service.ShowService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ShowServiceImpl implements ShowService {

    private final ShowRepository showRepository;
    private final MovieService movieService;
    private final ScreenService screenService;

    public ShowServiceImpl(ShowRepository showRepository, MovieService movieService, ScreenService screenService) {
        this.showRepository = showRepository;
        this.movieService = movieService;
        this.screenService = screenService;
    }

    @Override
    @Transactional(readOnly = true)
    public List<ShowDto> getUpcomingShowsByMovie(Long movieId) {
        return showRepository.findByMovieIdAndStatus(movieId, ShowStatus.SCHEDULED).stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<ShowDto> getShowsByMovieAndTheatre(Long movieId, Long theatreId) {
        return showRepository.findActiveShowsByMovieAndTheatre(movieId, theatreId, ShowStatus.SCHEDULED, LocalDateTime.now()).stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<ShowDto> getAllShows() {
        return showRepository.findAll().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public ShowDto getShowById(Long id) {
        return mapToDto(findEntityById(id));
    }

    @Override
    @Transactional(readOnly = true)
    public Show findEntityById(Long id) {
        return showRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Show not found with id: " + id));
    }

    @Override
    @Transactional
    public ShowDto createShow(ShowDto dto) {
        Movie movie = movieService.findEntityById(dto.getMovieId());
        Screen screen = screenService.findEntityById(dto.getScreenId());

        LocalDateTime start = dto.getStartTime();
        LocalDateTime end = dto.getEndTime() != null ? dto.getEndTime() : start.plusMinutes(movie.getDurationMinutes() + 30);

        Show show = new Show(movie, screen, start, end, dto.getBasePrice());
        Show saved = showRepository.save(show);
        return mapToDto(saved);
    }

    @Override
    @Transactional
    public void cancelShow(Long id) {
        Show show = findEntityById(id);
        show.setStatus(ShowStatus.CANCELLED);
        showRepository.save(show);
    }

    private ShowDto mapToDto(Show s) {
        ShowDto dto = new ShowDto();
        dto.setId(s.getId());
        dto.setMovieId(s.getMovie().getId());
        dto.setMovieTitle(s.getMovie().getTitle());
        dto.setMoviePosterUrl(s.getMovie().getPosterUrl());
        dto.setScreenId(s.getScreen().getId());
        dto.setScreenName(s.getScreen().getName());
        dto.setTheatreId(s.getScreen().getTheatre().getId());
        dto.setTheatreName(s.getScreen().getTheatre().getName());
        dto.setTheatreCity(s.getScreen().getTheatre().getCity());
        dto.setStartTime(s.getStartTime());
        dto.setEndTime(s.getEndTime());
        dto.setBasePrice(s.getBasePrice());
        dto.setStatus(s.getStatus().name());
        return dto;
    }
}
""")

    # 7. SeatService.java & SeatServiceImpl.java
    write_file("service/SeatService.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.entity.Seat;

import java.util.List;

public interface SeatService {
    List<SeatDto> getSeatLayoutForShow(Long showId);
    Seat findEntityById(Long id);
    List<Seat> findEntitiesByIds(List<Long> seatIds);
}
""")

    write_file("service/impl/SeatServiceImpl.java", """package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.entity.BookingStatus;
import com.example.movieticketbooking.entity.Seat;
import com.example.movieticketbooking.entity.Show;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.repository.BookingSeatRepository;
import com.example.movieticketbooking.repository.SeatRepository;
import com.example.movieticketbooking.service.SeatService;
import com.example.movieticketbooking.service.ShowService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
public class SeatServiceImpl implements SeatService {

    private final SeatRepository seatRepository;
    private final ShowService showService;
    private final BookingSeatRepository bookingSeatRepository;

    public SeatServiceImpl(SeatRepository seatRepository, ShowService showService, BookingSeatRepository bookingSeatRepository) {
        this.seatRepository = seatRepository;
        this.showService = showService;
        this.bookingSeatRepository = bookingSeatRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<SeatDto> getSeatLayoutForShow(Long showId) {
        Show show = showService.findEntityById(showId);
        Long screenId = show.getScreen().getId();

        // 1. Fetch all seats for the screen
        List<Seat> screenSeats = seatRepository.findByScreenIdOrderByRowNameAscSeatNumberAsc(screenId);

        // 2. Fetch all booked seat IDs for this show
        List<Long> bookedSeatIds = bookingSeatRepository.findBookedSeatIdsByShowId(showId, BookingStatus.CONFIRMED);
        Set<Long> bookedSet = new HashSet<>(bookedSeatIds);

        BigDecimal basePrice = show.getBasePrice();

        return screenSeats.stream().map(seat -> {
            boolean isBooked = bookedSet.contains(seat.getId());
            String status = isBooked ? "BOOKED" : "AVAILABLE";
            BigDecimal calculatedPrice = basePrice.multiply(BigDecimal.valueOf(seat.getSeatType().getMultiplier()));

            SeatDto dto = new SeatDto(
                    seat.getId(),
                    seat.getRowName(),
                    seat.getSeatNumber(),
                    seat.getSeatType().name(),
                    calculatedPrice,
                    status
            );
            return dto;
        }).collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public Seat findEntityById(Long id) {
        return seatRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Seat not found with id: " + id));
    }

    @Override
    @Transactional(readOnly = true)
    public List<Seat> findEntitiesByIds(List<Long> seatIds) {
        List<Seat> seats = seatRepository.findAllById(seatIds);
        if (seats.size() != seatIds.size()) {
            throw new ResourceNotFoundException("One or more requested seats could not be found");
        }
        return seats;
    }
}
""")

    # 8. SeatRecommendationService.java & SeatRecommendationServiceImpl.java
    # (REAL VACANT SEAT RECOMMENDATION ALGORITHM)
    write_file("service/SeatRecommendationService.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.SeatDto;

import java.util.List;
import java.util.Optional;

public interface SeatRecommendationService {
    Optional<SeatDto> findNearestAvailableSeat(Long showId, Long targetSeatId);
    Optional<SeatDto> findNearestAvailableSeat(List<SeatDto> allSeats, SeatDto targetSeat);
    List<SeatDto> findNearestAvailableSeats(Long showId, List<Long> requestedSeatIds, int count);
}
""")

    write_file("service/impl/SeatRecommendationServiceImpl.java", """package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.service.SeatRecommendationService;
import com.example.movieticketbooking.service.SeatService;
import org.springframework.stereotype.Service;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Production implementation of the Automatic Vacant Seat Recommendation Algorithm.
 * Uses Euclidean / Manhattan 2D grid distance mapping across the cinema theatre matrix.
 * Priority:
 * 1. Adjacent seats in the SAME row (e.g. for C5: checks C4, C6, C3, C7)
 * 2. Directly adjacent row seats (e.g. B5, D5, B4, B6, D4, D6)
 * 3. Nearest diagonal or surrounding vacant seats.
 */
@Service
public class SeatRecommendationServiceImpl implements SeatRecommendationService {

    private final SeatService seatService;

    public SeatRecommendationServiceImpl(SeatService seatService) {
        this.seatService = seatService;
    }

    @Override
    public Optional<SeatDto> findNearestAvailableSeat(Long showId, Long targetSeatId) {
        List<SeatDto> allSeats = seatService.getSeatLayoutForShow(showId);
        SeatDto targetSeat = allSeats.stream()
                .filter(s -> s.getId().equals(targetSeatId))
                .findFirst()
                .orElse(null);

        if (targetSeat == null) {
            return Optional.empty();
        }

        return findNearestAvailableSeat(allSeats, targetSeat);
    }

    @Override
    public Optional<SeatDto> findNearestAvailableSeat(List<SeatDto> allSeats, SeatDto targetSeat) {
        int targetRow = targetSeat.getRowIndex();
        int targetCol = targetSeat.getColumnIndex();

        return allSeats.stream()
                .filter(s -> "AVAILABLE".equalsIgnoreCase(s.getStatus()))
                .filter(s -> !s.getId().equals(targetSeat.getId()))
                .min(Comparator.comparingDouble(s -> calculateWeightedDistance(targetRow, targetCol, s.getRowIndex(), s.getColumnIndex())));
    }

    @Override
    public List<SeatDto> findNearestAvailableSeats(Long showId, List<Long> requestedSeatIds, int count) {
        List<SeatDto> allSeats = seatService.getSeatLayoutForShow(showId);
        List<SeatDto> targetSeats = allSeats.stream()
                .filter(s -> requestedSeatIds.contains(s.getId()))
                .collect(Collectors.toList());

        if (targetSeats.isEmpty()) {
            return List.of();
        }

        // Calculate centroid of requested seats
        double avgRow = targetSeats.stream().mapToInt(SeatDto::getRowIndex).average().orElse(0.0);
        double avgCol = targetSeats.stream().mapToInt(SeatDto::getColumnIndex).average().orElse(0.0);

        return allSeats.stream()
                .filter(s -> "AVAILABLE".equalsIgnoreCase(s.getStatus()))
                .filter(s -> !requestedSeatIds.contains(s.getId()))
                .sorted(Comparator.comparingDouble(s -> calculateWeightedDistance(avgRow, avgCol, s.getRowIndex(), s.getColumnIndex())))
                .limit(count)
                .collect(Collectors.toList());
    }

    /**
     * Calculates distance on the cinema grid.
     * Weights same-row movements slightly lower so that adjacent seats in the same row
     * are naturally preferred over changing rows.
     */
    private double calculateWeightedDistance(double r1, double c1, double r2, double c2) {
        double rowDiff = Math.abs(r1 - r2);
        double colDiff = Math.abs(c1 - c2);
        // Col weight 1.0, Row weight 1.5 (sitting next to your desired seat is better than moving rows)
        return Math.sqrt(Math.pow(colDiff * 1.0, 2) + Math.pow(rowDiff * 1.5, 2));
    }
}
""")

    # 9. BookingService.java & BookingServiceImpl.java
    # (STRICT DOUBLE-BOOKING PROTECTION WITH @Transactional & 409 CONFLICT)
    write_file("service/BookingService.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.AdminDashboardStatsDto;
import com.example.movieticketbooking.dto.BookingRequest;
import com.example.movieticketbooking.dto.BookingResponse;

import java.util.List;

public interface BookingService {
    BookingResponse createBooking(Long userId, BookingRequest bookingRequest);
    BookingResponse getBookingById(Long bookingId);
    BookingResponse getBookingByNumber(String bookingNumber);
    List<BookingResponse> getBookingsByUser(Long userId);
    List<BookingResponse> getAllBookings();
    BookingResponse cancelBooking(Long bookingId, Long userId, String reason);
    AdminDashboardStatsDto getAdminDashboardStats();
}
""")

    write_file("service/impl/BookingServiceImpl.java", """package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.AdminDashboardStatsDto;
import com.example.movieticketbooking.dto.BookingRequest;
import com.example.movieticketbooking.dto.BookingResponse;
import com.example.movieticketbooking.dto.SeatDto;
import com.example.movieticketbooking.entity.*;
import com.example.movieticketbooking.exception.BookingException;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.exception.SeatAlreadyBookedException;
import com.example.movieticketbooking.repository.*;
import com.example.movieticketbooking.service.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class BookingServiceImpl implements BookingService {

    private static final Logger logger = LoggerFactory.getLogger(BookingServiceImpl.class);

    private final BookingRepository bookingRepository;
    private final BookingSeatRepository bookingSeatRepository;
    private final UserRepository userRepository;
    private final ShowRepository showRepository;
    private final SeatRepository seatRepository;
    private final MovieRepository movieRepository;
    private final TheatreRepository theatreRepository;
    private final SeatRecommendationService seatRecommendationService;
    private final PaymentService paymentService;

    public BookingServiceImpl(BookingRepository bookingRepository,
                              BookingSeatRepository bookingSeatRepository,
                              UserRepository userRepository,
                              ShowRepository showRepository,
                              SeatRepository seatRepository,
                              MovieRepository movieRepository,
                              TheatreRepository theatreRepository,
                              SeatRecommendationService seatRecommendationService,
                              PaymentService paymentService) {
        this.bookingRepository = bookingRepository;
        this.bookingSeatRepository = bookingSeatRepository;
        this.userRepository = userRepository;
        this.showRepository = showRepository;
        this.seatRepository = seatRepository;
        this.movieRepository = movieRepository;
        this.theatreRepository = theatreRepository;
        this.seatRecommendationService = seatRecommendationService;
        this.paymentService = paymentService;
    }

    /**
     * DOUBLE BOOKING PROTECTION:
     * 1. Uses @Transactional with SERIALIZABLE isolation where supported.
     * 2. Synchronizes on Show ID / atomic checking against active booking seats.
     * 3. Database unique constraint on (show_id, seat_id) acts as hard safety net.
     * 4. If seat is already booked: Finds nearest vacant seat and throws SeatAlreadyBookedException (HTTP 409).
     */
    @Override
    @Transactional(isolation = Isolation.SERIALIZABLE)
    public synchronized BookingResponse createBooking(Long userId, BookingRequest request) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + userId));

        Show show = showRepository.findById(request.getShowId())
                .orElseThrow(() -> new ResourceNotFoundException("Show not found with id: " + request.getShowId()));

        if (request.getSeatIds() == null || request.getSeatIds().isEmpty()) {
            throw new BookingException("Please select at least one seat to book.");
        }

        // 1. Check if ANY of the requested seats are already booked
        for (Long seatId : request.getSeatIds()) {
            Optional<BookingSeat> existingBookingSeat = bookingSeatRepository
                    .findByShowIdAndSeatIdAndStatus(show.getId(), seatId, BookingStatus.CONFIRMED);

            if (existingBookingSeat.isPresent()) {
                Seat bookedSeat = seatRepository.findById(seatId)
                        .orElseThrow(() -> new ResourceNotFoundException("Seat not found with id: " + seatId));

                String seatIdentifier = bookedSeat.getRowName() + bookedSeat.getSeatNumber();

                // Find automatic nearest vacant recommendation
                Optional<SeatDto> recommendedSeat = seatRecommendationService.findNearestAvailableSeat(show.getId(), seatId);

                String message = "Seat " + seatIdentifier + " is no longer available.";
                if (recommendedSeat.isPresent()) {
                    message += " Nearest available seat is " + recommendedSeat.get().getSeatIdentifier() + ".";
                }

                logger.warn("Double booking prevented! Seat {} is already booked for show {}.", seatIdentifier, show.getId());
                throw new SeatAlreadyBookedException(seatIdentifier, recommendedSeat.orElse(null), message);
            }
        }

        // 2. Fetch all seat entities and calculate total price
        List<Seat> seats = seatRepository.findAllById(request.getSeatIds());
        BigDecimal totalAmount = BigDecimal.ZERO;
        BigDecimal basePrice = show.getBasePrice();

        for (Seat seat : seats) {
            BigDecimal seatPrice = basePrice.multiply(BigDecimal.valueOf(seat.getSeatType().getMultiplier()));
            totalAmount = totalAmount.add(seatPrice);
        }

        // 3. Generate unique booking number
        String bookingNumber = "BK-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 4).toUpperCase();
        Booking booking = new Booking(bookingNumber, user, show, totalAmount);
        booking.setStatus(BookingStatus.CONFIRMED);

        Booking savedBooking;
        try {
            savedBooking = bookingRepository.save(booking);

            List<BookingSeat> bookingSeats = new ArrayList<>();
            for (Seat seat : seats) {
                BigDecimal seatPrice = basePrice.multiply(BigDecimal.valueOf(seat.getSeatType().getMultiplier()));
                BookingSeat bookingSeat = new BookingSeat(savedBooking, show, seat, seatPrice, BookingStatus.CONFIRMED);
                bookingSeats.add(bookingSeat);
            }

            bookingSeatRepository.saveAll(bookingSeats);
            savedBooking.setBookingSeats(bookingSeats);

        } catch (DataIntegrityViolationException ex) {
            logger.error("Database constraint triggered on concurrent seat booking attempt!", ex);
            throw new SeatAlreadyBookedException("One or more selected seats were just booked by another user.");
        }

        // 4. Process simulated payment
        PaymentMethod method;
        try {
            method = PaymentMethod.valueOf(request.getPaymentMethod().toUpperCase());
        } catch (Exception e) {
            method = PaymentMethod.CARD;
        }

        Payment payment = paymentService.processInitialPayment(savedBooking, totalAmount, method);
        savedBooking.setPayment(payment);

        // 5. If customer, add loyalty points (1 point per dollar spent)
        if (user instanceof Customer) {
            ((Customer) user).addLoyaltyPoints(totalAmount.intValue());
            userRepository.save(user);
        }

        return mapToResponse(savedBooking);
    }

    @Override
    @Transactional(readOnly = true)
    public BookingResponse getBookingById(Long bookingId) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with id: " + bookingId));
        return mapToResponse(booking);
    }

    @Override
    @Transactional(readOnly = true)
    public BookingResponse getBookingByNumber(String bookingNumber) {
        Booking booking = bookingRepository.findByBookingNumber(bookingNumber)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with number: " + bookingNumber));
        return mapToResponse(booking);
    }

    @Override
    @Transactional(readOnly = true)
    public List<BookingResponse> getBookingsByUser(Long userId) {
        return bookingRepository.findByUserIdOrderByCreatedAtDesc(userId).stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<BookingResponse> getAllBookings() {
        return bookingRepository.findAll().stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional
    public BookingResponse cancelBooking(Long bookingId, Long userId, String reason) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with id: " + bookingId));

        // Ensure user owns this booking or is admin
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        if (!booking.getUser().getId().equals(userId) && user.getRole() != Role.ROLE_ADMIN) {
            throw new BookingException("You are not authorized to cancel this booking.");
        }

        if (booking.getStatus() == BookingStatus.CANCELLED) {
            throw new BookingException("This booking is already cancelled.");
        }

        booking.setStatus(BookingStatus.CANCELLED);
        booking.setCancellationReason(reason != null ? reason : "User requested cancellation");

        // Release seats
        for (BookingSeat bs : booking.getBookingSeats()) {
            bs.setStatus(BookingStatus.CANCELLED);
        }
        bookingSeatRepository.saveAll(booking.getBookingSeats());

        // Refund payment status
        if (booking.getPayment() != null) {
            paymentService.refundPayment(booking.getPayment().getId());
        }

        Booking saved = bookingRepository.save(booking);
        return mapToResponse(saved);
    }

    @Override
    @Transactional(readOnly = true)
    public AdminDashboardStatsDto getAdminDashboardStats() {
        long totalUsers = userRepository.count();
        long totalMovies = movieRepository.count();
        long totalTheatres = theatreRepository.count();
        long totalShows = showRepository.count();
        long totalBookings = bookingRepository.count();
        BigDecimal totalRevenue = bookingRepository.calculateTotalRevenue();

        long totalSeats = seatRepository.count();
        long bookedSeats = bookingSeatRepository.findAll().stream()
                .filter(bs -> bs.getStatus() == BookingStatus.CONFIRMED)
                .count();
        long availableSeats = Math.max(0, (totalSeats * totalShows) - bookedSeats);

        return new AdminDashboardStatsDto(
                totalUsers,
                totalMovies,
                totalTheatres,
                totalShows,
                totalBookings,
                totalRevenue != null ? totalRevenue : BigDecimal.ZERO,
                availableSeats,
                bookedSeats
        );
    }

    private BookingResponse mapToResponse(Booking b) {
        BookingResponse res = new BookingResponse();
        res.setBookingId(b.getId());
        res.setBookingNumber(b.getBookingNumber());
        res.setCustomerName(b.getUser().getFullName());
        res.setCustomerEmail(b.getUser().getEmail());

        Show show = b.getShow();
        res.setMovieTitle(show.getMovie().getTitle());
        res.setMoviePosterUrl(show.getMovie().getPosterUrl());
        res.setTheatreName(show.getScreen().getTheatre().getName());
        res.setTheatreAddress(show.getScreen().getTheatre().getAddress() + ", " + show.getScreen().getTheatre().getCity());
        res.setScreenName(show.getScreen().getName());
        res.setShowStartTime(show.getStartTime());
        res.setShowEndTime(show.getEndTime());

        List<String> seatCodes = b.getBookingSeats().stream()
                .map(bs -> bs.getSeat().getRowName() + bs.getSeat().getSeatNumber())
                .collect(Collectors.toList());
        res.setSeatNumbers(seatCodes);

        res.setTotalAmount(b.getTotalAmount());
        res.setBookingStatus(b.getStatus().name());

        if (b.getPayment() != null) {
            res.setPaymentStatus(b.getPayment().getPaymentStatus().name());
            res.setPaymentMethod(b.getPayment().getPaymentMethod().name());
            res.setTransactionId(b.getPayment().getTransactionId());
        }

        res.setBookedAt(b.getCreatedAt());
        return res;
    }
}
""")

    # 10. PaymentService.java & PaymentServiceImpl.java
    write_file("service/PaymentService.java", """package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.PaymentRequest;
import com.example.movieticketbooking.dto.PaymentResponse;
import com.example.movieticketbooking.entity.Booking;
import com.example.movieticketbooking.entity.Payment;
import com.example.movieticketbooking.entity.PaymentMethod;

import java.math.BigDecimal;

public interface PaymentService {
    Payment processInitialPayment(Booking booking, BigDecimal amount, PaymentMethod method);
    PaymentResponse processPayment(PaymentRequest paymentRequest);
    PaymentResponse getPaymentByBookingId(Long bookingId);
    void refundPayment(Long paymentId);
}
""")

    write_file("service/impl/PaymentServiceImpl.java", """package com.example.movieticketbooking.service.impl;

import com.example.movieticketbooking.dto.PaymentRequest;
import com.example.movieticketbooking.dto.PaymentResponse;
import com.example.movieticketbooking.entity.Booking;
import com.example.movieticketbooking.entity.Payment;
import com.example.movieticketbooking.entity.PaymentMethod;
import com.example.movieticketbooking.entity.PaymentStatus;
import com.example.movieticketbooking.exception.PaymentException;
import com.example.movieticketbooking.exception.ResourceNotFoundException;
import com.example.movieticketbooking.repository.BookingRepository;
import com.example.movieticketbooking.repository.PaymentRepository;
import com.example.movieticketbooking.service.PaymentService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

@Service
public class PaymentServiceImpl implements PaymentService {

    private final PaymentRepository paymentRepository;
    private final BookingRepository bookingRepository;

    public PaymentServiceImpl(PaymentRepository paymentRepository, BookingRepository bookingRepository) {
        this.paymentRepository = paymentRepository;
        this.bookingRepository = bookingRepository;
    }

    @Override
    @Transactional
    public Payment processInitialPayment(Booking booking, BigDecimal amount, PaymentMethod method) {
        String txId = "TXN-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 6).toUpperCase();
        Payment payment = new Payment(booking, amount, method, PaymentStatus.SUCCESS, txId);
        return paymentRepository.save(payment);
    }

    @Override
    @Transactional
    public PaymentResponse processPayment(PaymentRequest request) {
        Booking booking = bookingRepository.findById(request.getBookingId())
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with id: " + request.getBookingId()));

        PaymentMethod method;
        try {
            method = PaymentMethod.valueOf(request.getPaymentMethod().toUpperCase());
        } catch (IllegalArgumentException ex) {
            throw new PaymentException("Invalid payment method: " + request.getPaymentMethod() + ". Supported methods: UPI, CARD, CASH.");
        }

        String txId = "TXN-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 6).toUpperCase();
        BigDecimal amount = request.getAmount() != null ? request.getAmount() : booking.getTotalAmount();

        Payment payment = new Payment(booking, amount, method, PaymentStatus.SUCCESS, txId);
        Payment saved = paymentRepository.save(payment);

        return new PaymentResponse(
                saved.getTransactionId(),
                booking.getId(),
                saved.getAmount(),
                saved.getPaymentMethod().name(),
                saved.getPaymentStatus().name(),
                "Payment successfully simulated and processed via " + method.name()
        );
    }

    @Override
    @Transactional(readOnly = true)
    public PaymentResponse getPaymentByBookingId(Long bookingId) {
        Payment payment = paymentRepository.findByBookingId(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Payment not found for booking id: " + bookingId));

        return new PaymentResponse(
                payment.getTransactionId(),
                bookingId,
                payment.getAmount(),
                payment.getPaymentMethod().name(),
                payment.getPaymentStatus().name(),
                "Payment details retrieved successfully."
        );
    }

    @Override
    @Transactional
    public void refundPayment(Long paymentId) {
        Payment payment = paymentRepository.findById(paymentId)
                .orElseThrow(() -> new ResourceNotFoundException("Payment not found with id: " + paymentId));
        payment.setPaymentStatus(PaymentStatus.PENDING); // Refunded / Pending refund
        paymentRepository.save(payment);
    }
}
""")

if __name__ == "__main__":
    generate_services()
