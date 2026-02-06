from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ..models import Order, OrderItem, Product
from ..schemas import OrderCreate, OrderResponse
from ..dependencies import DbSession, CurrentUser

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, current_user: CurrentUser, db: DbSession):
    """
    Create a new order.
    
    - Validates products exist and have stock
    - Calculates totals
    - Creates order and order items
    """
    # Calculate totals
    subtotal = 0
    order_items_data = []
    
    for item in order_data.items:
        # Get product
        product = db.query(Product).filter(Product.id == item.product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found"
            )
        
        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product {product.name} is not available"
            )
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {product.name}"
            )
        
        item_subtotal = float(product.price) * item.quantity
        subtotal += item_subtotal
        
        order_items_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "product_price": float(product.price),
            "quantity": item.quantity,
            "subtotal": item_subtotal
        })
    
    # Calculate fees
    delivery_fee = 0 if subtotal > 500 else 49
    tax = round(subtotal * 0.05, 2)
    total = subtotal + delivery_fee + tax
    
    # Create order
    new_order = Order(
        user_id=current_user.id,
        delivery_street=order_data.delivery_street,
        delivery_city=order_data.delivery_city,
        delivery_state=order_data.delivery_state,
        delivery_postal_code=order_data.delivery_postal_code,
        delivery_country=order_data.delivery_country,
        delivery_instructions=order_data.delivery_instructions,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        tax=tax,
        total=total,
        payment_method=order_data.payment_method,
        status="pending",
        payment_status="pending"
    )
    
    db.add(new_order)
    db.flush()  # Get order ID without committing
    
    # Create order items
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=new_order.id,
            **item_data
        )
        db.add(order_item)
        
        # Update product stock
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        product.stock -= item_data["quantity"]
    
    db.commit()
    db.refresh(new_order)
    
    return new_order


@router.get("/", response_model=List[OrderResponse])
async def get_user_orders(current_user: CurrentUser, db: DbSession):
    """
    Get all orders for the current user.
    """
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).order_by(Order.created_at.desc()).all()
    
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, current_user: CurrentUser, db: DbSession):
    """
    Get a specific order by ID.
    Only returns if it belongs to the current user.
    """
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(order_id: int, current_user: CurrentUser, db: DbSession):
    """
    Cancel an order.
    Only works if order is still pending.
    """
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only cancel pending orders"
        )
    
    order.status = "cancelled"
    
    # Restore product stock
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity
    
    db.commit()
    db.refresh(order)
    
    return order
