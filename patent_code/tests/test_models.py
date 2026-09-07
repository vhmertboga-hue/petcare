import inspect

from backend.app import models


def test_animal_model_has_fields():
    from backend.app.models.animal import Animal

    attrs = {c.name for c in Animal.__table__.columns}
    expected = {"id", "owner_id", "name", "species", "microchip"}
    assert expected.issubset(attrs)


def test_file_model_has_fields():
    from backend.app.models.file import File

    attrs = {c.name for c in File.__table__.columns}
    expected = {"id", "filename", "file_data"}
    assert expected.issubset(attrs)


def test_health_models_defined():
    # ensure health models import without DB
    from backend.app.models.health import Vaccination, Medication

    assert inspect.isclass(Vaccination)
    assert inspect.isclass(Medication)
