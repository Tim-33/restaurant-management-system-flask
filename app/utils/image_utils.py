import base64

def render_picture(data):
    return base64.b64encode(data).decode('ascii') if data else None