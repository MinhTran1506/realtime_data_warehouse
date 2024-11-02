from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the secret key from the environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
print(SECRET_KEY)
if not SECRET_KEY:
    raise RuntimeError("A secret key is required to use CSRF1234.")

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

ENABLE_PROXY_FIX = True