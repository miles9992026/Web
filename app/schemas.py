from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field
import datetime

class PackageBase(BaseModel):
    slug: str
    name: str
    tagline: Optional[str] = None
    duration: str
    price: int
    original_price: Optional[int] = None
    advance_price: Optional[int] = None
    emoji: Optional[str] = "🌲"
    badge: Optional[str] = "Popular"
    category: Optional[str] = "Hill Station"
    colors: Optional[str] = '{"primary": "#0b8a8f", "accent": "#ff7a1a"}'
    active: Optional[bool] = True
    is_sample: Optional[bool] = True
    description: str
    highlights: Optional[str] = "[]"
    itinerary: Optional[str] = "[]"
    inclusions: Optional[str] = "[]"
    exclusions: Optional[str] = "[]"
    pickup_points: Optional[str] = "Uppal, LB Nagar, Kukatpally, Lakdikapul, Gachibowli"
    best_season: Optional[str] = "October to March"
    cancellation_policy: Optional[str] = "Full refund if cancelled 7 days prior."
    image_card: Optional[str] = None
    image_hero: Optional[str] = None
    gallery_images: Optional[str] = "[]"

class PackageCreate(PackageBase):
    pass

class PackageUpdate(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    duration: Optional[str] = None
    price: Optional[int] = None
    original_price: Optional[int] = None
    advance_price: Optional[int] = None
    emoji: Optional[str] = None
    badge: Optional[str] = None
    category: Optional[str] = None
    active: Optional[bool] = None
    is_sample: Optional[bool] = None
    description: Optional[str] = None
    highlights: Optional[str] = None
    itinerary: Optional[str] = None
    inclusions: Optional[str] = None
    exclusions: Optional[str] = None
    pickup_points: Optional[str] = None
    best_season: Optional[str] = None
    cancellation_policy: Optional[str] = None
    image_card: Optional[str] = None
    image_hero: Optional[str] = None
    gallery_images: Optional[str] = None

class PackageResponse(PackageBase):
    id: int
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    package_slug: str
    customer_name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    email: Optional[str] = None
    travel_date: str
    travelers: int = Field(default=1, ge=1, le=50)
    pay_type: str = Field(default="advance", pattern="^(advance|full)$")
    pickup_point: Optional[str] = None
    notes: Optional[str] = None

class UTRSubmit(BaseModel):
    utr: str = Field(..., min_length=6, max_length=100)

class StatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|payment_submitted|paid|confirmed|cancelled)$")

class BookingResponse(BaseModel):
    id: int
    ref: str
    package_id: Optional[int] = None
    package_name: str
    package_slug: Optional[str] = None
    customer_name: str
    phone: str
    email: Optional[str] = None
    travel_date: str
    travelers: int
    pay_type: str
    unit_price: int
    total_amount: int
    advance_amount: int
    balance_due: int
    utr: Optional[str] = None
    status: str
    pickup_point: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class ConfigResponse(BaseModel):
    business_name: str
    tagline: str
    motto: str
    email: str
    phones: List[str]
    whatsapp_number: str
    address: str
    google_reviews_url: str
    instagram_handle: str
    upi_id: str
    bank: dict
    advance_pct: int
    enquiry_form_url: str
    booking_form_url: str
