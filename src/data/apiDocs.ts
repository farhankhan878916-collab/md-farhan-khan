import { ApiEndpoint } from '../types';

export const API_ENDPOINTS: ApiEndpoint[] = [
  {
    method: 'POST',
    path: '/api/auth/register',
    summary: 'Register a new customer account with BCrypt password hashing',
    authRequired: false,
    requestBody: '{\n  "fullName": "Sarah Connor",\n  "username": "sarah",\n  "email": "sarah@example.com",\n  "password": "Password@123",\n  "phone": "+1-555-0199"\n}',
    responseBody: '{\n  "success": true,\n  "message": "User registered successfully",\n  "data": {\n    "id": 5,\n    "username": "sarah",\n    "email": "sarah@example.com",\n    "role": "ROLE_CUSTOMER"\n  }\n}'
  },
  {
    method: 'POST',
    path: '/api/auth/login',
    summary: 'Authenticate credentials and issue stateless JWT Bearer token',
    authRequired: false,
    requestBody: '{\n  "username": "customer",\n  "password": "Customer@123"\n}',
    responseBody: '{\n  "success": true,\n  "data": {\n    "token": "eyJhbGciOiJIUzI1NiJ9...",\n    "type": "Bearer",\n    "username": "customer",\n    "role": "ROLE_CUSTOMER"\n  }\n}'
  },
  {
    method: 'GET',
    path: '/api/movies',
    summary: 'Retrieve all active movie titles with ratings, genres, and posters',
    authRequired: false,
    responseBody: '{\n  "success": true,\n  "data": [\n    {\n      "id": 1,\n      "title": "Interstellar: Beyond Time",\n      "genre": "Sci-Fi / Adventure",\n      "rating": 8.9,\n      "durationMinutes": 169\n    }\n  ]\n}'
  },
  {
    method: 'GET',
    path: '/api/movies/{id}',
    summary: 'Get comprehensive movie metadata and description by ID',
    authRequired: false
  },
  {
    method: 'POST',
    path: '/api/movies',
    summary: 'Add a new movie title to the catalog',
    authRequired: true,
    role: 'ROLE_ADMIN'
  },
  {
    method: 'DELETE',
    path: '/api/movies/{id}',
    summary: 'Soft-delete a movie from active listing',
    authRequired: true,
    role: 'ROLE_ADMIN'
  },
  {
    method: 'GET',
    path: '/api/theatres',
    summary: 'List cinema theatres with city, address, and amenities',
    authRequired: false
  },
  {
    method: 'GET',
    path: '/api/shows/movie/{movieId}',
    summary: 'Get scheduled cinema shows grouped by theatre and screen',
    authRequired: false
  },
  {
    method: 'POST',
    path: '/api/shows',
    summary: 'Schedule a new show for a movie and screen auditorium',
    authRequired: true,
    role: 'ROLE_ADMIN'
  },
  {
    method: 'GET',
    path: '/api/seats/show/{showId}',
    summary: 'Fetch interactive seat matrix with live status (AVAILABLE, BOOKED)',
    authRequired: false
  },
  {
    method: 'GET',
    path: '/api/seats/recommend?showId={showId}&bookedSeatId={seatId}',
    summary: 'Smart Vacant Seat Assistant: calculates nearest available seat using 2D Euclidean distance',
    authRequired: false,
    responseBody: '{\n  "success": true,\n  "data": {\n    "id": 20,\n    "seatIdentifier": "C4",\n    "rowName": "C",\n    "seatNumber": 4,\n    "seatType": "PREMIUM",\n    "price": 22.50,\n    "status": "AVAILABLE"\n  }\n}'
  },
  {
    method: 'POST',
    path: '/api/bookings',
    summary: 'Create booking with serializable isolation & unique constraints against double-booking',
    authRequired: true,
    role: 'ROLE_CUSTOMER',
    requestBody: '{\n  "showId": 1,\n  "seatIds": [14, 15],\n  "paymentMethod": "CARD"\n}',
    responseBody: '{\n  "success": true,\n  "data": {\n    "bookingId": 12,\n    "bookingNumber": "BK-1726419200-ABCD",\n    "movieTitle": "Interstellar: Beyond Time",\n    "theatreName": "Grand Horizon IMAX Cinema",\n    "seatNumbers": ["C4", "C5"],\n    "totalAmount": 45.00,\n    "bookingStatus": "CONFIRMED"\n  }\n}'
  },
  {
    method: 'GET',
    path: '/api/bookings/my-bookings',
    summary: 'Retrieve reservation history for authenticated user',
    authRequired: true
  },
  {
    method: 'GET',
    path: '/api/bookings/{bookingNumber}',
    summary: 'Retrieve digital cinema pass details by booking reference code',
    authRequired: false
  },
  {
    method: 'POST',
    path: '/api/bookings/{id}/cancel',
    summary: 'Cancel ticket reservation, release seats, and trigger automatic refund',
    authRequired: true
  },
  {
    method: 'GET',
    path: '/api/admin/dashboard-stats',
    summary: 'Get gross revenue, total reservations, booked seats, and user count',
    authRequired: true,
    role: 'ROLE_ADMIN'
  },
  {
    method: 'GET',
    path: '/api/admin/bookings',
    summary: 'Audit log of all cinema bookings across all users',
    authRequired: true,
    role: 'ROLE_ADMIN'
  },
  {
    method: 'PUT',
    path: '/api/admin/users/{id}/toggle-status',
    summary: 'Suspend or reinstate user login privileges',
    authRequired: true,
    role: 'ROLE_ADMIN'
  }
];
