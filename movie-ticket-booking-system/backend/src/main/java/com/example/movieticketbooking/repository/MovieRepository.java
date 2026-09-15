package com.example.movieticketbooking.repository;

import com.example.movieticketbooking.entity.Movie;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MovieRepository extends JpaRepository<Movie, Long> {
    List<Movie> findByActiveTrue();
    List<Movie> findByGenreIgnoreCaseAndActiveTrue(String genre);
    List<Movie> findByLanguageIgnoreCaseAndActiveTrue(String language);
}
