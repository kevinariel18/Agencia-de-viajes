import pytest
from apps.destinations.models import Destination


@pytest.mark.django_db
class TestDestination:
    def test_create_destination(self, city):
        dest = Destination.objects.create(
            city=city, name="Laguna Azul",
            description="Hermosa laguna", difficulty="EASY",
        )
        assert dest.pk is not None
        assert dest.public_code.startswith("DST-")

    def test_destination_auto_code(self, destination):
        assert destination.public_code.startswith("DST-")

    def test_destination_difficulty_choices(self, city):
        dest = Destination.objects.create(
            city=city, name="Pico Alto",
            description="Montaña difícil", difficulty="HIGH",
        )
        assert dest.difficulty == "HIGH"
