import { Injectable } from '@angular/core';
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
