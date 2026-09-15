import { Component, OnInit } from '@angular/core';
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
