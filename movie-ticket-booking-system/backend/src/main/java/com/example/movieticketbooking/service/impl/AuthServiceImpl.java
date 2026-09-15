package com.example.movieticketbooking.service.impl;

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
