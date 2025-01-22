import pytest
import requests
from datetime import datetime
from .test_functional import TestFunctional as pets


@pytest.mark.pet
class TestNonFunctional:
    BASE_URL = "https://petstore.swagger.io/v2"
    API_KEY = "special-key"

    @pytest.fixture
    def headers(self):
        return {
            "Content-Type": "application/json",
            "api_key": self.API_KEY
        }

    @pytest.mark.skip("api-key not being used to auth.")
    def test_api_key_authentication(self):
        """
        TC015: API Authentication
        """
        pet_data = {
            "name": "test_pet",
            "photoUrls": ["string"],
            "status": "available"
        }
        response = requests.post(
            f"{self.BASE_URL}/pet",
            json=pet_data,
            headers={"Content-Type": "application/json", "api_key": "random"}
        )

        assert response.status_code in [401, 403, 404]

    """
    Test to ensure the response time of search api does not exceed the threshold.s
    """
    @pytest.mark.performance
    def test_search_response_time(self, headers):
        """
        TC016: Response time for pet search
        """
        start_time = datetime.now()
        response = pets.find_by_status_request("available")
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        assert response.status_code == 200
        assert duration < 4.0, f"Response time {duration}s exceeded 4s threshold"
