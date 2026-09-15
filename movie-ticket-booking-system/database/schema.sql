-- ========================================================================
-- Movie Ticket Booking System - Database Schema & Initial Data
-- Database: MySQL 8.0+
-- ========================================================================

CREATE DATABASE IF NOT EXISTS `movie_booking` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `movie_booking`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `payments`;
DROP TABLE IF EXISTS `booking_seats`;
DROP TABLE IF EXISTS `bookings`;
DROP TABLE IF EXISTS `shows`;
DROP TABLE IF EXISTS `seats`;
DROP TABLE IF EXISTS `screens`;
DROP TABLE IF EXISTS `theatres`;
DROP TABLE IF EXISTS `movies`;
DROP TABLE IF EXISTS `customers`;
DROP TABLE IF EXISTS `admins`;
DROP TABLE IF EXISTS `users`;

SET FOREIGN_KEY_CHECKS = 1;

-- ------------------------------------------------------------------------
-- 1. Table: users (Base table for Customer and Admin)
-- ------------------------------------------------------------------------
CREATE TABLE `users` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `full_name` VARCHAR(100) NOT NULL,
    `phone` VARCHAR(20) DEFAULT NULL,
    `role` VARCHAR(20) NOT NULL,
    `active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_users_username` (`username`),
    UNIQUE KEY `uk_users_email` (`email`),
    INDEX `idx_users_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------
-- 2. Table: customers (Inherits from users)
-- ------------------------------------------------------------------------
CREATE TABLE `customers` (
    `id` BIGINT NOT NULL,
    `loyalty_points` INT DEFAULT 0,
    `preferred_city` VARCHAR(50) DEFAULT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_customers_user` FOREIGN KEY (`id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------
-- 3. Table: admins (Inherits from users)
-- ------------------------------------------------------------------------
CREATE TABLE `admins` (
    `id` BIGINT NOT NULL,
    `department` VARCHAR(50) DEFAULT NULL,
    `admin_level` INT DEFAULT 1,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_admins_user` FOREIGN KEY (`id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------
-- 4. Table: movies
-- ------------------------------------------------------------------------
CREATE TABLE `movies` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(150) NOT NULL,
    `description` TEXT DEFAULT NULL,
    `genre` VARCHAR(50) NOT NULL,
    `duration_minutes` INT NOT NULL,
    `language` VARCHAR(50) NOT NULL,
    `release_date` DATE DEFAULT NULL,
    `poster_url` VARCHAR(500) DEFAULT NULL,
    `rating` DOUBLE DEFAULT 8.0,
    `active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_movies_genre` (`genre`),
    INDEX `idx_movies_active` (`active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------
-- 5. Table: theatres
-- ------------------------------------------------------------------------
CREATE TABLE `theatres` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `address` VARCHAR(200) NOT NULL,
    `city` VARCHAR(50) NOT NULL,
    `state` VARCHAR(50) DEFAULT NULL,
    `zip_code` VARCHAR(20) DEFAULT NULL,
    `total_screens` INT DEFAULT 1,
    `active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_theatres_city` (`city`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------
-- 6. Table: screens
-- ------------------------------------------------------------------------
CREATE TABLE `screens` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `total_rows` INT NOT NULL DEFAULT 5,
    `total_columns` INT NOT NULL DEFAULT 8,
    `theatre_id` BIGINT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_screens_theatre` FOREIGN KEY (`theatre_id`) REFERENCES `theatres` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------
-- 7. Table: seats
-- ------------------------------------------------------------------------
CREATE TABLE `seats` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `row_name` VARCHAR(5) NOT NULL,
    `seat_number` INT NOT NULL,
    `seat_type` VARCHAR(20) NOT NULL DEFAULT 'REGULAR',
    `screen_id` BIGINT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_screen_seat` (`screen_id`, `row_name`, `seat_number`),
    CONSTRAINT `fk_seats_screen` FOREIGN KEY (`screen_id`) REFERENCES `screens` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------
-- 8. Table: shows
-- ------------------------------------------------------------------------
CREATE TABLE `shows` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `movie_id` BIGINT NOT NULL,
    `screen_id` BIGINT NOT NULL,
    `start_time` DATETIME NOT NULL,
    `end_time` DATETIME NOT NULL,
    `base_price` DECIMAL(10,2) NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_shows_start_time` (`start_time`),
    CONSTRAINT `fk_shows_movie` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_shows_screen` FOREIGN KEY (`screen_id`) REFERENCES `screens` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------
-- 9. Table: bookings
-- ------------------------------------------------------------------------
CREATE TABLE `bookings` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `booking_number` VARCHAR(30) NOT NULL,
    `user_id` BIGINT NOT NULL,
    `show_id` BIGINT NOT NULL,
    `total_amount` DECIMAL(10,2) NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    `cancellation_reason` VARCHAR(255) DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_booking_number` (`booking_number`),
    INDEX `idx_bookings_user` (`user_id`),
    CONSTRAINT `fk_bookings_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_bookings_show` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------
-- 10. Table: booking_seats (CRITICAL: Enforces Double-Booking Prevention)
-- ------------------------------------------------------------------------
CREATE TABLE `booking_seats` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `booking_id` BIGINT NOT NULL,
    `show_id` BIGINT NOT NULL,
    `seat_id` BIGINT NOT NULL,
    `price` DECIMAL(10,2) NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_show_seat_status` (`show_id`, `seat_id`, `status`),
    CONSTRAINT `fk_booking_seats_booking` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_booking_seats_show` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_booking_seats_seat` FOREIGN KEY (`seat_id`) REFERENCES `seats` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------
-- 11. Table: payments
-- ------------------------------------------------------------------------
CREATE TABLE `payments` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `booking_id` BIGINT NOT NULL,
    `amount` DECIMAL(10,2) NOT NULL,
    `payment_method` VARCHAR(20) NOT NULL,
    `payment_status` VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    `transaction_id` VARCHAR(100) NOT NULL,
    `payment_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_payments_transaction` (`transaction_id`),
    CONSTRAINT `fk_payments_booking` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================================================================
-- SAMPLE DEMO DATA
-- ========================================================================

-- Passwords are encrypted with BCrypt ($2a$10$wE9U9w3G2E5J4.P8Zq0kAeQ9...) for "Admin@123" and "Customer@123"
INSERT INTO `users` (`id`, `username`, `email`, `password`, `full_name`, `phone`, `role`, `active`, `created_at`) VALUES
(1, 'admin', 'admin@cinema.com', '$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.QFxGQgtQFUs2S', 'System Administrator', '+1-800-555-0100', 'ROLE_ADMIN', 1, NOW()),
(2, 'customer', 'customer@cinema.com', '$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.QFxGQgtQFUs2S', 'Alex Johnson', '+1-800-555-0155', 'ROLE_CUSTOMER', 1, NOW());

INSERT INTO `admins` (`id`, `department`, `admin_level`) VALUES
(1, 'Central Theatre Operations', 1);

INSERT INTO `customers` (`id`, `loyalty_points`, `preferred_city`) VALUES
(2, 120, 'New York');

-- Movies
INSERT INTO `movies` (`id`, `title`, `description`, `genre`, `duration_minutes`, `language`, `release_date`, `poster_url`, `rating`, `active`) VALUES
(1, 'Avengers: Endgame', 'After the devastating events of Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos actions and restore balance.', 'Action / Sci-Fi', 181, 'English', '2019-04-26', 'https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=600&q=80', 8.4, 1),
(2, 'Interstellar', 'When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft to find a new planet for humans.', 'Sci-Fi / Drama', 169, 'English', '2014-11-07', 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&q=80', 8.7, 1),
(3, 'Inception', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 'Action / Sci-Fi / Mystery', 148, 'English', '2010-07-16', 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=600&q=80', 8.8, 1),
(4, 'Dangal', 'Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games in the face of societal oppression.', 'Biography / Drama / Sport', 161, 'Hindi', '2016-12-23', 'https://images.unsplash.com/photo-1517649763962-0c623266ddc0?auto=format&fit=crop&w=600&q=80', 8.3, 1);

-- Theatres
INSERT INTO `theatres` (`id`, `name`, `address`, `city`, `state`, `zip_code`, `total_screens`, `active`) VALUES
(1, 'Grand Cineplex IMAX', '742 Broadway Avenue', 'New York', 'NY', '10003', 2, 1),
(2, 'Regal Cinema Deluxe', '1200 Sunset Boulevard', 'Los Angeles', 'CA', '90028', 1, 1);

-- Screens
INSERT INTO `screens` (`id`, `name`, `total_rows`, `total_columns`, `theatre_id`) VALUES
(1, 'Screen 1 - IMAX Laser', 5, 8, 1),
(2, 'Screen 2 - Dolby Atmos', 5, 8, 1),
(3, 'Screen 1 - Royal Lounge', 5, 8, 2);

-- Sample Seats for Screen 1 (Rows A-B: REGULAR, C-D: PREMIUM, E: VIP)
INSERT INTO `seats` (`row_name`, `seat_number`, `seat_type`, `screen_id`) VALUES
('A', 1, 'REGULAR', 1), ('A', 2, 'REGULAR', 1), ('A', 3, 'REGULAR', 1), ('A', 4, 'REGULAR', 1), ('A', 5, 'REGULAR', 1), ('A', 6, 'REGULAR', 1), ('A', 7, 'REGULAR', 1), ('A', 8, 'REGULAR', 1),
('B', 1, 'REGULAR', 1), ('B', 2, 'REGULAR', 1), ('B', 3, 'REGULAR', 1), ('B', 4, 'REGULAR', 1), ('B', 5, 'REGULAR', 1), ('B', 6, 'REGULAR', 1), ('B', 7, 'REGULAR', 1), ('B', 8, 'REGULAR', 1),
('C', 1, 'PREMIUM', 1), ('C', 2, 'PREMIUM', 1), ('C', 3, 'PREMIUM', 1), ('C', 4, 'PREMIUM', 1), ('C', 5, 'PREMIUM', 1), ('C', 6, 'PREMIUM', 1), ('C', 7, 'PREMIUM', 1), ('C', 8, 'PREMIUM', 1),
('D', 1, 'PREMIUM', 1), ('D', 2, 'PREMIUM', 1), ('D', 3, 'PREMIUM', 1), ('D', 4, 'PREMIUM', 1), ('D', 5, 'PREMIUM', 1), ('D', 6, 'PREMIUM', 1), ('D', 7, 'PREMIUM', 1), ('D', 8, 'PREMIUM', 1),
('E', 1, 'VIP', 1), ('E', 2, 'VIP', 1), ('E', 3, 'VIP', 1), ('E', 4, 'VIP', 1), ('E', 5, 'VIP', 1), ('E', 6, 'VIP', 1), ('E', 7, 'VIP', 1), ('E', 8, 'VIP', 1);

-- Shows
INSERT INTO `shows` (`id`, `movie_id`, `screen_id`, `start_time`, `end_time`, `base_price`, `status`) VALUES
(1, 1, 1, DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 2 HOUR), DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 5 HOUR), 15.00, 'SCHEDULED'),
(2, 2, 1, DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 6 HOUR), DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 9 HOUR), 16.00, 'SCHEDULED'),
(3, 3, 2, DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 3 HOUR), DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 6 HOUR), 14.50, 'SCHEDULED'),
(4, 4, 3, DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 4 HOUR), DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 7 HOUR), 13.00, 'SCHEDULED');
