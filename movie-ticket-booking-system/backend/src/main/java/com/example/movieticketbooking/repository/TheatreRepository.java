package com.example.movieticketbooking.repository;

import com.example.movieticketbooking.entity.Theatre;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TheatreRepository extends JpaRepository<Theatre, Long> {
    List<Theatre> findByActiveTrue();
    List<Theatre> findByCityIgnoreCaseAndActiveTrue(String city);
}
