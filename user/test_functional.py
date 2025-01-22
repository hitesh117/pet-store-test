import pytest
import requests
from .commons import get_user_data


@pytest.mark.user
class TestFunctional:
    BASE_URL = "https://petstore.swagger.io/v2"
    API_KEY = "special-key"
    SAMPLE_USERNAME = "Max117"
    HEADERS = {
        "Content-Type": "application/json",
        "api_key": API_KEY
    }

    def test_create_user(self):
        """
        TC012: Create user by username
        """
        user_data = get_user_data(user_id=12, username=self.SAMPLE_USERNAME)
        user_response = self.create_user(user_data)
        assert user_response.status_code == 200

        # verify if user was created
        user = self.get_user(self.SAMPLE_USERNAME)
        assert user.json()['username'] == self.SAMPLE_USERNAME
        assert user.json()['id'] == 12

    @pytest.mark.skip(reason="Already covered in test_create_user")
    def test_get_user(self):
        """
        TC013: Get user by username
        """
        user_data = get_user_data(user_id=14, username=self.SAMPLE_USERNAME)
        self.create_user(user_data)
        username = self.SAMPLE_USERNAME

        response = self.get_user(username)
        assert response.status_code == 200

        res = response.json()
        assert res['username'] == self.SAMPLE_USERNAME

    @pytest.mark.parametrize("username", ["hitesh19"])
    def test_delete_user(self, username):
        """
        TC014: Delete user
        """
        user_data = get_user_data(user_id=15, username=username)
        self.create_user(user_data)

        response = self.delete_user(username)
        assert response.status_code == 200

        # verify if user was deleted
        user_response = self.get_user(username)
        assert user_response.status_code == 404

    @staticmethod
    def create_user(user_data):
        return requests.post(f"{TestFunctional.BASE_URL}/user", json=user_data, headers=TestFunctional.HEADERS)

    @staticmethod
    def get_user(username):
        return requests.get(f"{TestFunctional.BASE_URL}/user/{username}", headers=TestFunctional.HEADERS)

    @staticmethod
    def delete_user(username):
        return requests.delete(f"{TestFunctional.BASE_URL}/user/{username}", headers=TestFunctional.HEADERS)
