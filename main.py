from threading import Thread

from mitmproxy.http import HTTPFlow 
from adshied import web, Shield


# automatically start web interface on separate Thread
Thread(target=web.start_web_interface, daemon=True).start()

# adshield engine
shield = Shield(optimize=True, debug=True)

def request(flow: HTTPFlow):
    shield.analyze(flow)


