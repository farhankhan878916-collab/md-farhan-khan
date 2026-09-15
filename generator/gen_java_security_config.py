import os

BASE_DIR = "movie-ticket-booking-system"
SRC_JAVA = os.path.join(BASE_DIR, "backend", "src", "main", "java", "com", "example", "movieticketbooking")

def write_file(subpath, content):
    full_path = os.path.join(SRC_JAVA, subpath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {full_path}")

def generate_security_and_config():
    # UserPrincipal.java
    write_file("security/UserPrincipal.java", """package com.example.movieticketbooking.security;

import com.example.movieticketbooking.entity.User;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.Collections;

public class UserPrincipal implements UserDetails {
    private final Long id;
    private final String username;
    private final String email;
    private final String password;
    private final String fullName;
    private final Collection<? extends GrantedAuthority> authorities;
    private final boolean active;

    public UserPrincipal(Long id, String username, String email, String password, String fullName, Collection<? extends GrantedAuthority> authorities, boolean active) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.password = password;
        this.fullName = fullName;
        this.authorities = authorities;
        this.active = active;
    }

    public static UserPrincipal create(User user) {
        GrantedAuthority authority = new SimpleGrantedAuthority(user.getRole().name());
        return new UserPrincipal(
                user.getId(),
                user.getUsername(),
                user.getEmail(),
                user.getPassword(),
                user.getFullName(),
                Collections.singletonList(authority),
                user.isActive()
        );
    }

    public Long getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public String getFullName() {
        return fullName;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities;
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return username;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return active;
    }
}
""")

    # CustomUserDetailsService.java
    write_file("security/CustomUserDetailsService.java", """package com.example.movieticketbooking.security;

import com.example.movieticketbooking.entity.User;
import com.example.movieticketbooking.repository.UserRepository;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class CustomUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;

    public CustomUserDetailsService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public UserDetails loadUserByUsername(String usernameOrEmail) throws UsernameNotFoundException {
        User user = userRepository.findByUsername(usernameOrEmail)
                .or(() -> userRepository.findByEmail(usernameOrEmail))
                .orElseThrow(() -> new UsernameNotFoundException("User not found with username or email: " + usernameOrEmail));

        return UserPrincipal.create(user);
    }

    @Transactional(readOnly = true)
    public UserDetails loadUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UsernameNotFoundException("User not found with id: " + id));

        return UserPrincipal.create(user);
    }
}
""")

    # JwtTokenProvider.java
    write_file("security/JwtTokenProvider.java", """package com.example.movieticketbooking.security;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.security.Key;
import java.util.Date;

@Component
public class JwtTokenProvider {

    private static final Logger logger = LoggerFactory.getLogger(JwtTokenProvider.class);

    @Value("${app.jwt.secret:9a3f2c4e6b8a1d5e7f0c2b4a6d8e1f3a5c7e9b1d3f5a7c9e1b3d5f7a9c1e3b5a}")
    private String jwtSecret;

    @Value("${app.jwt.expiration-ms:86400000}")
    private long jwtExpirationInMs;

    private Key getSigningKey() {
        byte[] keyBytes = jwtSecret.getBytes(StandardCharsets.UTF_8);
        return Keys.hmacShaKeyFor(keyBytes);
    }

    public String generateToken(Authentication authentication) {
        UserPrincipal userPrincipal = (UserPrincipal) authentication.getPrincipal();

        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + jwtExpirationInMs);

        return Jwts.builder()
                .setSubject(Long.toString(userPrincipal.getId()))
                .claim("username", userPrincipal.getUsername())
                .claim("email", userPrincipal.getEmail())
                .claim("role", userPrincipal.getAuthorities().iterator().next().getAuthority())
                .setIssuedAt(new Date())
                .setExpiration(expiryDate)
                .signWith(getSigningKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    public Long getUserIdFromJWT(String token) {
        Claims claims = Jwts.parserBuilder()
                .setSigningKey(getSigningKey())
                .build()
                .parseClaimsJws(token)
                .getBody();

        return Long.parseLong(claims.getSubject());
    }

    public boolean validateToken(String authToken) {
        try {
            Jwts.parserBuilder().setSigningKey(getSigningKey()).build().parseClaimsJws(authToken);
            return true;
        } catch (SecurityException | MalformedJwtException ex) {
            logger.error("Invalid JWT signature");
        } catch (ExpiredJwtException ex) {
            logger.error("Expired JWT token");
        } catch (UnsupportedJwtException ex) {
            logger.error("Unsupported JWT token");
        } catch (IllegalArgumentException ex) {
            logger.error("JWT claims string is empty.");
        }
        return false;
    }
}
""")

    # JwtAuthenticationFilter.java
    write_file("security/JwtAuthenticationFilter.java", """package com.example.movieticketbooking.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private static final Logger logger = LoggerFactory.getLogger(JwtAuthenticationFilter.class);

    private final JwtTokenProvider tokenProvider;
    private final CustomUserDetailsService customUserDetailsService;

    public JwtAuthenticationFilter(JwtTokenProvider tokenProvider, CustomUserDetailsService customUserDetailsService) {
        this.tokenProvider = tokenProvider;
        this.customUserDetailsService = customUserDetailsService;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        try {
            String jwt = getJwtFromRequest(request);

            if (StringUtils.hasText(jwt) && tokenProvider.validateToken(jwt)) {
                Long userId = tokenProvider.getUserIdFromJWT(jwt);
                UserDetails userDetails = customUserDetailsService.loadUserById(userId);

                UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(
                        userDetails, null, userDetails.getAuthorities());
                authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

                SecurityContextHolder.getContext().setAuthentication(authentication);
            }
        } catch (Exception ex) {
            logger.error("Could not set user authentication in security context", ex);
        }

        filterChain.doFilter(request, response);
    }

    private String getJwtFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (StringUtils.hasText(bearerToken) && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }
}
""")

    # SecurityConfig.java
    write_file("security/SecurityConfig.java", """package com.example.movieticketbooking.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    private final CustomUserDetailsService userDetailsService;
    private final JwtAuthenticationFilter jwtAuthenticationFilter;

    public SecurityConfig(CustomUserDetailsService userDetailsService, JwtAuthenticationFilter jwtAuthenticationFilter) {
        this.userDetailsService = userDetailsService;
        this.jwtAuthenticationFilter = jwtAuthenticationFilter;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public DaoAuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
        authProvider.setUserDetailsService(userDetailsService);
        authProvider.setPasswordEncoder(passwordEncoder());
        return authProvider;
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration authConfig) throws Exception {
        return authConfig.getAuthenticationManager();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(AbstractHttpConfigurer::disable)
            .cors(cors -> {})
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                // Public endpoints
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/movies/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/theatres/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/shows/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/screens/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/seats/**").permitAll()
                .requestMatchers("/h2-console/**").permitAll()
                // Admin endpoints
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.POST, "/api/movies/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.PUT, "/api/movies/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.DELETE, "/api/movies/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.POST, "/api/theatres/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.POST, "/api/shows/**").hasRole("ADMIN")
                // Authenticated user endpoints (Customer or Admin)
                .requestMatchers("/api/bookings/**").authenticated()
                .requestMatchers("/api/payments/**").authenticated()
                .requestMatchers("/api/users/**").authenticated()
                .anyRequest().authenticated()
            );

        http.authenticationProvider(authenticationProvider());
        http.addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);

        // Required to allow H2 in-memory console if enabled
        http.headers(headers -> headers.frameOptions(frame -> frame.disable()));

        return http.build();
    }
}
""")

    # CorsConfig.java
    write_file("config/CorsConfig.java", """package com.example.movieticketbooking.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

import java.util.Arrays;
import java.util.List;

@Configuration
public class CorsConfig {

    @Bean
    public CorsFilter corsFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        
        config.setAllowCredentials(true);
        config.setAllowedOriginPatterns(List.of(
                "http://localhost:4200",
                "http://127.0.0.1:4200",
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "*"
        ));
        config.setAllowedHeaders(Arrays.asList(
                "Origin", "Content-Type", "Accept", "Authorization",
                "X-Requested-With", "Access-Control-Request-Method", "Access-Control-Request-Headers"
        ));
        config.setExposedHeaders(Arrays.asList(
                "Access-Control-Allow-Origin", "Access-Control-Allow-Credentials", "Authorization"
        ));
        config.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"));
        
        source.registerCorsConfiguration("/**", config);
        return new CorsFilter(source);
    }
}
""")

    # DataInitializer.java (Seeds Avengers, Interstellar, Inception, Dangal, theatres, screens, shows, seats, admin, customer)
    write_file("config/DataInitializer.java", """package com.example.movieticketbooking.config;

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
""")

    # Main Application Entry Point
    write_file("MovieTicketBookingApplication.java", """package com.example.movieticketbooking;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MovieTicketBookingApplication {

    public static void main(String[] args) {
        SpringApplication.run(MovieTicketBookingApplication.class, args);
    }
}
""")

if __name__ == "__main__":
    generate_security_and_config()
