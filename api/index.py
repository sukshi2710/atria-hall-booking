import sys
import os

# Define root and backend directories
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
backend_dir = os.path.join(root_dir, "backend")

# Insert paths to sys.path
for path in [root_dir, backend_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

from app.main import app
