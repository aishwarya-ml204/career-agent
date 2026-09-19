import base64
import os
import subprocess
import threading
import time
import urllib.request
import webbrowser

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

IMAGE_PATH = (
    PROJECT_DIR
    / "app"
    / "assets"
    / "career_compass_hero.png"
)

SPLASH_PORT = 8501
STREAMLIT_PORT = 8502


# ============================================================
# LOAD HERO IMAGE
# ============================================================

if IMAGE_PATH.exists():

    image_bytes = IMAGE_PATH.read_bytes()

    image_base64 = base64.b64encode(
        image_bytes
    ).decode()

else:

    image_base64 = ""


# ============================================================
# SPLASH PAGE
# ============================================================

HTML = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Career Compass</title>


<style>

* {{
    box-sizing: border-box;
}}


html,
body {{

    margin: 0;

    padding: 0;

    width: 100%;

    height: 100%;

    overflow: hidden;

    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}}


body {{

    background: #07111F;
}}


.splash {{

    position: relative;

    width: 100vw;

    height: 100vh;

    background-image:
        linear-gradient(
            90deg,
            rgba(4, 12, 27, 0.82),
            rgba(4, 12, 27, 0.30),
            rgba(4, 12, 27, 0.12)
        ),
        url("data:image/png;base64,{image_base64}");

    background-size: cover;

    background-position: center;

    display: flex;

    align-items: center;

    padding-left: 9vw;
}}


.content {{

    max-width: 650px;

    color: white;

    animation: appear 1.2s ease-out;
}}


