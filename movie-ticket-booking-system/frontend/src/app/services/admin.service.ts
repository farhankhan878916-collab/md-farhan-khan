import { Injectable } from '@angular/core';
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
