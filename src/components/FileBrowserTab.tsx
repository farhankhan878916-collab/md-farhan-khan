import React, { useState } from 'react';
import { FileCode, Folder, Database, Layers, Check, Copy } from 'lucide-react';
import { FileItem } from '../types';

const SAMPLE_FILES: FileItem[] = [
  {
    name: 'BookingServiceImpl.java',
    path: 'backend/src/main/java/com/example/movieticketbooking/service/impl/BookingServiceImpl.java',
    type: 'java',
    category: 'Backend Java',
    content: `@Service
@Transactional
public class BookingServiceImpl implements BookingService {

    // Double-Booking Barrier: Serializable isolation level ensures concurrent transactions do not overlap
    @Override
    @Transactional(isolation = Isolation.SERIALIZABLE)
    public BookingResponse createBooking(Long userId, BookingRequest request) {
        Show show = showRepository.findById(request.getShowId())
            .orElseThrow(() -> new ResourceNotFoundException("Show not found"));

        // Atomic double booking check across database
        for (Long seatId : request.getSeatIds()) {
            boolean isBooked = bookingRepository.isSeatAlreadyBookedForShow(request.getShowId(), seatId);
            if (isBooked) {
                Seat seat = seatRepository.findById(seatId).orElse(null);
                String seatName = seat != null ? seat.getSeatIdentifier() : String.valueOf(seatId);
                logger.warn("Double booking prevented! Seat {} is already booked for show {}", seatName, show.getId());
                throw new EntityConflictException("Seat " + seatName + " is already booked for this show.");
            }
        }

        // Save Booking with unique booking reference number
        Booking booking = new Booking();
        booking.setBookingNumber("BK-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 6).toUpperCase());
        booking.setUser(user);
        booking.setShow(show);
        booking.setStatus(BookingStatus.CONFIRMED);
        booking = bookingRepository.save(booking);

        // Link seats & save payment record
        // ...
        return mapToResponse(booking);
    }
}`
  },
  {
    name: 'SeatRecommendationServiceImpl.java',
    path: 'backend/src/main/java/com/example/movieticketbooking/service/impl/SeatRecommendationServiceImpl.java',
    type: 'java',
    category: 'Backend Java',
    content: `@Service
public class SeatRecommendationServiceImpl implements SeatRecommendationService {

    @Override
    public SeatResponse recommendNearestVacantSeat(Long showId, Long bookedSeatId) {
        Seat targetSeat = seatRepository.findById(bookedSeatId)
            .orElseThrow(() -> new ResourceNotFoundException("Target seat not found"));

        List<Seat> allSeats = seatRepository.findByScreenIdOrderByRowNameAscSeatNumberAsc(screen.getId());
        List<Long> bookedSeatIds = bookingRepository.findBookedSeatIdsByShowId(showId);
        Set<Long> bookedSet = new HashSet<>(bookedSeatIds);

        Seat bestMatch = null;
        double minDistance = Double.MAX_VALUE;

        int targetRowIdx = rowLetterToNumber(targetSeat.getRowName());
        int targetColIdx = targetSeat.getSeatNumber();

        for (Seat candidate : allSeats) {
            if (bookedSet.contains(candidate.getId())) continue;

            int candRowIdx = rowLetterToNumber(candidate.getRowName());
            int candColIdx = candidate.getSeatNumber();

            // Row distance is weighted slightly higher (1.5x) to prefer adjacent seats in same row
            double rowDiff = (candRowIdx - targetRowIdx) * 1.5;
            double colDiff = (candColIdx - targetColIdx);
            double distance = Math.sqrt(rowDiff * rowDiff + colDiff * colDiff);

            if (distance < minDistance) {
                minDistance = distance;
                bestMatch = candidate;
            }
        }

        return mapToResponse(bestMatch, SeatStatus.AVAILABLE);
    }
}`
  },
  {
    name: 'BookingServiceConcurrencyTest.java',
    path: 'backend/src/test/java/com/example/movieticketbooking/service/BookingServiceConcurrencyTest.java',
    type: 'java',
    category: 'Backend Java',
    content: `@SpringBootTest
@ActiveProfiles("h2")
public class BookingServiceConcurrencyTest {

    @Test
    @DisplayName("Verify concurrent booking attempts on the same seat: exactly 1 succeeds, 1 fails with 409")
    void testConcurrentBookingSameSeat() throws Exception {
        int threads = 2;
        ExecutorService executor = Executors.newFixedThreadPool(threads);
        CountDownLatch latch = new CountDownLatch(1);
        AtomicInteger successCount = new AtomicInteger(0);
        AtomicInteger conflictCount = new AtomicInteger(0);

        for (int i = 0; i < threads; i++) {
            executor.submit(() -> {
                try {
                    latch.await();
                    bookingService.createBooking(userId, request);
                    successCount.incrementAndGet();
                } catch (EntityConflictException ex) {
                    conflictCount.incrementAndGet();
                }
            });
        }

        latch.countDown();
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);

        assertEquals(1, successCount.get(), "Only one concurrent booking should succeed");
        assertEquals(1, conflictCount.get(), "The other concurrent request must encounter EntityConflictException");
    }
}`
  },
  {
    name: 'seat-selection.component.ts',
    path: 'frontend/src/app/components/seat-selection/seat-selection.component.ts',
    type: 'ts',
    category: 'Frontend Angular',
    content: `@Component({
  selector: 'app-seat-selection',
  templateUrl: './seat-selection.component.html',
  styleUrls: ['./seat-selection.component.css']
})
export class SeatSelectionComponent implements OnInit {
  show: Show | null = null;
  seats: Seat[] = [];
  selectedSeats: Seat[] = [];
  recommendedSeat: Seat | null = null;
  recommendationMessage: string | null = null;

  onSeatClick(seat: Seat): void {
    if (seat.status === SeatStatus.BOOKED) {
      // Query Spring Boot recommendation API
      this.seatService.recommendNearestVacantSeat(this.show.id, seat.id).subscribe({
        next: res => {
          if (res.data) {
            this.recommendedSeat = res.data;
            this.recommendationMessage = \`Seat \${seat.seatIdentifier} is booked! Nearest vacant seat is \${res.data.seatIdentifier} (\${res.data.seatType}, $\${res.data.price})\`;
          }
        }
      });
      return;
    }

    this.toggleSeat(seat);
  }
}`
  },
  {
    name: 'schema.sql',
    path: 'database/schema.sql',
    type: 'sql',
    category: 'Database',
    content: `-- Movie Ticket Booking System - Relational Schema DDL
CREATE DATABASE IF NOT EXISTS movie_booking;
USE movie_booking;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    role VARCHAR(20) NOT NULL DEFAULT 'ROLE_CUSTOMER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Composite unique constraint to guarantee zero double bookings
CREATE TABLE IF NOT EXISTS booking_seats (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    booking_id BIGINT NOT NULL,
    seat_id BIGINT NOT NULL,
    price_at_booking DECIMAL(8, 2) NOT NULL,
    CONSTRAINT uk_booking_seat_unique UNIQUE (booking_id, seat_id),
    CONSTRAINT fk_bs_booking FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    CONSTRAINT fk_bs_seat FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE RESTRICT
);`
  }
];

