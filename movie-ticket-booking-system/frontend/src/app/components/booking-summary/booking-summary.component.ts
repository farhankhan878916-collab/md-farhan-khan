import { Component, OnInit } from '@angular/core';
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
