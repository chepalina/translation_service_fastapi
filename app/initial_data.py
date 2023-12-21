"""
Put here any Python code that must be runned before application startup.
It is included in `init.sh` script.

By defualt `main` create a superuser if not exists
"""

import asyncio

from sqlalchemy import select

from app.core import config, security
from app.core.session import async_session
from app.models import User


async def main() -> None:
    """Function for data initialization."""
    print("Start initial data")


if __name__ == "__main__":
    asyncio.run(main())
