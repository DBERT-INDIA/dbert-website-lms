#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

# 1. In production CGI, keep bytecode caching enabled for faster startup
sys.dont_write_bytecode = False

# 2. Force unbuffered output so headers and SSE chunks flush immediately
os.environ["PYTHONUNBUFFERED"] = "1"
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

# 3. Resolve application directory
# Can be overridden by .htaccess 'SetEnv DBERT_APP_DIR /home/user/dbert-portal'
APP_DIR = os.environ.get("DBERT_APP_DIR") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 4. Check for virtual environment site-packages (in app directory or home directory)
home_dir = os.path.expanduser("~")
potential_sites = [
    os.path.join(APP_DIR, "venv", "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages"),
    os.path.join(home_dir, "virtualenv", "dbert-portal", f"{sys.version_info.major}.{sys.version_info.minor}", "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages"),
    os.path.join(home_dir, "venv", "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages"),
    os.path.join(home_dir, ".local", "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages"),
    os.path.join(APP_DIR, "vendor"),
]

for p in potential_sites:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

os.chdir(APP_DIR)

# 5. Diagnostic Wrapper (avoids blind 500 errors during initial host setup)
try:
    from wsgiref.handlers import CGIHandler
    from app import app

    # ProxyFix to handle CGI SCRIPT_NAME correctly
    class CGIProxyFix(object):
        def __init__(self, wsgi_app):
            self.wsgi_app = wsgi_app
        def __call__(self, environ, start_response):
            environ["SCRIPT_NAME"] = ""
            return self.wsgi_app(environ, start_response)

    app.wsgi_app = CGIProxyFix(app.wsgi_app)

    if __name__ == "__main__":
        CGIHandler().run(app)

except Exception as e:
    # If a critical import or configuration error happens, output valid HTTP headers
    import traceback
    sys.stdout.write("Status: 500 Internal Server Error\r\n")
    sys.stdout.write("Content-Type: text/plain; charset=utf-8\r\n\r\n")
    sys.stdout.write("DBERT CGI Gateway Initialization Error:\r\n\r\n")
    sys.stdout.write(traceback.format_exc())
