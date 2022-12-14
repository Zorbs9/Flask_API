import uuid
from flask import Flask, request
from flask_smorest import abort
import db

app = Flask(__name__)

@app.get("/store")
def get_stores():
    return {"stores": list(db.stores.values())}


@app.get("/items")
def get_items():
    return {"items": list(db.items.values())}


@app.get("/store/<string:store_id>")
def get_store(storeid):
    try:
        return db.stores[storeid]
    except KeyError:
        abort(404 , message = "Store not found")


@app.get("/item/<string:item_id>")
def get_item_(item_id):
    try:
        return db.items["item_id"]
    except KeyError:
       abort(404 , message = "Item not found")    



@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload.",
        )
    for store in db.stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    db.stores[store_id] = store

    return store

@app.post("/item")
def create_item():
    item_data = request.get_json()
    # Here not only we need to validate data exists,
    # But also what type of data. Price should be a float,
    # for example.
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
        )
    for item in db.items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message="Item already exists.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    db.items[item_id] = item

    return item


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del db.items["item_id"]
        return {"message" : "Iteme deleted."}
    except KeyError:
       abort(404 , message = "Item not found") 




