import { Component, OnInit } from '@angular/core';
import { MovieService } from '../../services/movie.service';
import { Movie } from '../../models/movie.model';

@Component({
  selector: 'app-movie-list',
  templateUrl: './movie-list.component.html',
  styleUrls: ['./movie-list.component.css']
})
export class MovieListComponent implements OnInit {
  movies: Movie[] = [];
  filteredMovies: Movie[] = [];
  selectedGenre = 'ALL';
  searchQuery = '';
  isLoading = true;

  genres = ['ALL', 'Action', 'Sci-Fi', 'Drama', 'Mystery'];

  constructor(private movieService: MovieService) {}

  ngOnInit(): void {
    this.loadMovies();
  }

  loadMovies(): void {
    this.isLoading = true;
    this.movieService.getAllMovies().subscribe({
      next: (res) => {
        if (res.success) {
          this.movies = res.data;
          this.filterMovies();
        }
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  selectGenre(genre: string): void {
    this.selectedGenre = genre;
    this.filterMovies();
  }

  onSearchChange(): void {
    this.filterMovies();
  }

  filterMovies(): void {
    this.filteredMovies = this.movies.filter(movie => {
      const matchesGenre = this.selectedGenre === 'ALL' || movie.genre.toLowerCase().includes(this.selectedGenre.toLowerCase());
      const matchesSearch = !this.searchQuery ||
        movie.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        movie.genre.toLowerCase().includes(this.searchQuery.toLowerCase());
      return matchesGenre && matchesSearch;
    });
  }
}
