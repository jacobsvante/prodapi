from typing import List

from prodapi import APIRouter, Depends, User

from . import permissions
from .auth import security
from .models import Product

router = APIRouter()


@router.post("/products", response_model=Product, status_code=201)
async def create_product(
    product: Product,
    user: User = Depends(security.user_holding(permissions.create_product)),
):
    """Create product"""
    # [TODO: Save product to db...]
    return product


@router.get("/products", response_model=List[Product])
async def list_products(
    user: User = Depends(security.user_holding(permissions.list_products_perm)),
    limit: int = 10,
):
    """List products"""
    # [TODO: Fetch products from db...]
    return [
        {"id": "d0b5b400-7488-404f-9d1b-8ff6cb32fa7c", "name": "T-Shirt"},
        {"id": "694bcf59-d0d9-4cd7-8539-d86dc1a62119", "name": "Sweater"},
    ]
