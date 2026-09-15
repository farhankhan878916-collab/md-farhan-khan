package com.example.movieticketbooking.service;

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
