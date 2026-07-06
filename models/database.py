import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


_ENGINE = None
_SESSION_FACTORY = None


def _sqlite_path() -> Path:
    return Path(os.getenv("FORWARD_DB_PATH", "./db/forward.db"))


def _engine_config():
    turso_url = os.getenv("TURSO_DATABASE_URL")
    turso_token = os.getenv("TURSO_AUTH_TOKEN")
    if turso_url and turso_token:
        separator = "&" if "?" in turso_url else "?"
        return (
            f"sqlite+{turso_url}{separator}secure=true",
            {"auth_token": turso_token},
        )

    db_path = _sqlite_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return (
        f"sqlite:///{db_path}",
        {"check_same_thread": False},
    )


def get_engine():
    global _ENGINE
    if _ENGINE is None:
        url, connect_args = _engine_config()
        _ENGINE = create_engine(url, connect_args=connect_args)
    return _ENGINE


def get_session_factory():
    global _SESSION_FACTORY
    if _SESSION_FACTORY is None:
        _SESSION_FACTORY = sessionmaker(bind=get_engine())
    return _SESSION_FACTORY
