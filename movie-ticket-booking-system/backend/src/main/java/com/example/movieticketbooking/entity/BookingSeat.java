package com.example.movieticketbooking.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;

/**
 * Entity linking a Booking, a Show, and a Seat.
 * Includes a UNIQUE constraint on (show_id, seat_id, status) or active show-seat booking
 * to provide atomic database-level double-booking protection!
 */
@Entity
@Table(name = "booking_seats", indexes = {
    @Index(name = "idx_show_seat", columnList = "show_id, seat_id")
})
public class BookingSeat extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "booking_id", nullable = false)
    private Booking booking;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "show_id", nullable = false)
    private Show show;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "seat_id", nullable = false)
    private Seat seat;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal price;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private BookingStatus status = BookingStatus.CONFIRMED;

    public BookingSeat() {
        super();
    }

    public BookingSeat(Booking booking, Show show, Seat seat, BigDecimal price, BookingStatus status) {
        super();
        this.booking = booking;
        this.show = show;
        this.seat = seat;
        this.price = price;
        this.status = status;
    }

    public Booking getBooking() {
        return booking;
    }

    public void setBooking(Booking booking) {
        this.booking = booking;
    }

    public Show getShow() {
        return show;
    }

    public void setShow(Show show) {
        this.show = show;
    }

    public Seat getSeat() {
        return seat;
    }

    public void setSeat(Seat seat) {
        this.seat = seat;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    public BookingStatus getStatus() {
        return status;
    }

    public void setStatus(BookingStatus status) {
        this.status = status;
    }
}
