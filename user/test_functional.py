import pytest
import requests
from .commons import create_user


@pytest.mark.user
class TestFunctional:
    BASE_URL = "https://petstore.swagger.io/v2"
    API_KEY = "special-key"
    SAMPLE_USERNAME = "Max117"

    @pytest.fixture
    def headers(self):
        return {
            "Content-Type": "application/json",
            "api_key": self.API_KEY
        }

    def test_create_user(self, headers):
        """
        TC012: Get user by username
        """
        user_data, user_response = create_user(self, headers)
        assert user_response.status_code == 200

        response = requests.post(f"{self.BASE_URL}/user/createWithList", json=[user_data], headers=headers)
        assert response.status_code == 200

    def test_get_user(self, headers):
        """
        TC013: Get user by username
        """
        create_user(self, headers)
        username = self.SAMPLE_USERNAME

        response = requests.get(f"{self.BASE_URL}/user/{username}", headers=headers)
        assert response.status_code == 200

        res = response.json()
        assert res['username'] == self.SAMPLE_USERNAME

    def test_delete_user(self, headers):
        """
        TC014: Delete user
        """
        create_user(self, headers)
        username = self.SAMPLE_USERNAME

        response = requests.delete(f"{self.BASE_URL}/user/{username}", headers=headers)
        assert response.status_code == 200
