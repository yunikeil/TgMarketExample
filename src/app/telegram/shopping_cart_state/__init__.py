from .shopping_cart_callback import shopping_cart_callbacks as __shopping_cart_callbacks
from .shopping_cart_states import shopping_cart_handler

shopping_cart_handlers = [
    *__shopping_cart_callbacks,
    shopping_cart_handler,
]
