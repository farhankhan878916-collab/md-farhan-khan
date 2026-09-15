import { Component, OnInit } from '@angular/core';
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
