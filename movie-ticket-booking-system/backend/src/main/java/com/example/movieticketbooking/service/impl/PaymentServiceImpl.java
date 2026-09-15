package com.example.movieticketbooking.service.impl;

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
