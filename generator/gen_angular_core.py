import os

BASE_DIR = "movie-ticket-booking-system"
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

def write_file(subpath, content):
    full_path = os.path.join(FRONTEND_DIR, subpath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {full_path}")

def generate_core():
    # 1. package.json
    write_file("package.json", """{
  "name": "movie-ticket-booking-frontend",
  "version": "1.0.0",
  "scripts": {
    "ng": "ng",
    "start": "ng serve --port 4200",
    "build": "ng build",
    "watch": "ng build --watch --configuration development",
    "test": "ng test"
  },
  "private": true,
  "dependencies": {
    "@angular/animations": "^17.3.0",
    "@angular/common": "^17.3.0",
    "@angular/compiler": "^17.3.0",
    "@angular/core": "^17.3.0",
    "@angular/forms": "^17.3.0",
    "@angular/platform-browser": "^17.3.0",
    "@angular/platform-browser-dynamic": "^17.3.0",
    "@angular/router": "^17.3.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.14.3"
  },
  "devDependencies": {
    "@angular-devkit/build-angular": "^17.3.0",
    "@angular/cli": "^17.3.0",
    "@angular/compiler-cli": "^17.3.0",
    "@types/jasmine": "~5.1.0",
    "jasmine-core": "~5.1.0",
    "karma": "~6.4.0",
    "karma-chrome-launcher": "~3.2.0",
    "karma-coverage": "~2.2.0",
    "karma-jasmine": "~5.1.0",
    "karma-jasmine-html-reporter": "~2.1.0",
    "typescript": "~5.4.2"
  }
}
""")

    # 2. angular.json
    write_file("angular.json", """{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {
    "movie-ticket-booking-frontend": {
      "projectType": "application",
      "schematics": {},
      "root": "",
      "sourceRoot": "src",
      "prefix": "app",
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:browser",
          "options": {
            "outputPath": "dist/movie-ticket-booking-frontend",
            "index": "src/index.html",
            "main": "src/main.ts",
            "polyfills": [
              "zone.js"
            ],
            "tsConfig": "tsconfig.app.json",
            "assets": [
              "src/favicon.ico",
              "src/assets"
            ],
            "styles": [
              "src/styles.css"
            ],
            "scripts": []
          },
          "configurations": {
            "production": {
              "budgets": [
                {
                  "type": "initial",
                  "maximumWarning": "1mb",
                  "maximumError": "2mb"
                },
                {
                  "type": "anyComponentStyle",
                  "maximumWarning": "4kb",
                  "maximumError": "8kb"
                }
              ],
              "outputHashing": "all"
            },
            "development": {
              "buildOptimizer": false,
              "optimization": false,
              "extractLicenses": false,
              "sourceMap": true
            }
          },
          "defaultConfiguration": "production"
        },
        "serve": {
          "builder": "@angular-devkit/build-angular:dev-server",
          "configurations": {
            "production": {
              "buildTarget": "movie-ticket-booking-frontend:build:production"
            },
            "development": {
              "buildTarget": "movie-ticket-booking-frontend:build:development"
            }
          },
          "defaultConfiguration": "development"
        }
      }
    }
  }
}
""")

    # 3. tsconfig.json & tsconfig.app.json
    write_file("tsconfig.json", """{
  "compileOnSave": false,
  "compilerOptions": {
    "baseUrl": "./",
    "outDir": "./dist/out-tsc",
    "forceConsistentCasingInFileNames": true,
    "strict": false,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "sourceMap": true,
    "declaration": false,
    "downlevelIteration": true,
    "experimentalDecorators": true,
    "moduleResolution": "node",
    "importHelpers": true,
    "target": "ES2022",
    "module": "ES2022",
    "useDefineForClassFields": false,
    "lib": [
      "ES2022",
      "dom"
    ]
  },
  "angularCompilerOptions": {
    "enableI18nLegacyMessageIdFormat": false,
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true,
    "strictTemplates": false
  }
}
""")

    write_file("tsconfig.app.json", """{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist/out-tsc/app",
    "types": []
  },
  "files": [
    "src/main.ts"
  ],
  "include": [
    "src/**/*.d.ts"
  ]
}
""")

    # 4. src/index.html
    write_file("src/index.html", """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>CinePass - Movie Ticket Booking System</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <!-- Google Fonts: Inter & Outfit -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <!-- FontAwesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
  <app-root></app-root>
</body>
</html>
""")

    # 5. src/main.ts
    write_file("src/main.ts", """import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));
""")

    # 6. src/styles.css (Global High-End Cinema Styling)
    write_file("src/styles.css", """/* ==========================================================================
   Global Styles - CinePass Movie Ticket Booking
   ========================================================================== */

:root {
  --primary: #e50914;
  --primary-hover: #b80710;
  --primary-glow: rgba(229, 9, 20, 0.4);
  --secondary: #1f2937;
  --bg-dark: #0f1016;
  --bg-card: #181a24;
  --bg-card-hover: #212433;
  --text-main: #f3f4f6;
  --text-muted: #9ca3af;
  --border-color: rgba(255, 255, 255, 0.08);
  --accent-gold: #f59e0b;
  --accent-cyan: #06b6d4;
  --accent-purple: #8b5cf6;
  --accent-green: #10b981;
  --accent-red: #ef4444;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --font-display: 'Outfit', sans-serif;
  --font-body: 'Inter', sans-serif;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-body);
  background-color: var(--bg-dark);
  color: var(--text-main);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display);
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.02em;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  outline: none;
  transition: all 0.2s ease-in-out;
}

/* Common Container */
.container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.7rem 1.4rem;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  text-align: center;
}

.btn-primary {
  background: var(--primary);
  color: #fff;
  box-shadow: 0 4px 14px var(--primary-glow);
}

.btn-primary:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--primary-glow);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.14);
  transform: translateY(-2px);
}

.btn-danger {
  background: var(--accent-red);
  color: #fff;
}

.btn-danger:hover {
  background: #dc2626;
  transform: translateY(-2px);
}

/* Glass Card */
.glass-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
}

/* Toast/Alerts */
.alert {
  padding: 1rem 1.25rem;
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.alert-danger {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #fca5a5;
}

.alert-success {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.4);
  color: #6ee7b7;
}

.alert-warning {
  background: rgba(245, 158, 11, 0.15);
  border: 1px solid rgba(245, 158, 11, 0.4);
  color: #fcd34d;
}

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-vip {
  background: rgba(245, 158, 11, 0.2);
  color: var(--accent-gold);
  border: 1px solid rgba(245, 158, 11, 0.4);
}

.badge-premium {
  background: rgba(139, 92, 246, 0.2);
  color: var(--accent-purple);
  border: 1px solid rgba(139, 92, 246, 0.4);
}

.badge-regular {
  background: rgba(6, 182, 212, 0.2);
  color: var(--accent-cyan);
  border: 1px solid rgba(6, 182, 212, 0.4);
}
""")

    # 7. src/environments
    write_file("src/environments/environment.ts", """export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api'
};
""")

    write_file("src/environments/environment.prod.ts", """export const environment = {
  production: true,
  apiUrl: 'http://localhost:8080/api'
};
""")

    # 8. Models
    write_file("src/app/models/user.model.ts", """export interface User {
  id: number;
  username: string;
  email: string;
  fullName: string;
  phone?: string;
  role: 'ROLE_ADMIN' | 'ROLE_CUSTOMER' | string;
  active: boolean;
}

export interface AuthResponse {
  token: string;
  type: string;
  id: number;
  username: string;
  email: string;
  fullName: string;
  role: string;
}
""")

    write_file("src/app/models/movie.model.ts", """export interface Movie {
  id: number;
  title: string;
  description: string;
  genre: string;
  durationMinutes: number;
  language: string;
  releaseDate: string;
  posterUrl: string;
  rating: number;
  active: boolean;
}
""")

    write_file("src/app/models/seat.model.ts", """export interface Seat {
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
""")

    write_file("src/app/models/theatre.model.ts", """export interface Theatre {
  id: number;
  name: string;
  address: string;
  city: string;
  state?: string;
  zipCode?: string;
  totalScreens: number;
  active: boolean;
}

export interface Screen {
  id: number;
  name: string;
  totalRows: number;
  totalColumns: number;
  theatreId: number;
  theatreName: string;
}
""")

    write_file("src/app/models/show.model.ts", """export interface Show {
  id: number;
  movieId: number;
  movieTitle: string;
  moviePosterUrl: string;
  screenId: number;
  screenName: string;
  theatreId: number;
  theatreName: string;
  theatreCity: string;
  startTime: string;
  endTime: string;
  basePrice: number;
  status: string;
}
""")

    write_file("src/app/models/booking.model.ts", """export interface BookingRequest {
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
""")

    write_file("src/app/models/api-response.model.ts", """export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  timestamp: string;
  recommendedSeat?: any;
}
""")

    # 9. Interceptors
    write_file("src/app/interceptors/jwt.interceptor.ts", """import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const token = this.authService.getToken();
    if (token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }
    return next.handle(request);
  }
}
""")

    # 10. Guards
    write_file("src/app/guards/auth.guard.ts", """import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (this.authService.isLoggedIn()) {
      return true;
    }
    this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
    return false;
  }
}
""")

    write_file("src/app/guards/admin.guard.ts", """import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (this.authService.isLoggedIn() && this.authService.isAdmin()) {
      return true;
    }
    this.router.navigate(['/']);
    return false;
  }
}
""")

if __name__ == "__main__":
    generate_core()
