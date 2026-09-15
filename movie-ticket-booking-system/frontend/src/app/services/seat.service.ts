import { Injectable } from '@angular/core';
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
