from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

# Products dataset
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 649, "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "in_stock": True}
]

# Cart and orders storage
cart = []
orders = []
order_id = 1


# Checkout model
class Checkout(BaseModel):
    customer_name: str
    delivery_address: str


# Helper function
def get_product(product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None


# Q1 – Add items to cart
@app.post("/cart/add")
def add_to_cart(product_id: int = Query(...), quantity: int = Query(1)):

    product = get_product(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Q3 – Out of stock check
    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    # Q4 – Update quantity if product already exists in cart
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = item["quantity"] * item["price"]

            return {
                "message": "Cart updated",
                "cart_item": item
            }

    new_item = {
        "product_id": product["id"],
        "product_name": product["name"],
        "price": product["price"],
        "quantity": quantity,
        "subtotal": product["price"] * quantity
    }

    cart.append(new_item)

    return {
        "message": "Added to cart",
        "cart_item": new_item
    }


# Q2 – View cart
@app.get("/cart")
def view_cart():

    if not cart:
        return {"message": "Cart is empty"}

    total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": total
    }


# Q5 – Remove item from cart
@app.delete("/cart/{product_id}")
def remove_item(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": f"{item['product_name']} removed from cart"}

    raise HTTPException(status_code=404, detail="Item not in cart")


# Q5 & Q6 – Checkout
@app.post("/cart/checkout")
def checkout(data: Checkout):

    global order_id

    # Bonus – prevent checkout if cart is empty
    if not cart:
        raise HTTPException(status_code=400, detail="CART_EMPTY")

    total = 0
    placed_orders = []

    for item in cart:
        order = {
            "order_id": order_id,
            "customer_name": data.customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"]
        }

        orders.append(order)
        placed_orders.append(order)

        total += item["subtotal"]
        order_id += 1

    cart.clear()

    return {
        "message": "Order placed successfully",
        "orders_placed": len(placed_orders),
        "grand_total": total
    }


# Q6 – View orders
@app.get("/orders")
def get_orders():

    return {
        "orders": orders,
        "total_orders": len(orders)
    }