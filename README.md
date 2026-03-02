# ZimLivestock API 🐄

> **Zimbabwe's Premier Livestock Marketplace** — A RESTful backend for online livestock auctions, enabling farmers and buyers across Zimbabwe to connect, list animals, and bid in real-time.

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Supported Livestock Categories](#supported-livestock-categories)
- [Business Logic](#business-logic)
- [Roadmap / Known Limitations](#roadmap--known-limitations)

---

## Overview

ZimLivestock is a **FastAPI**-powered backend that serves as the engine for a livestock auctioning platform built for the Zimbabwean market. It supports:

- **User registration & login** with password hashing
- **Livestock listings** — create, browse, filter by category, and delete
- **Bidding system** — place bids that enforce minimum increments and update the current bid in real time
- **Auction time tracking** — helpers to compute time-left, detect ending-soon windows, and flag concluded auctions
- **Phone number validation** specific to Zimbabwean number formats (`+263` or `07x` prefixes)

The backend was converted from a TypeScript/React frontend codebase (see comments in `utils/common.py` and `types/index.py`) and is structured as an MVP with planned production hardening.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| ORM / Models | [SQLModel](https://sqlmodel.tiangolo.com/) (Pydantic + SQLAlchemy) |
| Database | SQLite (`database.db`) |
| Auth | JWT tokens (placeholder `python-jose`), `passlib[bcrypt]` for hashing |
| Validation | Pydantic v2 |
| HTTP Client | `httpx` (for outbound requests, e.g. external payment APIs) |
| Server | Uvicorn (ASGI) |

---

## Project Structure

```
zimlivestock1/
├── app/
│   ├── main.py            # FastAPI app factory, CORS, router registration
│   ├── database.py        # SQLite engine, session dependency
│   ├── models.py          # SQLModel ORM models (User, LivestockItem, Bid)
│   ├── api/
│   │   ├── auth.py        # /auth — register, login
│   │   ├── listings.py    # /livestock — CRUD for livestock listings
│   │   └── bids.py        # /bids — place & retrieve bids
│   ├── types/
│   │   └── index.py       # Python TypedDicts mirroring frontend TS types
│   └── utils/
│       └── common.py      # Utility functions (currency, date, validation, auction logic)
├── requirements.txt
└── README.md
```

---

## Data Models

### User
| Field | Type | Notes |
|---|---|---|
| `id` | int (PK) | Auto-generated |
| `firstName` | str | |
| `lastName` | str | |
| `email` | str | Unique, indexed |
| `phone` | str | Zimbabwean format |
| `avatar` | str (optional) | URL |
| `location` | str (optional) | |
| `verified` | bool | Default: `False` |
| `password_hash` | str | bcrypt hashed |
| `created_at` | datetime | |
| `updated_at` | datetime | |

### LivestockItem
| Field | Type | Notes |
|---|---|---|
| `id` | int (PK) | Auto-generated |
| `title` | str | e.g. "Prime Brahman Bull" |
| `breed` | str | |
| `age` | str | |
| `weight` | str | |
| `location` | str | |
| `startingPrice` | float | USD |
| `currentBid` | float | Default: 0.0 |
| `category` | str | See categories below |
| `description` | str (optional) | |
| `imageUrl` | str | |
| `auctionEndDate` | datetime | |
| `healthStatus` | str | `verified` / `pending` / `unverified` |
| `seller_id` | int (FK) | References `User` |

### Bid
| Field | Type | Notes |
|---|---|---|
| `id` | int (PK) | Auto-generated |
| `amount` | float | USD |
| `timestamp` | datetime | |
| `isWinning` | bool | Default: `False` |
| `bidder_id` | int (FK) | References `User` |
| `livestock_id` | int (FK) | References `LivestockItem` |

---

## API Endpoints

### Auth — `/auth`
| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login with email + password, returns JWT token |

### Livestock Listings — `/livestock`
| Method | Path | Description |
|---|---|---|
| `GET` | `/livestock/` | List all livestock (pagination: `offset`, `limit`; filter: `category`) |
| `POST` | `/livestock/` | Create a new livestock listing |
| `GET` | `/livestock/{item_id}` | Get a single listing by ID |
| `DELETE` | `/livestock/{item_id}` | Delete a listing |

### Bids — `/bids`
| Method | Path | Description |
|---|---|---|
| `GET` | `/bids/livestock/{item_id}` | Get all bids for a listing, sorted by amount descending |
| `POST` | `/bids/` | Place a bid on a listing |

### System
| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Health check |

**Interactive Docs**: When running locally, visit `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc`.

---

## Getting Started

### Prerequisites
- Python 3.10+
- `pip`

### Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd zimlivestock1

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be live at `http://localhost:8000`.

### Quick Test

```bash
# Register a user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"firstName":"John","lastName":"Moyo","email":"john@example.com","phone":"+263771234567","password":"secret123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"contact":"john@example.com","password":"secret123"}'
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| Database | `database.db` (SQLite) | File-based, auto-created on first run |
| CORS Origins | `localhost:3000`, `localhost:8000` | Update in `main.py` for production |
| JWT Secret | Placeholder | Replace with `python-jose` + secret key for production |

---

## Supported Livestock Categories

| Category | Icon |
|---|---|
| `cattle` | 🐄 |
| `goats` | 🐐 |
| `sheep` | 🐑 |
| `pigs` | 🐷 |
| `chickens` | 🐔 |
| `horses` | 🐎 |
| `donkeys` | 🦙 |

---

## Business Logic

### Bid Increment Rules (`utils/common.py`)
The minimum bid increment is dynamically calculated based on the current bid:

| Current Bid | Minimum Increment |
|---|---|
| < $100 | $10 |
| $100 – $499 | $25 |
| $500 – $999 | $50 |
| $1,000 – $4,999 | $100 |
| ≥ $5,000 | 5% of current bid |

### Phone Validation
Accepts Zimbabwean mobile numbers only:
- Format: `+2637[7-8]XXXXXXX` or `07[7-8]XXXXXXX`

### Auction State Helpers
- `isAuctionEnding(endDate, hours=24)` — returns `True` if auction closes within the given hours
- `isAuctionEnded(endDate)` — returns `True` if auction end date has passed
- `formatTimeLeft(endDate)` — returns human-readable countdown (e.g. `"2d 4h"`, `"45m"`, `"Ended"`)

---

## Roadmap / Known Limitations

| Item | Status | Notes |
|---|---|---|
| Password hashing | ⚠️ Placeholder | Replace mock hash with `passlib[bcrypt]` |
| JWT tokens | ⚠️ Placeholder | Implement proper `python-jose` JWTs with secret key |
| Database | ⚠️ MVP | Migrate SQLite → PostgreSQL for production |
| Payments | 🔲 Planned | Paynow integration (see `PAYNOW_INTEGRATION.md`) |
| WebSockets | 🔲 Planned | Real-time bid updates |
| File uploads | 🔲 Planned | Animal image uploads to S3/Supabase Storage |
| Notifications | 🔲 Planned | SMS/email alerts for outbid, auction won |
| Seller ratings | 🔲 Planned | Review and rating system |
| Health verification | 🔲 Planned | Vet certificate upload and approval workflow |

---

## Attributions

See [Attributions.md](./Attributions.md) for third-party library credits.

---

*Built for Zimbabwe's farming community 🇿🇼*
