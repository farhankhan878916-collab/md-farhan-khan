import os

BASE_DIR = "movie-ticket-booking-system"
APP_DIR = os.path.join(BASE_DIR, "frontend", "src", "app")

def write_file(subpath, content):
    full_path = os.path.join(APP_DIR, subpath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {full_path}")

def generate_auth_admin():
    # 1. Login Component
    write_file("components/login/login.component.ts", """import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  isLoading = false;
  errorMessage = '';
  returnUrl = '/';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/']);
      return;
    }

    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';

    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) return;

    this.isLoading = true;
    this.errorMessage = '';

    this.authService.login(this.loginForm.value).subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res.success) {
          this.router.navigateByUrl(this.returnUrl);
        }
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.error?.message || 'Invalid username or password';
      }
    });
  }

  fillDemoCustomer(): void {
    this.loginForm.patchValue({
      username: 'customer',
      password: 'Customer@123'
    });
  }

  fillDemoAdmin(): void {
    this.loginForm.patchValue({
      username: 'admin',
      password: 'Admin@123'
    });
  }
}
""")

    write_file("components/login/login.component.html", """<div class="auth-page container">
  <div class="auth-card glass-card">
    <div class="auth-header">
      <div class="auth-icon"><i class="fa-solid fa-lock"></i></div>
      <h2>Welcome Back</h2>
      <p class="auth-sub">Sign in to your CinePass account to manage bookings and tickets</p>
    </div>

    <!-- Error Alert -->
    <div *ngIf="errorMessage" class="alert alert-danger">
      <i class="fa-solid fa-circle-exclamation"></i>
      <span>{{ errorMessage }}</span>
    </div>

    <!-- Quick Demo Credentials Box -->
    <div class="demo-credentials-box">
      <span class="demo-title"><i class="fa-solid fa-key"></i> Quick Demo Login:</span>
      <div class="demo-btns">
        <button type="button" (click)="fillDemoCustomer()" class="btn btn-secondary btn-xs">
          Customer (customer / Customer@123)
        </button>
        <button type="button" (click)="fillDemoAdmin()" class="btn btn-secondary btn-xs">
          Admin (admin / Admin@123)
        </button>
      </div>
    </div>

    <form [formGroup]="loginForm" (ngSubmit)="onSubmit()" class="auth-form">
      <div class="form-group">
        <label for="username">Username or Email</label>
        <div class="input-icon-wrap">
          <i class="fa-regular fa-user input-icon"></i>
          <input type="text" id="username" formControlName="username" class="form-control" placeholder="Enter username">
        </div>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <div class="input-icon-wrap">
          <i class="fa-solid fa-key input-icon"></i>
          <input type="password" id="password" formControlName="password" class="form-control" placeholder="Enter password">
        </div>
      </div>

      <button type="submit" [disabled]="loginForm.invalid || isLoading" class="btn btn-primary btn-submit">
        <span *ngIf="!isLoading">Sign In</span>
        <span *ngIf="isLoading"><i class="fa-solid fa-spinner fa-spin"></i> Authenticating...</span>
      </button>
    </form>

    <div class="auth-footer">
      <span>Don't have an account?</span>
      <a routerLink="/register" class="auth-link">Create an account</a>
    </div>
  </div>
</div>
""")

    write_file("components/login/login.component.css", """.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 150px);
  padding: 3rem 1.5rem;
}

.auth-card {
  width: 100%;
  max-width: 440px;
  padding: 2.5rem;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(229, 9, 20, 0.15);
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 1.25rem;
}

.auth-sub {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-top: 0.35rem;
}

.demo-credentials-box {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-color);
  padding: 0.85rem;
  border-radius: var(--radius-md);
  margin-bottom: 1.5rem;
}

.demo-title {
  display: block;
  font-size: 0.75rem;
  color: var(--accent-gold);
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.demo-btns {
  display: flex;
  gap: 0.5rem;
  flex-direction: column;
}

.btn-xs {
  font-size: 0.75rem;
  padding: 0.35rem 0.6rem;
  text-align: left;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-main);
}

.input-icon-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: var(--text-muted);
}

.input-icon-wrap input {
  padding-left: 2.75rem;
  width: 100%;
}

.btn-submit {
  width: 100%;
  padding: 0.85rem;
  font-size: 1rem;
  margin-top: 0.5rem;
}

.auth-footer {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.9rem;
  color: var(--text-muted);
  border-top: 1px solid var(--border-color);
  padding-top: 1.25rem;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.auth-link {
  color: var(--primary);
  font-weight: 600;
}
""")

    # 2. Register Component
    write_file("components/register/register.component.ts", """import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  isLoading = false;
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/']);
      return;
    }

    this.registerForm = this.fb.group({
      fullName: ['', [Validators.required, Validators.minLength(2)]],
      username: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      phone: [''],
      role: ['ROLE_CUSTOMER']
    });
  }

  onSubmit(): void {
    if (this.registerForm.invalid) return;

    this.isLoading = true;
    this.errorMessage = '';

    this.authService.register(this.registerForm.value).subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res.success) {
          this.router.navigate(['/']);
        }
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.error?.message || 'Registration failed. Please try again.';
      }
    });
  }
}
""")

    write_file("components/register/register.component.html", """<div class="auth-page container">
  <div class="auth-card glass-card">
    <div class="auth-header">
      <div class="auth-icon"><i class="fa-solid fa-user-plus"></i></div>
      <h2>Create CinePass Account</h2>
      <p class="auth-sub">Join CinePass for seamless seat selection, discounts, and real-time ticketing</p>
    </div>

    <!-- Error Alert -->
    <div *ngIf="errorMessage" class="alert alert-danger">
      <i class="fa-solid fa-circle-exclamation"></i>
      <span>{{ errorMessage }}</span>
    </div>

    <form [formGroup]="registerForm" (ngSubmit)="onSubmit()" class="auth-form">
      <div class="form-group">
        <label for="fullName">Full Name</label>
        <div class="input-icon-wrap">
          <i class="fa-regular fa-id-card input-icon"></i>
          <input type="text" id="fullName" formControlName="fullName" class="form-control" placeholder="e.g. Sarah Connor">
        </div>
      </div>

      <div class="form-group">
        <label for="username">Username</label>
        <div class="input-icon-wrap">
          <i class="fa-regular fa-user input-icon"></i>
          <input type="text" id="username" formControlName="username" class="form-control" placeholder="Choose a username">
        </div>
      </div>

      <div class="form-group">
        <label for="email">Email Address</label>
        <div class="input-icon-wrap">
          <i class="fa-regular fa-envelope input-icon"></i>
          <input type="email" id="email" formControlName="email" class="form-control" placeholder="name@example.com">
        </div>
      </div>

      <div class="form-group">
        <label for="phone">Phone (Optional)</label>
        <div class="input-icon-wrap">
          <i class="fa-solid fa-phone input-icon"></i>
          <input type="tel" id="phone" formControlName="phone" class="form-control" placeholder="+1-555-0199">
        </div>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <div class="input-icon-wrap">
          <i class="fa-solid fa-key input-icon"></i>
          <input type="password" id="password" formControlName="password" class="form-control" placeholder="Minimum 6 characters">
        </div>
      </div>

      <button type="submit" [disabled]="registerForm.invalid || isLoading" class="btn btn-primary btn-submit">
        <span *ngIf="!isLoading">Register Account</span>
        <span *ngIf="isLoading"><i class="fa-solid fa-spinner fa-spin"></i> Creating Profile...</span>
      </button>
    </form>

    <div class="auth-footer">
      <span>Already have an account?</span>
      <a routerLink="/login" class="auth-link">Sign In</a>
    </div>
  </div>
</div>
""")

    write_file("components/register/register.component.css", """.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 150px);
  padding: 3rem 1.5rem;
}

.auth-card {
  width: 100%;
  max-width: 480px;
  padding: 2.5rem;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(229, 9, 20, 0.15);
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 1.25rem;
}

.auth-sub {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-top: 0.35rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-main);
}

.input-icon-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: var(--text-muted);
}

.input-icon-wrap input {
  padding-left: 2.75rem;
  width: 100%;
}

.btn-submit {
  width: 100%;
  padding: 0.85rem;
  font-size: 1rem;
  margin-top: 0.5rem;
}

.auth-footer {
  margin-top: 1.75rem;
  text-align: center;
  font-size: 0.9rem;
  color: var(--text-muted);
  border-top: 1px solid var(--border-color);
  padding-top: 1.25rem;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.auth-link {
  color: var(--primary);
  font-weight: 600;
}
""")

    # 3. My Bookings Component
    write_file("components/my-bookings/my-bookings.component.ts", """import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { BookingService } from '../../services/booking.service';
import { BookingResponse } from '../../models/booking.model';

@Component({
  selector: 'app-my-bookings',
  templateUrl: './my-bookings.component.html',
  styleUrls: ['./my-bookings.component.css']
})
export class MyBookingsComponent implements OnInit {
  bookings: BookingResponse[] = [];
  isLoading = true;
  actionMessage = '';

  constructor(
    private bookingService: BookingService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadBookings();
  }

  loadBookings(): void {
    this.isLoading = true;
    this.bookingService.getMyBookings().subscribe({
      next: (res) => {
        if (res.success) {
          this.bookings = res.data;
        }
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  viewTicket(bookingNumber: string): void {
    this.router.navigate(['/booking/confirmation', bookingNumber]);
  }

  cancelBooking(booking: BookingResponse): void {
    if (!confirm(`Are you sure you want to cancel booking ${booking.bookingNumber}? Seats will be released and a refund will be processed.`)) {
      return;
    }

    this.bookingService.cancelBooking(booking.bookingId, 'Customer cancellation request').subscribe({
      next: (res) => {
        this.actionMessage = `Booking ${booking.bookingNumber} successfully cancelled. A refund of $${Number(booking.totalAmount).toFixed(2)} was initiated.`;
        this.loadBookings();
      },
      error: (err) => {
        alert(err.error?.message || 'Failed to cancel booking.');
      }
    });
  }
}
""")

    write_file("components/my-bookings/my-bookings.component.html", """<div class="my-bookings-page container">
  <div class="page-title-row">
    <div>
      <h1><i class="fa-solid fa-ticket"></i> My Bookings & Tickets</h1>
      <p class="sub-text">View your reservation history, digital e-passes, and cancellation status</p>
    </div>
  </div>

  <div *ngIf="actionMessage" class="alert alert-success">
    <i class="fa-solid fa-circle-check"></i>
    <span>{{ actionMessage }}</span>
  </div>

  <div *ngIf="isLoading" class="loading-state">
    <i class="fa-solid fa-spinner fa-spin"></i>
    <p>Retrieving your bookings...</p>
  </div>

  <div *ngIf="!isLoading && bookings.length === 0" class="empty-state glass-card">
    <i class="fa-solid fa-ticket empty-icon"></i>
    <h3>No Bookings Found</h3>
    <p>You haven't booked any movie tickets yet. Check out the latest blockbusters now showing!</p>
    <a routerLink="/" class="btn btn-primary">Browse Now Showing</a>
  </div>

  <div *ngIf="!isLoading && bookings.length > 0" class="bookings-list">
    <div *ngFor="let b of bookings" class="booking-item glass-card">
      <div class="item-movie-thumb">
        <img [src]="b.moviePosterUrl || 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=300&q=80'" [alt]="b.movieTitle">
      </div>

      <div class="item-info">
        <div class="item-header-row">
          <h3 class="movie-title">{{ b.movieTitle }}</h3>
          <span class="status-badge" [class.confirmed]="b.bookingStatus === 'CONFIRMED'" [class.cancelled]="b.bookingStatus === 'CANCELLED'">
            {{ b.bookingStatus }}
          </span>
        </div>

        <p class="cinema-name"><i class="fa-solid fa-location-dot"></i> {{ b.theatreName }} - {{ b.screenName }}</p>
        <p class="showtime"><i class="fa-regular fa-clock"></i> {{ b.showStartTime | date:'EEE, MMM d, y - hh:mm a' }}</p>

        <div class="item-meta-chips">
          <span class="seat-tag"><i class="fa-solid fa-chair"></i> Seats: {{ b.seatNumbers.join(', ') }}</span>
          <span class="ref-tag">Ref: {{ b.bookingNumber }}</span>
          <span class="paid-tag">${{ b.totalAmount | number:'1.2-2' }} ({{ b.paymentMethod }})</span>
        </div>
      </div>

      <div class="item-actions">
        <button (click)="viewTicket(b.bookingNumber)" class="btn btn-primary btn-sm">
          <i class="fa-solid fa-qrcode"></i> View Pass
        </button>
        <button *ngIf="b.bookingStatus === 'CONFIRMED'" (click)="cancelBooking(b)" class="btn btn-secondary btn-sm btn-cancel">
          <i class="fa-solid fa-ban"></i> Cancel Booking
        </button>
      </div>
    </div>
  </div>
</div>
""")

    write_file("components/my-bookings/my-bookings.component.css", """.my-bookings-page {
  padding: 3rem 1.5rem 5rem;
}

.page-title-row {
  margin-bottom: 2rem;
}

.sub-text {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.booking-item {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.item-movie-thumb {
  width: 90px;
  height: 125px;
  flex-shrink: 0;
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.item-movie-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-info {
  flex: 1;
  min-width: 260px;
}

.item-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.35rem;
}

.movie-title {
  font-size: 1.35rem;
}

.status-badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
  font-weight: 700;
  text-transform: uppercase;
}

.status-badge.confirmed {
  background: rgba(16, 185, 129, 0.2);
  color: var(--accent-green);
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.status-badge.cancelled {
  background: rgba(239, 68, 68, 0.2);
  color: var(--accent-red);
  border: 1px solid rgba(239, 68, 68, 0.4);
}

.cinema-name, .showtime {
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.item-meta-chips {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.75rem;
  flex-wrap: wrap;
  font-size: 0.8rem;
}

.seat-tag {
  color: var(--accent-gold);
  font-weight: 600;
}

.ref-tag {
  color: var(--text-muted);
  font-family: monospace;
}

.paid-tag {
  color: var(--accent-green);
  font-weight: 600;
}

.item-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.btn-cancel:hover {
  color: var(--accent-red);
  border-color: var(--accent-red);
}

@media (max-width: 768px) {
  .booking-item {
    flex-direction: column;
    align-items: flex-start;
  }
  .item-actions {
    width: 100%;
    flex-direction: row;
  }
}
""")

    # 4. Admin Dashboard Component
    write_file("components/admin-dashboard/admin-dashboard.component.ts", """import { Component, OnInit } from '@angular/core';
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
""")

    write_file("components/admin-dashboard/admin-dashboard.component.html", """<div class="admin-page container">
  <div class="admin-header">
    <div>
      <h1><i class="fa-solid fa-chart-line"></i> Operations Management Dashboard</h1>
      <p class="admin-sub">Monitor theatre analytics, schedule cinema shows, manage titles and bookings</p>
    </div>

    <div class="header-actions">
      <button (click)="showAddMovieModal = true" class="btn btn-primary">
        <i class="fa-solid fa-film"></i> Add Movie
      </button>
      <button (click)="showAddShowModal = true" class="btn btn-secondary">
        <i class="fa-solid fa-calendar-plus"></i> Add Show
      </button>
    </div>
  </div>

  <div *ngIf="actionMessage" class="alert alert-success">
    <i class="fa-solid fa-circle-check"></i>
    <span>{{ actionMessage }}</span>
  </div>

  <!-- KPI METRICS -->
  <div class="kpi-grid" *ngIf="stats">
    <div class="kpi-card glass-card">
      <div class="kpi-icon icon-revenue"><i class="fa-solid fa-sack-dollar"></i></div>
      <div class="kpi-body">
        <span class="kpi-lbl">Total Gross Revenue</span>
        <h2 class="kpi-val">${{ stats.totalRevenue | number:'1.2-2' }}</h2>
      </div>
    </div>

    <div class="kpi-card glass-card">
      <div class="kpi-icon icon-bookings"><i class="fa-solid fa-ticket"></i></div>
      <div class="kpi-body">
        <span class="kpi-lbl">Total Bookings</span>
        <h2 class="kpi-val">{{ stats.totalBookings }}</h2>
      </div>
    </div>

    <div class="kpi-card glass-card">
      <div class="kpi-icon icon-seats"><i class="fa-solid fa-chair"></i></div>
      <div class="kpi-body">
        <span class="kpi-lbl">Booked Seats</span>
        <h2 class="kpi-val">{{ stats.bookedSeats }}</h2>
      </div>
    </div>

    <div class="kpi-card glass-card">
      <div class="kpi-icon icon-users"><i class="fa-solid fa-users"></i></div>
      <div class="kpi-body">
        <span class="kpi-lbl">Registered Patrons</span>
        <h2 class="kpi-val">{{ stats.totalUsers }}</h2>
      </div>
    </div>
  </div>

  <!-- TABS NAV -->
  <div class="admin-tabs">
    <button (click)="activeTab = 'OVERVIEW'" [class.active]="activeTab === 'OVERVIEW'" class="tab-btn">
      <i class="fa-solid fa-chart-pie"></i> Overview
    </button>
    <button (click)="activeTab = 'MOVIES'" [class.active]="activeTab === 'MOVIES'" class="tab-btn">
      <i class="fa-solid fa-film"></i> Movies ({{ movies.length }})
    </button>
    <button (click)="activeTab = 'BOOKINGS'" [class.active]="activeTab === 'BOOKINGS'" class="tab-btn">
      <i class="fa-solid fa-ticket"></i> Bookings ({{ bookings.length }})
    </button>
    <button (click)="activeTab = 'USERS'" [class.active]="activeTab === 'USERS'" class="tab-btn">
      <i class="fa-solid fa-users"></i> Users ({{ users.length }})
    </button>
  </div>

  <!-- TAB 1: OVERVIEW -->
  <div *ngIf="activeTab === 'OVERVIEW'" class="tab-content">
    <div class="overview-grid">
      <div class="glass-card">
        <h3>Recent Transactions</h3>
        <table class="data-table">
          <thead>
            <tr>
              <th>Ref</th>
              <th>Customer</th>
              <th>Movie</th>
              <th>Seats</th>
              <th>Total</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let b of bookings.slice(0, 5)">
              <td><code>{{ b.bookingNumber }}</code></td>
              <td>{{ b.customerName }}</td>
              <td>{{ b.movieTitle }}</td>
              <td>{{ b.seatNumbers.join(', ') }}</td>
              <td class="text-green">${{ b.totalAmount | number:'1.2-2' }}</td>
              <td><span class="badge" [class.badge-regular]="b.bookingStatus === 'CONFIRMED'">{{ b.bookingStatus }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 2: MOVIES -->
  <div *ngIf="activeTab === 'MOVIES'" class="tab-content">
    <div class="glass-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Poster</th>
            <th>Title</th>
            <th>Genre</th>
            <th>Duration</th>
            <th>Rating</th>
            <th>Language</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let m of movies">
            <td><img [src]="m.posterUrl" class="tbl-thumb" alt="poster"></td>
            <td><strong>{{ m.title }}</strong></td>
            <td>{{ m.genre }}</td>
            <td>{{ m.durationMinutes }}m</td>
            <td><i class="fa-solid fa-star text-gold"></i> {{ m.rating }}</td>
            <td>{{ m.language }}</td>
            <td>
              <button (click)="deleteMovie(m.id, m.title)" class="btn-icon text-danger" title="Delete">
                <i class="fa-solid fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- TAB 3: BOOKINGS -->
  <div *ngIf="activeTab === 'BOOKINGS'" class="tab-content">
    <div class="glass-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Booking Ref</th>
            <th>User</th>
            <th>Movie</th>
            <th>Showtime</th>
            <th>Seats</th>
            <th>Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let b of bookings">
            <td><code>{{ b.bookingNumber }}</code></td>
            <td>{{ b.customerName }} ({{ b.customerEmail }})</td>
            <td>{{ b.movieTitle }}</td>
            <td>{{ b.showStartTime | date:'short' }}</td>
            <td>{{ b.seatNumbers.join(', ') }}</td>
            <td class="text-green">${{ b.totalAmount | number:'1.2-2' }}</td>
            <td><span class="badge" [class.badge-regular]="b.bookingStatus === 'CONFIRMED'">{{ b.bookingStatus }}</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- TAB 4: USERS -->
  <div *ngIf="activeTab === 'USERS'" class="tab-content">
    <div class="glass-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Username</th>
            <th>Full Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let u of users">
            <td>{{ u.username }}</td>
            <td>{{ u.fullName }}</td>
            <td>{{ u.email }}</td>
            <td><span class="badge" [class.badge-vip]="u.role === 'ROLE_ADMIN'" [class.badge-regular]="u.role !== 'ROLE_ADMIN'">{{ u.role }}</span></td>
            <td><span [class.text-green]="u.active" [class.text-danger]="!u.active">{{ u.active ? 'ACTIVE' : 'SUSPENDED' }}</span></td>
            <td>
              <button (click)="toggleUser(u)" class="btn btn-secondary btn-xs">
                {{ u.active ? 'Suspend' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- MODAL: ADD MOVIE -->
  <div *ngIf="showAddMovieModal" class="modal-overlay">
    <div class="modal-card glass-card">
      <div class="modal-header">
        <h3>Add New Movie Title</h3>
        <button (click)="showAddMovieModal = false" class="btn-close"><i class="fa-solid fa-xmark"></i></button>
      </div>

      <form [formGroup]="movieForm" (ngSubmit)="submitMovie()" class="modal-form">
        <div class="form-group">
          <label>Title</label>
          <input type="text" formControlName="title" class="form-control" placeholder="Movie title">
        </div>
        <div class="form-group">
          <label>Description</label>
          <textarea formControlName="description" class="form-control" rows="3"></textarea>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Genre</label>
            <input type="text" formControlName="genre" class="form-control">
          </div>
          <div class="form-group">
            <label>Duration (Mins)</label>
            <input type="number" formControlName="durationMinutes" class="form-control">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Language</label>
            <input type="text" formControlName="language" class="form-control">
          </div>
          <div class="form-group">
            <label>Release Date</label>
            <input type="date" formControlName="releaseDate" class="form-control">
          </div>
        </div>
        <div class="form-group">
          <label>Poster URL</label>
          <input type="text" formControlName="posterUrl" class="form-control">
        </div>

        <button type="submit" [disabled]="movieForm.invalid" class="btn btn-primary btn-submit">Save Movie</button>
      </form>
    </div>
  </div>

  <!-- MODAL: ADD SHOW -->
  <div *ngIf="showAddShowModal" class="modal-overlay">
    <div class="modal-card glass-card">
      <div class="modal-header">
        <h3>Schedule New Show</h3>
        <button (click)="showAddShowModal = false" class="btn-close"><i class="fa-solid fa-xmark"></i></button>
      </div>

      <form [formGroup]="showForm" (ngSubmit)="submitShow()" class="modal-form">
        <div class="form-group">
          <label>Movie</label>
          <select formControlName="movieId" class="form-control">
            <option value="">Select Movie</option>
            <option *ngFor="let m of movies" [value]="m.id">{{ m.title }}</option>
          </select>
        </div>

        <div class="form-group">
          <label>Theatre</label>
          <select formControlName="theatreId" (change)="onTheatreChange()" class="form-control">
            <option value="">Select Cinema Theatre</option>
            <option *ngFor="let t of theatres" [value]="t.id">{{ t.name }} ({{ t.city }})</option>
          </select>
        </div>

        <div class="form-group">
          <label>Screen Auditorium</label>
          <select formControlName="screenId" class="form-control">
            <option value="">Select Screen</option>
            <option *ngFor="let s of theatreScreens" [value]="s.id">{{ s.name }}</option>
          </select>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Showtime (Local Date & Time)</label>
            <input type="datetime-local" formControlName="startTime" class="form-control">
          </div>
          <div class="form-group">
            <label>Base Price ($)</label>
            <input type="number" formControlName="basePrice" class="form-control" step="0.5">
          </div>
        </div>

        <button type="submit" [disabled]="showForm.invalid" class="btn btn-primary btn-submit">Schedule Show</button>
      </form>
    </div>
  </div>
</div>
""")

    write_file("components/admin-dashboard/admin-dashboard.component.css", """.admin-page {
  padding: 3rem 1.5rem 6rem;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.admin-sub {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.kpi-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
}

.kpi-icon {
  width: 54px;
  height: 54px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
}

.icon-revenue { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }
.icon-bookings { background: rgba(6, 182, 212, 0.15); color: var(--accent-cyan); }
.icon-seats { background: rgba(245, 158, 11, 0.15); color: var(--accent-gold); }
.icon-users { background: rgba(139, 92, 246, 0.15); color: var(--accent-purple); }

.kpi-lbl {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.kpi-val {
  font-size: 1.85rem;
  line-height: 1.2;
}

.admin-tabs {
  display: flex;
  gap: 0.5rem;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 1.5rem;
  overflow-x: auto;
}

.tab-btn {
  background: transparent;
  color: var(--text-muted);
  padding: 0.75rem 1.25rem;
  border-bottom: 2px solid transparent;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
}

.tab-btn:hover, .tab-btn.active {
  color: #fff;
  border-bottom-color: var(--primary);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.data-table th {
  padding: 0.85rem 1rem;
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  border-bottom: 1px solid var(--border-color);
}

.data-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  font-size: 0.9rem;
}

.tbl-thumb {
  width: 45px;
  height: 65px;
  object-fit: cover;
  border-radius: 4px;
}

.text-danger { color: var(--accent-red); }

/* MODALS */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.modal-card {
  width: 100%;
  max-width: 550px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.btn-close {
  background: transparent;
  color: var(--text-muted);
  font-size: 1.25rem;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
""")

    # 5. App Component
    write_file("app.component.ts", """import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <app-navbar></app-navbar>
    <main class="main-content">
      <router-outlet></router-outlet>
    </main>
    <footer class="app-footer">
      <div class="container footer-content">
        <p>&copy; 2026 CinePass Movie Ticket Booking System. All rights reserved.</p>
        <div class="footer-links">
          <span>Production-grade Java & Angular Architecture</span>
          <span>Double-Booking Concurrency Safe</span>
        </div>
      </div>
    </footer>
  `,
  styles: [`
    .main-content {
      flex: 1;
    }
    .app-footer {
      background: var(--bg-card);
      border-top: 1px solid var(--border-color);
      padding: 2rem 0;
      color: var(--text-muted);
      font-size: 0.85rem;
      margin-top: auto;
    }
    .footer-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }
    .footer-links {
      display: flex;
      gap: 1.5rem;
    }
  `]
})
export class AppComponent {
  title = 'movie-ticket-booking-frontend';
}
""")

    # 6. App Routing Module
    write_file("app-routing.module.ts", """import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { MovieListComponent } from './components/movie-list/movie-list.component';
import { MovieDetailsComponent } from './components/movie-details/movie-details.component';
import { SeatSelectionComponent } from './components/seat-selection/seat-selection.component';
import { BookingSummaryComponent } from './components/booking-summary/booking-summary.component';
import { TicketConfirmationComponent } from './components/ticket-confirmation/ticket-confirmation.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { MyBookingsComponent } from './components/my-bookings/my-bookings.component';
import { AdminDashboardComponent } from './components/admin-dashboard/admin-dashboard.component';

import { AuthGuard } from './guards/auth.guard';
import { AdminGuard } from './guards/admin.guard';

const routes: Routes = [
  { path: '', component: MovieListComponent },
  { path: 'movies/:id', component: MovieDetailsComponent },
  { path: 'booking/seats/:showId', component: SeatSelectionComponent },
  { path: 'booking/summary', component: BookingSummaryComponent, canActivate: [AuthGuard] },
  { path: 'booking/confirmation/:bookingNumber', component: TicketConfirmationComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'my-bookings', component: MyBookingsComponent, canActivate: [AuthGuard] },
  { path: 'admin', component: AdminDashboardComponent, canActivate: [AdminGuard] },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { scrollPositionRestoration: 'enabled' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
""")

    # 7. App Module
    write_file("app.module.ts", """import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { MovieListComponent } from './components/movie-list/movie-list.component';
import { MovieDetailsComponent } from './components/movie-details/movie-details.component';
import { SeatSelectionComponent } from './components/seat-selection/seat-selection.component';
import { BookingSummaryComponent } from './components/booking-summary/booking-summary.component';
import { TicketConfirmationComponent } from './components/ticket-confirmation/ticket-confirmation.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { MyBookingsComponent } from './components/my-bookings/my-bookings.component';
import { AdminDashboardComponent } from './components/admin-dashboard/admin-dashboard.component';

import { JwtInterceptor } from './interceptors/jwt.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    MovieListComponent,
    MovieDetailsComponent,
    SeatSelectionComponent,
    BookingSummaryComponent,
    TicketConfirmationComponent,
    LoginComponent,
    RegisterComponent,
    MyBookingsComponent,
    AdminDashboardComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
""")

if __name__ == "__main__":
    generate_auth_admin()
