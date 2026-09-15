import { Injectable } from '@angular/core';
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
