from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
from redis_om import HashModel

app = FastAPI()

origins = ['https//localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Basic connection example.
"""


r = redis.Redis(
    host='redis-12217.c341.af-south-1-1.ec2.redns.redis-cloud.com',
    port=12217,
    decode_responses=True,
    username="default",
    password="fLKpm0gkzgY08fU7Hh3nhnnhMsmODFpR",
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = r


@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.post("/products")
def create(product: Product):
    return product.save()

@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)

@app.delete("/products/{pk}")
def delete(pk: str):
    return Product.delete(pk)