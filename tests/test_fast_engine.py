import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fast_engine


def test_version_exists():
    assert isinstance(fast_engine.__version__, str)

