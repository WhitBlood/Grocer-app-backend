from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Product, Category
from ..schemas import ProductResponse
from ..dependencies import DbSession

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    db: DbSession,
    category: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """
    Get all products with optional filtering.
    
    - category: Filter by category name
    - search: Search in product name/description
    - skip: Number of products to skip (pagination)
    - limit: Maximum number of products to return
    """
    query = db.query(Product).filter(Product.is_active == True)
    
    # Filter by category
    if category:
        cat = db.query(Category).filter(Category.name == category).first()
        if cat:
            query = query.filter(Product.category_id == cat.id)
    
    # Search in name and description
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Product.name.ilike(search_term)) | 
            (Product.description.ilike(search_term))
        )
    
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: DbSession):
    """
    Get a specific product by ID.
    """
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.get("/category/{category_name}", response_model=List[ProductResponse])
async def get_products_by_category(category_name: str, db: DbSession):
    """
    Get all products in a specific category.
    """
    category = db.query(Category).filter(Category.name == category_name).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    products = db.query(Product).filter(
        Product.category_id == category.id,
        Product.is_active == True
    ).all()
    
    return products
