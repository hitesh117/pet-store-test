import requests


def create_user(self, headers):
    user_data = {
        "id": 1,
        "username": "Max117",
        "firstName": "Max",
        "lastName": "Venom",
        "email": "Max@mail.com",
        "password": "abc",
        "phone": "1234",
        "userStatus": 0
    }
    user_response = requests.post(f"{self.BASE_URL}/user", json=user_data, headers=headers)
    return user_data, user_response
