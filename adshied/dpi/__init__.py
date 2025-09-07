__doc__ = """
Deep packet inspection (DPI) module.
This module provides functionality for deep packet inspection (DPI) of network traffic.

It includes classes and methods for analyzing network packets, filtering content, and blocking unwanted traffic.
It is designed to be used with the mitmproxy library for intercepting and modifying HTTP requests and responses.
"""

__all__ = [
    "YTInspector",
]

from mitmproxy import http
from .yt import YTInspector



class DPI:
    """
    Deep Packet Inspection (DPI) class.
    
    This class is responsible for performing deep packet inspection on network traffic.  
    It can analyze and filter network packets based on various criteria.
    """
    
    def __init__(self, aggressive: bool = False, debug: bool = False):
        self.debug = debug
        self.inspectors = {
            YTInspector(aggressive=aggressive),
        }

    def inspect(self, flow: http.HTTPFlow):
        """
        Analyze the given HTTP flow for ads and unwanted content.

        Args:
            flow (http.HTTPFlow): The HTTP flow to analyze.
        """
        for inspector in self.inspectors:
            try:
                if res := inspector.inspect(flow):
                    return res
            except:
                # TODO: log this error, may help in debugging crashes
                pass