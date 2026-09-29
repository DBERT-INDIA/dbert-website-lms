# This file tells Passenger (cPanel WSGI server) where to find the app.
# It is an alias for wsgi.py — both work identically.
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wsgi import application
