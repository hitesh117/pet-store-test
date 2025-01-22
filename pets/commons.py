def get_pet_data(pet_name="doggie", pet_id=0, category="default", tag="default", status="available"):
    return {
        "id": pet_id,
        "category": {
            "id": 0,
            "name": category
        },
        "name": pet_name,
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": tag
            }
        ],
        "status": status
    }
