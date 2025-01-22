import pytest
from pets.test_functional import TestFunctional as pets
from pets.commons import get_pet_data
from store.commons import get_order_data
from store.test_functional import TestFunctional as store


@pytest.mark.e2e
class TestFunctional:
    BASE_URL = "https://petstore.swagger.io/v2"
    API_KEY = "special-key"  # should be provided during test init. Using a static value here for now.

    @pytest.fixture
    def headers(self):
        return {
            "Content-Type": "application/json",
            "api_key": self.API_KEY
        }

    @pytest.mark.parametrize("pet_category", ["pajaro"])
    @pytest.mark.parametrize("pet_name", ["pupo"])
    @pytest.mark.parametrize("pet_status", ["available"])
    def test_search_pet_by_name_and_category_and_place_order(self, headers, pet_category, pet_name, pet_status):
        """
        TC017: Buyer can check available pets named “pupo” with category name “pajaro” and place an order for a pet.
        """
        # create pet data
        pet_data = get_pet_data(pet_name=pet_name, category=pet_category, status=pet_status)

        create_pet = pets.post_pet_request(pet_data)
        assert create_pet.status_code == 200

        # search pet
        response = pets.find_by_status_request(pet_status=pet_status)
        assert response.status_code == 200

        pet_details = [pet for pet in response.json()
                       if pet.get("name") == pet_name
                       and pet.get("category", {}).get("name") == pet_category]

        assert len(pet_details) > 0, "No pets found matching criteria"

        # place order for the pet
        order_data = get_order_data(22, pet_data["id"], 1)
        order_response = store.place_order_request(order_data)

        assert order_response.status_code == 200
        assert order_response.json()["status"] == "placed", "Order could not be placed"

    @pytest.mark.parametrize("pet_category", ["pomeranian"])
    @pytest.mark.parametrize("pet_name", ["kurikuri"])
    @pytest.mark.parametrize("pet_status", ["available"])
    @pytest.mark.parametrize("pet_tag", ["Super Cute"])
    def test_update_pet_tag(self, headers, pet_category, pet_name, pet_status, pet_tag):
        """
        TC018: update the pet information of pets named “kurikuri” under category “Pomeranian” to add the tag “Super Cute”
        """
        # add the dog
        pet_data = get_pet_data(pet_name=pet_name, category=pet_category, status=pet_status)
        pets.post_pet_request(pet_data)

        # find pet
        pets_available = pets.find_by_status_request("available").json()
        pets_sold = pets.find_by_status_request("sold").json()
        pets_pending = pets.find_by_status_request("pending").json()
        pet_to_find = None

        for pet in pets_available + pets_pending + pets_sold:
            if pet.get("name") == pet_name and pet.get("category", {}).get("name") == pet_category:
                pet_to_find = pet
                break
        assert pet_to_find is not None, f"${pet_name} not found"

        # update tags
        current_tags = pet_to_find.get("tags", [])
        if not any(tag.get("name") == pet_tag for tag in current_tags):
            current_tags.append({
                "id": len(current_tags) + 1,
                "name": pet_tag
            })
        pet_to_find["tags"] = current_tags

        # update pet
        update_response = pets.put_pet_request(pet_to_find)
        assert update_response.status_code == 200, "Failed to update pet"

        # verify update
        verify_response = pets.find_pet_by_id(pet_to_find['id'])
        assert verify_response.status_code == 200

        updated_pet = verify_response.json()
        assert any(tag.get("name") == pet_tag for tag in updated_pet["tags"]), \
            f"${pet_tag} tag was not found in updated pet tags"
