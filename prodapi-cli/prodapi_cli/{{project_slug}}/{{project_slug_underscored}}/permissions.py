from .auth import security

create_product = security.user_permission("products:create")
list_products = security.user_permission("products:list")
