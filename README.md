# HappyMiles Tours 🎒✨
> **Tagline:** Turning Miles into Memories!  
> **Motto:** Travel More, Worry Less.  
> **Base:** Shivanagar, Alwyn Colony, Kukatpally, Hyderabad 500072  
> **Phones / WhatsApp:** 8074016910, 9381936910 (WhatsApp: +91 8074016910)  
> **Email:** happymilestravelss@gmail.com  
> **Instagram:** [@happymilestours_](https://instagram.com/happymilestours_)  
> **Google Reviews:** [https://share.google/soEV05LLv3ZGWSFKF](https://share.google/soEV05LLv3ZGWSFKF)

---

## 1. Project Architecture

This is a complete, premium, cinematic, mobile-first full-stack website built with a **FastAPI** backend and an animated, responsive frontend.

```
Bharath/
├── app/
│   ├── database.py       # SQLite engine, session & connection pooling
│   ├── models.py         # SQLAlchemy models for Packages & Bookings
│   ├── schemas.py        # Pydantic v2 schemas for request validation & response
│   └── seed_data.py      # Pre-seeds the 6 authentic tour packages
├── data/
│   └── happymiles.db     # SQLite database
├── static/
│   ├── css/
│   │   ├── style.css     # Premium design system (teal, sunset orange, soft sand)
│   │   └── admin.css     # Clean admin portal styling
│   ├── js/
│   │   ├── main.js       # Preloader, Ken Burns slider, lightbox, FAQ, cursor follower
│   │   ├── booking.js    # Multi-step booking sheet, live price roll, Kotak QR & WhatsApp
│   │   └── admin.js      # Admin dashboard, status updater, CSV export, package manager
│   ├── images/
│   │   ├── logo/         # SVG brand marks & vectors
│   │   ├── payment/      # Kotak UPI QR code (WebP + fallback)
│   │   ├── happy-customers/ # Converted & optimized WebP group traveler photos
│   │   └── places/       # Converted destination posters & scenic cuts
│   ├── index.html        # Main landing page with all 10 sections
│   ├── packages.html     # Catalog page with filter tabs
│   ├── package-detail.html # Rich itinerary, highlights, and sticky booking card
│   ├── about.html        # Story, motto, values & trust promise
│   ├── contact.html      # Office address, Google Maps embed, WhatsApp form
│   ├── terms.html        # Terms & Conditions
│   ├── privacy.html      # Privacy Policy
│   ├── refund.html       # Transparent Refund & Cancellation policy
│   ├── 404.html          # Polite travel-themed 404 page
│   └── admin.html        # Password-protected admin dashboard
├── .env.example          # Environment variables template
├── main.py               # FastAPI entrypoint, routes, basic auth & static mounting
├── requirements.txt      # Python dependencies
└── README.md             # This document
```

---

## 2. Image Processing & Section Mapping

All original photos were inspected, metadata (EXIF/GPS) stripped for traveler privacy, converted into responsive WebP formats (Hero, 900w Card, 400w Thumbnail, and 20px blurred placeholders):

| Image Name | Processed WebP Path | Section Used | Description / Alt Text |
| :--- | :--- | :--- | :--- |
| **HC1.jpeg** | `static/images/happy-customers/coorg-bylakuppe-monastery.webp` | Happy Customers (`coorg`) & Coorg Detail | Group selfie with monk at Namdroling Golden Temple, Bylakuppe |
| **HC2.jpeg** | `static/images/happy-customers/chikmagalur-coffee-trail-trek.webp` | Happy Customers (`chikmagalur`) & Chikmagalur Detail | Group trekking along misty coffee plantation trail |
| **HC3.jpeg** | `static/images/happy-customers/coorg-viewpoint-rockfall.webp` | Happy Customers (`coorg`) | HappyMiles travelers at scenic waterfall viewpoint in Coorg |
| **HC4.jpeg** | `static/images/happy-customers/maddur-highway-journey-stop.webp` | Happy Customers (`all`) | Refreshing highway breakfast stop at Maddur Tiffany's |
| **HC5.jpeg** | `static/images/happy-customers/travelers-welcome-departure.webp` | Happy Customers (`all`) | Cheerful group selfie at departure pickup spot |
| **COORG & CHIKMAGALUR.jpeg** | `static/images/places/coorg-chikmagalur/coorg-chikmagalur-poster.webp` | Hero, Packages, Detail | 3D/2N Coorg & Chikmagalur Coffee Hills package poster |
| **ARAKU VALLEY...jpeg** | `static/images/places/araku-vanjangi-lambasingi/araku-vanjangi-poster.webp` | Packages, Gallery, Detail | 4D/3N Araku Valley & Vanjangi Sea of Clouds package poster |
| **GOKARNA...jpeg** | `static/images/places/gokarna-dandeli-murudeshwar/gokarna-dandeli-poster.webp` | Packages, Gallery, Detail | 3D/2N Gokarna, Dandeli Rafting & Murudeshwar package poster |
| **KERELA.jpeg** | `static/images/places/kerala/kerala-poster.webp` | Packages, Gallery, Detail | 5D/4N Kerala Alleppey, Thekkady & Munnar package poster |
| **OOTY & COONOOR.jpeg** | `static/images/places/ooty-coonoor/ooty-coonoor-poster.webp` | Packages, Detail | 3D/2N Ooty & Coonoor Backpacking with Free Toy Train |
| **SHIMLA & MANALI.jpeg** | `static/images/places/shimla-manali/shimla-manali-poster.webp` | Packages, Gallery, Detail | 6D/5N Shimla, Manali, Kasol & Manikaran package poster |
| **Payment Scanner.jpeg** | `static/images/payment/kotak-upi-qr.webp` | Booking Modal Payment Sheet | Miryala Bharath Kotak 811 UPI QR Code |

---

## 3. Manual Payment Verification Flow

1. Customer browses packages and clicks **Book Seat**.
2. Form calculates prices on server:
   - Full Payment or 30% Advance deposit.
3. Animated payment sheet reveals:
   - Official **Kotak 811 UPI QR Code**.
   - **Tap to Pay via UPI App** deep link (`upi://pay?pa=7661981338@kotakbank&pn=HappyMiles%20Tours&am=...`).
   - One-click copy buttons for:
     - **UPI ID:** `7661981338@kotakbank`
     - **Bank:** `Kotak Mahindra Bank`
     - **A/c No.:** `2248401328`
     - **IFSC:** `KKBK0007475`
     - **Branch:** `KPHB (Pratiba Vidyaniketan), Hyderabad`
4. Customer transfers and enters their **12-digit UTR Reference**.
5. Booking status transitions to `payment_submitted`.
6. Summary opens in WhatsApp directly to `+91 8074016910` with formatted booking reference.
7. Admin verifies the UTR in the Kotak Bank app and marks the status as `paid` or `confirmed` in `/admin`.

### 3.1 Google Forms Integration (Dual Booking & Enquiry Flow)

To offer maximum accessibility for travelers and corporate/group planners, the application integrates two official Google Forms alongside the custom SQLite/FastAPI engine:
- **Enquiry Google Form:** `https://forms.gle/8dFCPRhFAX5Rzg3W7` (Linked across Navbar, Hero, Catalog banner, Package details, Contact page, and Footer)
- **Bookings Google Form:** `https://forms.gle/r97LBQdCx39JAZfQ6` (Accessible in the Booking Modal banner, Package Details sticky booking card, Catalog header, and Footer)

Both URLs are centralized and dynamically fetched from `/api/config` (`ENQUIRY_FORM_URL`, `BOOKING_FORM_URL` in `.env`), ensuring zero hardcoding across the frontend.

### 3.2 Official Government Registrations & Compliance

HappyMiles Tours is officially registered and licensed with both Central and State government authorities:
1. **MSME Udyam Registration (Govt. of India):** `UDYAM-TS-20-0227292` (Micro enterprise — Services, NIC 79120: Tour operator activities)
   - Route: `/certificates/udyam` (Serves official PDF)
2. **Telangana Shops & Establishments Act, 1988 (Labour Dept., Govt. of Telangana):** `SEA/MED/ALO/QB/1440094/2026` (Travel Agency for booking operations)
   - Route: `/certificates/telangana-establishment` (Serves official PDF)
3. Dedicated showcase section on `/about#registrations` and verification badges on `/contact`.

---

## 4. Beginner-Friendly Deployment Guide

### Step 1: Run Locally on Your Computer
1. Open PowerShell / Terminal in this project folder:
   ```bash
   cd "C:\Users\AKSHARA\OneDrive\Desktop\Bharath"
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
5. Open your browser:
   - Public Website: `http://localhost:8000/`
   - Admin Portal: `http://localhost:8000/admin` (Default: `admin` / `happymiles2026`)
   - Interactive API Docs: `http://localhost:8000/docs`

---

### Step 2: Deploy to Render (Cloud Hosting with Persistent DB)
1. Push this project folder to your GitHub account (as a private or public repository).
2. Go to [render.com](https://render.com) and create a free account.
3. Click **New +** > **Web Service** > Connect your GitHub repository.
4. Set the following settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt && python -m app.seed_data`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Under **Environment Variables**, add:
   - `ADMIN_USER` = `admin`
   - `ADMIN_PASS` = `[Choose a strong password]`
   - `UPI_ID` = `7661981338@kotakbank`
   - `WA_NUMBER` = `918074016910`
   - `ADVANCE_PCT` = `30`
   - `DB_PATH` = `data/happymiles.db`
6. Click **Create Web Service**. Your site will be live on `https://your-app-name.onrender.com`!

---

### Step 3: Deploy Frontend Free on Netlify or GitHub Pages (Optional)
If you prefer hosting the HTML frontend separately:
- Simply drag-and-drop the `static` folder into [Netlify Drop](https://app.netlify.com/drop).
- Update the API fetch calls in `main.js` and `booking.js` to point to your live Render backend URL.

---

### Step 4: Custom Domain & Free HTTPS
1. Purchase your domain (e.g. `happymilestours.com` or `happymiles.in`) on GoDaddy, Namecheap, or Hostinger.
2. In your Render / Netlify dashboard, click **Custom Domains** and enter `happymilestours.com`.
3. Add the provided `CNAME` and `A` records to your domain DNS settings.
4. Render / Netlify automatically provisions free Let's Encrypt SSL certificates (HTTPS) within a few minutes.

---

### Step 5: Google Business Profile & Analytics Linking
1. **Google Business Profile:**
   - Go to [Google Business](https://business.google.com) and link your verified business location at `Shivanagar, Alwyn Colony, Kukatpally, Hyderabad 500072`.
   - Add your website URL and link your reviews URL (`https://share.google/soEV05LLv3ZGWSFKF`).
2. **Google Analytics & Meta Pixel:**
   - In `static/index.html`, paste your Google Analytics `G-XXXXXXXXXX` tag and Meta Pixel code right before `</head>`.

---

### Step 6: Managing Photos & Updating Packages
- **To update package prices or itineraries:**
  Log in to `https://your-domain.com/admin` to adjust prices or hide/activate batches.
- **To add new photos:**
  Place optimized `.webp` images into `static/images/places/<destination>/` or `static/images/happy-customers/`, and reference them in `static/index.html` or via the Admin panel.

---

### Step 7: Pre-Launch Quality Checklist
- [x] Test responsive layouts at 360px (mobile), 768px (tablet), and 1440px (desktop).
- [x] Test booking submission and verify server computes accurate 30% advance.
- [x] Test Kotak UPI QR code scan from GPay / PhonePe / Paytm.
- [x] Test UTR submission and verify status changes to `payment_submitted`.
- [x] Test WhatsApp prefilled message opens with exact customer details.
- [x] Test Admin login and verify booking status update to `confirmed`.
- [x] Verify `prefers-reduced-motion` media queries for accessibility.
- [x] Verify all images load in lightweight WebP format.
