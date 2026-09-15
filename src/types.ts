export interface Movie {
  id: number;
  title: string;
  genre: string;
  durationMinutes: number;
  rating: number;
  language: string;
  posterUrl: string;
  description: string;
  releaseDate: string;
}

export interface Show {
  id: number;
  movieTitle: string;
  theatreName: string;
  screenName: string;
  startTime: string;
  basePrice: number;
}

export interface SeatItem {
  id: number;
  rowName: string;
  seatNumber: number;
  seatIdentifier: string;
  seatType: 'REGULAR' | 'PREMIUM' | 'VIP';
  price: number;
  status: 'AVAILABLE' | 'SELECTED' | 'BOOKED';
}

export interface ApiEndpoint {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  summary: string;
  authRequired: boolean;
  role?: string;
  requestBody?: string;
  responseBody?: string;
}

export interface FileItem {
  name: string;
  path: string;
  type: 'java' | 'ts' | 'html' | 'css' | 'sql' | 'xml' | 'json' | 'md';
  category: 'Backend Java' | 'Frontend Angular' | 'Database' | 'Documentation';
  content: string;
}
