import React, { useState } from 'react';
import { Sparkles, AlertTriangle, CheckCircle2, Ticket, RefreshCw, Armchair, ShieldAlert, CreditCard } from 'lucide-react';
import { SeatItem } from '../types';

const INITIAL_SEATS: SeatItem[] = [
  // Row A - VIP ($25)
  { id: 1, rowName: 'A', seatNumber: 1, seatIdentifier: 'A1', seatType: 'VIP', price: 25.0, status: 'AVAILABLE' },
  { id: 2, rowName: 'A', seatNumber: 2, seatIdentifier: 'A2', seatType: 'VIP', price: 25.0, status: 'AVAILABLE' },
  { id: 3, rowName: 'A', seatNumber: 3, seatIdentifier: 'A3', seatType: 'VIP', price: 25.0, status: 'BOOKED' },
  { id: 4, rowName: 'A', seatNumber: 4, seatIdentifier: 'A4', seatType: 'VIP', price: 25.0, status: 'BOOKED' },
  { id: 5, rowName: 'A', seatNumber: 5, seatIdentifier: 'A5', seatType: 'VIP', price: 25.0, status: 'AVAILABLE' },
  { id: 6, rowName: 'A', seatNumber: 6, seatIdentifier: 'A6', seatType: 'VIP', price: 25.0, status: 'AVAILABLE' },
  { id: 7, rowName: 'A', seatNumber: 7, seatIdentifier: 'A7', seatType: 'VIP', price: 25.0, status: 'AVAILABLE' },
  { id: 8, rowName: 'A', seatNumber: 8, seatIdentifier: 'A8', seatType: 'VIP', price: 25.0, status: 'AVAILABLE' },

  // Row B - PREMIUM ($20)
  { id: 9, rowName: 'B', seatNumber: 1, seatIdentifier: 'B1', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },
  { id: 10, rowName: 'B', seatNumber: 2, seatIdentifier: 'B2', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },
  { id: 11, rowName: 'B', seatNumber: 3, seatIdentifier: 'B3', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },
  { id: 12, rowName: 'B', seatNumber: 4, seatIdentifier: 'B4', seatType: 'PREMIUM', price: 20.0, status: 'BOOKED' },
  { id: 13, rowName: 'B', seatNumber: 5, seatIdentifier: 'B5', seatType: 'PREMIUM', price: 20.0, status: 'BOOKED' },
  { id: 14, rowName: 'B', seatNumber: 6, seatIdentifier: 'B6', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },
  { id: 15, rowName: 'B', seatNumber: 7, seatIdentifier: 'B7', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },
  { id: 16, rowName: 'B', seatNumber: 8, seatIdentifier: 'B8', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },

  // Row C - PREMIUM ($20)
  { id: 17, rowName: 'C', seatNumber: 1, seatIdentifier: 'C1', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },
  { id: 18, rowName: 'C', seatNumber: 2, seatIdentifier: 'C2', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },
  { id: 19, rowName: 'C', seatNumber: 3, seatIdentifier: 'C3', seatType: 'PREMIUM', price: 20.0, status: 'BOOKED' },
  { id: 20, rowName: 'C', seatNumber: 4, seatIdentifier: 'C4', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },
  { id: 21, rowName: 'C', seatNumber: 5, seatIdentifier: 'C5', seatType: 'PREMIUM', price: 20.0, status: 'BOOKED' },
  { id: 22, rowName: 'C', seatNumber: 6, seatIdentifier: 'C6', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },
  { id: 23, rowName: 'C', seatNumber: 7, seatIdentifier: 'C7', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },
  { id: 24, rowName: 'C', seatNumber: 8, seatIdentifier: 'C8', seatType: 'PREMIUM', price: 20.0, status: 'AVAILABLE' },

  // Row D - REGULAR ($15)
  { id: 25, rowName: 'D', seatNumber: 1, seatIdentifier: 'D1', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 26, rowName: 'D', seatNumber: 2, seatIdentifier: 'D2', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 27, rowName: 'D', seatNumber: 3, seatIdentifier: 'D3', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 28, rowName: 'D', seatNumber: 4, seatIdentifier: 'D4', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 29, rowName: 'D', seatNumber: 5, seatIdentifier: 'D5', seatType: 'REGULAR', price: 15.0, status: 'BOOKED' },
  { id: 30, rowName: 'D', seatNumber: 6, seatIdentifier: 'D6', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 31, rowName: 'D', seatNumber: 7, seatIdentifier: 'D7', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 32, rowName: 'D', seatNumber: 8, seatIdentifier: 'D8', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },

  // Row E - REGULAR ($15)
  { id: 33, rowName: 'E', seatNumber: 1, seatIdentifier: 'E1', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 34, rowName: 'E', seatNumber: 2, seatIdentifier: 'E2', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 35, rowName: 'E', seatNumber: 3, seatIdentifier: 'E3', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 36, rowName: 'E', seatNumber: 4, seatIdentifier: 'E4', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 37, rowName: 'E', seatNumber: 5, seatIdentifier: 'E5', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 38, rowName: 'E', seatNumber: 6, seatIdentifier: 'E6', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 39, rowName: 'E', seatNumber: 7, seatIdentifier: 'E7', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
  { id: 40, rowName: 'E', seatNumber: 8, seatIdentifier: 'E8', seatType: 'REGULAR', price: 15.0, status: 'AVAILABLE' },
];

export const SimulatorTab: React.FC = () => {
  const [seats, setSeats] = useState<SeatItem[]>(INITIAL_SEATS);
  const [recommendedSeat, setRecommendedSeat] = useState<SeatItem | null>(null);
  const [recommendationMessage, setRecommendationMessage] = useState<string | null>(null);
  const [conflictWarning, setConflictWarning] = useState<string | null>(null);
  const [confirmedBooking, setConfirmedBooking] = useState<{
    bookingNumber: string;
    seats: string[];
    total: number;
    time: string;
  } | null>(null);

  const selectedSeats = seats.filter(s => s.status === 'SELECTED');
  const totalPrice = selectedSeats.reduce((acc, s) => acc + s.price, 0);

  // Smart Euclidean recommendation calculation matching Spring Boot SeatRecommendationServiceImpl
  const findNearestVacantSeat = (bookedSeat: SeatItem) => {
    const rowToIndex: Record<string, number> = { A: 1, B: 2, C: 3, D: 4, E: 5 };
    const bookedRow = rowToIndex[bookedSeat.rowName] || 1;
    const bookedCol = bookedSeat.seatNumber;

    let bestSeat: SeatItem | null = null;
    let minDistance = Infinity;

    seats.forEach(candidate => {
      if (candidate.status === 'AVAILABLE') {
        const candRow = rowToIndex[candidate.rowName] || 1;
        const candCol = candidate.seatNumber;
        const rowDiff = (candRow - bookedRow) * 1.5;
        const colDiff = candCol - bookedCol;
        const distance = Math.sqrt(rowDiff * rowDiff + colDiff * colDiff);

        if (distance < minDistance) {
          minDistance = distance;
          bestSeat = candidate;
        }
      }
    });

    return bestSeat;
  };

  const handleSeatClick = (seat: SeatItem) => {
    setConflictWarning(null);
    if (seat.status === 'BOOKED') {
      // Trigger Smart Recommendation Assistant
      const nearest = findNearestVacantSeat(seat);
      if (nearest) {
        setRecommendedSeat(nearest);
        setRecommendationMessage(`Seat ${seat.seatIdentifier} is occupied! Smart Assistant found nearest vacant seat: ${nearest.seatIdentifier} (${nearest.seatType}, $${nearest.price.toFixed(2)})`);
      }
      return;
    }

    // Toggle selection
    setSeats(prev =>
      prev.map(s => {
        if (s.id === seat.id) {
          return { ...s, status: s.status === 'SELECTED' ? 'AVAILABLE' : 'SELECTED' };
        }
        return s;
      })
    );
  };

  const applyRecommendation = () => {
    if (!recommendedSeat) return;
    setSeats(prev =>
      prev.map(s => (s.id === recommendedSeat.id ? { ...s, status: 'SELECTED' } : s))
    );
    setRecommendedSeat(null);
    setRecommendationMessage(null);
  };

  const simulateConcurrencyConflict = () => {
    if (selectedSeats.length === 0) {
      alert('Please select at least one seat first.');
      return;
    }
    const victim = selectedSeats[0];
    // Simulate another user booking it concurrently
    setSeats(prev =>
      prev.map(s => (s.id === victim.id ? { ...s, status: 'BOOKED' } : s))
    );
    setConflictWarning(
      `409 Conflict Detected! Seat ${victim.seatIdentifier} was just reserved by another patron in a concurrent transaction! Double-booking was prevented by Serializable Isolation.`
    );
    const nearest = findNearestVacantSeat(victim);
    if (nearest) {
      setRecommendedSeat(nearest);
      setRecommendationMessage(`Automated fallback recommendation: Seat ${nearest.seatIdentifier} is vacant!`);
    }
  };

  const completeBooking = () => {
    if (selectedSeats.length === 0) return;
    const seatNames = selectedSeats.map(s => s.seatIdentifier);
    const bookingNum = `BK-${Date.now().toString().slice(-6)}-${Math.random().toString(36).substring(2, 6).toUpperCase()}`;

    // Mark as booked
    setSeats(prev =>
      prev.map(s => (s.status === 'SELECTED' ? { ...s, status: 'BOOKED' } : s))
    );

    setConfirmedBooking({
      bookingNumber: bookingNum,
      seats: seatNames,
      total: totalPrice,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    });
  };

  const resetCinema = () => {
    setSeats(INITIAL_SEATS);
    setRecommendedSeat(null);
    setRecommendationMessage(null);
    setConflictWarning(null);
    setConfirmedBooking(null);
  };

  return (
    <div className="space-y-6">
      {/* Simulation Controls & Status banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-slate-900/75 backdrop-blur-md border border-slate-700/60 shadow-lg">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Armchair className="w-5 h-5 text-red-500" />
            Auditorium 1 — IMAX Laser Projection
          </h3>
          <p className="text-xs text-slate-400">
            Movie: <strong>Interstellar: Beyond Time</strong> • 7:30 PM • Grand Horizon IMAX
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={simulateConcurrencyConflict}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-amber-500/10 text-amber-300 border border-amber-500/30 hover:bg-amber-500/20 transition flex items-center gap-1.5"
            title="Simulates 2 users booking the same seat at the exact same millisecond"
          >
            <ShieldAlert className="w-4 h-4" /> Simulate Race Condition (409)
          </button>
          <button
            onClick={resetCinema}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Reset Grid
          </button>
        </div>
      </div>

      {/* Warning/Conflict Banner */}
      {conflictWarning && (
        <div className="p-4 rounded-xl bg-red-950/40 border border-red-500/40 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
          <div className="text-xs text-red-200">
            <p className="font-bold text-red-300">Concurrency Barrier Engaged</p>
            <p className="mt-0.5">{conflictWarning}</p>
          </div>
        </div>
      )}

      {/* Smart Recommendation Banner */}
      {recommendationMessage && recommendedSeat && (
        <div className="p-4 rounded-xl bg-amber-950/40 border border-amber-500/40 flex items-center justify-between gap-4 flex-wrap">
          <div className="flex items-center gap-3">
            <Sparkles className="w-5 h-5 text-amber-400 shrink-0" />
            <div className="text-xs text-amber-200">
              <span className="font-bold text-amber-300">Smart Seat Recommendation: </span>
              {recommendationMessage}
            </div>
          </div>
          <button
            onClick={applyRecommendation}
            className="px-3 py-1 text-xs font-bold rounded-lg bg-amber-500 text-slate-950 hover:bg-amber-400 transition"
          >
            Select {recommendedSeat.seatIdentifier} ($ {recommendedSeat.price.toFixed(2)})
          </button>
        </div>
      )}

      {/* Cinema Screen Projection graphic */}
      <div className="relative pt-2 pb-4 text-center">
        <div className="w-3/4 max-w-xl mx-auto h-2.5 rounded-t-full bg-gradient-to-r from-transparent via-red-500 to-transparent opacity-80 shadow-[0_4px_25px_rgba(239,68,68,0.5)]"></div>
        <p className="text-[10px] tracking-widest text-slate-500 uppercase font-mono mt-1.5">IMAX Curved Screen</p>
      </div>

      {/* Visual Seat Grid */}
      <div className="bg-slate-950/75 backdrop-blur-md rounded-xl p-6 border border-slate-700/60 shadow-xl flex flex-col items-center">
        {['A', 'B', 'C', 'D', 'E'].map(rowName => {
          const rowSeats = seats.filter(s => s.rowName === rowName);
          const rowType = rowSeats[0]?.seatType;
          return (
            <div key={rowName} className="flex items-center gap-3 mb-2.5">
              <span className="w-5 text-center text-xs font-mono font-bold text-slate-400">{rowName}</span>
              <div className="flex items-center gap-1.5 sm:gap-2">
                {rowSeats.map(seat => {
                  let colorClass = 'bg-slate-800 text-slate-300 border-slate-700 hover:border-slate-500';
                  if (seat.status === 'BOOKED') {
                    colorClass = 'bg-red-950/50 text-red-400/60 border-red-900/60 cursor-not-allowed';
                  } else if (seat.status === 'SELECTED') {
                    colorClass = 'bg-emerald-600 text-white border-emerald-400 shadow-[0_0_12px_rgba(16,185,129,0.4)]';
                  } else if (recommendedSeat && recommendedSeat.id === seat.id) {
                    colorClass = 'bg-amber-600/30 text-amber-300 border-amber-400 animate-pulse';
                  }

                  return (
                    <button
                      key={seat.id}
                      onClick={() => handleSeatClick(seat)}
                      className={`w-8 h-8 sm:w-9 sm:h-9 rounded-md border text-xs font-mono font-semibold flex items-center justify-center transition-all ${colorClass}`}
                      title={`${seat.seatIdentifier} (${seat.seatType} - $${seat.price}) - Status: ${seat.status}`}
                    >
                      {seat.seatNumber}
                    </button>
                  );
                })}
              </div>
              <span className="text-[10px] uppercase font-mono text-slate-400 w-16 text-right hidden sm:inline">
                {rowType}
              </span>
            </div>
          );
        })}

        {/* Legend */}
        <div className="flex flex-wrap items-center justify-center gap-6 mt-6 pt-4 border-t border-slate-800/80 text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-slate-800 border border-slate-700"></div>
            <span>Available</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-emerald-600 border border-emerald-400"></div>
            <span>Selected</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-red-950/50 border border-red-900"></div>
            <span>Booked (Click for Smart AI)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-amber-500/40 border border-amber-400"></div>
            <span>Recommended</span>
          </div>
        </div>
      </div>

      {/* Checkout Summary or Ticket Confirmation */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col justify-between">
          <div>
            <h4 className="text-base font-bold text-white mb-2 flex items-center gap-2">
              <CreditCard className="w-4 h-4 text-emerald-400" />
              Reservation Summary
            </h4>
            <div className="space-y-2 text-xs text-slate-300 mt-4">
              <div className="flex justify-between">
                <span className="text-slate-400">Selected Seats:</span>
                <span className="font-mono font-bold text-white">
                  {selectedSeats.length > 0 ? selectedSeats.map(s => s.seatIdentifier).join(', ') : 'None'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Quantity:</span>
                <span className="font-mono text-white">{selectedSeats.length} ticket(s)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Convenience Fee:</span>
                <span className="font-mono text-emerald-400">$0.00 (Waived)</span>
              </div>
              <div className="pt-2 border-t border-slate-800 flex justify-between text-sm font-bold">
                <span className="text-white">Total Amount:</span>
                <span className="text-emerald-400 font-mono">${totalPrice.toFixed(2)}</span>
              </div>
            </div>
          </div>

          <button
            onClick={completeBooking}
            disabled={selectedSeats.length === 0}
            className="mt-6 w-full py-2.5 rounded-lg bg-red-600 hover:bg-red-500 disabled:opacity-40 text-white font-bold text-xs uppercase tracking-wider transition flex items-center justify-center gap-2"
          >
            <Ticket className="w-4 h-4" /> Confirm &amp; Issue Cinema Pass
          </button>
        </div>

        {/* Digital Ticket Pass Card */}
        {confirmedBooking ? (
          <div className="p-6 rounded-xl bg-gradient-to-br from-slate-900 to-slate-950 border border-emerald-500/40 relative overflow-hidden">
            <div className="flex justify-between items-start mb-4">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-emerald-400 font-bold">
                  Verified Cinema Pass
                </span>
                <h4 className="text-base font-bold text-white">Interstellar: Beyond Time</h4>
                <p className="text-xs text-slate-400 font-mono">Ref: {confirmedBooking.bookingNumber}</p>
              </div>
              <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                <CheckCircle2 className="w-6 h-6" />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs font-mono text-slate-300 mb-4 p-3 bg-slate-950 rounded-lg border border-slate-800">
              <div>
                <span className="text-slate-500 text-[10px] block">SEATS</span>
                <span className="font-bold text-emerald-400">{confirmedBooking.seats.join(', ')}</span>
              </div>
              <div>
                <span className="text-slate-500 text-[10px] block">TOTAL PAID</span>
                <span className="font-bold text-white">${confirmedBooking.total.toFixed(2)}</span>
              </div>
              <div>
                <span className="text-slate-500 text-[10px] block">TIME</span>
                <span>Today, 7:30 PM</span>
              </div>
              <div>
                <span className="text-slate-500 text-[10px] block">STATUS</span>
                <span className="text-emerald-400">CONFIRMED</span>
              </div>
            </div>

            {/* Barcode Graphic */}
            <div className="p-2 bg-white rounded flex items-center justify-center space-x-1">
              {[4, 2, 6, 2, 8, 4, 3, 5, 2, 7, 4, 2, 5, 8, 3, 6, 2, 4, 7, 3, 5, 2, 6].map((h, i) => (
                <div
                  key={i}
                  style={{ height: `${h * 4}px`, width: i % 2 === 0 ? '2px' : '4px' }}
                  className="bg-black inline-block"
                ></div>
              ))}
            </div>
            <p className="text-center font-mono text-[9px] text-slate-400 mt-1">
              SCAN AT AUDITORIUM ENTRANCE
            </p>
          </div>
        ) : (
          <div className="p-6 rounded-xl bg-slate-900/40 border border-dashed border-slate-800 flex flex-col items-center justify-center text-center text-slate-500 text-xs">
            <Ticket className="w-10 h-10 mb-2 opacity-40 text-slate-400" />
            <p className="font-semibold text-slate-400">Digital Cinema Pass Preview</p>
            <p className="text-slate-500 mt-1 max-w-xs">
              Select seats and click &quot;Confirm &amp; Issue Cinema Pass&quot; to preview the generated ticket with barcode.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
