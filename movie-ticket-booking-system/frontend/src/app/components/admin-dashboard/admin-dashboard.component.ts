import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AdminService, AdminDashboardStats } from '../../services/admin.service';
import { MovieService } from '../../services/movie.service';
import { TheatreService } from '../../services/theatre.service';
import { ShowService } from '../../services/show.service';
import { Movie } from '../../models/movie.model';
import { Theatre, Screen } from '../../models/theatre.model';
import { BookingResponse } from '../../models/booking.model';
import { User } from '../../models/user.model';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})
export class AdminDashboardComponent implements OnInit {
  activeTab: 'OVERVIEW' | 'MOVIES' | 'SHOWS' | 'BOOKINGS' | 'USERS' = 'OVERVIEW';

  stats?: AdminDashboardStats;
  movies: Movie[] = [];
  theatres: Theatre[] = [];
  theatreScreens: Screen[] = [];
  bookings: BookingResponse[] = [];
  users: User[] = [];

  isLoading = true;
  actionMessage = '';

  // Forms
  movieForm!: FormGroup;
  showForm!: FormGroup;
  showAddMovieModal = false;
  showAddShowModal = false;

  constructor(
    private adminService: AdminService,
    private movieService: MovieService,
    private theatreService: TheatreService,
    private showService: ShowService,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.initForms();
    this.loadAllData();
  }

  initForms(): void {
    this.movieForm = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      genre: ['Action', Validators.required],
      durationMinutes: [120, [Validators.required, Validators.min(30)]],
      language: ['English', Validators.required],
      releaseDate: ['2026-06-01', Validators.required],
      posterUrl: ['https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=600&q=80'],
      rating: [8.5, [Validators.required, Validators.min(1), Validators.max(10)]],
      active: [true]
    });

    this.showForm = this.fb.group({
      movieId: ['', Validators.required],
      theatreId: ['', Validators.required],
      screenId: ['', Validators.required],
      startTime: ['', Validators.required],
      basePrice: [15.00, [Validators.required, Validators.min(5)]]
    });
  }

  loadAllData(): void {
    this.isLoading = true;
    this.adminService.getDashboardStats().subscribe(res => {
      if (res.success) this.stats = res.data;
    });

    this.movieService.getAllMovies().subscribe(res => {
      if (res.success) this.movies = res.data;
    });

    this.theatreService.getAllTheatres().subscribe(res => {
      if (res.success) this.theatres = res.data;
    });

    this.adminService.getAllBookings().subscribe(res => {
      if (res.success) this.bookings = res.data;
    });

    this.adminService.getAllUsers().subscribe(res => {
      if (res.success) this.users = res.data;
      this.isLoading = false;
    });
  }

  onTheatreChange(): void {
    const theatreId = this.showForm.get('theatreId')?.value;
    if (theatreId) {
      this.theatreService.getScreensByTheatre(theatreId).subscribe(res => {
        if (res.success) {
          this.theatreScreens = res.data;
          if (this.theatreScreens.length > 0) {
            this.showForm.patchValue({ screenId: this.theatreScreens[0].id });
          }
        }
      });
    }
  }

  submitMovie(): void {
    if (this.movieForm.invalid) return;

    this.movieService.createMovie(this.movieForm.value).subscribe({
      next: (res) => {
        this.actionMessage = `Movie "${res.data.title}" successfully added!`;
        this.showAddMovieModal = false;
        this.movieForm.reset({ active: true, durationMinutes: 120, rating: 8.5 });
        this.loadAllData();
      },
      error: (err) => alert(err.error?.message || 'Failed to create movie')
    });
  }

  deleteMovie(id: number, title: string): void {
    if (!confirm(`Delete movie "${title}"?`)) return;

    this.movieService.deleteMovie(id).subscribe({
      next: () => {
        this.actionMessage = `Movie "${title}" removed.`;
        this.loadAllData();
      }
    });
  }

  submitShow(): void {
    if (this.showForm.invalid) return;

    this.showService.createShow(this.showForm.value).subscribe({
      next: (res) => {
        this.actionMessage = 'New show schedule created!';
        this.showAddShowModal = false;
        this.loadAllData();
      },
      error: (err) => alert(err.error?.message || 'Failed to create show')
    });
  }

  toggleUser(user: User): void {
    this.adminService.toggleUserStatus(user.id).subscribe({
      next: () => {
        user.active = !user.active;
        this.actionMessage = `User status updated for ${user.username}`;
      }
    });
  }
}
