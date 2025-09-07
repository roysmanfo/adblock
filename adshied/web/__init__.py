from adshied.web.router import app as app


def start_web_interface(port: int = 5000):
    app.run(port=port)
