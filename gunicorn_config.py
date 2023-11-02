import os
from config.config import PORT

white_cane_port = os.getenv("WHITE_CANE_PORT", PORT)

workers = int(os.environ.get("GUNICORN_PROCESSES", "2"))

threads = int(os.environ.get("GUNICORN_THREADS", "4"))

bind = os.environ.get("GUNICORN_BIND", f"0.0.0.0:{white_cane_port}")


forwarded_allow_ips = "*"

secure_scheme_headers = {"X-Forwarded-Proto": "https"}
