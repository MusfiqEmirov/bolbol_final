import requests


host = "http://0.0.0.0/"
request_url = f"{host}/api/v1/auth/login/send-otp/"

def _normalize_phone_number(phone_number: str) -> str:
    return phone_number.lstrip("+")

post_data = {
    "phone_number": _normalize_phone_number(input(">> "))
}

response = requests.post(request_url, json=post_data)
print(response.json())
#slkndvls
