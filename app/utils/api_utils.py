import requests
from flask import Flask

def generate_api_route(endpoint: str) -> str:
    return f"/api/{endpoint}"

def build_api_route(base_url: str, port: int, route: str) -> str:
    return f"{base_url}:{port}{generate_api_route(route)}"

def make_api_request(url: str, headers: dict, app: Flask) -> dict:
    app.logger.info(f"Making API request to {url}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()