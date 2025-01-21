import pytest
import requests
from .commons import get_pet_data


@pytest.mark.pet
class TestFunctional:
    BASE_URL = "https://petstore.swagger.io/v2"
    API_KEY = "special-key"

    @pytest.fixture
    def headers(self):
        return {
            "Content-Type": "application/json",
            "api_key": self.API_KEY
        }

    def test_search_pet_by_name_and_category(self, headers):
        """
        TC001: Search available pets by name "pupo" and category "pajaro"
        """
        pet_data = {
            "id": 0,
            "category": {
                "id": 0,
                "name": "pajaro"
            },
            "name": "pupo",
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "string"
                }
            ],
            "status": "available"
        }

        create_response = requests.post(
            f"{self.BASE_URL}/pet",
            json=pet_data,
            headers=headers
        )
        assert create_response.status_code == 200

        response = requests.get(
            f"{self.BASE_URL}/pet/findByStatus",
            params={"status":"available"},
            headers=headers
        )

        assert response.status_code == 200

        pets = [pet for pet in response.json()
                if pet.get("name") == "pupo"
                and pet.get("category", {}).get("name") == "pajaro"]

        assert len(pets) > 0, "No pets found matching criteria"

    def test_search_pets_invalid_status(self, headers):
        """
        TC002: Search pets with invalid status
        """
        response = requests.get(
            f"{self.BASE_URL}/pet/findByStatus",
            params={"status": "invalid_status"},
            headers=headers
        )

        assert response.json() == [] or response.status_code == 400

    def test_update_pet_with_tag(self, headers):
        """
        TC003: Update pet named "kurikuri" with new tag
        """
        pet_data = {
            "name": "kurikuri",
            "category": {
                "name": "Pomeranian"
            },
            "photoUrls": ["string"],
            "tags": [
                {
                    "name": "Super Cute"
                }
            ],
            "status": "available"
        }

        response = requests.put(
            f"{self.BASE_URL}/pet",
            json=pet_data,
            headers=headers
        )
        assert response.status_code == 200
        updated_pet = response.json()
        assert any(tag["name"] == "Super Cute" for tag in updated_pet["tags"])

    def test_find_by_petID(self, headers):
        """
        TC004: Find the Pet using PetID
        """
        pet_data = get_pet_data()
        create_response = requests.post(f"{self.BASE_URL}/pet", json=pet_data, headers=headers)
        assert create_response.status_code == 200
        pet_id = create_response.json()["id"]
        response = requests.get(f"{self.BASE_URL}/pet/{pet_id}", headers=headers)
        assert response.status_code == 200

    def test_find_by_invalid_petId_should_fail(self, headers):
        """
        TC005: Find the Pet usng Invalid PetID
        """
        invalid_pet_id = 9879879999
        response = requests.get(f"{self.BASE_URL}/pet/{invalid_pet_id}", headers=headers)
        assert response.status_code == 404
        assert response.json()["message"] == "Pet not found"
        assert response.json()["type"] == "error"

    def test_delete_pet_using_pet_id(self, headers):
        """
        TC006: Delete Pet using PetID
        """
        pet_data = get_pet_data()

        create_response = requests.post(f"{self.BASE_URL}/pet", json=pet_data, headers=headers)
        assert create_response.status_code == 200

        pet_id = create_response.json()["id"]

        response = requests.delete(f"{self.BASE_URL}/pet/{pet_id}", headers=headers)
        assert response.status_code == 200