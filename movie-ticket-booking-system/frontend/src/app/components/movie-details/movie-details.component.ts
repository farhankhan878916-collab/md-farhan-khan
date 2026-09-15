import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { ShowService } from '../../services/show.service';
import { Movie } from '../../models/movie.model';
import { Show } from '../../models/show.model';

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  movieId!: number;
  movie?: Movie;
  shows: Show[] = [];
  groupedShows: { [theatreName: string]: Show[] } = {};
  isLoading = true;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private movieService: MovieService,
    private showService: ShowService
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.movieId = +params['id'];
      this.loadMovieDetails();
      this.loadShows();
    });
  }

  loadMovieDetails(): void {
    this.movieService.getMovieById(this.movieId).subscribe({
      next: (res) => {
        if (res.success) {
          this.movie = res.data;
        }
      },
      error: (err) => {
        this.error = 'Failed to load movie details.';
      }
    });
  }

  loadShows(): void {
    this.isLoading = true;
    this.showService.getShowsByMovie(this.movieId).subscribe({
      next: (res) => {
        if (res.success) {
          this.shows = res.data;
          this.groupShowsByTheatre();
        }
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  groupShowsByTheatre(): void {
    this.groupedShows = {};
    for (const show of this.shows) {
      const key = `${show.theatreName} (${show.theatreCity})`;
      if (!this.groupedShows[key]) {
        this.groupedShows[key] = [];
      }
      this.groupedShows[key].push(show);
    }
  }

  getTheatreKeys(): string[] {
    return Object.keys(this.groupedShows);
  }

  selectShow(showId: number): void {
    this.router.navigate(['/booking/seats', showId]);
  }
}
