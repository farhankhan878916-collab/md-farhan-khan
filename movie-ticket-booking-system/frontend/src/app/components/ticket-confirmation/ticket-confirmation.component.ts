import { Component, OnInit } from '@angular/core';
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
