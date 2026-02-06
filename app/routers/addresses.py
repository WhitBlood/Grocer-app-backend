from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ..models import UserAddress
from ..schemas import AddressCreate, AddressUpdate, AddressResponse
from ..dependencies import DbSession, CurrentUser

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.get("/", response_model=List[AddressResponse])
async def get_user_addresses(current_user: CurrentUser, db: DbSession):
    """
    Get all addresses for the current user.
    """
    addresses = db.query(UserAddress).filter(
        UserAddress.user_id == current_user.id
    ).order_by(UserAddress.is_default.desc(), UserAddress.created_at.desc()).all()
    
    return addresses


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def create_address(address_data: AddressCreate, current_user: CurrentUser, db: DbSession):
    """
    Create a new address for the current user.
    
    - If is_default=True, removes default from other addresses
    """
    # If this is set as default, remove default from other addresses
    if address_data.is_default:
        db.query(UserAddress).filter(
            UserAddress.user_id == current_user.id
        ).update({"is_default": False})
    
    # Create new address
    new_address = UserAddress(
        user_id=current_user.id,
        **address_data.model_dump()
    )
    
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    
    return new_address


@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(address_id: int, current_user: CurrentUser, db: DbSession):
    """
    Get a specific address by ID.
    Only returns if it belongs to the current user.
    """
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    return address


@router.put("/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    address_data: AddressUpdate,
    current_user: CurrentUser,
    db: DbSession
):
    """
    Update an existing address.
    Only updates if it belongs to the current user.
    """
    # Find address
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    # If setting as default, remove default from others
    if address_data.is_default:
        db.query(UserAddress).filter(
            UserAddress.user_id == current_user.id,
            UserAddress.id != address_id
        ).update({"is_default": False})
    
    # Update address fields
    update_data = address_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(address, field, value)
    
    db.commit()
    db.refresh(address)
    
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: int, current_user: CurrentUser, db: DbSession):
    """
    Delete an address.
    Only deletes if it belongs to the current user.
    """
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    db.delete(address)
    db.commit()
    
    return None


@router.post("/{address_id}/set-default", response_model=AddressResponse)
async def set_default_address(address_id: int, current_user: CurrentUser, db: DbSession):
    """
    Set an address as the default delivery address.
    """
    # Find address
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    # Remove default from all other addresses
    db.query(UserAddress).filter(
        UserAddress.user_id == current_user.id
    ).update({"is_default": False})
    
    # Set this as default
    address.is_default = True
    db.commit()
    db.refresh(address)
    
    return address
