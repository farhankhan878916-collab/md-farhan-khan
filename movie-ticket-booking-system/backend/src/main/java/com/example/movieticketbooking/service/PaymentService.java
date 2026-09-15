package com.example.movieticketbooking.service;

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
