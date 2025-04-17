from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI(
    title="Order Submission API",
    description="API to submit orders with name, email, product, and quantity (as string)",
    version="1.0.0"
)

# Updated schema
class Order(BaseModel):
    name: str = Field(..., example="John Doe")
    email: str = Field(..., example="anything@not.email")
    product: str = Field(..., example="Paracetamol")
    quantity: str = Field(..., example="2 strips")  # Now a string

def insert_order(order: Order):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO orders (name, product, quantity, email)
        VALUES (?, ?, ?, ?)
    ''', (order.name, order.product, order.quantity, order.email))

    conn.commit()
    conn.close()

def fetch_all_orders():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, product, quantity, email FROM orders')
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "product": row[2],
            "quantity": row[3],
            "email": row[4]
        } for row in rows
    ]

@app.post("/submit-order/")
def submit_order(order: Order):
    try:
        insert_order(order)
        return {
            "message": f"{order.name}, your order of {order.product} quantity: {order.quantity} has been submitted successfully Details will be sent to {order.email}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/view-orders/")
def view_orders():
    try:
        orders = fetch_all_orders()
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
