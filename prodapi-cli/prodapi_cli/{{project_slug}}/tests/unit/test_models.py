import uuid

from {{project_slug}}.models import Product


def test_that_product_gets_id_automatically():
    product = Product(name="T-shirt")
    assert isinstance(product.id, uuid.UUID)
