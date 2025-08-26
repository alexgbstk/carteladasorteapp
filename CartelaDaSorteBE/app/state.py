import asyncio
from typing import Optional
from .models import Cartela

cartela_atual: Optional[Cartela] = None
lock = asyncio.Lock()
