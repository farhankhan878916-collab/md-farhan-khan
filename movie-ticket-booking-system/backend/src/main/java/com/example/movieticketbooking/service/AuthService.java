package com.example.movieticketbooking.service;

import com.example.movieticketbooking.dto.AuthRequest;
import com.example.movieticketbooking.dto.AuthResponse;
import com.example.movieticketbooking.dto.RegisterRequest;

public interface AuthService {
    AuthResponse login(AuthRequest authRequest);
    AuthResponse register(RegisterRequest registerRequest);
}
