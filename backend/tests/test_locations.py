import pytest
from apps.locations.models import Country, City


@pytest.mark.django_db
class TestCountry:
    def test_create_country(self):
        c = Country.objects.create(code="FR", name="Francia")
        assert c.pk is not None
        assert str(c) == "Francia (FR)"

    def test_country_code_unique(self, country):
        with pytest.raises(Exception):
            Country.objects.create(code=country.code, name="Otro")

    def test_country_name_unique(self, country):
        with pytest.raises(Exception):
            Country.objects.create(code="XX", name=country.name)


@pytest.mark.django_db
class TestCity:
    def test_create_city(self, country):
        city = City.objects.create(country=country, name="NuevaCity")
        assert city.pk is not None
        assert city.country == country

    def test_city_str(self, city):
        assert city.country.name in str(city)
