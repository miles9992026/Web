import os
import csv
import io
import time
import uuid
import secrets
from typing import Optional, List
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.database import get_db, Base, engine
from app.models import Package, Booking
from app.schemas import (
    PackageBase, PackageCreate, PackageUpdate, PackageResponse,
    BookingCreate, BookingResponse, UTRSubmit, StatusUpdate, ConfigResponse
)
from app.seed_data import init_db

# Environment Configurations
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "happymiles2026")
UPI_ID = os.getenv("UPI_ID", "7661981338@kotakbank")
WA_NUMBER = os.getenv("WA_NUMBER", "918074016910")
ADVANCE_PCT = int(os.getenv("ADVANCE_PCT", "30"))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
ENQUIRY_FORM_URL = os.getenv("ENQUIRY_FORM_URL", "https://forms.gle/8dFCPRhFAX5Rzg3W7")
BOOKING_FORM_URL = os.getenv("BOOKING_FORM_URL", "https://forms.gle/r97LBQdCx39JAZfQ6")

# Initialize DB
init_db()

app = FastAPI(
    title="HappyMiles Tours API",
    description="Backend API for HappyMiles Tours — Turning Miles into Memories!",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory simple rate limiting for booking endpoint (max 10 requests / 60 seconds per IP)
RATE_LIMIT_STORE = {}

def rate_limiter(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()
    history = RATE_LIMIT_STORE.get(client_ip, [])
    # Filter timestamps within last 60s
    history = [t for t in history if current_time - t < 60]
    if len(history) >= 10:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Oops! Too many booking attempts in a short time. Please take a breath and try again in a minute."
        )
    history.append(current_time)
    RATE_LIMIT_STORE[client_ip] = history

# Basic Auth for Admin
security = HTTPBasic()

def authenticate_admin(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_correct = secrets.compare_digest(credentials.username, ADMIN_USER)
    is_pass_correct = secrets.compare_digest(credentials.password, ADMIN_PASS)
    if not (is_user_correct and is_pass_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# ----------------- PUBLIC API ENDPOINTS -----------------

@app.get("/api/config", response_model=ConfigResponse)
def get_site_config():
    """Return public business configuration, payment details, and policies"""
    return {
        "business_name": "HappyMiles Tours",
        "tagline": "Turning Miles into Memories!",
        "motto": "Travel More, Worry Less.",
        "email": "happymilestravelss@gmail.com",
        "phones": ["8074016910", "9381936910"],
        "whatsapp_number": WA_NUMBER,
        "address": "Shivanagar, Alwyn Colony, Kukatpally, Hyderabad 500072",
        "google_reviews_url": "https://share.google/soEV05LLv3ZGWSFKF",
        "instagram_handle": "@happymilestours_",
        "upi_id": UPI_ID,
        "bank": {
            "bank_name": "Kotak Mahindra Bank",
            "account_name": "Miryala Bharath",
            "account_number": "2248401328",
            "ifsc": "KKBK0007475",
            "branch": "KPHB (Pratiba Vidyaniketan), Hyderabad"
        },
        "advance_pct": ADVANCE_PCT,
        "enquiry_form_url": ENQUIRY_FORM_URL,
        "booking_form_url": BOOKING_FORM_URL
    }

@app.get("/api/packages", response_model=List[PackageResponse])
def get_packages(active_only: bool = True, db: Session = Depends(get_db)):
    """Retrieve list of tour packages"""
    query = db.query(Package)
    if active_only:
        query = query.filter(Package.active == True)
    return query.order_by(Package.id.asc()).all()

@app.get("/api/packages/{slug}", response_model=PackageResponse)
def get_package(slug: str, db: Session = Depends(get_db)):
    """Retrieve a single package by slug"""
    pkg = db.query(Package).filter(Package.slug == slug).first()
    if not pkg:
        raise HTTPException(status_code=404, detail="We could not find the requested package.")
    return pkg

@app.post("/api/bookings", response_model=BookingResponse, dependencies=[Depends(rate_limiter)])
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking with strictly server-calculated totals"""
    # 1. Fetch package
    pkg = db.query(Package).filter(Package.slug == payload.package_slug).first()
    if not pkg or not pkg.active:
        raise HTTPException(
            status_code=400,
            detail="The chosen package is currently unavailable. Please select another trip."
        )

    # 2. Server-side financial calculations
    travelers = max(1, payload.travelers)
    unit_price = pkg.price
    total_amount = unit_price * travelers

    # Advance amount calculation
    if pkg.advance_price and pkg.advance_price > 0:
        unit_advance = pkg.advance_price
    else:
        unit_advance = int(unit_price * (ADVANCE_PCT / 100))
    advance_amount = unit_advance * travelers

    if payload.pay_type == "advance":
        due_now = advance_amount
        balance_due = total_amount - advance_amount
    else:
        due_now = total_amount
        balance_due = 0

    # 3. Generate unique booking ref
    date_str = datetime.utcnow().strftime("%Y%m")
    unique_suffix = secrets.token_hex(2).upper()
    ref = f"HM-{date_str}-{unique_suffix}"

    booking = Booking(
        ref=ref,
        package_id=pkg.id,
        package_name=pkg.name,
        package_slug=pkg.slug,
        customer_name=payload.customer_name.strip(),
        phone=payload.phone.strip(),
        email=payload.email.strip() if payload.email else None,
        travel_date=payload.travel_date,
        travelers=travelers,
        pay_type=payload.pay_type,
        unit_price=unit_price,
        total_amount=total_amount,
        advance_amount=advance_amount,
        balance_due=balance_due,
        status="pending",
        pickup_point=payload.pickup_point,
        notes=payload.notes
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@app.post("/api/bookings/{ref}/utr", response_model=BookingResponse)
def submit_utr(ref: str, payload: UTRSubmit, db: Session = Depends(get_db)):
    """Customer submits UPI / Bank UTR after transfer"""
    booking = db.query(Booking).filter(Booking.ref == ref).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking reference was not found.")

    clean_utr = payload.utr.strip()
    booking.utr = clean_utr
    booking.status = "payment_submitted"
    booking.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(booking)
    return booking

@app.get("/api/bookings/{ref}", response_model=BookingResponse)
def get_booking_status(ref: str, db: Session = Depends(get_db)):
    """Check booking status by ref"""
    booking = db.query(Booking).filter(Booking.ref == ref).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking reference was not found.")
    return booking

# ----------------- ADMIN API ENDPOINTS (Protected) -----------------

@app.get("/api/admin/bookings")
def admin_list_bookings(
    status_filter: Optional[str] = None,
    q: Optional[str] = None,
    admin: str = Depends(authenticate_admin),
    db: Session = Depends(get_db)
):
    """Admin: list bookings with optional status filter and search query"""
    query = db.query(Booking)
    if status_filter and status_filter != "all":
        query = query.filter(Booking.status == status_filter)
    if q:
        query = query.filter(
            (Booking.ref.ilike(f"%{q}%")) |
            (Booking.customer_name.ilike(f"%{q}%")) |
            (Booking.phone.ilike(f"%{q}%")) |
            (Booking.utr.ilike(f"%{q}%"))
        )
    return query.order_by(Booking.id.desc()).all()

@app.patch("/api/admin/bookings/{ref}/status", response_model=BookingResponse)
def admin_update_booking_status(
    ref: str,
    payload: StatusUpdate,
    admin: str = Depends(authenticate_admin),
    db: Session = Depends(get_db)
):
    """Admin: update booking status (pending, payment_submitted, paid, confirmed, cancelled)"""
    booking = db.query(Booking).filter(Booking.ref == ref).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking was not found.")
    booking.status = payload.status
    booking.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(booking)
    return booking

@app.get("/api/admin/bookings/export")
def admin_export_csv(
    admin: str = Depends(authenticate_admin),
    db: Session = Depends(get_db)
):
    """Admin: export bookings to CSV file"""
    bookings = db.query(Booking).order_by(Booking.id.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Reference", "Package", "Customer Name", "Phone", "Email",
        "Travel Date", "Travelers", "Pay Type", "Total (₹)", "Advance (₹)",
        "Balance Due (₹)", "UTR", "Status", "Pickup Point", "Created At"
    ])
    for b in bookings:
        writer.writerow([
            b.ref, b.package_name, b.customer_name, b.phone, b.email or "",
            b.travel_date, b.travelers, b.pay_type, b.total_amount, b.advance_amount,
            b.balance_due, b.utr or "", b.status, b.pickup_point or "",
            b.created_at.strftime("%Y-%m-%d %H:%M:%S") if b.created_at else ""
        ])
    output.seek(0)
    filename = f"happymiles-bookings-{datetime.utcnow().strftime('%Y%m%d-%H%M')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/api/admin/stats")
def admin_stats(
    admin: str = Depends(authenticate_admin),
    db: Session = Depends(get_db)
):
    """Admin: return high-level analytics"""
    total_bookings = db.query(Booking).count()
    payment_submitted = db.query(Booking).filter(Booking.status == "payment_submitted").count()
    confirmed = db.query(Booking).filter(Booking.status.in_(["paid", "confirmed"])).count()
    cancelled = db.query(Booking).filter(Booking.status == "cancelled").count()
    packages_count = db.query(Package).count()

    total_revenue = sum(
        b.total_amount for b in db.query(Booking).filter(Booking.status.in_(["paid", "confirmed"])).all()
    )

    return {
        "total_bookings": total_bookings,
        "payment_submitted": payment_submitted,
        "confirmed": confirmed,
        "cancelled": cancelled,
        "packages_count": packages_count,
        "total_revenue": total_revenue
    }

@app.post("/api/admin/packages", response_model=PackageResponse)
def admin_create_package(
    payload: PackageCreate,
    admin: str = Depends(authenticate_admin),
    db: Session = Depends(get_db)
):
    """Admin: Add a new tour package"""
    existing = db.query(Package).filter(Package.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Package slug already exists.")
    pkg = Package(**payload.dict())
    db.add(pkg)
    db.commit()
    db.refresh(pkg)
    return pkg

@app.put("/api/admin/packages/{package_id}", response_model=PackageResponse)
def admin_update_package(
    package_id: int,
    payload: PackageUpdate,
    admin: str = Depends(authenticate_admin),
    db: Session = Depends(get_db)
):
    """Admin: update existing tour package"""
    pkg = db.query(Package).filter(Package.id == package_id).first()
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found.")
    for key, val in payload.dict(exclude_unset=True).items():
        setattr(pkg, key, val)
    pkg.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(pkg)
    return pkg

@app.delete("/api/admin/packages/{package_id}")
def admin_delete_package(
    package_id: int,
    admin: str = Depends(authenticate_admin),
    db: Session = Depends(get_db)
):
    """Admin: toggle active state or delete package"""
    pkg = db.query(Package).filter(Package.id == package_id).first()
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found.")
    db.delete(pkg)
    db.commit()
    return {"message": "Package deleted successfully"}

# ----------------- HTML PAGE ROUTES -----------------

@app.get("/", response_class=FileResponse)
def serve_home():
    return FileResponse("static/index.html")

@app.get("/packages", response_class=FileResponse)
def serve_packages():
    return FileResponse("static/packages.html")

@app.get("/packages/{slug}", response_class=FileResponse)
def serve_package_detail(slug: str):
    return FileResponse("static/package-detail.html")

@app.get("/package-detail.html", response_class=FileResponse)
def serve_package_detail_direct():
    return FileResponse("static/package-detail.html")

@app.get("/about", response_class=FileResponse)
def serve_about():
    return FileResponse("static/about.html")

@app.get("/contact", response_class=FileResponse)
def serve_contact():
    return FileResponse("static/contact.html")

@app.get("/terms", response_class=FileResponse)
def serve_terms():
    return FileResponse("static/terms.html")

@app.get("/privacy", response_class=FileResponse)
def serve_privacy():
    return FileResponse("static/privacy.html")

@app.get("/refund", response_class=FileResponse)
def serve_refund():
    return FileResponse("static/refund.html")

@app.get("/admin", response_class=FileResponse)
def serve_admin():
    return FileResponse("static/admin.html")

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# 404 Fallback
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=404, content={"detail": "API endpoint not found"})
    return FileResponse("static/404.html", status_code=404)
