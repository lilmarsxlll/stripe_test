from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
import stripe
import os


load_dotenv()

app = FastAPI()
stripe.api_key = os.getenv('SK_STRIPE_API_KEY')

class Item(BaseModel):
    name: str
    description: str | None = None
    price: int

class Order(BaseModel):
    item_ids: List[int]


fake_db = {
    1: Item(name="Om Nom", description="Best Om Nom", price=10000),
    2: Item(name="Phone", description="IPhone", price=50000),
    3: Item(name="Controller", description="Dualsense", price=15000)
}

@app.get("/buy/{item_id}", response_model=dict)
async def buy_item(item_id: int):
    item = fake_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': item.price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )
    return {"session_id": session.id}

@app.post("/order/buy", response_model=dict)
async def buy_order(order: Order):
    items = []
    for item_id in order.item_ids:
        item = fake_db.get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
        items.append(item)

    if not items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    line_items = [{
        'price_data': {
            'currency': 'rub',
            'product_data': {
                'name': item.name,
                'description': item.description or ''
            },
            'unit_amount': item.price,
        },
        'quantity': 1,
    } for item in items]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )
    return {"session_id": session.id}

@app.get("/item/{item_id}", response_class=HTMLResponse)
async def get_item(item_id: int):
    item = fake_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404)

    return f"""
    <html>
        <head>
            <script src="https://js.stripe.com/v3/"></script>
        </head>
        <body>
            <h1>{item.name}</h1>
            <p>{item.description}</p>
            <p>Price: ${item.price / 100}</p>
            <button onclick="buy()">Buy</button>
            <script>
                async function buy() {{
                    const response = await fetch('/buy/{item_id}');
                    const {{ session_id }} = await response.json();
                    const stripe = Stripe('pk_test_ВАШ_ПУБЛИЧНЫЙ_КЛЮЧ');
                    stripe.redirectToCheckout({{ sessionId: session_id }});
                }}
            </script>
        </body>
    </html>
    """
