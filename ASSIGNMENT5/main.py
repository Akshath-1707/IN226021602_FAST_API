from fastapi import FastAPI
import math

app = FastAPI()

products = [
    {"product_id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"product_id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"product_id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"product_id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = []
order_id = 1


# Q1
@app.get("/products/search")
def search_products(keyword: str):
    found = []
    for p in products:
        if keyword.lower() in p["name"].lower():
            found.append(p)

    if len(found) == 0:
        return {"message": f"No products found for: {keyword}"}

    return {
        "total_found": len(found),
        "products": found
    }


# Q2
@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by != "price" and sort_by != "name":
        return {"error": "sort_by must be 'price' or 'name'"}

    rev = False
    if order == "desc":
        rev = True

    sorted_data = sorted(products, key=lambda x: x[sort_by], reverse=rev)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_data
    }


# Q3
@app.get("/products/page")
def get_products_page(page: int = 1, limit: int = 2):

    total = len(products)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    data = products[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": data
    }


# Q5
@app.get("/products/sort-by-category")
def sort_cat():
    data = sorted(products, key=lambda x: (x["category"], x["price"]))
    return {"products": data}


# Q6
@app.get("/products/browse")
def browse(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):

    data = products

    if keyword is not None:
        temp = []
        for p in data:
            if keyword.lower() in p["name"].lower():
                temp.append(p)
        data = temp

    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = (order == "desc")
    data = sorted(data, key=lambda x: x[sort_by], reverse=reverse)

    total = len(data)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": total_pages,
        "products": data[start:end]
    }


# Q4
@app.post("/orders")
def create_order(customer_name: str):
    global order_id

    new_order = {
        "order_id": order_id,
        "customer_name": customer_name
    }

    orders.append(new_order)
    order_id += 1

    return {"message": "Order created", "order": new_order}


# Q4
@app.get("/orders/search")
def search_orders(customer_name: str):

    result = []

    for o in orders:
        if customer_name.lower() in o["customer_name"].lower():
            result.append(o)

    if len(result) == 0:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "total_found": len(result),
        "orders": result
    }


# BONUS
@app.get("/orders/page")
def orders_page(page: int = 1, limit: int = 3):

    total = len(orders)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "total_pages": total_pages,
        "orders": orders[start:end]
    }


@app.get("/products/{product_id}")
def get_product(product_id: int):

    for p in products:
        if p["product_id"] == product_id:
            return p

    return {"error": "Product not found"}