@keyframes appear {{

    from {{
        opacity: 0;
        transform: translateY(20px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}

}}


.badge {{

    display: inline-flex;

    align-items: center;

    padding: 9px 16px;

    border-radius: 30px;

    background: rgba(255,255,255,0.11);

    border: 1px solid rgba(255,255,255,0.22);

    backdrop-filter: blur(12px);

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.2px;

    color: #DDE8FF;
}}


.logo-title {{

    margin-top: 24px;

    font-size: clamp(52px, 7vw, 88px);

    line-height: 0.95;

    font-weight: 900;

    letter-spacing: -4px;
}}


.logo-title span {{

    background:
        linear-gradient(
            90deg,
            #78A9FF,
            #9E7BFF,
            #D8B5FF
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}}


.subtitle {{

    margin-top: 25px;

    font-size: 20px;

    line-height: 1.55;

    color: #E0E8F7;

    max-width: 570px;
}}


.loading {{

    margin-top: 38px;

    display: flex;

    align-items: center;

    gap: 14px;

    color: #C9D5EA;

    font-size: 12px;

    font-weight: 650;

    letter-spacing: 0.5px;
}}


.loader {{

    width: 25px;

    height: 25px;

    border-radius: 50%;

    border: 2px solid rgba(255,255,255,0.20);

    border-top-color: #78A9FF;

    animation: spin 0.8s linear infinite;
}}


@keyframes spin {{

    to {{
        transform: rotate(360deg);
    }}

}}


.progress {{

    margin-top: 18px;

    width: 320px;

    height: 3px;

    background: rgba(255,255,255,0.15);

    border-radius: 20px;

    overflow: hidden;
}}


.progress-bar {{

    height: 100%;

    width: 0%;

    background:
        linear-gradient(
            90deg,
            #3B82F6,
            #8B5CF6
        );

    border-radius: 20px;

    animation: loading 3.5s ease-in-out forwards;
}}


@keyframes loading {{

    0% {{
        width: 0%;
    }}

    50% {{
        width: 55%;
    }}

    80% {{
        width: 78%;
    }}

    100% {{
        width: 100%;
    }}

}}


.footer {{

    position: absolute;

    bottom: 28px;

    left: 9vw;

    color: rgba(255,255,255,0.55);

    font-size: 10px;

    letter-spacing: 0.7px;
}}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {{

    .splash {{
        padding: 35px;
        align-items: flex-end;
        padding-bottom: 90px;
    }}

    .logo-title {{
        font-size: 54px;
    }}

    .subtitle {{
        font-size: 16px;
    }}

    .progress {{
        width: 240px;
    }}

    .footer {{
        left: 35px;
    }}

}}

</style>

</head>


<body>


<div class="splash">


    <div class="content">


        <div class="badge">
            ✦ AI-POWERED CAREER INTELLIGENCE
        </div>


        <div class="logo-title">

            Career
            <br>

            <span>Compass.</span>

        </div>


        <div class="subtitle">

            Navigate your future with clarity.

            Discover opportunities, understand your
            skill gaps, and build the career path
            that moves you forward.

        </div>


        <div class="loading">

            <div class="loader"></div>

            <span id="status">
                Preparing your career journey...
            </span>

        </div>


        <div class="progress">

            <div class="progress-bar"></div>

        </div>


    </div>


    <div class="footer">

        EXPLORE &nbsp; • &nbsp;
        ANALYZE &nbsp; • &nbsp;
        DISCOVER &nbsp; • &nbsp;
        GROW

    </div>


</div>


<script>

async function checkStreamlit() {{

    try {{

        const response = await fetch(
            "/ready",
            {{
                cache: "no-store"
            }}
        );

        if (response.ok) {{

            const data =
                await response.text();

            if (data === "READY") {{

                document.getElementById(
                    "status"
                ).innerText =
                    "Your career compass is ready...";

                setTimeout(
                    function() {{

                        window.location.href =
                            "http://localhost:{STREAMLIT_PORT}";

                    }},
                    500
                );

                return;

            }}

        }}

    }} catch (error) {{

        // Streamlit is still starting.
    }}


    setTimeout(
        checkStreamlit,
        500
    );
}}


checkStreamlit();

</script>


</body>

</html>
"""


# ============================================================
# CHECK STREAMLIT STATUS
# ============================================================

def streamlit_is_ready():

    try:

        url = (
            f"http://localhost:{STREAMLIT_PORT}"
            "/_stcore/health"
        )

        with urllib.request.urlopen(
            url,
            timeout=0.5
        ) as response:

            return response.status == 200

    except Exception:

        return False


# ============================================================
# SPLASH SERVER
# ============================================================

class SplashHandler(
    BaseHTTPRequestHandler
):

    def do_GET(self):

        if self.path == "/ready":

            if streamlit_is_ready():

                self.send_response(200)

                self.send_header(
                    "Content-Type",
                    "text/plain"
                )

                self.end_headers()

                self.wfile.write(
                    b"READY"
                )

            else:

                self.send_response(200)

                self.send_header(
                    "Content-Type",
                    "text/plain"
                )

                self.end_headers()

                self.wfile.write(
                    b"LOADING"
                )

            return


        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.end_headers()

        self.wfile.write(
            HTML.encode("utf-8")
        )


    def log_message(
        self,
        format,
        *args
    ):

        return


# ============================================================
# START STREAMLIT
# ============================================================

def start_streamlit():

    subprocess.Popen(
        [
            "python",
            "-m",
            "streamlit",
            "run",
            "app/app.py",
            "--server.port",
            str(STREAMLIT_PORT),
            "--server.headless",
            "true"
        ],
        cwd=PROJECT_DIR
    )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("       CAREER COMPASS")
    print("=" * 55)
    print()
    print("Starting Career Compass...")
    print()

    # Start Streamlit in background
    threading.Thread(
        target=start_streamlit,
        daemon=True
    ).start()

    # Start splash server
    server = HTTPServer(
        ("localhost", SPLASH_PORT),
        SplashHandler
    )

    # Open splash page immediately
    threading.Timer(
        0.5,
        lambda: webbrowser.open(
            f"http://localhost:{SPLASH_PORT}"
        )
    ).start()

    print(
        f"Splash screen: "
        f"http://localhost:{SPLASH_PORT}"
    )

    print(
        f"Streamlit app: "
        f"http://localhost:{STREAMLIT_PORT}"
    )

    print()
    print("Career Compass is starting...")
    print()

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print()
        print("Career Compass stopped.")

        server.server_close()