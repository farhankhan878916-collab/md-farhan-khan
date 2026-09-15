import { Component } from '@angular/core';

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
