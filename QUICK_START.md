# ZimLivestock - Quick Start Guide

## ✅ Current Status

### Running Services
- ✅ **Backend API** - Running on `http://localhost:8000`
  - FastAPI server with database
  - All endpoints ready (auth, payments, livestock, bids)
  
- ✅ **Frontend App** - Running on `http://localhost:3000`
  - React + Vite development server
  - Live reload enabled

- ✅ **Manifest.json** - Created and valid
  - PWA configuration ready

---

## 🚀 How to Run the Application

### Terminal 1: Start the Backend
```bash
cd /Users/michaelnyemudzo/Desktop/zimlivestock1
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```   

**Output should show:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
```

### Terminal 2: Start the Frontend
```bash
cd /Users/michaelnyemudzo/Desktop/zimlivestock1/frontend
npm run dev
```

**Output should show:**
```
VITE v5.4.21  ready in XXX ms
➜  Local:   http://localhost:3000/
```

---

## 🌐 Access the Application

1. **Open your browser** and go to: `http://localhost:3000`
2. **You should see** the ZimLivestock login/signup page
3. **Sign up** with test credentials:
   - First Name: `Test`
   - Last Name: `User`
   - Email: `test@example.com`
   - Phone: `0771234567`
   - Password: `TestPassword123`

   > ⚠️ You must register before you can log in. Any attempt to log in with an unregistered email/phone or wrong password will result in a 401 Unauthorized error.

4. **After signing up**, you'll be logged in and see the home feed

5. When you click an item to view it, the bidding screen will appear. A **Pay Now** button is shown at the bottom (next to the bid input) for logged‑in users – use it to start a payment for the selected item.

---

## 🔍 Troubleshooting

### Issue: "ERR_CONNECTION_REFUSED" on login
**Solution:** Make sure the backend is running on port 8000
```bash
# Check if backend is running
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

### Issue: 401 "Unauthorized" when attempting to log in
This means the server received your credentials but could not verify them. The most common causes are:
- You haven't registered a user yet (use the signup form first)
- You mistyped the email/phone or password

Register via the UI or call `POST /auth/register` before logging in, then retry.

### Warning: "Error while trying to use the following icon from the Manifest" or similar
This occurs when the manifest lists icons that don't exist in `frontend/public`. The repo now includes placeholder PNGs of the required sizes so the warning should disappear after you restart the dev server. If you ever change `manifest.json`, be sure the referenced files are present.

### Issue: "Manifest: Line: 1, column: 1, Syntax error"
**Solution:** Hard refresh your browser
```
Mac: Cmd + Shift + R
Windows/Linux: Ctrl + Shift + R
```

### Issue: "Cannot find module 'xyz'" in frontend
**Solution:** Install dependencies
```bash
cd frontend
npm install
npm run dev
```

### Issue: Backend won't start
**Solution:** Check if port 8000 is in use
```bash
# Kill any process using port 8000
lsof -ti:8000 | xargs kill -9

# Then try again
python -m uvicorn app.main:app --reload --port 8000
```

---

## 📝 API Endpoints

### Authentication
- `POST /auth/register` - Create new user account
- `POST /auth/login` - Log in with email/phone + password

### Livestock
- `GET /livestock` - List all livestock items
- `GET /livestock/{id}` - Get specific livestock item

### Payments
- `POST /payments/initiate` - Start a payment process
- `GET /payments/status/{reference}` - Check payment status
- `POST /payments/webhook` - PayNow webhook (auto-handled)

### Health Check
- `GET /health` - Verify backend is running

---

## 📊 Database

The application uses SQLite for development:
```
database.db (auto-created on startup)
```

**Tables:**
- `user` - User accounts
- `livestockitem` - Livestock listings
- `bid` - Auction bids
- `payment` - Payment transactions

---

## 🔐 PayNow Integration

### Test Credentials (in `.env`)
```
PAYNOW_INTEGRATION_ID=23629
PAYNOW_INTEGRATION_KEY=0ac007f7-e809-424d-9d25-433d27335488
```

These are demo credentials and will return "Invalid Hash" errors, which is expected.

### For Real Payments
1. Get real credentials from: https://www.paynow.co.zw/merchant/management
2. Update `.env` with real credentials
3. Update `PAYNOW_RESULT_URL` for webhook

---

## 📦 Project Structure

```
zimlivestock1/
├── app/                    # Backend (FastAPI)
│   ├── api/               # API routes
│   ├── models.py          # Database models
│   ├── database.py        # Database setup
│   ├── services/          # PayNow integration
│   └── tests/             # Unit tests
├── frontend/              # Frontend (React + Vite)
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── stores/        # Zustand stores
│   │   ├── services/      # API client
│   │   └── types.ts       # TypeScript types
│   └── public/
│       └── manifest.json  # PWA manifest
└── database.db            # SQLite database (auto-created)
```

---

## 🧪 Running Tests

```bash
# All tests
python -m pytest app/tests/test_auth_and_payments.py -v

# Specific test
python -m pytest app/tests/test_auth_and_payments.py::test_register_and_login -v

# Results should show: 3 passed ✓
```

---

## ⚡ Key Features Working

✅ User signup and login
✅ JWT token generation (fake for now)
✅ Livestock listings browse
✅ Auction bidding system
✅ PayNow payment integration
✅ Payment status tracking
✅ Mobile-responsive UI
✅ PWA support

---

## 🎯 Common Tasks

### View API Documentation
```
http://localhost:8000/docs (Swagger UI)
http://localhost:8000/redoc (ReDoc)
```

### Clear Database
```bash
rm database.db
# Database will be recreated on next backend start
```

### Check Backend Health
```bash
curl http://localhost:8000/health
```

### View Logs
- **Backend logs** - Visible in terminal running uvicorn
- **Frontend logs** - Visible in browser console (F12)

---

## 🆘 Need Help?

1. **Check terminal output** - Look for error messages
2. **Check browser console** - F12 → Console tab
3. **Check browser network tab** - F12 → Network tab
4. **Verify both servers running** - Check both terminal windows

**Both services must be running for the app to work!**

---

**Status: ✅ READY TO USE**

Backend: http://localhost:8000
Frontend: http://localhost:3000
