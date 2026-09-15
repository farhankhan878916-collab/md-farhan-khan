import os

BASE_DIR = "movie-ticket-booking-system"
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend", "src", "app", "components")

def write_file(subpath, content):
    full_path = os.path.join(FRONTEND_DIR, subpath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {full_path}")

def generate_booking_components():
    # 1. Movie Details Component
    write_file("movie-details/movie-details.component.ts", """import { Component, OnInit } from '@angular/core';
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
""")

    write_file("movie-details/movie-details.component.html", """<div class="movie-details-page" *ngIf="movie">
  <!-- Movie Banner Header -->
  <div class="movie-backdrop" [style.background-image]="'linear-gradient(to bottom, rgba(15,16,22,0.6), rgba(15,16,22,1)), url(' + (movie.posterUrl || 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=1200&q=80') + ')'">
    <div class="container backdrop-content">
      <div class="poster-box glass-card">
        <img [src]="movie.posterUrl || 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=600&q=80'" [alt]="movie.title">
      </div>

      <div class="movie-info">
        <div class="badge-row">
          <span class="badge badge-regular">{{ movie.genre }}</span>
          <span class="badge badge-vip"><i class="fa-solid fa-star"></i> {{ movie.rating | number:'1.1-1' }} IMDb</span>
          <span class="badge badge-premium">{{ movie.language }}</span>
        </div>

        <h1 class="movie-title">{{ movie.title }}</h1>

        <div class="meta-chips">
          <span><i class="fa-regular fa-clock"></i> {{ movie.durationMinutes }} Minutes</span>
          <span><i class="fa-regular fa-calendar"></i> {{ movie.releaseDate | date:'mediumDate' }}</span>
          <span><i class="fa-solid fa-film"></i> 2D, 3D, IMAX</span>
        </div>

        <p class="movie-synopsis">{{ movie.description }}</p>
      </div>
    </div>
  </div>

  <!-- Shows & Theatres Section -->
  <section class="container shows-section">
    <div class="section-title-wrap">
      <h2><i class="fa-solid fa-calendar-check"></i> Select Theatre & Showtime</h2>
      <p class="section-sub">Choose your preferred cinema and timing to begin seat selection</p>
    </div>

    <div *ngIf="isLoading" class="loading-state">
      <i class="fa-solid fa-spinner fa-spin"></i>
      <p>Loading available showtimes...</p>
    </div>

    <div *ngIf="!isLoading && getTheatreKeys().length === 0" class="empty-shows glass-card">
      <i class="fa-regular fa-calendar-xmark empty-icon"></i>
      <h3>No Scheduled Shows Available</h3>
      <p>There are currently no upcoming shows scheduled for this movie. Please check back later or select another title.</p>
      <a routerLink="/" class="btn btn-secondary">Browse Other Movies</a>
    </div>

    <div *ngIf="!isLoading && getTheatreKeys().length > 0" class="theatres-list">
      <div *ngFor="let theatreKey of getTheatreKeys()" class="theatre-card glass-card">
        <div class="theatre-header">
          <div class="theatre-title-area">
            <h3><i class="fa-solid fa-building-columns"></i> {{ theatreKey }}</h3>
            <span class="theatre-screens-badge">{{ groupedShows[theatreKey][0].screenName }}</span>
          </div>
          <div class="amenity-tags">
            <span><i class="fa-solid fa-circle-check text-green"></i> M-Ticket</span>
            <span><i class="fa-solid fa-utensils text-gold"></i> Food Court</span>
            <span><i class="fa-solid fa-square-parking text-cyan"></i> Parking</span>
          </div>
        </div>

        <div class="showtimes-grid">
          <button *ngFor="let show of groupedShows[theatreKey]"
                  (click)="selectShow(show.id)"
                  class="showtime-btn">
            <span class="show-time">{{ show.startTime | date:'hh:mm a' }}</span>
            <span class="show-screen">{{ show.screenName }}</span>
            <span class="show-price">from ${{ show.basePrice | number:'1.2-2' }}</span>
          </button>
        </div>
      </div>
    </div>
  </section>
</div>
""")

    write_file("movie-details/movie-details.component.css", """.movie-details-page {
  padding-bottom: 4rem;
}

.movie-backdrop {
  background-size: cover;
  background-position: center;
  padding: 4rem 0 3rem;
  border-bottom: 1px solid var(--border-color);
}

.backdrop-content {
  display: flex;
  gap: 3rem;
  align-items: flex-start;
}

.poster-box {
  flex-shrink: 0;
  width: 280px;
  height: 400px;
  padding: 0.5rem;
  overflow: hidden;
}

.poster-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--radius-md);
}

.movie-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-top: 1rem;
}

.badge-row {
  display: flex;
  gap: 0.6rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.movie-title {
  font-size: 2.8rem;
  line-height: 1.15;
  margin-bottom: 1rem;
}

.meta-chips {
  display: flex;
  gap: 1.5rem;
  color: var(--text-muted);
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.meta-chips span {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.movie-synopsis {
  color: var(--text-main);
  font-size: 1.05rem;
  line-height: 1.7;
  max-width: 800px;
}

.shows-section {
  margin-top: 3rem;
}

.section-title-wrap {
  margin-bottom: 2rem;
}

.section-title-wrap h2 {
  font-size: 1.75rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.4rem;
}

.section-sub {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.theatres-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.theatre-card {
  padding: 1.5rem;
}

.theatre-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.theatre-title-area h3 {
  font-size: 1.25rem;
  margin-bottom: 0.35rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.theatre-screens-badge {
  font-size: 0.8rem;
  color: var(--accent-cyan);
  font-weight: 600;
}

.amenity-tags {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.amenity-tags span {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.text-green { color: var(--accent-green); }
.text-gold { color: var(--accent-gold); }
.text-cyan { color: var(--accent-cyan); }

.showtimes-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.showtime-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 0.75rem 1.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.2s ease;
}

.showtime-btn:hover {
  background: var(--bg-card-hover);
  border-color: var(--primary);
  transform: translateY(-2px);
}

.show-time {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
}

.show-screen {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.show-price {
  font-size: 0.8rem;
  color: var(--accent-green);
  font-weight: 600;
}

.loading-state, .empty-shows {
  text-align: center;
  padding: 3.5rem 1rem;
}

.empty-icon {
  font-size: 3rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .backdrop-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .poster-box {
    width: 220px;
    height: 310px;
  }
  .movie-title {
    font-size: 2rem;
  }
}
""")

    # 2. Seat Selection Component (INTERACTIVE MATRIX + VACANT RECOMMENDATION + DOUBLE-BOOKING PROTECTION)
    write_file("seat-selection/seat-selection.component.ts", """import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ShowService } from '../../services/show.service';
import { SeatService } from '../../services/seat.service';
import { BookingService } from '../../services/booking.service';
import { AuthService } from '../../services/auth.service';
import { Show } from '../../models/show.model';
import { Seat } from '../../models/seat.model';

@Component({
  selector: 'app-seat-selection',
  templateUrl: './seat-selection.component.html',
  styleUrls: ['./seat-selection.component.css']
})
export class SeatSelectionComponent implements OnInit {
  showId!: number;
  show?: Show;
  seats: Seat[] = [];
  groupedSeats: { [row: string]: Seat[] } = {};
  rowKeys: string[] = [];

  selectedSeats: Seat[] = [];
  totalPrice = 0;
  isLoading = true;

  // Real vacant seat recommendation state
  recommendedSeat: Seat | null = null;
  recommendationMessage = '';
  showRecommendationAlert = false;

  // Double booking error state
  doubleBookingError = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private showService: ShowService,
    private seatService: SeatService,
    private bookingService: BookingService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.showId = +params['showId'];
      this.loadShowAndSeats();
    });
  }

  loadShowAndSeats(): void {
    this.isLoading = true;
    this.showService.getShowById(this.showId).subscribe({
      next: (res) => {
        if (res.success) {
          this.show = res.data;
          this.loadSeats();
        }
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  loadSeats(): void {
    this.seatService.getSeatsForShow(this.showId).subscribe({
      next: (res) => {
        if (res.success) {
          this.seats = res.data;
          this.groupSeatsByRow();
        }
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  groupSeatsByRow(): void {
    this.groupedSeats = {};
    for (const seat of this.seats) {
      if (!this.groupedSeats[seat.rowName]) {
        this.groupedSeats[seat.rowName] = [];
      }
      this.groupedSeats[seat.rowName].push(seat);
    }
    // Sort rows alphabetically (A, B, C...)
    this.rowKeys = Object.keys(this.groupedSeats).sort();
    // Sort seats in each row by seatNumber
    for (const row of this.rowKeys) {
      this.groupedSeats[row].sort((a, b) => a.seatNumber - b.seatNumber);
    }
  }

  onSeatClick(seat: Seat): void {
    this.doubleBookingError = '';

    // If seat is BOOKED -> trigger real vacant seat recommendation algorithm
    if (seat.status === 'BOOKED') {
      this.triggerRecommendation(seat);
      return;
    }

    // Toggle selected
    const index = this.selectedSeats.findIndex(s => s.id === seat.id);
    if (index > -1) {
      this.selectedSeats.splice(index, 1);
      seat.status = 'AVAILABLE';
    } else {
      if (this.selectedSeats.length >= 8) {
        alert('You can select a maximum of 8 seats per booking.');
        return;
      }
      this.selectedSeats.push(seat);
      seat.status = 'SELECTED';
    }

    this.calculateTotalPrice();
  }

  triggerRecommendation(bookedSeat: Seat): void {
    this.seatService.getRecommendedSeat(this.showId, bookedSeat.id).subscribe({
      next: (res) => {
        if (res.success && res.data) {
          this.recommendedSeat = res.data;
          this.recommendationMessage = `Seat ${bookedSeat.seatIdentifier} is already booked. Nearest available seat is ${res.data.seatIdentifier}.`;
          this.showRecommendationAlert = true;
        } else {
          this.recommendationMessage = `Seat ${bookedSeat.seatIdentifier} is already booked. No vacant seats nearby.`;
          this.showRecommendationAlert = true;
        }
      },
      error: () => {
        this.recommendationMessage = `Seat ${bookedSeat.seatIdentifier} is already booked.`;
        this.showRecommendationAlert = true;
      }
    });
  }

  acceptRecommendedSeat(): void {
    if (!this.recommendedSeat) return;

    // Find the seat in our local layout
    const target = this.seats.find(s => s.id === this.recommendedSeat!.id);
    if (target && target.status === 'AVAILABLE') {
      this.selectedSeats.push(target);
      target.status = 'SELECTED';
      this.calculateTotalPrice();
    }

    this.showRecommendationAlert = false;
    this.recommendedSeat = null;
  }

  dismissRecommendation(): void {
    this.showRecommendationAlert = false;
    this.recommendedSeat = null;
  }

  calculateTotalPrice(): void {
    this.totalPrice = this.selectedSeats.reduce((sum, s) => sum + Number(s.price), 0);
  }

  getSelectedSeatIdentifiers(): string {
    return this.selectedSeats.map(s => s.seatIdentifier).join(', ');
  }

  proceedToSummary(): void {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login'], { queryParams: { returnUrl: `/booking/seats/${this.showId}` } });
      return;
    }

    if (this.selectedSeats.length === 0) {
      alert('Please select at least one seat to proceed.');
      return;
    }

    // Pass booking parameters via state
    sessionStorage.setItem('pendingBooking', JSON.stringify({
      show: this.show,
      seats: this.selectedSeats,
      totalPrice: this.totalPrice
    }));

    this.router.navigate(['/booking/summary']);
  }
}
""")

    write_file("seat-selection/seat-selection.component.html", """<div class="seat-page container" *ngIf="show">
  <!-- Top Bar Navigation & Movie Details -->
  <div class="booking-top-bar glass-card">
    <div class="movie-brief">
      <h2>{{ show.movieTitle }}</h2>
      <div class="brief-meta">
        <span><i class="fa-solid fa-location-dot"></i> {{ show.theatreName }} ({{ show.screenName }})</span>
        <span><i class="fa-regular fa-clock"></i> {{ show.startTime | date:'EEE, MMM d, hh:mm a' }}</span>
      </div>
    </div>

    <div class="seat-type-legend">
      <div class="legend-item"><span class="legend-box available-box"></span> Available</div>
      <div class="legend-item"><span class="legend-box selected-box"></span> Selected</div>
      <div class="legend-item"><span class="legend-box booked-box"></span> Booked</div>
    </div>
  </div>

  <!-- VACANT SEAT RECOMMENDATION BANNER -->
  <div *ngIf="showRecommendationAlert" class="alert alert-warning recommendation-banner">
    <div class="recommendation-info">
      <i class="fa-solid fa-wand-magic-sparkles magic-icon"></i>
      <div>
        <strong>Smart Seat Assistant:</strong> {{ recommendationMessage }}
      </div>
    </div>
    <div class="recommendation-actions">
      <button *ngIf="recommendedSeat" (click)="acceptRecommendedSeat()" class="btn btn-primary btn-sm">
        <i class="fa-solid fa-check"></i> Select {{ recommendedSeat.seatIdentifier }}
      </button>
      <button (click)="dismissRecommendation()" class="btn btn-secondary btn-sm">
        <i class="fa-solid fa-xmark"></i> Dismiss
      </button>
    </div>
  </div>

  <!-- DOUBLE BOOKING ERROR ALERT -->
  <div *ngIf="doubleBookingError" class="alert alert-danger">
    <i class="fa-solid fa-triangle-exclamation"></i>
    <span>{{ doubleBookingError }}</span>
  </div>

  <!-- CINEMA SEATING STAGE -->
  <div class="cinema-stage glass-card">
    <!-- Curved Screen Indicator -->
    <div class="screen-container">
      <div class="curved-screen"></div>
      <p class="screen-text"><i class="fa-solid fa-eye"></i> SCREEN THIS WAY (ALL EYES FORWARD)</p>
    </div>

    <!-- Loading Spinner -->
    <div *ngIf="isLoading" class="loading-state">
      <i class="fa-solid fa-spinner fa-spin"></i>
      <p>Configuring seat layout...</p>
    </div>

    <!-- Seat Matrix Grid -->
    <div *ngIf="!isLoading" class="seat-matrix">
      <div *ngFor="let row of rowKeys" class="seat-row">
        <div class="row-label">{{ row }}</div>

        <div class="seats-lane">
          <button *ngFor="let seat of groupedSeats[row]"
                  (click)="onSeatClick(seat)"
                  class="seat-btn"
                  [ngClass]="[
                    seat.status.toLowerCase(),
                    'seat-' + seat.seatType.toLowerCase()
                  ]"
                  [title]="seat.seatIdentifier + ' (' + seat.seatType + ') - $' + seat.price"
                  [disabled]="false">
            <span class="seat-num">{{ seat.seatNumber }}</span>
            <i *ngIf="seat.status === 'BOOKED'" class="fa-solid fa-xmark booked-icon"></i>
          </button>
        </div>

        <div class="row-label">{{ row }}</div>
      </div>
    </div>

    <!-- Seat Category Pricing Legend -->
    <div class="category-pricing">
      <div class="cat-pill"><span class="cat-dot regular-dot"></span> Regular: ${{ (show.basePrice * 1.0) | number:'1.2-2' }}</div>
      <div class="cat-pill"><span class="cat-dot premium-dot"></span> Premium: ${{ (show.basePrice * 1.5) | number:'1.2-2' }}</div>
      <div class="cat-pill"><span class="cat-dot vip-dot"></span> VIP: ${{ (show.basePrice * 2.0) | number:'1.2-2' }}</div>
    </div>
  </div>

  <!-- STICKY BOTTOM CHECKOUT TRAY -->
  <div class="bottom-checkout-tray glass-card">
    <div class="tray-content container">
      <div class="tray-selection">
        <span class="tray-label">Selected Seats ({{ selectedSeats.length }}):</span>
        <span class="tray-seats">{{ selectedSeats.length > 0 ? getSelectedSeatIdentifiers() : 'None selected' }}</span>
      </div>

      <div class="tray-pricing">
        <span class="tray-label">Total Amount:</span>
        <span class="tray-price">${{ totalPrice | number:'1.2-2' }}</span>
      </div>

      <button (click)="proceedToSummary()"
              [disabled]="selectedSeats.length === 0"
              class="btn btn-primary btn-checkout">
        Proceed to Payment <i class="fa-solid fa-arrow-right"></i>
      </button>
    </div>
  </div>
</div>
""")

    write_file("seat-selection/seat-selection.component.css", """.seat-page {
  padding: 2rem 1.5rem 6rem;
}

.booking-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 2rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.movie-brief h2 {
  font-size: 1.5rem;
  margin-bottom: 0.35rem;
}

.brief-meta {
  display: flex;
  gap: 1.25rem;
  color: var(--text-muted);
  font-size: 0.85rem;
}

.brief-meta span {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.seat-type-legend {
  display: flex;
  gap: 1.25rem;
  font-size: 0.85rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-box {
  width: 18px;
  height: 18px;
  border-radius: 4px;
}

.available-box {
  background: var(--bg-card-hover);
  border: 1px solid var(--border-color);
}

.selected-box {
  background: var(--primary);
  box-shadow: 0 0 8px var(--primary);
}

.booked-box {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* RECOMMENDATION BANNER */
.recommendation-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  animation: pulseGlow 2s infinite alternate;
}

@keyframes pulseGlow {
  from { box-shadow: 0 0 10px rgba(245, 158, 11, 0.2); }
  to { box-shadow: 0 0 20px rgba(245, 158, 11, 0.5); }
}

.recommendation-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.magic-icon {
  font-size: 1.4rem;
  color: var(--accent-gold);
}

.recommendation-actions {
  display: flex;
  gap: 0.5rem;
}

/* CINEMA STAGE */
.cinema-stage {
  padding: 3rem 2rem;
  text-align: center;
  margin-bottom: 2rem;
}

.screen-container {
  margin-bottom: 3.5rem;
  perspective: 500px;
}

.curved-screen {
  height: 12px;
  width: 75%;
  max-width: 600px;
  margin: 0 auto 1rem;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.1) 100%);
  border-radius: 50% / 100% 100% 0 0;
  box-shadow: 0 15px 35px rgba(255, 255, 255, 0.4);
}

.screen-text {
  color: var(--text-muted);
  font-size: 0.8rem;
  letter-spacing: 0.15em;
  font-weight: 600;
}

.seat-matrix {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 640px;
  margin: 0 auto;
}

.seat-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.row-label {
  width: 24px;
  font-weight: 700;
  color: var(--text-muted);
  font-size: 0.85rem;
}

.seats-lane {
  display: flex;
  gap: 0.5rem;
}

.seat-btn {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  background: var(--bg-card-hover);
  border: 1px solid var(--border-color);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.15s ease-in-out;
}

.seat-btn:hover:not(.booked) {
  transform: scale(1.15);
  border-color: #fff;
  z-index: 10;
}

/* SEAT TYPES */
.seat-vip {
  border-bottom: 3px solid var(--accent-gold);
}

.seat-premium {
  border-bottom: 3px solid var(--accent-purple);
}

.seat-regular {
  border-bottom: 3px solid var(--accent-cyan);
}

/* SEAT STATUS */
.seat-btn.selected {
  background: var(--primary) !important;
  border-color: #fff !important;
  color: #fff;
  box-shadow: 0 0 12px var(--primary);
  transform: scale(1.1);
}

.seat-btn.booked {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: rgba(255, 255, 255, 0.05) !important;
  color: rgba(255, 255, 255, 0.2);
  cursor: pointer; /* Allows clicking to trigger nearest recommendation! */
}

.booked-icon {
  font-size: 0.65rem;
  color: rgba(255, 255, 255, 0.3);
}

.category-pricing {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 3rem;
  flex-wrap: wrap;
}

.cat-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.cat-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.regular-dot { background: var(--accent-cyan); }
.premium-dot { background: var(--accent-purple); }
.vip-dot { background: var(--accent-gold); }

/* BOTTOM TRAY */
.bottom-checkout-tray {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  border-radius: 0;
  border-left: none;
  border-right: none;
  border-bottom: none;
  z-index: 90;
  padding: 1rem 0;
}

.tray-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.tray-selection, .tray-pricing {
  display: flex;
  flex-direction: column;
}

.tray-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.tray-seats {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
}

.tray-price {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--accent-green);
}

.btn-checkout {
  padding: 0.85rem 2rem;
  font-size: 1rem;
}

@media (max-width: 600px) {
  .seat-btn {
    width: 28px;
    height: 28px;
    font-size: 0.65rem;
  }
}
""")

    # 3. Booking Summary Component
    write_file("booking-summary/booking-summary.component.ts", """import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { BookingService } from '../../services/booking.service';
import { Show } from '../../models/show.model';
import { Seat } from '../../models/seat.model';

@Component({
  selector: 'app-booking-summary',
  templateUrl: './booking-summary.component.html',
  styleUrls: ['./booking-summary.component.css']
})
export class BookingSummaryComponent implements OnInit {
  show?: Show;
  seats: Seat[] = [];
  subtotal = 0;
  taxes = 0;
  grandTotal = 0;

  paymentMethod = 'CARD';
  isProcessing = false;
  errorMessage = '';

  // Recommended seat returned on 409 conflict
  recommendedSeatOnConflict?: any;

  constructor(
    private router: Router,
    private bookingService: BookingService
  ) {}

  ngOnInit(): void {
    const raw = sessionStorage.getItem('pendingBooking');
    if (!raw) {
      this.router.navigate(['/']);
      return;
    }

    try {
      const data = JSON.parse(raw);
      this.show = data.show;
      this.seats = data.seats;
      this.subtotal = data.totalPrice;
      this.taxes = Number((this.subtotal * 0.10).toFixed(2));
      this.grandTotal = this.subtotal + this.taxes;
    } catch (e) {
      this.router.navigate(['/']);
    }
  }

  getSeatCodes(): string {
    return this.seats.map(s => s.seatIdentifier).join(', ');
  }

  confirmBooking(): void {
    if (!this.show || this.seats.length === 0) return;

    this.isProcessing = true;
    this.errorMessage = '';
    this.recommendedSeatOnConflict = null;

    const request = {
      showId: this.show.id,
      seatIds: this.seats.map(s => s.id),
      paymentMethod: this.paymentMethod
    };

    this.bookingService.createBooking(request).subscribe({
      next: (res) => {
        this.isProcessing = false;
        if (res.success && res.data) {
          sessionStorage.removeItem('pendingBooking');
          sessionStorage.setItem('confirmedTicket', JSON.stringify(res.data));
          this.router.navigate(['/booking/confirmation', res.data.bookingNumber]);
        }
      },
      error: (err) => {
        this.isProcessing = false;
        if (err.status === 409) {
          // Double-booking conflict caught!
          const body = err.error;
          this.errorMessage = body?.message || 'One or more seats have just been booked by another user.';
          this.recommendedSeatOnConflict = body?.recommendedSeat;
        } else {
          this.errorMessage = err.error?.message || 'An error occurred while confirming your booking. Please try again.';
        }
      }
    });
  }

  backToSeats(): void {
    if (this.show) {
      this.router.navigate(['/booking/seats', this.show.id]);
    } else {
      this.router.navigate(['/']);
    }
  }
}
""")

    write_file("booking-summary/booking-summary.component.html", """<div class="summary-page container" *ngIf="show">
  <div class="page-header">
    <button (click)="backToSeats()" class="btn-back">
      <i class="fa-solid fa-arrow-left"></i> Change Seats
    </button>
    <h1>Booking Summary & Payment</h1>
  </div>

  <!-- DOUBLE BOOKING CONFLICT ALERT -->
  <div *ngIf="errorMessage" class="alert alert-danger conflict-alert">
    <i class="fa-solid fa-triangle-exclamation alert-icon"></i>
    <div class="conflict-content">
      <strong>Seat Conflict Detected:</strong> {{ errorMessage }}
      <div *ngIf="recommendedSeatOnConflict" class="conflict-rec">
        <a [routerLink]="['/booking/seats', show.id]" class="btn btn-primary btn-sm">
          <i class="fa-solid fa-chair"></i> Return to Seat Layout & Select {{ recommendedSeatOnConflict.seatIdentifier }}
        </a>
      </div>
    </div>
  </div>

  <div class="summary-grid">
    <!-- Left: Movie & Order Breakdown -->
    <div class="breakdown-card glass-card">
      <div class="order-movie-header">
        <img [src]="show.moviePosterUrl || 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=300&q=80'" [alt]="show.movieTitle" class="order-thumb">
        <div>
          <h3>{{ show.movieTitle }}</h3>
          <p class="order-theatre"><i class="fa-solid fa-location-dot"></i> {{ show.theatreName }} ({{ show.screenName }})</p>
          <p class="order-time"><i class="fa-regular fa-clock"></i> {{ show.startTime | date:'EEE, MMM d, y, hh:mm a' }}</p>
        </div>
      </div>

      <div class="divider"></div>

      <div class="ticket-breakdown">
        <h4>Seats Selected</h4>
        <div class="seat-badge-list">
          <span *ngFor="let s of seats" class="seat-pill">
            {{ s.seatIdentifier }} ({{ s.seatType }}) - ${{ s.price | number:'1.2-2' }}
          </span>
        </div>
      </div>

      <div class="divider"></div>

      <div class="price-calc">
        <div class="price-row">
          <span>Tickets Subtotal</span>
          <span>${{ subtotal | number:'1.2-2' }}</span>
        </div>
        <div class="price-row">
          <span>Taxes & Processing (10%)</span>
          <span>${{ taxes | number:'1.2-2' }}</span>
        </div>
        <div class="price-row total-row">
          <span>Grand Total</span>
          <span class="total-amount">${{ grandTotal | number:'1.2-2' }}</span>
        </div>
      </div>
    </div>

    <!-- Right: Payment Methods & Action -->
    <div class="payment-card glass-card">
      <h3>Select Payment Method</h3>
      <p class="payment-sub">All transactions are simulated and securely authorized.</p>

      <div class="payment-options">
        <label class="pay-option" [class.selected]="paymentMethod === 'CARD'">
          <input type="radio" name="payMethod" [(ngModel)]="paymentMethod" value="CARD">
          <div class="option-body">
            <div class="option-title"><i class="fa-regular fa-credit-card"></i> Credit / Debit Card</div>
            <span class="option-desc">Visa, Mastercard, American Express</span>
          </div>
        </label>

        <label class="pay-option" [class.selected]="paymentMethod === 'UPI'">
          <input type="radio" name="payMethod" [(ngModel)]="paymentMethod" value="UPI">
          <div class="option-body">
            <div class="option-title"><i class="fa-solid fa-mobile-screen"></i> Instant UPI / QR</div>
            <span class="option-desc">Google Pay, PhonePe, Paytm, BHIM</span>
          </div>
        </label>

        <label class="pay-option" [class.selected]="paymentMethod === 'CASH'">
          <input type="radio" name="payMethod" [(ngModel)]="paymentMethod" value="CASH">
          <div class="option-body">
            <div class="option-title"><i class="fa-solid fa-money-bill-wave"></i> Pay at Box Office</div>
            <span class="option-desc">Collect tickets at the cinema counter</span>
          </div>
        </label>
      </div>

      <!-- Card details mock input -->
      <div *ngIf="paymentMethod === 'CARD'" class="card-inputs">
        <div class="form-group">
          <label>Card Number</label>
          <input type="text" class="form-control" value="•••• •••• •••• 4242" readonly>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Expiry</label>
            <input type="text" class="form-control" value="12/28" readonly>
          </div>
          <div class="form-group">
            <label>CVV</label>
            <input type="text" class="form-control" value="•••" readonly>
          </div>
        </div>
      </div>

      <button (click)="confirmBooking()" [disabled]="isProcessing" class="btn btn-primary btn-pay-now">
        <span *ngIf="!isProcessing"><i class="fa-solid fa-lock"></i> Authorize & Pay ${{ grandTotal | number:'1.2-2' }}</span>
        <span *ngIf="isProcessing"><i class="fa-solid fa-spinner fa-spin"></i> Securing Your Seats...</span>
      </button>

      <p class="safe-note"><i class="fa-solid fa-shield-halved"></i> Protected by backend concurrency locking against double-booking.</p>
    </div>
  </div>
</div>
""")

    write_file("booking-summary/booking-summary.component.css", """.summary-page {
  padding: 3rem 1.5rem 5rem;
}

.page-header {
  margin-bottom: 2rem;
}

.btn-back {
  background: transparent;
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-back:hover {
  color: #fff;
}

.conflict-alert {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.alert-icon {
  font-size: 1.5rem;
}

.conflict-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 2rem;
}

.order-movie-header {
  display: flex;
  gap: 1.25rem;
  align-items: center;
}

.order-thumb {
  width: 90px;
  height: 130px;
  object-fit: cover;
  border-radius: var(--radius-sm);
}

.order-theatre, .order-time {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-top: 0.35rem;
}

.divider {
  height: 1px;
  background: var(--border-color);
  margin: 1.5rem 0;
}

.seat-badge-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.seat-pill {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--border-color);
  padding: 0.35rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  color: #fff;
}

.price-calc {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.price-row {
  display: flex;
  justify-content: space-between;
  color: var(--text-muted);
  font-size: 0.95rem;
}

.total-row {
  border-top: 1px solid var(--border-color);
  padding-top: 1rem;
  color: #fff;
  font-size: 1.2rem;
  font-weight: 700;
}

.total-amount {
  color: var(--accent-green);
  font-size: 1.4rem;
}

.payment-sub {
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-bottom: 1.5rem;
}

.payment-options {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  margin-bottom: 1.5rem;
}

.pay-option {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: var(--bg-card-hover);
  border: 1px solid var(--border-color);
  padding: 1rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
}

.pay-option.selected {
  border-color: var(--primary);
  background: rgba(229, 9, 20, 0.08);
}

.option-title {
  font-weight: 600;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.option-desc {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.card-inputs {
  margin-bottom: 1.5rem;
  background: rgba(0, 0, 0, 0.2);
  padding: 1rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  margin-bottom: 0.75rem;
}

.form-group label {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.form-control {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 0.6rem;
  border-radius: var(--radius-sm);
  color: #fff;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.btn-pay-now {
  width: 100%;
  padding: 1rem;
  font-size: 1.05rem;
}

.safe-note {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.8rem;
  margin-top: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
}

@media (max-width: 768px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
""")

    # 4. Ticket Confirmation Component
    write_file("ticket-confirmation/ticket-confirmation.component.ts", """import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BookingService } from '../../services/booking.service';
import { BookingResponse } from '../../models/booking.model';

@Component({
  selector: 'app-ticket-confirmation',
  templateUrl: './ticket-confirmation.component.html',
  styleUrls: ['./ticket-confirmation.component.css']
})
export class TicketConfirmationComponent implements OnInit {
  bookingNumber = '';
  ticket?: BookingResponse;
  isLoading = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private bookingService: BookingService
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.bookingNumber = params['bookingNumber'];
      this.loadTicket();
    });
  }

  loadTicket(): void {
    // Check session first
    const saved = sessionStorage.getItem('confirmedTicket');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (parsed.bookingNumber === this.bookingNumber) {
          this.ticket = parsed;
          this.isLoading = false;
          return;
        }
      } catch (e) {}
    }

    // Otherwise fetch from API
    this.bookingService.getBookingByNumber(this.bookingNumber).subscribe({
      next: (res) => {
        if (res.success) {
          this.ticket = res.data;
        }
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  printTicket(): void {
    window.print();
  }

  downloadTicket(): void {
    if (!this.ticket) return;

    const content = `
========================================
       CINEPASS CINEMA TICKET
========================================
Booking Reference: ${this.ticket.bookingNumber}
Customer: ${this.ticket.customerName} (${this.ticket.customerEmail})
Status: ${this.ticket.bookingStatus}

Movie: ${this.ticket.movieTitle}
Theatre: ${this.ticket.theatreName}
Screen: ${this.ticket.screenName}
Date & Time: ${this.ticket.showStartTime}

Seats: ${this.ticket.seatNumbers.join(', ')}
Total Paid: $${Number(this.ticket.totalAmount).toFixed(2)}
Payment Method: ${this.ticket.paymentMethod}
Transaction ID: ${this.ticket.transactionId}

Thank you for choosing CinePass Cinemas!
========================================
`;
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Ticket-${this.ticket.bookingNumber}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  }
}
""")

    write_file("ticket-confirmation/ticket-confirmation.component.html", """<div class="confirmation-page container">
  <div *ngIf="isLoading" class="loading-state">
    <i class="fa-solid fa-spinner fa-spin"></i>
    <p>Loading ticket receipt...</p>
  </div>

  <div *ngIf="!isLoading && ticket" class="ticket-wrapper">
    <div class="success-header">
      <div class="check-icon-circle"><i class="fa-solid fa-check"></i></div>
      <h1>Booking Confirmed!</h1>
      <p class="success-sub">Your digital cinema pass is ready. A confirmation email has been dispatched.</p>
    </div>

    <!-- THE PROFESSIONAL CINEMA PASS -->
    <div class="cinema-pass-card" id="printable-ticket">
      <!-- Left Stub -->
      <div class="pass-main">
        <div class="pass-top">
          <div class="brand-tag">
            <i class="fa-solid fa-film"></i> CINEPASS CINEMAS
          </div>
          <span class="booking-ref-pill">REF: {{ ticket.bookingNumber }}</span>
        </div>

        <div class="pass-movie-row">
          <img [src]="ticket.moviePosterUrl || 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=300&q=80'" [alt]="ticket.movieTitle" class="pass-thumb">
          <div class="pass-details">
            <h2 class="pass-movie-title">{{ ticket.movieTitle }}</h2>
            <p class="pass-cinema"><i class="fa-solid fa-building-columns"></i> {{ ticket.theatreName }}</p>
            <p class="pass-screen"><i class="fa-solid fa-desktop"></i> {{ ticket.screenName }}</p>
          </div>
        </div>

        <div class="pass-info-grid">
          <div class="info-block">
            <span class="info-lbl">SHOWTIME</span>
            <span class="info-val">{{ ticket.showStartTime | date:'EEE, MMM d, y - hh:mm a' }}</span>
          </div>

          <div class="info-block">
            <span class="info-lbl">SEATS ALLOCATED</span>
            <span class="info-val highlight-val">{{ ticket.seatNumbers.join(', ') }}</span>
          </div>

          <div class="info-block">
            <span class="info-lbl">GUEST NAME</span>
            <span class="info-val">{{ ticket.customerName }}</span>
          </div>

          <div class="info-block">
            <span class="info-lbl">TOTAL PAID</span>
            <span class="info-val highlight-green">${{ ticket.totalAmount | number:'1.2-2' }}</span>
          </div>
        </div>

        <!-- Dynamic Simulated Barcode -->
        <div class="barcode-wrapper">
          <svg class="barcode-svg" viewBox="0 0 260 40" preserveAspectRatio="none">
            <rect x="0" y="0" width="3" height="40" fill="#fff" />
            <rect x="6" y="0" width="2" height="40" fill="#fff" />
            <rect x="12" y="0" width="6" height="40" fill="#fff" />
            <rect x="22" y="0" width="2" height="40" fill="#fff" />
            <rect x="28" y="0" width="4" height="40" fill="#fff" />
            <rect x="36" y="0" width="8" height="40" fill="#fff" />
            <rect x="48" y="0" width="2" height="40" fill="#fff" />
            <rect x="54" y="0" width="4" height="40" fill="#fff" />
            <rect x="64" y="0" width="6" height="40" fill="#fff" />
            <rect x="74" y="0" width="2" height="40" fill="#fff" />
            <rect x="80" y="0" width="8" height="40" fill="#fff" />
            <rect x="92" y="0" width="4" height="40" fill="#fff" />
            <rect x="100" y="0" width="2" height="40" fill="#fff" />
            <rect x="108" y="0" width="6" height="40" fill="#fff" />
            <rect x="120" y="0" width="4" height="40" fill="#fff" />
            <rect x="130" y="0" width="8" height="40" fill="#fff" />
            <rect x="144" y="0" width="2" height="40" fill="#fff" />
            <rect x="150" y="0" width="4" height="40" fill="#fff" />
            <rect x="160" y="0" width="6" height="40" fill="#fff" />
            <rect x="172" y="0" width="2" height="40" fill="#fff" />
            <rect x="180" y="0" width="8" height="40" fill="#fff" />
            <rect x="194" y="0" width="4" height="40" fill="#fff" />
            <rect x="204" y="0" width="6" height="40" fill="#fff" />
            <rect x="216" y="0" width="2" height="40" fill="#fff" />
            <rect x="224" y="0" width="4" height="40" fill="#fff" />
            <rect x="234" y="0" width="8" height="40" fill="#fff" />
            <rect x="248" y="0" width="2" height="40" fill="#fff" />
            <rect x="254" y="0" width="6" height="40" fill="#fff" />
          </svg>
          <span class="barcode-num">{{ ticket.bookingNumber }}</span>
        </div>
      </div>

      <!-- Perforated Tear Line -->
      <div class="pass-notch">
        <div class="notch-circle notch-top"></div>
        <div class="notch-line"></div>
        <div class="notch-circle notch-bottom"></div>
      </div>

      <!-- Right Pass Stub with QR Code -->
      <div class="pass-stub">
        <div class="qr-box">
          <!-- Vector QR Code representation -->
          <svg viewBox="0 0 100 100" class="qr-svg">
            <rect x="0" y="0" width="100" height="100" fill="#fff" />
            <rect x="10" y="10" width="25" height="25" fill="#000" />
            <rect x="15" y="15" width="15" height="15" fill="#fff" />
            <rect x="18" y="18" width="9" height="9" fill="#000" />

            <rect x="65" y="10" width="25" height="25" fill="#000" />
            <rect x="70" y="15" width="15" height="15" fill="#fff" />
            <rect x="73" y="18" width="9" height="9" fill="#000" />

            <rect x="10" y="65" width="25" height="25" fill="#000" />
            <rect x="15" y="70" width="15" height="15" fill="#fff" />
            <rect x="18" y="73" width="9" height="9" fill="#000" />

            <rect x="42" y="15" width="8" height="8" fill="#000" />
            <rect x="48" y="30" width="8" height="12" fill="#000" />
            <rect x="60" y="45" width="12" height="8" fill="#000" />
            <rect x="42" y="60" width="12" height="8" fill="#000" />
            <rect x="58" y="65" width="8" height="16" fill="#000" />
            <rect x="75" y="70" width="12" height="12" fill="#000" />
          </svg>
        </div>
        <span class="qr-label">SCAN AT USHER ENTRANCE</span>

        <div class="stub-seats">
          <span class="stub-lbl">SEATS</span>
          <span class="stub-val">{{ ticket.seatNumbers.join(', ') }}</span>
        </div>

        <div class="stub-status">
          <span class="badge badge-regular">{{ ticket.paymentStatus }}</span>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="pass-actions">
      <button (click)="printTicket()" class="btn btn-primary">
        <i class="fa-solid fa-print"></i> Print Ticket
      </button>
      <button (click)="downloadTicket()" class="btn btn-secondary">
        <i class="fa-solid fa-download"></i> Download E-Ticket
      </button>
      <a routerLink="/" class="btn btn-secondary">
        <i class="fa-solid fa-house"></i> Book Another Movie
      </a>
    </div>
  </div>
</div>
""")

    write_file("ticket-confirmation/ticket-confirmation.component.css", """.confirmation-page {
  padding: 3rem 1.5rem 6rem;
}

.ticket-wrapper {
  max-width: 860px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.success-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.check-icon-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.2);
  border: 2px solid var(--accent-green);
  color: var(--accent-green);
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.25rem;
}

.success-sub {
  color: var(--text-muted);
  font-size: 1rem;
}

/* THE PASS */
.cinema-pass-card {
  display: flex;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
  width: 100%;
  margin-bottom: 2.5rem;
  position: relative;
}

.pass-main {
  flex: 1;
  padding: 2rem;
}

.pass-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.brand-tag {
  color: var(--primary);
  font-weight: 800;
  letter-spacing: 0.1em;
  font-size: 0.9rem;
}

.booking-ref-pill {
  background: rgba(255, 255, 255, 0.08);
  padding: 0.25rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  color: var(--text-muted);
  font-family: monospace;
}

.pass-movie-row {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  margin-bottom: 1.75rem;
}

.pass-thumb {
  width: 90px;
  height: 125px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}

.pass-movie-title {
  font-size: 1.75rem;
  line-height: 1.2;
  margin-bottom: 0.35rem;
}

.pass-cinema, .pass-screen {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.pass-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  background: rgba(0, 0, 0, 0.25);
  padding: 1.25rem;
  border-radius: var(--radius-md);
  margin-bottom: 1.5rem;
}

.info-block {
  display: flex;
  flex-direction: column;
}

.info-lbl {
  font-size: 0.7rem;
  color: var(--text-muted);
  letter-spacing: 0.08em;
  font-weight: 600;
}

.info-val {
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  margin-top: 0.2rem;
}

.highlight-val {
  color: var(--accent-gold);
}

.highlight-green {
  color: var(--accent-green);
}

.barcode-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
}

.barcode-svg {
  width: 260px;
  height: 38px;
}

.barcode-num {
  font-family: monospace;
  font-size: 0.75rem;
  color: var(--text-muted);
  letter-spacing: 0.2em;
}

/* PERFORATION NOTCH */
.pass-notch {
  width: 24px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.notch-circle {
  width: 24px;
  height: 24px;
  background: var(--bg-dark);
  border-radius: 50%;
  position: absolute;
  left: 0;
}

.notch-top {
  top: -12px;
}

.notch-bottom {
  bottom: -12px;
}

.notch-line {
  height: 100%;
  width: 1px;
  border-left: 2px dashed var(--border-color);
}

/* STUB */
.pass-stub {
  width: 220px;
  background: rgba(0, 0, 0, 0.2);
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.qr-box {
  width: 110px;
  height: 110px;
  padding: 8px;
  background: #fff;
  border-radius: 8px;
  margin-bottom: 0.75rem;
}

.qr-svg {
  width: 100%;
  height: 100%;
}

.qr-label {
  font-size: 0.65rem;
  color: var(--text-muted);
  font-weight: 700;
  letter-spacing: 0.05em;
  margin-bottom: 1.25rem;
}

.stub-seats {
  margin-bottom: 1rem;
}

.stub-lbl {
  display: block;
  font-size: 0.7rem;
  color: var(--text-muted);
}

.stub-val {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--accent-gold);
}

.pass-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

@media print {
  body * {
    visibility: hidden;
  }
  #printable-ticket, #printable-ticket * {
    visibility: visible;
  }
  #printable-ticket {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    border: 1px solid #ccc;
    background: #fff;
    color: #000;
  }
}

@media (max-width: 768px) {
  .cinema-pass-card {
    flex-direction: column;
  }
  .pass-notch {
    display: none;
  }
  .pass-stub {
    width: 100%;
    border-top: 1px dashed var(--border-color);
  }
}
""")

if __name__ == "__main__":
    generate_booking_components()
