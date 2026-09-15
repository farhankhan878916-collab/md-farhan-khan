import os

BASE_DIR = "movie-ticket-booking-system"
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend", "src", "app", "services")

def write_file(subpath, content):
    full_path = os.path.join(FRONTEND_DIR, subpath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {full_path}")

def generate_services():
    # 1. auth.service.ts
    write_file("auth.service.ts", """import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthResponse, User } from '../models/user.model';
import { ApiResponse } from '../models/api-response.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  private currentUserSubject = new BehaviorSubject<AuthResponse | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
      try {
        this.currentUserSubject.next(JSON.parse(savedUser));
      } catch (e) {
        localStorage.removeItem('currentUser');
      }
    }
  }

  public get currentUserValue(): AuthResponse | null {
    return this.currentUserSubject.value;
  }

  login(credentials: { username: string; password: string }): Observable<ApiResponse<AuthResponse>> {
    return this.http.post<ApiResponse<AuthResponse>>(`${this.apiUrl}/login`, credentials).pipe(
      tap(res => {
        if (res.success && res.data) {
          localStorage.setItem('currentUser', JSON.stringify(res.data));
          localStorage.setItem('token', res.data.token);
          this.currentUserSubject.next(res.data);
        }
      })
    );
  }

  register(userData: any): Observable<ApiResponse<AuthResponse>> {
    return this.http.post<ApiResponse<AuthResponse>>(`${this.apiUrl}/register`, userData).pipe(
      tap(res => {
        if (res.success && res.data) {
          localStorage.setItem('currentUser', JSON.stringify(res.data));
          localStorage.setItem('token', res.data.token);
          this.currentUserSubject.next(res.data);
        }
      })
    );
  }

  logout(): void {
    localStorage.removeItem('currentUser');
    localStorage.removeItem('token');
    this.currentUserSubject.next(null);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  isAdmin(): boolean {
    const user = this.currentUserValue;
    return !!user && user.role === 'ROLE_ADMIN';
  }
}
""")

    # 2. movie.service.ts
    write_file("movie.service.ts", """import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Movie } from '../models/movie.model';
import { ApiResponse } from '../models/api-response.model';

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  private apiUrl = `${environment.apiUrl}/movies`;

  constructor(private http: HttpClient) {}

  getAllMovies(): Observable<ApiResponse<Movie[]>> {
    return this.http.get<ApiResponse<Movie[]>>(this.apiUrl);
  }

  getMovieById(id: number): Observable<ApiResponse<Movie>> {
    return this.http.get<ApiResponse<Movie>>(`${this.apiUrl}/${id}`);
  }

  getMoviesByGenre(genre: string): Observable<ApiResponse<Movie[]>> {
    return this.http.get<ApiResponse<Movie[]>>(`${this.apiUrl}/genre/${genre}`);
  }

  createMovie(movie: Partial<Movie>): Observable<ApiResponse<Movie>> {
    return this.http.post<ApiResponse<Movie>>(this.apiUrl, movie);
  }

  updateMovie(id: number, movie: Partial<Movie>): Observable<ApiResponse<Movie>> {
    return this.http.put<ApiResponse<Movie>>(`${this.apiUrl}/${id}`, movie);
  }

  deleteMovie(id: number): Observable<ApiResponse<void>> {
    return this.http.delete<ApiResponse<void>>(`${this.apiUrl}/${id}`);
  }
}
""")

    # 3. theatre.service.ts
    write_file("theatre.service.ts", """import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Theatre, Screen } from '../models/theatre.model';
import { ApiResponse } from '../models/api-response.model';

@Injectable({
  providedIn: 'root'
})
export class TheatreService {
  private apiUrl = `${environment.apiUrl}/theatres`;

  constructor(private http: HttpClient) {}

  getAllTheatres(): Observable<ApiResponse<Theatre[]>> {
    return this.http.get<ApiResponse<Theatre[]>>(this.apiUrl);
  }

  getTheatreById(id: number): Observable<ApiResponse<Theatre>> {
    return this.http.get<ApiResponse<Theatre>>(`${this.apiUrl}/${id}`);
  }

  createTheatre(theatre: Partial<Theatre>): Observable<ApiResponse<Theatre>> {
    return this.http.post<ApiResponse<Theatre>>(this.apiUrl, theatre);
  }

  updateTheatre(id: number, theatre: Partial<Theatre>): Observable<ApiResponse<Theatre>> {
    return this.http.put<ApiResponse<Theatre>>(`${this.apiUrl}/${id}`, theatre);
  }

  deleteTheatre(id: number): Observable<ApiResponse<void>> {
    return this.http.delete<ApiResponse<void>>(`${this.apiUrl}/${id}`);
  }

  getScreensByTheatre(theatreId: number): Observable<ApiResponse<Screen[]>> {
    return this.http.get<ApiResponse<Screen[]>>(`${environment.apiUrl}/screens/theatre/${theatreId}`);
  }
}
""")

    # 4. show.service.ts
    write_file("show.service.ts", """import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Show } from '../models/show.model';
import { ApiResponse } from '../models/api-response.model';

@Injectable({
  providedIn: 'root'
})
export class ShowService {
  private apiUrl = `${environment.apiUrl}/shows`;

  constructor(private http: HttpClient) {}

  getAllShows(): Observable<ApiResponse<Show[]>> {
    return this.http.get<ApiResponse<Show[]>>(this.apiUrl);
  }

  getShowById(id: number): Observable<ApiResponse<Show>> {
    return this.http.get<ApiResponse<Show>>(`${this.apiUrl}/${id}`);
  }

  getShowsByMovie(movieId: number): Observable<ApiResponse<Show[]>> {
    return this.http.get<ApiResponse<Show[]>>(`${this.apiUrl}/movie/${movieId}`);
  }

  getShowsByMovieAndTheatre(movieId: number, theatreId: number): Observable<ApiResponse<Show[]>> {
    return this.http.get<ApiResponse<Show[]>>(`${this.apiUrl}/movie/${movieId}/theatre/${theatreId}`);
  }

  createShow(show: any): Observable<ApiResponse<Show>> {
    return this.http.post<ApiResponse<Show>>(this.apiUrl, show);
  }

  cancelShow(id: number): Observable<ApiResponse<void>> {
    return this.http.delete<ApiResponse<void>>(`${this.apiUrl}/${id}`);
  }
}
""")

    # 5. seat.service.ts
    write_file("seat.service.ts", """import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Seat } from '../models/seat.model';
import { ApiResponse } from '../models/api-response.model';

@Injectable({
  providedIn: 'root'
})
export class SeatService {
  private apiUrl = `${environment.apiUrl}/shows`;

  constructor(private http: HttpClient) {}

  getSeatsForShow(showId: number): Observable<ApiResponse<Seat[]>> {
    return this.http.get<ApiResponse<Seat[]>>(`${this.apiUrl}/${showId}/seats`);
  }

  getRecommendedSeat(showId: number, targetSeatId: number): Observable<ApiResponse<Seat>> {
    return this.http.get<ApiResponse<Seat>>(`${this.apiUrl}/${showId}/seats/recommend?targetSeatId=${targetSeatId}`);
  }
}
""")

    # 6. booking.service.ts
    write_file("booking.service.ts", """import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { BookingRequest, BookingResponse } from '../models/booking.model';
import { ApiResponse } from '../models/api-response.model';

@Injectable({
  providedIn: 'root'
})
export class BookingService {
  private apiUrl = `${environment.apiUrl}/bookings`;

  constructor(private http: HttpClient) {}

  createBooking(request: BookingRequest): Observable<ApiResponse<BookingResponse>> {
    return this.http.post<ApiResponse<BookingResponse>>(this.apiUrl, request);
  }

  getMyBookings(): Observable<ApiResponse<BookingResponse[]>> {
    return this.http.get<ApiResponse<BookingResponse[]>>(`${this.apiUrl}/my`);
  }

  getBookingById(id: number): Observable<ApiResponse<BookingResponse>> {
    return this.http.get<ApiResponse<BookingResponse>>(`${this.apiUrl}/${id}`);
  }

  getBookingByNumber(bookingNumber: string): Observable<ApiResponse<BookingResponse>> {
    return this.http.get<ApiResponse<BookingResponse>>(`${this.apiUrl}/number/${bookingNumber}`);
  }

  cancelBooking(id: number, reason?: string): Observable<ApiResponse<BookingResponse>> {
    const params = reason ? `?reason=${encodeURIComponent(reason)}` : '';
    return this.http.delete<ApiResponse<BookingResponse>>(`${this.apiUrl}/${id}${params}`);
  }
}
""")

    # 7. admin.service.ts
    write_file("admin.service.ts", """import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { User } from '../models/user.model';
import { BookingResponse } from '../models/booking.model';
import { ApiResponse } from '../models/api-response.model';

export interface AdminDashboardStats {
  totalUsers: number;
  totalMovies: number;
  totalTheatres: number;
  totalShows: number;
  totalBookings: number;
  totalRevenue: number;
  availableSeats: number;
  bookedSeats: number;
}

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = `${environment.apiUrl}/admin`;

  constructor(private http: HttpClient) {}

  getDashboardStats(): Observable<ApiResponse<AdminDashboardStats>> {
    return this.http.get<ApiResponse<AdminDashboardStats>>(`${this.apiUrl}/dashboard`);
  }

  getAllUsers(): Observable<ApiResponse<User[]>> {
    return this.http.get<ApiResponse<User[]>>(`${this.apiUrl}/users`);
  }

  toggleUserStatus(id: number): Observable<ApiResponse<void>> {
    return this.http.put<ApiResponse<void>>(`${this.apiUrl}/users/${id}/toggle-status`, {});
  }

  getAllBookings(): Observable<ApiResponse<BookingResponse[]>> {
    return this.http.get<ApiResponse<BookingResponse[]>>(`${this.apiUrl}/bookings`);
  }
}
""")

if __name__ == "__main__":
    generate_services()
