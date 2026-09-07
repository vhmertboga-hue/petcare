import os
import sys
import pathlib
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure the project root is on sys.path so `import backend` works when pytest
# is invoked from different CWDs or virtualenvs.
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.models.base import Base
from backend.app.db import session as db_session

# Create and patch the test database at import time so that any imports of the
# application modules during pytest collection will use the testing engine.
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite+pysqlite:///:memory:")
# Use StaticPool and disable same-thread checks so the in-memory SQLite database
# can be shared across threads used by the testclient.
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

# Patch the SessionLocal used by the app modules
db_session.engine = engine
db_session.SessionLocal = TestingSessionLocal


@pytest.fixture(scope="session", autouse=True)
def teardown_test_db():
    # Nothing to do on setup (done at import time); teardown will drop all tables
    yield
    Base.metadata.drop_all(bind=engine)
