from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ============= USER SCHEMAS =============

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# ============= ADDRESS SCHEMAS =============

class AddressBase(BaseModel):
    label: str = Field(..., max_length=50)
    street: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    postal_code: str = Field(..., max_length=20)
    country: str = Field(default="India", max_length=100)
    is_default: bool = False
    delivery_instructions: Optional[str] = None

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    label: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = None
    delivery_instructions: Optional[str] = None

class AddressResponse(AddressBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============= PRODUCT SCHEMAS =============

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    image_url: Optional[str] = None
    badge: Optional[str] = None
    category_id: int

class ProductResponse(ProductBase):
    id: int
    rating: float
    reviews_count: int
    stock: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============= ORDER SCHEMAS =============

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    delivery_street: str
    delivery_city: str
    delivery_state: str
    delivery_postal_code: str
    delivery_country: str = "India"
    delivery_instructions: Optional[str] = None
    payment_method: str = "card"

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_price: float
    quantity: int
    subtotal: float
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    delivery_street: str
    delivery_city: str
    delivery_state: str
    delivery_postal_code: str
    delivery_country: str
    subtotal: float
    delivery_fee: float
    tax: float
    total: float
    status: str
    payment_method: str
    payment_status: str
    created_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True
