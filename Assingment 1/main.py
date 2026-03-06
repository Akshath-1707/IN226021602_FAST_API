from fastapi import FastAPI

app = FastAPI()

# Temporary product storage
items = [
    {"id": 1, "name": "Smartphone X", "price": 22000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Wireless Earbuds", "price": 3499, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Sports Sneakers", "price": 4599, "category": "Fashion", "in_stock": True},
    {"id": 4, "name": "Travel Backpack", "price": 1899, "category": "Accessories", "in_stock": True},

    # Added Products
    {"id": 5, "name": "Laptop Stand", "price": 1350, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2599, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "HD Webcam", "price": 1999, "category": "Electronics", "in_stock": False}
]

# Home endpoint
@app.get("/")
def home():
    return {"status": "FastAPI server running"}

# Q1 — List all products
@app.get("/products")
def list_products():
    return {
        "products": items,
        "total": len(items)
    }

# Q2 — Products by category
@app.get("/products/category/{category_name}")
def category_products(category_name: str):

    filtered = [item for item in items if item["category"].lower() == category_name.lower()]

    if len(filtered) == 0:
        return {"message": "No products available in this category"}

    return {
        "category": category_name,
        "products": filtered,
        "total": len(filtered)
    }

# Q3 — Products in stock
@app.get("/products/instock")
def instock_items():

    available = [item for item in items if item["in_stock"]]

    return {
        "available_products": available,
        "count": len(available)
    }

# Q4 — Store summary
@app.get("/store/summary")
def store_overview():

    stock_count = len([item for item in items if item["in_stock"]])
    out_stock_count = len([item for item in items if not item["in_stock"]])

    category_list = list(set([item["category"] for item in items]))

    return {
        "store_name": "Online Tech Store",
        "total_products": len(items),
        "in_stock": stock_count,
        "out_of_stock": out_stock_count,
        "categories": category_list
    }

# Q5 — Search products
@app.get("/products/search/{keyword}")
def search_item(keyword: str):

    results = [item for item in items if keyword.lower() in item["name"].lower()]

    if not results:
        return {"message": "No matching products found"}

    return {
        "keyword": keyword,
        "matched_products": results,
        "matches": len(results)
    }

# Q6 — Deals endpoint
@app.get("/products/deals")
def deals():

    cheapest = min(items, key=lambda x: x["price"])
    expensive = max(items, key=lambda x: x["price"])

    return {
        "best_deal": cheapest,
        "premium_product": expensive
    }