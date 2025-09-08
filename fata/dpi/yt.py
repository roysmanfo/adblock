from mitmproxy import http
import json

from adshied.dpi.base import Inspector

STATUS_NO_CONTENT = 204
"""No content response code."""

RES_NO_CONTENT = http.Response.make(
    STATUS_NO_CONTENT,
    b"",
    {"Content-Type": "application/json"}
)

class YTInspector(Inspector):    
    def inspect(self, flow: http.HTTPFlow) -> bool:
        self.current_flow = flow
        
        checks = [
            self._check_json_contains_ads,
            self._check_player_contains_ads,
            ]

        if self._is_youtube_player_api(flow):
            try:
                for check in checks:
                    if check():
                        return True

            except Exception as e:
                self.logger.info(f"[YT AD DETECT] Error parsing response: {e}")
        
        return False

    def _is_youtube_player_api(self, flow: http.HTTPFlow) -> bool:
        """check if the request is from the YouTube player API. (those may contain ads)"""
        return (
            self._is_youtube_site(flow) and
            any(endpoint in flow.request.path for endpoint in ["/watch", "/get_video_info", "player", "player_204"])
        )
    
    def _is_youtube_site(self, flow: http.HTTPFlow) -> bool:
        """check if the request is from a YouTube site"""
        return "youtube.com" in flow.request.pretty_host

    def _check_json_contains_ads(self) -> bool:
        # Check for common ad-related fields in YouTube player responses
        
        text = self.current_flow.response.text
        json_data = json.loads(text)
        ad_keys = ["adPlacements", "playerAds", "adParams", "adSlots"]
        
        if any(key in json_data for key in ad_keys):
            if self.aggressive:
                self.current_flow.response = RES_NO_CONTENT

            return True
        return False

    def _check_player_contains_ads(self) -> bool:
        if "/v1/player" in self.current_flow.request.path and "youtube.com" in self.current_flow.request.pretty_host:
            try:
                data: dict[str, dict] = json.loads(self.current_flow.response.text)
                formats: list[dict[str, str]] = data.get("streamingData", {}).get("formats", []) + \
                        data.get("streamingData", {}).get("adaptiveFormats", [])

                for fmt in formats:
                    dur = int(fmt.get("approxDurationMs", "0"))
                    url = fmt.get("url", "")
                    
                    # likely an ad if it's <15s
                    # TODO: check for other ad-related fields in the player response
                    if dur < 15000:
                        self.logger.info("[YT AD DETECTED] Likely ad stream:", url)
                        
                        if self.aggressive:
                            fmt["url"] = "" # Remove the ad URL from the response
                            self.current_flow.response = RES_NO_CONTENT
                        return True

            except Exception as e:
                self.logger.error("Could not parse player JSON:", e)
        
        return False

