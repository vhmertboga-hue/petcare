from backend.app.models import Business


def test_business_class():
    assert getattr(Business, "__tablename__", None) == "businesses"
