import asyncio
import logging
from typing import Any, Callable, TypeVar
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')

async def retry_async(
    func: Callable[..., T], 
    max_retries: int = 3, 
    delay: float = 1.0,
    *args, 
    **kwargs
) -> T:
    """Retry funcion async con delay exponencial"""
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            wait_time = delay * (2 ** attempt)
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)

def ensure_directory(path: Path):
    """Crear directorio si no existe"""
    path.mkdir(parents=True, exist_ok=True)
