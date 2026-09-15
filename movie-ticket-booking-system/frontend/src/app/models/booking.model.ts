export interface BookingRequest {
  showId: number;
  seatIds: number[];
  paymentMethod: string;
}

export interface BookingResponse {
  bookingId: number;
  bookingNumber: string;
  customerName: string;
  customerEmail: string;
  movieTitle: string;
  moviePosterUrl: string;
  theatreName: string;
  theatreAddress: string;
  screenName: string;
  showStartTime: string;
  showEndTime: string;
  seatNumbers: string[];
  totalAmount: number;
  bookingStatus: string;
  paymentStatus: string;
  paymentMethod: string;
  transactionId: string;
  bookedAt: string;
}
