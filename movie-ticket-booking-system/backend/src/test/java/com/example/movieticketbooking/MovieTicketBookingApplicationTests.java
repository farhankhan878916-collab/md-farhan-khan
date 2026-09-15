package com.example.movieticketbooking;

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
