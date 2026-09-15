export interface Seat {
  id: number;
  rowName: string;
  seatNumber: number;
  seatType: 'REGULAR' | 'PREMIUM' | 'VIP';
  price: number;
  status: 'AVAILABLE' | 'BOOKED' | 'SELECTED';
  seatIdentifier: string;
  rowIndex: number;
  columnIndex: number;
}
