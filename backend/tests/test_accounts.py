import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestClientRegister:
    def test_register_success(self, client):
        resp = client.post(reverse("register"), {
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "nuevo@test.com",
            "password1": "TestPass123*",
            "password2": "TestPass123*",
        })
        # Should redirect after successful register
        assert resp.status_code == 302
        from apps.accounts.models import User
        assert User.objects.filter(email="nuevo@test.com").exists()

    def test_register_duplicate_email(self, client, client_user):
        resp = client.post(reverse("register"), {
            "first_name": "Otro",
            "last_name": "Usuario",
            "email": client_user.email,
            "password1": "TestPass123*",
            "password2": "TestPass123*",
        })
        # Form re-renders with errors
        assert resp.status_code == 200

    def test_register_password_mismatch(self, client):
        resp = client.post(reverse("register"), {
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "otro@test.com",
            "password1": "TestPass123*",
            "password2": "Different456*",
        })
        assert resp.status_code == 200


@pytest.mark.django_db
class TestLogin:
    def test_login_success_admin_redirects_to_admin(self, client, admin_user):
        resp = client.post(reverse("login"), {
            "username": admin_user.email,
            "password": "Admin123*",
        })
        assert resp.status_code == 302
        assert "/administracion/" in resp["Location"]

    def test_login_success_client_redirects_to_client(self, client, client_user):
        resp = client.post(reverse("login"), {
            "username": client_user.email,
            "password": "Cliente123*",
        })
        assert resp.status_code == 302
        assert "/cliente/" in resp["Location"]

    def test_login_wrong_password_returns_form(self, client, client_user):
        resp = client.post(reverse("login"), {
            "username": client_user.email,
            "password": "wrongpassword",
        })
        assert resp.status_code == 200

    def test_login_nonexistent_email(self, client):
        resp = client.post(reverse("login"), {
            "username": "noexiste@test.com",
            "password": "somepass",
        })
        assert resp.status_code == 200


@pytest.mark.django_db
class TestAuthProtection:
    def test_admin_dashboard_requires_login(self, client):
        resp = client.get("/administracion/")
        assert resp.status_code in (302, 403)

    def test_client_packages_requires_login(self, client):
        resp = client.get("/cliente/paquetes/")
        assert resp.status_code in (302, 403)

    def test_client_cannot_access_admin_dashboard(self, client, client_user):
        client.force_login(client_user)
        resp = client.get("/administracion/")
        assert resp.status_code in (302, 403)

    def test_admin_cannot_access_client_reservation_create(self, client, admin_user, departure):
        client.force_login(admin_user)
        resp = client.get(f"/cliente/reservas/nueva/{departure.pk}/")
        assert resp.status_code in (302, 403)

    def test_unauthenticated_cannot_access_reservations(self, client):
        resp = client.get("/cliente/reservas/")
        assert resp.status_code in (302, 403)
