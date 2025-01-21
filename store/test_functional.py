import pytest
import requests
from .commons import get_order_data


@pytest.mark.store
class TestFunctional:
    BASE_URL = "https://petstore.swagger.io/v2"
    API_KEY = "special-key"

    @pytest.fixture
    def headers(self):
        return {
            "Content-Type": "application/json",
            "api_key": self.API_KEY
        }

    def test_place_order(self, headers):
        """
        TC007: Place valid order for pet
        """
        order_data = get_order_data()

        response = requests.post(
            f"{self.BASE_URL}/store/order",
            json=order_data,
            headers=headers
        )

        assert response.status_code == 200
        order = response.json()
        assert order["status"] == "placed"

    def test_delete_order(self, headers):
        """
        TC008: Delete purchase order by ID
        """
        order_data = get_order_data()

        order_response = requests.post(f"{self.BASE_URL}/store/order", json=order_data, headers=headers)
        assert order_response.status_code == 200

        order = order_response.json()
        order_id = order["id"]

        delete_response = requests.delete(f"{self.BASE_URL}/store/order/{order_id}", headers=headers)
        assert delete_response.status_code == 200
        print(order_id, "is deleted")

    def test_delete_invalid_order_should_return_404(self, headers):
        """
        TC009: Delete purchase order by invalid ID
        """
        invalid_order_id = 87098
        delete_response = requests.delete(f"{self.BASE_URL}/store/order/{invalid_order_id}", headers=headers)
        assert delete_response.status_code == 404

    def test_find_order(self, headers):
        """
        TC0010: Find Purchase order by ID
        """
        order_data = get_order_data()

        order_response = requests.post(f"{self.BASE_URL}/store/order", json=order_data, headers=headers)
        assert order_response.status_code == 200

        order = order_response.json()
        order_id = order["id"]

        find_response = requests.get(f"{self.BASE_URL}/store/order/{order_id}", headers=headers)
        assert find_response.status_code == 200

        res = find_response.json()
        print(res)
        assert res["petId"] == 789

    def test_inventory_status(self, headers):
        """
        TC011: Return the inventory status
        """
        response = requests.get(f"{self.BASE_URL}/store/inventory", headers=headers)
        assert response.status_code == 200

        assert isinstance(response.json()['available'], int)
