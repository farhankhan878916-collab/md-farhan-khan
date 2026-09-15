package com.example.movieticketbooking.config;

import com.example.movieticketbooking.entity.*;
import com.example.movieticketbooking.repository.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Component
public class DataInitializer implements CommandLineRunner {

    private static final Logger logger = LoggerFactory.getLogger(DataInitializer.class);

    private final UserRepository userRepository;
    private final MovieRepository movieRepository;
    private final TheatreRepository theatreRepository;
    private final ScreenRepository screenRepository;
    private final SeatRepository seatRepository;
    private final ShowRepository showRepository;
    private final PasswordEncoder passwordEncoder;

    public DataInitializer(UserRepository userRepository, MovieRepository movieRepository,
                           TheatreRepository theatreRepository, ScreenRepository screenRepository,
                           SeatRepository seatRepository, ShowRepository showRepository,
                           PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.movieRepository = movieRepository;
        this.theatreRepository = theatreRepository;
        this.screenRepository = screenRepository;
        this.seatRepository = seatRepository;
        this.showRepository = showRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    @Transactional
    public void run(String... args) {
        if (userRepository.count() > 0) {
            logger.info("Database already seeded. Skipping initial data creation.");
            return;
        }

        logger.info("Seeding initial demo data for Movie Ticket Booking System...");

        // 1. Create Demo Users (Admin and Customer)
        Admin admin = new Admin(
                "admin",
                "admin@cinema.com",
                passwordEncoder.encode("Admin@123"),
                "Cinema Head Administrator",
                "+1-800-555-0199",
                "Theatre Operations"
        );
        admin.setAdminLevel(1);
        userRepository.save(admin);

        Customer customer = new Customer(
                "customer",
                "customer@cinema.com",
                passwordEncoder.encode("Customer@123"),
                "Alex Johnson",
                "+1-800-555-0144",
                "New York"
        );
        customer.setLoyaltyPoints(150);
        userRepository.save(customer);

        Customer customer2 = new Customer(
                "sarah",
                "sarah@cinema.com",
                passwordEncoder.encode("Sarah@123"),
                "Sarah Connor",
                "+1-800-555-0177",
                "Los Angeles"
        );
        customer2.setLoyaltyPoints(80);
        userRepository.save(customer2);

        // 2. Create Demo Movies (Avengers, Interstellar, Inception, Dangal)
        Movie avengers = new Movie(
                "Avengers: Endgame",
                "After the devastating events of Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos' actions and restore balance.",
                "Action / Sci-Fi",
                181,
                "English",
                LocalDate.of(2019, 4, 26),
                "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=600&q=80",
                8.4
        );

        Movie interstellar = new Movie(
                "Interstellar",
                "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.",
                "Sci-Fi / Drama",
                169,
                "English",
                LocalDate.of(2014, 11, 7),
                "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&q=80",
                8.7
        );

        Movie inception = new Movie(
                "Inception",
                "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O., but his tragic past may doom the project.",
                "Action / Sci-Fi / Mystery",
                148,
                "English",
                LocalDate.of(2010, 7, 16),
                "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=600&q=80",
                8.8
        );

        Movie dangal = new Movie(
                "Dangal",
                "Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games in the face of societal oppression and bureaucratic challenges.",
                "Biography / Drama / Sport",
                161,
                "Hindi",
                LocalDate.of(2016, 12, 23),
                "https://images.unsplash.com/photo-1517649763962-0c623266ddc0?auto=format&fit=crop&w=600&q=80",
                8.3
        );

        movieRepository.saveAll(List.of(avengers, interstellar, inception, dangal));

        // 3. Create Theatres
        Theatre grandCineplex = new Theatre("Grand Cineplex IMAX", "742 Broadway Avenue", "New York", "NY", "10003", 3);
        Theatre regalCinema = new Theatre("Regal Cinema Deluxe", "1200 Sunset Boulevard", "Los Angeles", "CA", "90028", 2);
        theatreRepository.saveAll(List.of(grandCineplex, regalCinema));

        // 4. Create Screens
        Screen screen1 = new Screen("Screen 1 - IMAX Laser", 5, 8, grandCineplex);
        Screen screen2 = new Screen("Screen 2 - Dolby Atmos", 5, 8, grandCineplex);
        Screen screen3 = new Screen("Screen 1 - Royal Lounge", 5, 8, regalCinema);
        screenRepository.saveAll(List.of(screen1, screen2, screen3));

        // 5. Generate Standard Cinema Seat Layout (Rows A to E, Seats 1 to 8)
        // Rows A-B: REGULAR, Row C-D: PREMIUM, Row E: VIP
        createSeatsForScreen(screen1);
        createSeatsForScreen(screen2);
        createSeatsForScreen(screen3);

        // 6. Create Shows (Today and Tomorrow)
        LocalDateTime now = LocalDateTime.now();
        List<Show> shows = new ArrayList<>();

        shows.add(new Show(avengers, screen1, now.plusHours(2).withMinute(0).withSecond(0), now.plusHours(5), new BigDecimal("14.50")));
        shows.add(new Show(avengers, screen1, now.plusHours(6).withMinute(30).withSecond(0), now.plusHours(9).plusMinutes(30), new BigDecimal("16.00")));
        shows.add(new Show(interstellar, screen2, now.plusHours(3).withMinute(0).withSecond(0), now.plusHours(6), new BigDecimal("15.00")));
        shows.add(new Show(inception, screen1, now.plusDays(1).withHour(18).withMinute(0), now.plusDays(1).withHour(20).plusMinutes(30), new BigDecimal("14.00")));
        shows.add(new Show(dangal, screen3, now.plusHours(4).withMinute(0).withSecond(0), now.plusHours(7), new BigDecimal("13.00")));

        showRepository.saveAll(shows);

        logger.info("Successfully seeded database with {} movies, {} theatres, and {} initial shows.",
                movieRepository.count(), theatreRepository.count(), showRepository.count());
    }

    private void createSeatsForScreen(Screen screen) {
        List<Seat> seats = new ArrayList<>();
        String[] rows = {"A", "B", "C", "D", "E"};

        for (String row : rows) {
            SeatType type;
            if (row.equals("E")) {
                type = SeatType.VIP;
            } else if (row.equals("C") || row.equals("D")) {
                type = SeatType.PREMIUM;
            } else {
                type = SeatType.REGULAR;
            }

            for (int col = 1; col <= 8; col++) {
                seats.add(new Seat(row, col, type, screen));
            }
        }
        seatRepository.saveAll(seats);
    }
}
