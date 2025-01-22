import pytest
import requests
from .commons import get_pet_data


@pytest.mark.pet
class TestFunctional:
    BASE_URL = "https://petstore.swagger.io/v2"
    API_KEY = "special-key"
    HEADERS = {
        "Content-Type": "application/json",
        "api_key": API_KEY
    }

    @pytest.mark.parametrize("pet_category", ["pajaro"])
    @pytest.mark.parametrize("pet_name", ["pupo"])
    @pytest.mark.parametrize("pet_status", ["available"])
    def test_search_pet_by_name_and_category(self, pet_category, pet_name, pet_status):
        """
        TC001: Search available pets by name "pupo" and category "pajaro"
        """
        pet_data = get_pet_data(pet_id=11, pet_name=pet_name, category=pet_category, status=pet_status)

        create_response = self.post_pet_request(pet_data)
        assert create_response.status_code == 200

        response = self.find_by_status_request(pet_status)

        assert response.status_code == 200

        pets = [pet for pet in response.json()
                if pet.get("name") == "pupo"
                and pet.get("category", {}).get("name") == "pajaro"]

        assert len(pets) > 0, "No pets found matching criteria"

    def test_search_pets_invalid_status(self):
        """
        TC002: Search pets with invalid status
        """
        response = self.find_by_status_request("invalid")

        assert response.json() == [] or response.status_code == 400

    @pytest.mark.parametrize("pet_name", ["kurikuri"])
    @pytest.mark.parametrize("new_tag", ["Super Cute"])
    def test_update_pet_with_tag(self, pet_name, new_tag):
        """
        TC003: Update pet named "kurikuri" with new tag
        """
        # create pet
        pet_data = get_pet_data(pet_id=10, pet_name=pet_name, status="available")
        create_pet_res = self.post_pet_request(pet_data)

        # update pet data
        update_req = create_pet_res.json()
        update_req["tags"] = [{"id": 1, "name": new_tag}]
        response = self.put_pet_request(update_req)
        assert response.status_code == 200
        assert response.json()["tags"] == [{"id": 1, "name": new_tag}]

    def test_find_by_petID(self):
        """
        TC004: Find the Pet using PetID
        """
        # create pet
        pet_data = get_pet_data()
        create_response = self.post_pet_request(pet_data)
        assert create_response.status_code == 200

        # find by id
        pet_id = create_response.json()["id"]
        response = self.find_pet_by_id(pet_id)
        assert response.status_code == 200
        assert response.json()["name"] == "doggie"

    def test_find_by_invalid_petId_should_fail(self):
        """
        TC005: Find the Pet usng Invalid PetID
        """
        invalid_pet_id = 9879879999
        response = self.find_pet_by_id(invalid_pet_id)
        assert response.status_code == 404
        assert response.json()["message"] == "Pet not found"
        assert response.json()["type"] == "error"

    def test_delete_pet_using_pet_id(self):
        """
        TC006: Delete Pet using PetID
        """
        # create pet
        pet_data = get_pet_data(pet_id=123)
        create_response = self.post_pet_request(pet_data)
        assert create_response.status_code == 200

        pet_id = create_response.json()["id"]

        response = self.delete_pet_request(pet_id)
        assert response.status_code == 200

        # verify pet is deleted from datastore
        verify_response = self.find_pet_by_id(pet_id)
        assert verify_response.status_code == 404
        assert verify_response.json()["message"] == "Pet not found"

    @staticmethod
    def post_pet_request(pet_data):
        return requests.post(
            f"{TestFunctional.BASE_URL}/pet",
            json=pet_data,
            headers=TestFunctional.HEADERS
        )

    @staticmethod
    def find_by_status_request(pet_status):
        return requests.get(
            f"{TestFunctional.BASE_URL}/pet/findByStatus",
            params={"status": pet_status},
            headers=TestFunctional.HEADERS
        )

    @staticmethod
    def put_pet_request(pet_data):
        return requests.put(
            f"{TestFunctional.BASE_URL}/pet",
            json=pet_data,
            headers=TestFunctional.HEADERS
        )

    @staticmethod
    def delete_pet_request(pet_id):
        return requests.delete(f"{TestFunctional.BASE_URL}/pet/{pet_id}", headers=TestFunctional.HEADERS)

    @staticmethod
    def find_pet_by_id(pet_id):
        return requests.get(f"{TestFunctional.BASE_URL}/pet/{pet_id}", headers=TestFunctional.HEADERS)
