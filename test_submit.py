import requests

res = requests.post(
    "http://127.0.0.1:5000/submit",
    json={
        "text": "Hello world I am testing this system",
        "creator_id": "test-user-1"
    }
)

print(res.status_code)
print(res.json())



