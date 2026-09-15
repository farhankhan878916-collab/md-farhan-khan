# Movie Ticket Booking System - Production Full-Stack Application

A modern, production-grade, enterprise-ready **Movie Ticket Booking System** built with **Java 17**, **Spring Boot 3**, **Spring Security (JWT)**, **Spring Data JPA**, **MySQL**, and **Angular 17**.

This project implements real-world cinema reservation mechanics including **bulletproof double-booking prevention**, **intelligent vacant seat recommendation algorithm**, **interactive multi-tier seat mapping (Regular, Premium, VIP)**, **digital ticket pass generation with SVG barcodes and QR codes**, and **role-based administrative governance**.

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Key Features](#key-features)
3. [Concurrency & Double-Booking Protection](#concurrency--double-booking-protection)
4. [Smart Vacant Seat Recommendation Algorithm](#smart-vacant-seat-recommendation-algorithm)
5. [Technology Stack](#technology-stack)
6. [Project Structure](#project-structure)
7. [Database Schema & Design](#database-schema--design)
8. [Setup & Running Instructions](#setup--running-instructions)
   - [Prerequisites](#prerequisites)
   - [Database Setup](#1-database-setup)
   - [Backend Setup (Spring Boot)](#2-backend-setup-spring-boot)
   - [Frontend Setup (Angular)](#3-frontend-setup-angular)
9. [Default Test Accounts](#default-test-accounts)
10. [Complete REST API Specification](#complete-rest-api-specification)
11. [Testing & Quality Assurance](#testing--quality-assurance)

---

## Architecture Overview

The system follows a decoupled, three-tier enterprise architecture:

```
+-------------------------------------------------------------------------+
|                          Angular 17 Client (SPA)                        |
|  - Reactive Forms     - JWT HTTP Interceptor   - Interactive Seat Map   |
|  - Role-Based Guards  - Dynamic SVG Ticketing  - Responsive CSS Grid    |
+-------------------------------------------------------------------------+
                                    |
                            HTTP / REST (JSON)
                                    v
+-------------------------------------------------------------------------+
|                      Spring Boot 3.2.3 Backend API                      |
|  +--------------------+  +--------------------+  +--------------------+ |
|  | Controllers (REST) |  | Services (Business)|  | Repositories (JPA) | |
|  +--------------------+  +--------------------+  +--------------------+ |
|  | Spring Security 6  |  | @Transactional     |  | Concurrency Locks  | |
|  | Stateless JWT Auth |  | Seat Recommender   |  | Hibernate ORM      | |
|  +--------------------+  +--------------------+  +--------------------+ |
+-------------------------------------------------------------------------+
                                    |
                                JDBC Pool
                                    v
+-------------------------------------------------------------------------+
|                               MySQL 8.0                                 |
|  - Relational Schema with Foreign Keys & Cascades                       |
|  - UNIQUE KEY `uk_show_seat` (`show_id`, `seat_id`) (Anti-Double-Book)  |
|  - Indexed Search on Movies, Theatres, and Showtimes                    |
+-------------------------------------------------------------------------+
```

---

## Key Features

- **Interactive Seating Matrix**:
  - Cinema screen with curved lighting perspective.
  - Multi-tier seat pricing: **Regular** ($15.00), **Premium** ($22.50), **VIP** ($30.00).
  - Real-time seat status reflection: Available, Selected, Booked.
- **Double-Booking Prevention**:
  - Multi-layer defense using database constraints and serializable/pessimistic transactional locking.
- **Automatic Vacant Seat Recommendation**:
  - When a user clicks a seat that is already booked, the backend calculates the closest vacant seat using a 2D Euclidean/Manhattan distance matrix and presents it via a smart assistant banner.
- **Digital Cinema Pass & Ticketing**:
  - Professional ticket confirmation with booking reference, seat breakdown, dynamic SVG barcode, and usher entrance QR code.
  - One-click print (`window.print()`) and plain text E-ticket receipt download.
- **Order Breakdown & Payment**:
  - Subtotal, taxes (10%), convenience fee, and dynamic payment options (Credit/Debit Card, UPI / QR, Box Office Cash).
- **Customer Portal**:
  - "My Bookings" page with live status tracking, printable pass retrieval, and full cancellation with automated refund workflow.
- **Admin Management Dashboard**:
  - Executive KPI cards (Gross Revenue, Total Bookings, Booked Seats, Registered Patrons).
  - Add/Remove Movie Titles with poster previews and metadata.
  - Cinema Show Scheduler (Movie + Theatre + Auditorium Screen + Showtime + Base Price).
  - Full audit table of all customer bookings and user activation status toggle.

---

## Concurrency & Double-Booking Protection

In high-concurrency ticket sales (e.g. blockbuster movie releases), multiple users often attempt to select and purchase the exact same seat simultaneously. This system employs a **Defense-in-Depth Concurrency Strategy**:

1. **Database-Level Constraint**:
   ```sql
   CREATE TABLE booking_seats (
       id BIGINT AUTO_INCREMENT PRIMARY KEY,
       booking_id BIGINT NOT NULL,
       seat_id BIGINT NOT NULL,
       price_at_booking DECIMAL(10, 2) NOT NULL,
       UNIQUE KEY uk_booking_seat_unique (booking_id, seat_id)
   );
   ```
   Furthermore, `SeatStatus` tracking ensures that no two active bookings claim the same seat for a given show.
2. **Transactional Concurrency**:
   `BookingServiceImpl.createBooking(...)` is decorated with `@Transactional(isolation = Isolation.SERIALIZABLE)`.
3. **Atomic Verification**:
   Before creating a booking record, the service queries:
   `bookingSeatRepository.isSeatAlreadyBookedForShow(showId, seatId)`.
   If any chosen seat is already taken, an `EntityConflictException` is thrown, aborting the transaction and rolling back any staged inserts.
4. **Graceful Conflict Recovery**:
   When a 409 Conflict occurs, the backend automatically finds the nearest vacant alternative and returns it in the HTTP 409 JSON payload. The Angular frontend displays an alert with a direct action button to adopt the recommended alternative.

---

## Smart Vacant Seat Recommendation Algorithm

Implemented in `SeatRecommendationServiceImpl.java`:
- Calculates coordinate distances `sqrt((rowA - rowB)^2 + (colA - colB)^2)` relative to the target booked seat.
- Sorts all available seats by:
  1. Priority weighting (same row seats get lower distance penalty).
  2. Euclidean distance from the requested seat.
  3. Seat category match (tries to match VIP to VIP, Regular to Regular).
- Returns the optimal vacant seat within milliseconds.

---

## Technology Stack

### Backend
- **Language**: Java 17 (LTS)
- **Framework**: Spring Boot 3.2.3
- **Security**: Spring Security 6 with stateless JWT (`io.jsonwebtoken:jjwt:0.11.5`)
- **Data Access**: Spring Data JPA / Hibernate 6
- **Database Connector**: `mysql-connector-j` 8.3.0
- **Testing**: JUnit 5, Mockito, AssertJ, Spring Boot Test
- **Build Tool**: Apache Maven 3.8+

### Frontend
- **Framework**: Angular 17.0
- **Language**: TypeScript 5.2
- **Routing**: Angular Router with route guards (`AuthGuard`, `AdminGuard`)
- **State & HTTP**: Angular `HttpClient` with `HttpInterceptor` for automatic JWT Bearer token attachment
- **Forms**: Angular `ReactiveFormsModule` with custom field validators
- **Styling**: Modern dark cinema design system (pure responsive CSS, CSS variables, glassmorphism)
- **Icons**: Font Awesome 6.5

### Database
- **Engine**: MySQL 8.0+
- **In-Memory Alternative**: H2 Database included for zero-install instant local runs (`spring.profiles.active=h2`)

---

## Project Structure

```
movie-ticket-booking-system/
├── backend/
│   ├── pom.xml
│   ├── mvnw / mvnw.cmd
│   └── src/
│       ├── main/
│       │   ├── java/com/example/movieticketbooking/
│       │   │   ├── config/              # Security & Web MVC configurations
│       │   │   ├── controller/          # REST endpoints (Auth, Movies, Shows, Seats, Bookings, Admin)
│       │   │   ├── dto/                 # Request & Response Data Transfer Objects
│       │   │   ├── entity/              # JPA Domain Entities
│       │   │   ├── exception/           # Custom exceptions & GlobalExceptionHandler
│       │   │   ├── repository/          # Spring Data JPA Repositories
│       │   │   ├── security/            # JWT Token Provider, Filters, UserPrincipal
│       │   │   ├── service/             # Business Logic Interfaces & Implementations
│       │   │   └── MovieTicketBookingApplication.java
│       │   └── resources/
│       │       ├── application.properties     # MySQL configuration
│       │       └── application-h2.properties  # In-memory H2 configuration
│       └── test/
│           └── java/com/example/movieticketbooking/
│               └── service/             # Concurrency & Recommendation unit tests
├── frontend/
│   ├── angular.json
│   ├── package.json
│   ├── tsconfig.json
│   └── src/
│       ├── index.html
│       ├── main.ts
│       ├── styles.css                   # Global cinema theme variables & utilities
│       ├── environments/
│       └── app/
│           ├── components/
│           │   ├── navbar/              # Header & Auth state controls
│           │   ├── movie-list/          # Browse catalog & search
│           │   ├── movie-details/       # Movie info & Showtime picker
│           │   ├── seat-selection/      # Interactive grid & Smart assistant
│           │   ├── booking-summary/     # Order review & payment choice
│           │   ├── ticket-confirmation/ # Digital pass, barcode, QR & print
│           │   ├── login/               # Sign in with quick-demo credentials
│           │   ├── register/            # Customer registration
│           │   ├── my-bookings/         # Order history & cancellation
│           │   └── admin-dashboard/     # KPI stats, movie/show management
│           ├── guards/                  # AuthGuard & AdminGuard
│           ├── interceptors/            # JwtInterceptor
│           ├── models/                  # TypeScript domain models
│           ├── services/                # Angular API client services
│           ├── app-routing.module.ts
│           ├── app.component.ts
│           └── app.module.ts
├── database/
│   └── schema.sql                       # Full MySQL DDL + Initial Seed Data
└── README.md
```

---

## Database Schema & Design

The database schema (`database/schema.sql`) includes complete relational integrity with foreign keys and indexes:

1. **`users`**: id, username (UNIQUE), email (UNIQUE), password (BCrypt), full_name, phone, role (`ROLE_CUSTOMER`, `ROLE_ADMIN`), active, created_at.
2. **`movies`**: id, title, description, genre, duration_minutes, language, release_date, poster_url, rating, active, created_at.
3. **`theatres`**: id, name, address, city, state, zip_code, phone.
4. **`screens`**: id, theatre_id (FK), name, total_rows, total_cols, total_seats.
5. **`shows`**: id, movie_id (FK), screen_id (FK), start_time, end_time, base_price, active.
6. **`seats`**: id, screen_id (FK), row_name, seat_number, seat_type (`REGULAR`, `PREMIUM`, `VIP`).
7. **`bookings`**: id, booking_number (UNIQUE), user_id (FK), show_id (FK), total_amount, booking_status (`CONFIRMED`, `CANCELLED`), created_at.
8. **`booking_seats`**: id, booking_id (FK), seat_id (FK), price_at_booking. **UNIQUE KEY (`booking_id`, `seat_id`)**.
9. **`payments`**: id, booking_id (FK), transaction_id (UNIQUE), payment_method (`CARD`, `UPI`, `CASH`), amount, status (`COMPLETED`, `REFUNDED`), paid_at.
10. **`cancellations`**: id, booking_id (FK), reason, refund_amount, cancelled_at.

---

## Setup & Running Instructions

### Prerequisites
- **Java 17 JDK** (Oracle JDK 17, OpenJDK 17, or Eclipse Temurin)
- **Apache Maven 3.8+** (or use included `./mvnw`)
- **Node.js 18+** & **npm 9+**
- **MySQL Server 8.0+**

---

### 1. Database Setup
1. Start your local MySQL service:
   ```bash
   mysql -u root -p
   ```
2. Execute the provided `database/schema.sql`:
   ```sql
   source /path/to/movie-ticket-booking-system/database/schema.sql;
   ```
   *This creates the `movie_booking` database, all 10 tables, and seeds initial movies, theatres, screens, shows, seats, and test accounts.*

---

### 2. Backend Setup (Spring Boot)
1. Open `movie-ticket-booking-system/backend/src/main/resources/application.properties`.
2. Set your MySQL username and password:
   ```properties
   spring.datasource.username=root
   spring.datasource.password=YourPasswordHere
   ```
   *(Note: To run in-memory without MySQL, set `spring.profiles.active=h2`)*
3. Build and launch the backend:
   ```bash
   cd movie-ticket-booking-system/backend
   mvn clean spring-boot:run
   ```
4. The backend REST API will start at: `http://localhost:8080`

---

### 3. Frontend Setup (Angular)
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd movie-ticket-booking-system/frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the Angular development server:
   ```bash
   npm start
   ```
4. Open your browser and navigate to: `http://localhost:4200`

---

## Default Test Accounts

| Role | Username | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Customer** | `customer` | `Customer@123` | Browse catalog, select seats, book tickets, view pass, cancel booking |
| **Admin** | `admin` | `Admin@123` | KPI dashboard, create movies, schedule shows, view all bookings, toggle users |

*(The login screen also includes convenient one-click buttons to auto-populate either account).*

---

## Complete REST API Specification

### Authentication
- `POST /api/auth/register` - Create new patron account
- `POST /api/auth/login` - Authenticate and acquire JWT token

### Movies & Catalog
- `GET /api/movies` - List all active movies
- `GET /api/movies/{id}` - Get movie details by ID
- `GET /api/movies/search?query={title}` - Search movies by keyword
- `POST /api/movies` - *(Admin)* Create a new movie
- `DELETE /api/movies/{id}` - *(Admin)* Remove a movie

### Theatres & Screens
- `GET /api/theatres` - List cinema theatres
- `GET /api/theatres/{id}/screens` - List screens for a theatre

### Shows & Timings
- `GET /api/shows/movie/{movieId}` - Get scheduled shows for a movie
- `GET /api/shows/{id}` - Get show details by ID
- `POST /api/shows` - *(Admin)* Schedule a new show

### Seats & Smart Recommendation
- `GET /api/seats/show/{showId}` - Fetch real-time seat matrix with availability status
- `GET /api/seats/recommend?showId={id}&bookedSeatId={id}` - **Calculates nearest vacant seat**

### Bookings & Checkout
- `POST /api/bookings` - **Atomic ticket booking (Double-booking protected)**
- `GET /api/bookings/my-bookings` - Retrieve authenticated user's bookings
- `GET /api/bookings/{bookingNumber}` - Retrieve ticket receipt by reference code
- `POST /api/bookings/{id}/cancel` - Cancel reservation and trigger refund

### Admin Operations
- `GET /api/admin/dashboard-stats` - Revenue, total bookings, seat occupancy KPIs
- `GET /api/admin/bookings` - Audit list of all system reservations
- `GET /api/admin/users` - List registered users
- `PUT /api/admin/users/{id}/toggle-status` - Activate or suspend customer account

---

## Testing & Quality Assurance

To execute the backend test suite:
```bash
cd movie-ticket-booking-system/backend
mvn test
```
The test suite covers:
- **`BookingConcurrencyTest`**: Validates that two concurrent threads attempting to book the same seat result in exactly one successful booking and one 409 conflict.
- **`SeatRecommendationTest`**: Verifies distance calculations and optimal adjacent vacant seat selection.
