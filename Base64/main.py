import base64
import webview
import sys
import binascii

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
    window = webview.create_window(
        title='Base64 Encode/Decode',
        html=UI_HTML,
        js_api=bridge,
        width=550,
        height=700,
        resizable=False,
        background_color='#0f1115'
    )
    webview.start(debug=False)

UI_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        :root {
            --bg: #0f1115;
            --surface: #1a1d23;
            --accent: #3b82f6;
            --text-main: #e5e7eb;
            --text-dim: #9ca3af;
            --error: #ef4444;
        }
        body { 
            background: var(--bg); 
            color: var(--text-main); 
            font-family: 'Inter', sans-serif; 
            margin: 0; padding: 24px; 
            user-select: none;
        }
        .container { display: flex; flex-direction: column; gap: 16px; }
        header { margin-bottom: 8px; }
        h1 { font-size: 18px; font-weight: 600; margin: 0; color: var(--accent); }
        .field-label { font-size: 11px; text-transform: uppercase; color: var(--text-dim); margin-bottom: 6px; }
        textarea { 
            width: 100%; height: 160px; 
            background: var(--surface); border: 1px solid #2d3139; 
            color: #fff; padding: 12px; border-radius: 8px; 
            resize: none; font-family: 'Fira Code', monospace; font-size: 13px;
            box-sizing: border-box; outline: none;
        }
        textarea:focus { border-color: var(--accent); }
        .controls { display: flex; gap: 12px; }
        button { 
            flex: 1; padding: 12px; border: none; border-radius: 6px; 
            cursor: pointer; font-weight: 600; font-size: 13px;
            background: #2d3139; color: white; transition: 0.2s;
        }
        button.primary { background: var(--accent); }
        button.primary:hover { background: #2563eb; }
    </style>
</head>
<body>
    <div class="container">
        <header><h1>Base64 Encode/Decode</h1></header>
        <div>
            <div class="field-label">Input Source</div>
            <textarea id="input" spellcheck="false"></textarea>
        </div>
        <div class="controls">
            <button class="primary" onclick="invoke('encode')">Encode</button>
            <button class="primary" onclick="invoke('decode')">Decode</button>
            <button onclick="clearAll()">Clear</button>
        </div>
        <div>
            <div class="field-label">Output</div>
            <textarea id="output" readonly spellcheck="false"></textarea>
        </div>
    </div>
    <script>
        async function invoke(mode) {
            const input = document.getElementById('input').value;
            const output = document.getElementById('output');
            if (!input.trim()) return;
            try {
                const result = await pywebview.api.process(input, mode);
                output.value = result;
                output.style.color = result.startsWith('ERR_') ? 'var(--error)' : 'var(--text-dim)';
            } catch (err) {
                output.value = "FATAL: Bridge communication failed.";
            }
        }
        function clearAll() {
            document.getElementById('input').value = '';
            document.getElementById('output').value = '';
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    initialize_application()
