import json

import requests
from fastapi import FastAPI
from pydantic import BaseModel

from get_recommendation import get_recommendation_for_product
from util import create_raw_astra_client

use_sync = True
#use_sync = False

app = FastAPI()

astra_client = create_raw_astra_client()
class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str

@app.get("/products")
def get_all_products(session_id: str):
    response = astra_client.collection("products").find()
    products = []
    for doc in response["data"]["documents"]:
        product = parse_product(doc)
        products.append(product)
    return {"products": products, "recommended_products": find_async_recommendations(session_id)}


def parse_product(doc):
    metadata = doc["metadata"]
    product = {
        "id": doc["_id"],
        "name": metadata["NAME"],
        "price": metadata["PRICE"],
        "description": metadata["DESCRIPTION"],
    }
    return product


def get_recommendations(selected_product, session_id):

    if use_sync:
        print("Getting recommendation sync")
        result = get_recommendation_for_product(selected_product)
        print(result)
        return result
    else:
        print(f"Getting recommendation async for {selected_product} and session {session_id}")
        langstream_url = "http://localhost:8091/api/gateways/produce/default/lc/send-event"
        body = {"value": {"product_name": selected_product["name"], "product_description": selected_product["description"], "session_id": session_id}}
        response = requests.post(langstream_url, json=body, headers={"Content-Type": "application/json"})
        if response.status_code != 200:
            print(f"Error while calling langstream: {response.status_code} - {response.text}")
        return find_async_recommendations(session_id)


def find_async_recommendations(session_id):
    rec = astra_client.collection("recommendations").find_one({
        "id": session_id
    })
    if rec["data"]["document"]:
        return json.loads(rec["data"]["document"]["rec"])
    else:
        return []


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, session_id: str):
    response = astra_client.collection("products").find_one({"_id": product_id})
    if response and response["data"]["document"]:
        selected_product = parse_product(response["data"]["document"])
        return {
            "selected_product": selected_product,
            "recommended_products": get_recommendations(selected_product, session_id)
        }
    return {"message": f"Product {product_id} not found"}, 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)