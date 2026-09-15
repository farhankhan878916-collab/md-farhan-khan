import { Injectable } from '@angular/core';
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
