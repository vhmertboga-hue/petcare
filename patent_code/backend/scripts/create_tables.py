import os
from sqlalchemy import create_engine
from backend.app.db.session import Base


def sync_url(url: str) -> str:
    # convert async driver urls to sync for create_all
    if url.startswith("sqlite+aiosqlite:"):
        return url.replace("+aiosqlite", "")
    if "+asyncpg" in url:
        return url.replace("+asyncpg", "")
    return url


def main():
    url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    surl = sync_url(url)
    engine = create_engine(surl)
    # import modules so models are registered
    import backend.app.models.user
    import backend.app.models.session
    import backend.app.models.audit
    import backend.app.models.file
    import backend.app.models.animal
    import backend.app.models.health

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
