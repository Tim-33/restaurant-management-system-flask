import requests
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

def make_api_request(url: str, headers: dict, app: Flask,method: ApiMethodsEnum, body: dict | None = None ) -> dict:
    app.logger.info(f"Making API request to {url}")
    match method.value:
        case "GET":
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        case "POST":
            response = requests.post(url, headers=headers, body=body)
            response.raise_for_status()
            return response.json()
        case "PUT":
            response = requests.put(url, headers=headers, body=body)
            response.raise_for_status()
            return response.json()
        case "DELETE":
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return response.json()