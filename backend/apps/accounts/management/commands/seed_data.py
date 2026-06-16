from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
import datetime


class Command(BaseCommand):
    help = "Carga datos iniciales de prueba"

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando seed de datos...")
        self._seed_countries()
        self._seed_cities()
        self._seed_users()
        self._seed_destinations()
        self._seed_packages()
        self._seed_departures()
        self._seed_reservations()
        self.stdout.write(self.style.SUCCESS("\n✅ Seed completado exitosamente."))

    # ── Países ────────────────────────────────────────────────────────────────
    def _seed_countries(self):
        from apps.locations.models import Country
        countries = [
            ("EC", "Ecuador"), ("PE", "Perú"), ("CO", "Colombia"),
            ("AR", "Argentina"), ("MX", "México"), ("ES", "España"),
            ("IT", "Italia"), ("BO", "Bolivia"),
        ]
        for code, name in countries:
            Country.objects.get_or_create(code=code, defaults={"name": name})
        self.stdout.write("  ✓ 8 países")

    # ── Ciudades ──────────────────────────────────────────────────────────────
    def _seed_cities(self):
        from apps.locations.models import Country, City
        cities = [
            ("EC", "Quito",        "+593", "170150", "Sierra"),
            ("EC", "Guayaquil",    "+593", "090150", "Costa"),
            ("EC", "Cuenca",       "+593", "010150", "Sierra"),
            ("PE", "Lima",         "+51",  "15001",  "Costa"),
            ("PE", "Cusco",        "+51",  "08001",  "Sierra"),
            ("CO", "Bogotá",       "+57",  "110111", "Andina"),
            ("CO", "Cartagena",    "+57",  "130001", "Caribe"),
            ("AR", "Buenos Aires", "+54",  "1000",   "Pampa"),
            ("AR", "Bariloche",    "+54",  "8400",   "Patagonia"),
            ("MX", "Cancún",       "+52",  "77500",  "Caribe"),
            ("ES", "Madrid",       "+34",  "28001",  "Centro"),
            ("IT", "Roma",         "+39",  "00100",  "Lazio"),
        ]
        for code, name, prefix, postal, zone in cities:
            country = Country.objects.get(code=code)
            City.objects.get_or_create(
                country=country, name=name,
                defaults={"phone_prefix": prefix, "postal_code": postal, "region_zone": zone},
            )
        self.stdout.write("  ✓ 12 ciudades")

    # ── Usuarios ──────────────────────────────────────────────────────────────
    def _seed_users(self):
        from apps.accounts.models import User
        from apps.locations.models import City

        quito  = City.objects.filter(name="Quito").first()
        lima   = City.objects.filter(name="Lima").first()
        bogota = City.objects.filter(name="Bogotá").first()

        # Administrador
        if not User.objects.filter(email="admin@tourpack.com").exists():
            admin = User(
                username="admin@tourpack.com",
                email="admin@tourpack.com",
                first_name="Carlos",
                last_name="Administrador",
                role=User.Role.ADMIN,
                status=User.Status.ACTIVE,
                city=quito,
                phone="+593991234567",
                is_staff=True,
                is_superuser=True,
            )
            admin.set_password("Admin123*")
            admin.save()

        # 9 clientes
        clients_data = [
            ("cliente@tourpack.com",    "Cliente123*", "Ana",       "García",   quito),
            ("maria@tourpack.com",      "Cliente123*", "María",     "López",    lima),
            ("pedro@tourpack.com",      "Cliente123*", "Pedro",     "Ramírez",  bogota),
            ("lucia@tourpack.com",      "Cliente123*", "Lucía",     "Torres",   quito),
            ("jorge@tourpack.com",      "Cliente123*", "Jorge",     "Mendoza",  lima),
            ("sofia@tourpack.com",      "Cliente123*", "Sofía",     "Vargas",   bogota),
            ("andres@tourpack.com",     "Cliente123*", "Andrés",    "Castro",   quito),
            ("valentina@tourpack.com",  "Cliente123*", "Valentina", "Ríos",     lima),
            ("miguel@tourpack.com",     "Cliente123*", "Miguel",    "Herrera",  bogota),
        ]
        for email, pwd, fn, ln, city in clients_data:
            if not User.objects.filter(email=email).exists():
                u = User(
                    username=email,
                    email=email,
                    first_name=fn,
                    last_name=ln,
                    role=User.Role.CLIENT,
                    status=User.Status.ACTIVE,
                    city=city,
                    phone="+593999000001",
                )
                u.set_password(pwd)
                u.save()
        self.stdout.write("  ✓ 1 admin + 9 clientes")

    # ── Destinos ──────────────────────────────────────────────────────────────
    def _seed_destinations(self):
        from apps.destinations.models import Destination
        from apps.locations.models import City

        destinations_data = [
            ("Cusco",        "Machu Picchu",      "Ciudadela inca en los Andes peruanos",          "Ruinas incas, llamas, montañas",         "Templado", "Dic-Mar",       "MODERATE"),
            ("Quito",        "Galápagos",          "Archipiélago de biodiversidad única",           "Tortugas gigantes, lobos marinos",        "Tropical", "Jun-Nov",       "EASY"),
            ("Bariloche",    "Patagonia",           "Paisajes glaciares y lagos del sur argentino",  "Lagos, glaciares, trekking extremo",      "Frío",     "Ene-Mar",       "HIGH"),
            ("Cartagena",    "Cartagena Colonial",  "Ciudad histórica con arquitectura colonial",   "Murallas, plazas, playas del Caribe",     "Cálido",   "Dic-Abr",       "EASY"),
            ("Cancún",       "Cancún",              "Resort caribeño con playas de arena blanca",    "Playas, cenotes, Chichen Itzá",           "Cálido",   "Nov-Abr",       "EASY"),
            ("Madrid",       "Madrid",              "Capital española con arte y gastronomía",       "Prado, Retiro, flamenco",                 "Templado", "Mar-Jun",       "EASY"),
            ("Roma",         "Venecia",             "Ciudad de canales y arte renacentista",         "Góndolas, San Marcos, Rialto",            "Templado", "Abr-Oct",       "EASY"),
            ("Quito",        "Quito Colonial",      "Centro histórico Patrimonio de la Humanidad",  "Iglesias, plazas coloniales, mercados",   "Templado", "Todo el año",   "EASY"),
            ("Buenos Aires", "Buenos Aires",        "Capital del tango y la gastronomía porteña",   "Tango, Recoleta, La Boca, San Telmo",     "Templado", "Mar-May",       "EASY"),
            ("Bogotá",       "Bogotá",              "Capital colombiana con museos y cultura",       "Monserrate, La Candelaria, museos",       "Templado", "Dic-Mar",       "EASY"),
        ]
        for city_name, name, desc, attractions, climate, season, difficulty in destinations_data:
            city = City.objects.filter(name=city_name).first()
            if city and not Destination.objects.filter(name=name).exists():
                Destination.objects.create(
                    city=city, name=name, description=desc,
                    attractions=attractions, climate=climate,
                    season=season, difficulty=difficulty,
                )
        self.stdout.write("  ✓ 10 destinos")

    # ── Paquetes ──────────────────────────────────────────────────────────────
    def _seed_packages(self):
        from apps.packages.models import TourPackage, PackageDestination
        from apps.destinations.models import Destination

        # Imágenes de Unsplash (libres de uso, formato directo)
        packages_data = [
            (
                "Maravillas de Machu Picchu",
                "Descubre la ciudadela inca más famosa del mundo",
                7, 6, Decimal("1200.00"), "ADVENTURE",
                ["Machu Picchu"],
                "https://images.unsplash.com/photo-1526392060635-9d6019884377?w=800&q=80",
            ),
            (
                "Caribe Colombiano",
                "Playas y cultura en la hermosa Cartagena",
                5, 4, Decimal("850.00"), "STANDARD",
                ["Cartagena Colonial"],
                "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80",
            ),
            (
                "Patagonia Extrema",
                "Aventura en los glaciares del fin del mundo",
                10, 9, Decimal("2500.00"), "ADVENTURE",
                ["Patagonia"],
                "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800&q=80",
            ),
            (
                "Cancún Todo Incluido",
                "Relax total en el paraíso caribeño",
                7, 6, Decimal("1500.00"), "PREMIUM",
                ["Cancún"],
                "https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?w=800&q=80",
            ),
            (
                "Europa Clásica",
                "Lo mejor de España e Italia en un solo viaje",
                12, 11, Decimal("3200.00"), "LUXURY",
                ["Madrid", "Venecia"],
                "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=800&q=80",
            ),
            (
                "Galápagos Único",
                "Explora el laboratorio natural de Darwin",
                8, 7, Decimal("2800.00"), "ECOLOGICAL",
                ["Galápagos"],
                "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=80",
            ),
            (
                "Buenos Aires Cultural",
                "Tango, arte y gastronomía porteña",
                6, 5, Decimal("1100.00"), "STANDARD",
                ["Buenos Aires"],
                "https://images.unsplash.com/photo-1589909202802-8f4aadce1849?w=800&q=80",
            ),
            (
                "Venecia Romántica",
                "La ciudad de los canales para parejas y viajeros",
                5, 4, Decimal("1800.00"), "LUXURY",
                ["Venecia"],
                "https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=800&q=80",
            ),
            (
                "Ruta Azteca",
                "Cultura prehispánica y playas del Caribe mexicano",
                9, 8, Decimal("1600.00"), "STANDARD",
                ["Cancún"],
                "https://images.unsplash.com/photo-1518638150340-f706e86654de?w=800&q=80",
            ),
            (
                "Ecuador Sierra y Costa",
                "Lo mejor de Ecuador: sierra, costa y Galápagos",
                8, 7, Decimal("900.00"), "ECOLOGICAL",
                ["Galápagos", "Quito Colonial"],
                "https://images.unsplash.com/photo-1531065208531-4036c0dba3ca?w=800&q=80",
            ),
        ]

        for name, desc, days, nights, price, category, dest_names, img_url in packages_data:
            pkg, created = TourPackage.objects.get_or_create(
                name=name,
                defaults={
                    "description": desc,
                    "days": days,
                    "nights": nights,
                    "price": price,
                    "category": category,
                    "image_url": img_url,
                    "includes": "Transporte aéreo, alojamiento, guía bilingüe, desayunos incluidos.",
                    "stops": f"Día 1: Llegada y bienvenida.\nDías 2-{days - 1}: Recorrido por destinos.\nDía {days}: Traslado y regreso.",
                },
            )
            # Actualizar image_url si el paquete ya existía sin imagen o cambió
            if not created and (not pkg.image_url or not pkg.image):
                pkg.image_url = img_url
                pkg.save(update_fields=["image_url"])

            if created:
                for order, dest_name in enumerate(dest_names, start=1):
                    dest = Destination.objects.filter(name=dest_name).first()
                    if dest:
                        PackageDestination.objects.get_or_create(
                            package=pkg,
                            destination=dest,
                            defaults={"visit_order": order},
                        )
        self.stdout.write("  ✓ 10 paquetes turísticos con imágenes")

    # ── Fechas de salida ──────────────────────────────────────────────────────
    def _seed_departures(self):
        from apps.packages.models import TourPackage, Departure
        today = timezone.now().date()
        created_count = 0

        for pkg in TourPackage.objects.all():
            for delta in [30, 60, 90]:
                dep_date = today + datetime.timedelta(days=delta)
                _, created = Departure.objects.get_or_create(
                    package=pkg,
                    departure_date=dep_date,
                    defaults={"capacity": 20, "status": "AVAILABLE"},
                )
                if created:
                    created_count += 1

        self.stdout.write(f"  ✓ {created_count} fechas de salida (3 por paquete)")

    # ── Reservas ──────────────────────────────────────────────────────────────
    def _seed_reservations(self):
        from apps.packages.models import Departure
        from apps.accounts.models import User
        from apps.reservations.models import Reservation

        clients  = list(User.objects.filter(role=User.Role.CLIENT).order_by("id")[:5])
        departures = list(Departure.objects.select_related("package").order_by("id")[:10])

        if not clients or not departures:
            self.stdout.write(self.style.WARNING("  ⚠ No hay clientes o salidas para crear reservas."))
            return

        reservation_scenarios = [
            ("PENDING",    "PENDING"),
            ("CONFIRMED",  "PAID"),
            ("CONFIRMED",  "PAID"),
            ("CANCELLED",  "REFUNDED"),
            ("PENDING",    "PENDING"),
            ("CONFIRMED",  "PAID"),
            ("IN_PROCESS", "PENDING"),
            ("CONFIRMED",  "PAID"),
            ("CANCELLED",  "REFUNDED"),
            ("PENDING",    "PENDING"),
        ]

        created_count = 0
        for i, (status, payment) in enumerate(reservation_scenarios):
            user      = clients[i % len(clients)]
            departure = departures[i % len(departures)]

            if Reservation.objects.filter(user=user, departure=departure).exists():
                continue

            people     = (i % 3) + 1
            unit_price = departure.package.price

            Reservation.objects.create(
                user=user,
                departure=departure,
                number_of_people=people,
                unit_price=unit_price,
                total_amount=unit_price * people,
                status=status,
                payment_status=payment,
            )
            created_count += 1

        self.stdout.write(f"  ✓ {created_count} reservas con distintos estados")
