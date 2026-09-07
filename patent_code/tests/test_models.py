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


def test_vet_model_has_fields():
    from backend.app.models.vet import Vet

    attrs = {c.name for c in Vet.__table__.columns}
    expected = {"id", "name", "latitude", "longitude", "emergency", "open_24_7"}
    assert expected.issubset(attrs)


def test_clinic_review_model_import():
    from backend.app.models.clinic_review import ClinicReview

    assert hasattr(ClinicReview, "clinic_id")


def test_vet_tariff_model_import():
    from backend.app.models.vet_tariff import VetTariff

    assert hasattr(VetTariff, "province")


def test_phase6_models_import():
    from backend.app.models.lost_pet import LostPet
    from backend.app.models.adoption import Adoption
    from backend.app.models.user_location import UserLocation
    from backend.app.models.notification import Notification

    assert hasattr(LostPet, "species")
    assert hasattr(Adoption, "status")
    assert hasattr(UserLocation, "latitude")
    assert hasattr(Notification, "type")
