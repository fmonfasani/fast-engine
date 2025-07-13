import sys
from pathlib import Path
# Ensure package can be imported when running tests via the pytest entrypoint
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
