import base64
import webview
import sys
import binascii
import os

class Base64Service:
    @staticmethod
    def to_b64(payload: str) -> str:
        if not payload:
            return ""
        try:
            return base64.b64encode(payload.encode("utf-8")).decode("utf-8")
        except UnicodeEncodeError:
            return "ERR_UNICODE_ENCODING"
        except Exception as e:
            return f"SYSTEM_ERR: {str(e)}"

    @staticmethod
    def from_b64(payload: str) -> str:
        if not payload:
            return ""
        try:
            missing_padding = len(payload) % 4
            if missing_padding:
                payload += '=' * (4 - missing_padding)
            decoded_bytes = base64.b64decode(payload, validate=True)
            return decoded_bytes.decode("utf-8")
        except binascii.Error:
            return "ERR_INVALID_BASE64_FORMAT"
        except UnicodeDecodeError:
            return "ERR_NON_UTF8_CONTENT"
        except Exception:
            return "ERR_DECODE_FAILED"

class Bridge:
    def __init__(self):
        self.service = Base64Service()

    def process(self, payload, mode):
        if mode == 'encode':
            return self.service.to_b64(payload)
        return self.service.from_b64(payload)

def initialize_application():
    bridge = Bridge()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(current_dir, 'index.html')
    
    window = webview.create_window(
        title='Base64 Encode/Decode',
        url=html_file,
        js_api=bridge,
        width=550,
        height=700,
        resizable=False,
        background_color='#0f1115'
    )
    webview.start(debug=False)

if __name__ == "__main__":
    initialize_application()
