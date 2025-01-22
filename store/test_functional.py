import pytest
import requests
from .commons import get_order_data


@pytest.mark.store
class TestFunctional:
    BASE_URL = "https://petstore.swagger.io/v2"
    API_KEY = "special-key"
    HEADERS = {
        "Content-Type": "application/json",
        "api_key": API_KEY
    }

    def test_place_order(self):
        """
        TC007: Place valid order for pet
        """
        order_data = get_order_data(22, 789, 1)
        response = self.place_order_request(order_data)

        assert response.status_code == 200
        order = response.json()
        assert order["status"] == "placed"

    def test_delete_order(self):
        """
        TC008: Delete purchase order by ID
        """
        # create order
        order_data = get_order_data(22, 789, 1)

        order_response = self.place_order_request(order_data)
        assert order_response.status_code == 200

        order = order_response.json()
        order_id = order["id"]

        # delete order
        delete_response = self.delete_order(order_id)
        assert delete_response.status_code == 200

        # verify deletion
        order = self.get_order(order_id)
        assert order.status_code == 404

    def test_delete_invalid_order_should_return_404(self):
        """
        TC009: Delete purchase order by invalid ID
        """
        invalid_order_id = 87098
        delete_response = self.delete_order(invalid_order_id)
        assert delete_response.status_code == 404

    def test_find_order(self):
        """
        TC0010: Find Purchase order by ID
        """
        # create order
        order_data = get_order_data(22, 789, 1)

        order_response = self.place_order_request(order_data)
        assert order_response.status_code == 200

        order = order_response.json()
        order_id = order["id"]

        # find order
        find_response = self.get_order(order_id)
        assert find_response.status_code == 200

        res = find_response.json()
        assert res["petId"] == 789

    def test_inventory_status(self):
        """
        TC011: Return the inventory status
        """
        response = self.get_inventory_status()
        assert response.status_code == 200
        assert isinstance(response.json()['available'], int)

    @staticmethod
    def place_order_request(order_data):
        return requests.post(
            f"{TestFunctional.BASE_URL}/store/order", json=order_data, headers=TestFunctional.HEADERS)

    @staticmethod
    def delete_order(order_id):
        return requests.delete(f"{TestFunctional.BASE_URL}/store/order/{order_id}", headers=TestFunctional.HEADERS)

    @staticmethod
    def get_order(order_id):
        return requests.get(f"{TestFunctional.BASE_URL}/store/order/{order_id}", headers=TestFunctional.HEADERS)

    @staticmethod
    def get_inventory_status():
        return requests.get(f"{TestFunctional.BASE_URL}/store/inventory", headers=TestFunctional.HEADERS)
