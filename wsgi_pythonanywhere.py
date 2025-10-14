"""
WSGI Configuration for PythonAnywhere
Copy this content to: /var/www/callensxavier_pythonanywhere_com_wsgi.py
"""

import sys
import os

# ============================================================================
# CONFIGURATION - Update these paths for your PythonAnywhere account
# ============================================================================

# Your PythonAnywhere username
USERNAME = 'callensxavier'

# Project directory
project_home = f'/home/{USERNAME}/proutman'

# Virtual environment
venv_path = f'/home/{USERNAME}/proutman/venv'

# ============================================================================
# DO NOT MODIFY BELOW THIS LINE
# ============================================================================

# Add project directory to Python path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')

# For Python 3.10+, activate_this.py might not exist
# Use this alternative method:
if not os.path.exists(activate_this):
    # Add virtualenv site-packages to path
    site_packages = os.path.join(venv_path, 'lib', 'python3.10', 'site-packages')
    if os.path.exists(site_packages):
        sys.path.insert(0, site_packages)
else:
    # Traditional activation
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

# Import Flask application
from flask_app import app as application

# Optional: Set up logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log startup
logging.info(f"Proutman WSGI application started")
logging.info(f"Project home: {project_home}")
logging.info(f"Virtual env: {venv_path}")
logging.info(f"Python path: {sys.path}")
