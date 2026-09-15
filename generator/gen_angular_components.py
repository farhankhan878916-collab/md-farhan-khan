import os

BASE_DIR = "movie-ticket-booking-system"
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend", "src", "app")

def write_file(subpath, content):
    full_path = os.path.join(FRONTEND_DIR, subpath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {full_path}")

def generate_components():
    # 1. Navbar Component
    write_file("components/navbar/navbar.component.ts", """import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  isMenuOpen = false;

  constructor(public authService: AuthService, private router: Router) {}

  toggleMenu(): void {
    this.isMenuOpen = !this.isMenuOpen;
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
""")

    write_file("components/navbar/navbar.component.html", """<nav class="navbar">
  <div class="container nav-content">
    <a routerLink="/" class="nav-brand">
      <span class="brand-icon"><i class="fa-solid fa-film"></i></span>
      <span class="brand-name">Cine<span class="brand-accent">Pass</span></span>
    </a>

    <div class="nav-links" [class.active]="isMenuOpen">
      <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}" class="nav-item">
        <i class="fa-solid fa-compass"></i> Movies
      </a>

      <ng-container *ngIf="authService.isLoggedIn()">
        <a routerLink="/my-bookings" routerLinkActive="active" class="nav-item">
          <i class="fa-solid fa-ticket"></i> My Bookings
        </a>

        <a *ngIf="authService.isAdmin()" routerLink="/admin" routerLinkActive="active" class="nav-item admin-link">
          <i class="fa-solid fa-chart-line"></i> Admin Dashboard
        </a>
      </ng-container>
    </div>

    <div class="nav-actions">
      <ng-container *ngIf="authService.currentUser$ | async as user; else guestTpl">
        <div class="user-profile">
          <div class="user-avatar">
            {{ user.fullName.charAt(0) }}
          </div>
          <div class="user-info">
            <span class="user-name">{{ user.fullName }}</span>
            <span class="user-role">{{ user.role === 'ROLE_ADMIN' ? 'Admin' : 'Customer' }}</span>
          </div>
          <button (click)="logout()" class="btn-icon" title="Logout">
            <i class="fa-solid fa-arrow-right-from-bracket"></i>
          </button>
        </div>
      </ng-container>

      <ng-template #guestTpl>
        <div class="guest-actions">
          <a routerLink="/login" class="btn btn-secondary btn-sm">Sign In</a>
          <a routerLink="/register" class="btn btn-primary btn-sm">Sign Up</a>
        </div>
      </ng-template>

      <button class="mobile-toggle" (click)="toggleMenu()">
        <i class="fa-solid" [class.fa-bars]="!isMenuOpen" [class.fa-xmark]="isMenuOpen"></i>
      </button>
    </div>
  </div>
</nav>
""")

    write_file("components/navbar/navbar.component.css", """.navbar {
  background: rgba(15, 16, 22, 0.9);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 0.85rem 0;
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 1.45rem;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.brand-icon {
  color: var(--primary);
  font-size: 1.6rem;
}

.brand-accent {
  color: var(--primary);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.8rem;
}

.nav-item {
  color: var(--text-muted);
  font-weight: 500;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.nav-item:hover, .nav-item.active {
  color: #fff;
}

.admin-link {
  color: var(--accent-gold);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: var(--bg-card);
  padding: 0.35rem 0.8rem;
  border-radius: 9999px;
  border: 1px solid var(--border-color);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #fff;
}

.user-role {
  font-size: 0.7rem;
  color: var(--text-muted);
}

.btn-icon {
  background: transparent;
  color: var(--text-muted);
  font-size: 1rem;
  padding: 0.3rem;
}

.btn-icon:hover {
  color: var(--accent-red);
}

.guest-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-sm {
  padding: 0.45rem 0.9rem;
  font-size: 0.85rem;
}

.mobile-toggle {
  display: none;
  background: transparent;
  color: #fff;
  font-size: 1.3rem;
}

@media (max-width: 768px) {
  .mobile-toggle {
    display: block;
  }
  .nav-links {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--bg-card);
    flex-direction: column;
    padding: 1.5rem;
    gap: 1.25rem;
    border-bottom: 1px solid var(--border-color);
  }
  .nav-links.active {
    display: flex;
  }
}
""")

    # 2. Movie List Component
    write_file("components/movie-list/movie-list.component.ts", """import { Component, OnInit } from '@angular/core';
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
""")

    write_file("components/movie-list/movie-list.component.html", """<div class="movie-list-page">
  <!-- Hero Featured Banner -->
  <section class="hero-section">
    <div class="container hero-content">
      <div class="hero-badge"><i class="fa-solid fa-fire"></i> BLOCKBUSTER NOW SHOWING</div>
      <h1 class="hero-title">Experience Cinema In Stunning IMAX & 4DX</h1>
      <p class="hero-sub">Book your favorite seats seamlessly with real-time double-booking protection and instant smart vacant seat suggestions.</p>

      <div class="search-bar">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input type="text" [(ngModel)]="searchQuery" (input)="onSearchChange()" placeholder="Search movies by title, genre, or actor...">
      </div>
    </div>
  </section>

  <!-- Movies Section -->
  <section class="movies-container container">
    <div class="filter-row">
      <div class="section-header">
        <h2>Now Showing</h2>
        <span class="count-tag">{{ filteredMovies.length }} Movies</span>
      </div>

      <div class="genre-pills">
        <button *ngFor="let g of genres"
                (click)="selectGenre(g)"
                class="genre-btn"
                [class.active]="selectedGenre === g">
          {{ g }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div *ngIf="isLoading" class="loading-state">
      <i class="fa-solid fa-spinner fa-spin"></i>
      <p>Loading premier titles...</p>
    </div>

    <!-- Empty State -->
    <div *ngIf="!isLoading && filteredMovies.length === 0" class="empty-state glass-card">
      <i class="fa-solid fa-film empty-icon"></i>
      <h3>No Movies Found</h3>
      <p>We could not find any movies matching your search or filter.</p>
      <button (click)="selectedGenre = 'ALL'; searchQuery = ''; filterMovies()" class="btn btn-secondary">Reset Filters</button>
    </div>

    <!-- Movie Grid -->
    <div *ngIf="!isLoading && filteredMovies.length > 0" class="movie-grid">
      <div *ngFor="let movie of filteredMovies" class="movie-card glass-card">
        <div class="poster-wrapper">
          <img [src]="movie.posterUrl || 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=600&q=80'" [alt]="movie.title" class="poster-img">
          <div class="poster-overlay">
            <a [routerLink]="['/movies', movie.id]" class="btn btn-primary btn-book">
              <i class="fa-solid fa-ticket"></i> Book Now
            </a>
          </div>
          <div class="rating-badge">
            <i class="fa-solid fa-star star-icon"></i> {{ movie.rating | number:'1.1-1' }}
          </div>
        </div>

        <div class="movie-meta">
          <div class="meta-row">
            <span class="genre-tag">{{ movie.genre }}</span>
            <span class="duration-tag"><i class="fa-regular fa-clock"></i> {{ movie.durationMinutes }}m</span>
          </div>

          <h3 class="movie-title">
            <a [routerLink]="['/movies', movie.id]">{{ movie.title }}</a>
          </h3>

          <p class="movie-desc">{{ movie.description }}</p>

          <div class="card-footer">
            <span class="lang-tag"><i class="fa-solid fa-language"></i> {{ movie.language }}</span>
            <a [routerLink]="['/movies', movie.id]" class="details-link">
              View Shows <i class="fa-solid fa-arrow-right"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</div>
""")

    write_file("components/movie-list/movie-list.component.css", """.movie-list-page {
  padding-bottom: 4rem;
}

.hero-section {
  background: linear-gradient(180deg, rgba(229, 9, 20, 0.12) 0%, rgba(15, 16, 22, 0) 100%);
  padding: 4rem 0 3rem;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-badge {
  background: rgba(229, 9, 20, 0.15);
  border: 1px solid rgba(229, 9, 20, 0.3);
  color: var(--primary);
  padding: 0.35rem 0.9rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  margin-bottom: 1.25rem;
}

.hero-title {
  font-size: 2.75rem;
  line-height: 1.15;
  margin-bottom: 1rem;
}

.hero-sub {
  color: var(--text-muted);
  font-size: 1.1rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 0.85rem 1.25rem;
  border-radius: 9999px;
  width: 100%;
  max-width: 580px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
}

.search-icon {
  color: var(--text-muted);
  font-size: 1.1rem;
}

.search-bar input {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 1rem;
  width: 100%;
  outline: none;
}

.search-bar input::placeholder {
  color: var(--text-muted);
}

.filter-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 2.5rem 0 1.75rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.count-tag {
  background: rgba(255, 255, 255, 0.08);
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.genre-pills {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.genre-btn {
  background: var(--bg-card);
  color: var(--text-muted);
  padding: 0.45rem 1rem;
  border-radius: 9999px;
  border: 1px solid var(--border-color);
  font-size: 0.85rem;
  font-weight: 600;
}

.genre-btn.active, .genre-btn:hover {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 1.75rem;
}

.movie-card {
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.movie-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 35px rgba(0, 0, 0, 0.6);
}

.poster-wrapper {
  position: relative;
  height: 380px;
  overflow: hidden;
  background: #000;
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.movie-card:hover .poster-img {
  transform: scale(1.05);
}

.poster-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.25s ease;
}

.movie-card:hover .poster-overlay {
  opacity: 1;
}

.rating-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(15, 16, 22, 0.85);
  backdrop-filter: blur(8px);
  padding: 0.3rem 0.6rem;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  border: 1px solid var(--border-color);
}

.star-icon {
  color: var(--accent-gold);
}

.movie-meta {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.8rem;
}

.genre-tag {
  color: var(--accent-cyan);
  font-weight: 600;
}

.duration-tag {
  color: var(--text-muted);
}

.movie-title {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.movie-title a:hover {
  color: var(--primary);
}

.movie-desc {
  color: var(--text-muted);
  font-size: 0.85rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 1rem;
  flex-grow: 1;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--border-color);
  padding-top: 0.75rem;
  font-size: 0.85rem;
}

.lang-tag {
  color: var(--text-muted);
}

.details-link {
  color: var(--primary);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.details-link:hover {
  text-decoration: underline;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 4rem 1rem;
}

.empty-icon {
  font-size: 3rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
}
""")

if __name__ == "__main__":
    generate_components()
