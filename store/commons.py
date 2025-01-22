from datetime import datetime


def get_order_data(order_id, pet_id, qty):
    return {
        "id": order_id,
        "petId": pet_id,
        "quantity": qty,
        "shipDate": datetime.now().isoformat(),
        "status": "placed",
        "complete": True
    }
