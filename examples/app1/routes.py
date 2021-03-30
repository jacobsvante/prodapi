from typing import List

from prodapi import APIRouter, Depends, FastAPISecurity, User

from . import db
from .models import Product


def make_router(security: FastAPISecurity) -> APIRouter:
    create_product_perm = security.user_permission("products:create")
    list_products_perm = security.user_permission("products:list")

    router = APIRouter()

    @router.post("/products", response_model=Product, status_code=201)
    async def create_product(
        product: Product,
        user: User = Depends(security.user_holding(create_product_perm)),
    ):
        """Create product

        Requires the authenticated user to have the `products:create` permission
        """
        await db.persist(product)
        return product

    @router.get("/products", response_model=List[Product])
    async def list_products(
        user: User = Depends(security.user_holding(list_products_perm)),
        limit: int = 10,
    ):
        """List products

        Requires the authenticated user to have the `products:list` permission
        """
        products = await db.fetch(limit=limit)
        return products

    return router
