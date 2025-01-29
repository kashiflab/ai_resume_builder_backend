import sys
print("Python version:", sys.version)
print("Attempting imports...")

try:
    from app.core.config import get_settings
    print("Successfully imported get_settings")
except Exception as e:
    print("Error importing get_settings:", str(e))

try:
    from app.core import security
    print("Successfully imported security")
except Exception as e:
    print("Error importing security:", str(e))

try:
    from app.models import schemas
    print("Successfully imported schemas")
except Exception as e:
    print("Error importing schemas:", str(e)) 