export const FileBrowserTab: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<FileItem>(SAMPLE_FILES[0]);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(selectedFile.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* File Sidebar */}
      <div className="space-y-4">
        <div className="p-4 rounded-xl bg-slate-900/75 backdrop-blur-md border border-slate-700/60 shadow-lg">
          <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
            <Folder className="w-4 h-4 text-amber-400" /> Source Files ({SAMPLE_FILES.length} Highlighted)
          </h4>
          <div className="space-y-1">
            {SAMPLE_FILES.map(file => (
              <button
                key={file.path}
                onClick={() => setSelectedFile(file)}
                className={`w-full text-left p-2.5 rounded-lg text-xs font-mono transition flex items-center justify-between ${
                  selectedFile.path === file.path
                    ? 'bg-red-600/10 text-red-400 border border-red-500/30 font-semibold'
                    : 'text-slate-400 hover:bg-slate-800/60 hover:text-white'
                }`}
              >
                <div className="flex items-center gap-2 truncate">
                  <FileCode className="w-4 h-4 shrink-0 opacity-70" />
                  <span className="truncate">{file.name}</span>
                </div>
                <span className="text-[10px] text-slate-400 px-1.5 py-0.5 rounded bg-slate-800 shrink-0">
                  {file.category.split(' ')[0]}
                </span>
              </button>
            ))}
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400">
          <p className="font-semibold text-white mb-1">Total Project Files: 156</p>
          <p className="leading-relaxed">
            Every controller, service, repository, entity, DTO, Angular component, module, guard, and SQL migration is packaged in the ZIP file.
          </p>
        </div>
      </div>

      {/* File Preview */}
      <div className="lg:col-span-2 rounded-xl bg-slate-950/80 backdrop-blur-md border border-slate-700/60 shadow-xl flex flex-col overflow-hidden">
        <div className="p-3 bg-slate-900/80 border-b border-slate-800 flex items-center justify-between gap-4">
          <span className="font-mono text-xs text-slate-300 truncate">{selectedFile.path}</span>
          <button
            onClick={handleCopy}
            className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 hover:text-white text-xs font-mono flex items-center gap-1.5 transition"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
        </div>

        <pre className="p-4 font-mono text-xs text-slate-300 overflow-x-auto leading-relaxed max-h-[500px]">
          <code>{selectedFile.content}</code>
        </pre>
      </div>
    </div>
  );
};
