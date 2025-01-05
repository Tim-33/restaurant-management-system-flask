from flask import Flask
from enum import Enum

class ApiMethodsEnum(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

def generate_api_route(endpoint: str) -> str:
    return f"/api/{endpoint}"

def build_api_route(base_url: str, port: int, route: str) -> str:
    return f"{base_url}:{port}{generate_api_route(route)}"

def make_api_request(url: str, headers: dict, app: Flask, method: ApiMethodsEnum, body: dict | None = None ):
    app.logger.info(f"Making API request to {url}")
    with app.test_client() as client:
        if method == ApiMethodsEnum.GET:
            response = client.get(url, headers=headers)
        elif method == ApiMethodsEnum.POST:
            response = client.post(url, headers=headers, json=body)
        elif method == ApiMethodsEnum.PUT:
            response = client.put(url, headers=headers, json=body)
        elif method == ApiMethodsEnum.DELETE:
            response = client.delete(url, headers=headers, json=body)
        else:
            raise ValueError(f"Unsupported method: {method}")

        return response.get_json()