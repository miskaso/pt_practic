
import json
import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTMwYWY4ZWQtNTFkZi00Y2M3LTkwYTYtNDQwMjU5ZjgwNTY3IiwidHlwZSI6ImFwaV90b2tlbiJ9.x-4w65QfUcblhUpwOMUJVPgpOM-oWXln3TD0TxGI4HI",
    "accept": "application/json",
    "content-type": "application/json",
    }

url = "https://api.edenai.run/v2/image/generation"

payload = {
    "providers": "openai/dall-e-3",
    "text": "Телефон ест мясо",
    "response_as_dict": True,
    "attributes_as_list": False,
    "show_base_64": True,
    "show_original_response": False,
    "num_images": 1,
    "resolution": "512x512"
}

# response = requests.post(url, json=payload, headers=headers)

# print(result['openai/dall-e-3']['items'])


response = requests.post(url, json=payload, headers=headers)
result = json.loads(response.text)
print(response.text)