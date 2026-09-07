from backend.app.db.session import Base
from backend.app.models.base import Base
# Import models to register them with SQLAlchemy metadata
from backend.app.models.user import User
from backend.app.models.refresh_token import RefreshToken
from backend.app.models.otp import OTP
from backend.app.models.audit import AuditLog
from backend.app.models.animal import Animal
from backend.app.models.vet import Vet
from backend.app.models.health import (
	Vaccination,
	Medication,
	Visit,
	LabTest,
	Operation,
	Illness,
	WeightHistory,
	HealthNote,
	HealthDocument,
)
from backend.app.models.clinic_review import ClinicReview
from backend.app.models.vet_tariff import VetTariff
from backend.app.models.lost_pet import LostPet
from backend.app.models.adoption import Adoption
from backend.app.models.user_location import UserLocation
from backend.app.models.notification import Notification
from backend.app.models.ai_request_log import AIRequestLog
