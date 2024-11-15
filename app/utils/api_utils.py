def generate_api_route(endpoint: str) -> str:
    return f"/api/{endpoint}"

def build_api_route(base_url: str, port: int, route: str) -> str:
    return f"{base_url}:{port}{generate_api_route(route)}"