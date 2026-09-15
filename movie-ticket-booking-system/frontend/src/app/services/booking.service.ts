import { Injectable } from '@angular/core';
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
