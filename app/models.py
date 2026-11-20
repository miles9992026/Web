import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from .database import Base

class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    tagline = Column(String(255), nullable=True)
    duration = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    original_price = Column(Integer, nullable=True)
    advance_price = Column(Integer, nullable=True)
    emoji = Column(String(10), default="✈️")
    badge = Column(String(50), default="Featured")
    category = Column(String(50), default="Hill Station")
    colors = Column(Text, default='{"primary": "#0b8a8f", "accent": "#ff7a1a"}')
    active = Column(Boolean, default=True)
    is_sample = Column(Boolean, default=True)
    description = Column(Text, nullable=False)
    highlights = Column(Text, default="[]")  # JSON string
    itinerary = Column(Text, default="[]")   # JSON string
    inclusions = Column(Text, default="[]")  # JSON string
    exclusions = Column(Text, default="[]")  # JSON string
    pickup_points = Column(String(255), default="Uppal, LB Nagar, Kukatpally, Lakdikapul, Gachibowli")
    best_season = Column(String(100), default="October to March")
    cancellation_policy = Column(Text, default="Full refund if cancelled 7 days prior. 50% refund 3-6 days prior. No refund within 48 hours.")
    image_card = Column(String(255), nullable=True)
    image_hero = Column(String(255), nullable=True)
    gallery_images = Column(Text, default="[]") # JSON string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    ref = Column(String(30), unique=True, index=True, nullable=False)
    package_id = Column(Integer, nullable=True)
    package_name = Column(String(150), nullable=False)
    package_slug = Column(String(100), nullable=True)
    customer_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(120), nullable=True)
    travel_date = Column(String(50), nullable=False)
    travelers = Column(Integer, default=1)
    pay_type = Column(String(20), default="advance") # "advance" or "full"
    unit_price = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)
    advance_amount = Column(Integer, nullable=False)
    balance_due = Column(Integer, nullable=False)
    utr = Column(String(100), nullable=True)
    status = Column(String(30), default="pending") # pending, payment_submitted, paid, confirmed, cancelled
    pickup_point = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
