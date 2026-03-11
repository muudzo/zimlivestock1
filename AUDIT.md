# ZimLivestock Codebase Audit

## Project Overview
**Zimbabwe's Premier Livestock Marketplace** — a full-stack web app for buying, selling, and auctioning livestock with Paynow payment integration.

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| Backend | Flask (Python) with Blueprints |
| Database | Supabase (PostgreSQL + Auth) |
| Payments | Paynow (web + mobile/EcoCash) |
| State | Zustand (client) + React Query (server) |
| UI Library | Radix UI / shadcn/ui (51 components) |

**Size:** ~675 lines backend (7 files) + ~68 frontend source files | 12 API endpoints | PWA-ready

---

## Critical Issues (fix before production)

### 1. `requirements.txt` is broken
- Still lists FastAPI/SQLModel/uvicorn from the old architecture
- **Missing:** `flask`, `flask-cors`, `supabase` — the app won't install from this file

### 2. Debug mode hardcoded ON
- `app.py:53`: `app.run(debug=True)` exposes stack traces and Werkzeug debugger in production

### 3. Hardcoded API URL in frontend
- `frontend/src/services/api.ts:4`: `http://localhost:8000` — needs an environment variable for deployment

### 4. CORS allows all origins
- `app.py:11`: `CORS(app)` with no restrictions

### 5. Payment status endpoint is unauthenticated
- `GET /payments/status/<reference>` — anyone can check any payment status, and references are guessable (`ZL-{id}-{hex}`)

---

## High Priority Issues

### 6. Supabase client initialized 5 separate times
Duplicated in `app.py`, `routes/auth.py`, `routes/listings.py`, `routes/bids.py`, `routes/payments.py`. Should be centralized in a shared module.

### 7. Bare `except:` blocks (7 instances)
In `routes/bids.py`, `routes/listings.py`, `routes/payments.py` — silently swallows errors, making debugging impossible.

### 8. Low auth coverage
Only **4 of 12 endpoints** (33%) require authentication. Public endpoints expose listing and payment data without access control.

### 9. No frontend tests
Vitest is installed but **zero test files exist**. No unit, integration, or E2E tests.

### 10. Dead code: `seed.py`
Imports `User` and `LivestockItem` from old SQLModel models that no longer exist. Cannot run.

---

## Medium Priority Issues

| Issue | Details |
|-------|---------|
| **Outdated README** | Still references FastAPI/SQLModel; should reflect Flask/Supabase |
| **No input validation** | No length/type/range checks on listing fields (title, price, etc.) |
| **Internal error leakage** | `str(e)` returned directly to clients in error responses |
| **Mock data in production code** | `HomeFeed.tsx` and `useLivestock.ts` contain hardcoded mock data |
| **Unused frontend deps** | Recharts, vaul, cmdk, react-day-picker installed but likely unused |
| **No Docker/CI/CD** | No containerization or deployment pipeline |
| **No logging config** | Uses Flask defaults — no structured logging |
| **Token handling** | No refresh token mechanism or expiration handling |

---

## What's Working Well

- **Clean blueprint architecture** — routes are well-organized by domain (auth, listings, bids, payments)
- **Paynow integration is solid** — supports both web and mobile payments with webhook verification (SHA512)
- **Modern frontend stack** — React 18 + Vite + TypeScript with good DX
- **PWA configured** — manifest, icons, share target all set up
- **Zustand with persist** — lightweight and effective state management
- **shadcn/ui component library** — comprehensive, accessible UI primitives
- **Dark mode support** — CSS variables with class-based toggle

---

## API Endpoints

### Authentication (`/auth`)
| Method | Endpoint | Auth Required |
|--------|----------|:---:|
| POST | `/auth/register` | No |
| POST | `/auth/login` | No |
| GET | `/auth/me` | Yes |

### Livestock Listings (`/livestock`)
| Method | Endpoint | Auth Required |
|--------|----------|:---:|
| GET | `/livestock` | No |
| GET | `/livestock/<id>` | No |
| POST | `/livestock` | Yes |

### Bidding (`/bids`)
| Method | Endpoint | Auth Required |
|--------|----------|:---:|
| GET | `/bids/livestock/<id>` | No |
| POST | `/bids` | Yes |

### Payments (`/payments`)
| Method | Endpoint | Auth Required |
|--------|----------|:---:|
| POST | `/payments/initiate` | Yes |
| POST | `/payments/webhook` | No (Paynow callback) |
| GET | `/payments/status/<ref>` | No |
| GET | `/payments/history` | Yes |

### System
| Method | Endpoint | Auth Required |
|--------|----------|:---:|
| GET | `/` | No |
| GET | `/health` | No |

---

## Recommended Priority Order

1. Fix `requirements.txt` (add Flask, flask-cors, supabase; remove FastAPI deps)
2. Centralize Supabase client into a shared module
3. Make API URL configurable via env variable
4. Add proper error handling (replace bare `except:` blocks)
5. Secure debug mode and CORS for production
6. Add auth to payment status endpoint
7. Add input validation on backend
8. Clean up dead code (seed.py, mock data)
9. Add frontend tests
10. Update documentation
