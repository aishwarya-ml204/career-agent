import http.server
import threading
import subprocess
import webbrowser
import time
import base64
import urllib.request
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent

SPLASH_PORT = 8501
STREAMLIT_PORT = 8502

PYTHON_EXE = PROJECT_DIR / "venv" / "Scripts" / "python.exe"

IMAGE_PATH = PROJECT_DIR / "app" / "assets" / "career_compass_hero.png"


# ------------------------------------------------------------
# IMAGE
# ------------------------------------------------------------

def get_image():

    if not IMAGE_PATH.exists():
        print("IMAGE NOT FOUND:")
        print(IMAGE_PATH)
        return ""

    with open(IMAGE_PATH, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    return f"""
    <img src="data:image/png;base64,{data}" class="hero">
    """


# ------------------------------------------------------------
# SPLASH PAGE
# ------------------------------------------------------------

def splash_html():

    image = get_image()

    return f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<title>Career Compass</title>

<style>

* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
    width: 100%;
    height: 100%;
}}

body {{

    background:
        radial-gradient(
            circle at 80% 20%,
            rgba(63, 105, 235, 0.22),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #07111f,
            #0c1930,
            #111d38
        );

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    color: white;

    display: flex;

    justify-content: center;

    align-items: center;

    overflow: hidden;
}}

.wrapper {{

    width: 90%;

    max-width: 1000px;

    text-align: center;
}}

.hero {{

    width: min(600px, 80vw);

    max-height: 55vh;

    object-fit: contain;

    border-radius: 24px;

    box-shadow:
        0 30px 80px rgba(0,0,0,.45);

    animation:
        appear 1s ease-out,
        float 5s ease-in-out infinite;
}}

.title {{

    margin-top: 24px;

    font-size: 52px;

    font-weight: 800;

    letter-spacing: -2px;
}}

.subtitle {{

    margin-top: 8px;

    font-size: 15px;

    letter-spacing: 3px;

    text-transform: uppercase;

    color: #9fb3d9;
}}

.loading {{

    margin-top: 28px;

    color: #c9d6ef;

    font-size: 14px;

    display: flex;

    align-items: center;

    justify-content: center;

    gap: 10px;
}}

.spinner {{

    width: 18px;

    height: 18px;

    border-radius: 50%;

    border: 2px solid rgba(255,255,255,.25);

    border-top-color: #4d7cff;

    animation: spin .8s linear infinite;
}}

@keyframes spin {{

    to {{
        transform: rotate(360deg);
    }}

}}

@keyframes appear {{

    from {{
        opacity: 0;
        transform: scale(.94);
    }}

    to {{
        opacity: 1;
        transform: scale(1);
    }}

}}

@keyframes float {{

    0%, 100% {{
        transform: translateY(0);
    }}

    50% {{
        transform: translateY(-8px);
    }}

}}

</style>

</head>

<body>

<div class="wrapper">

    {image}

    <div class="title">
        Career Compass
    </div>

    <div class="subtitle">
        Intelligent Career Navigation
    </div>

    <div class="loading">

        <div class="spinner"></div>

        <span>
            Preparing your personalized career experience...
        </span>

    </div>

</div>

</body>

</html>
"""


# ------------------------------------------------------------
# SPLASH SERVER
# ------------------------------------------------------------

class SplashHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        html = splash_html()

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Cache-Control",
            "no-cache, no-store, must-revalidate"
        )

        self.end_headers()

        self.wfile.write(
            html.encode("utf-8")
        )

    def log_message(self, format, *args):
        pass


def start_splash():

    server = http.server.ThreadingHTTPServer(
        ("localhost", SPLASH_PORT),
        SplashHandler
    )

    print(
        f"Splash: http://localhost:{SPLASH_PORT}"
    )

    server.serve_forever()


# ------------------------------------------------------------
# START STREAMLIT
# ------------------------------------------------------------

def start_streamlit():

    print()
    print("Starting Career Compass...")
    print("Python:", PYTHON_EXE)
    print("Python exists:", PYTHON_EXE.exists())
    print("Image:", IMAGE_PATH)
    print("Image exists:", IMAGE_PATH.exists())
    print()

    subprocess.Popen(
        [
            str(PYTHON_EXE),

            "-m",
            "streamlit",

            "run",

            "app/app.py",

            "--server.port",
            str(STREAMLIT_PORT),

            "--server.address",
            "localhost",

            "--server.headless",
            "true",

            "--browser.gatherUsageStats",
            "false"
        ],

        cwd=str(PROJECT_DIR)
    )


# ------------------------------------------------------------
# WAIT FOR STREAMLIT
# ------------------------------------------------------------

def wait_for_streamlit():

    url = f"http://localhost:{STREAMLIT_PORT}"

    print("Waiting for Streamlit...")

    while True:

        try:

            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "CareerCompassLauncher"
                }
            )

            response = urllib.request.urlopen(
                request,
                timeout=2
            )

            if response.status == 200:

                print("Streamlit is responding.")

                return True

        except Exception:
            pass

        time.sleep(1)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("======================================")
    print("          CAREER COMPASS")
    print("======================================")
    print()

    # Start splash FIRST
    splash_thread = threading.Thread(
        target=start_splash,
        daemon=True
    )

    splash_thread.start()

    time.sleep(0.5)

    # Open image immediately
    webbrowser.open(
        f"http://localhost:{SPLASH_PORT}"
    )

    # Start Streamlit in background
    streamlit_thread = threading.Thread(
        target=start_streamlit,
        daemon=True
    )

    streamlit_thread.start()

    # Wait until Streamlit responds
    wait_for_streamlit()

    print("Career Compass is ready.")

    # Give browser a moment to display splash
    time.sleep(2)

    # Now open actual application
    webbrowser.open(
        f"http://localhost:{STREAMLIT_PORT}"
    )

    print(
        f"Application: http://localhost:{STREAMLIT_PORT}"
    )

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("Career Compass stopped.")