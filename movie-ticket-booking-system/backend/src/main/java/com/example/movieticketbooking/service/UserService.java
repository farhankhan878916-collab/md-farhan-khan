package com.example.movieticketbooking.service;

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
