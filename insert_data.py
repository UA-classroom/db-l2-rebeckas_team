import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host="localhost",  # change if needed
        port="5432",  # change if needed
    )

def seed_data():
    """
    Insert a larger realistic Swedish-style dataset.
    Assumes an empty database. If users already exist, seeding is skipped.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Don't seed twice
    cursor.execute("SELECT COUNT(*) FROM users;")
    if cursor.fetchone()[0] > 0:
        print("Seed data already exists, skipping seeding.")
        cursor.close()
        connection.close()
        return

    # ---------------- CATEGORIES ----------------
    categories_by_name = {}

    main_categories = [
        ("Massage", "Alla typer av massagebehandlingar"),
        ("Frisör", "Klippning och hårvård"),
        ("Hudvård", "Ansiktsbehandlingar och hudvård"),
        ("Naglar", "Manikyr, pedikyr och nagelbehandlingar"),
        ("Träning", "Personlig träning och gruppträning"),
    ]

    for name, desc in main_categories:
        cursor.execute(
            """
            INSERT INTO categories (name, description, parent_id)
            VALUES (%s, %s, NULL)
            RETURNING id;
            """,
            (name, desc),
        )
        cat_id = cursor.fetchone()[0]
        categories_by_name[name] = cat_id

    sub_categories = [
        ("Klassisk massage", "Avslappnande klassisk massage", "Massage"),
        ("Djupgående massage", "Behandlande massage", "Massage"),
        ("Gravidmassage", "Massage för gravida", "Massage"),

        ("Klippning dam", "Klippning och styling för dam", "Frisör"),
        ("Klippning herr", "Herrklippning", "Frisör"),
        ("Färg & klipp", "Färgning och klippning", "Frisör"),

        ("Ansiktsbehandling", "Rengöring och hudvård för ansiktet", "Hudvård"),
        ("Ansiktsbehandling lyx", "Lyxigare ansiktskur", "Hudvård"),

        ("Spa-manikyr", "Lyxig manikyr", "Naglar"),
        ("Spa-pedikyr", "Lyxig pedikyr", "Naglar"),

        ("Personlig träning", "En-till-en-träning", "Träning"),
        ("Gruppträning", "Träning i mindre grupp", "Träning"),
    ]

    for name, desc, parent_name in sub_categories:
        parent_id = categories_by_name[parent_name]
        cursor.execute(
            """
            INSERT INTO categories (name, description, parent_id)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (name, desc, parent_id),
        )
        cat_id = cursor.fetchone()[0]
        categories_by_name[name] = cat_id

    # ---------------- USERS ----------------
    provider_data = [
        ("provider", "Anna", "Lindström", "annal", "anna.lindstrom@example.com", "0701234501"),
        ("provider", "Johan", "Eriksson", "johane", "johan.eriksson@example.com", "0701234502"),
        ("provider", "Elin", "Karlsson", "elink", "elin.karlsson@example.com", "0701234503"),
        ("provider", "Mats", "Sundberg", "matss", "mats.sundberg@example.com", "0701234504"),
        ("provider", "Sofia", "Berg", "sofiab", "sofia.berg@example.com", "0701234505"),
        ("provider", "Patrik", "Nilsson", "patrikin", "patrik.nilsson@example.com", "0701234506"),
        ("provider", "Hanna", "Björk", "hannab", "hanna.bjork@example.com", "0701234507"),
        ("provider", "Lars", "Holm", "larsh", "lars.holm@example.com", "0701234508"),
        ("provider", "Ida", "Nyström", "idan", "ida.nystrom@example.com", "0701234509"),
        ("provider", "Oskar", "Lund", "oskarl", "oskar.lund@example.com", "0701234510"),
    ]

    customer_data = [
        ("customer", "Sara", "Nilsson", "saran", "sara.nilsson@example.com", "0731112201"),
        ("customer", "Markus", "Sundberg", "markuss", "markus.sundberg@example.com", "0731112202"),
        ("customer", "Karin", "Bergström", "karinb", "karin.bergstrom@example.com", "0731112203"),
        ("customer", "Anders", "Johansson", "andersj", "anders.johansson@example.com", "0731112204"),
        ("customer", "Linda", "Persson", "lindap", "linda.persson@example.com", "0731112205"),
        ("customer", "Mikael", "Dahl", "mikaeld", "mikael.dahl@example.com", "0731112206"),
        ("customer", "Jenny", "Åkesson", "jennya", "jenny.akesson@example.com", "0731112207"),
        ("customer", "Tobias", "Lundgren", "tobiasl", "tobias.lundgren@example.com", "0731112208"),
        ("customer", "Emelie", "Olofsson", "emelieno", "emelie.olofsson@example.com", "0731112209"),
        ("customer", "Per", "Svensson", "pers", "per.svensson@example.com", "0731112210"),
        ("customer", "Felicia", "Hedlund", "feliciah", "felicia.hedlund@example.com", "0731112211"),
        ("customer", "Niklas", "Arvidsson", "niklasa", "niklas.arvidsson@example.com", "0731112212"),
        ("customer", "Hanna", "Lind", "hannalind", "hanna.lind@example.com", "0731112213"),
        ("customer", "Olle", "Sandberg", "olles", "olle.sandberg@example.com", "0731112214"),
        ("customer", "Frida", "Wikström", "fridaw", "frida.wikstrom@example.com", "0731112215"),
        ("customer", "Daniel", "Ek", "danielek", "daniel.ek@example.com", "0731112216"),
        ("customer", "Lisa", "Ström", "lisas", "lisa.strom@example.com", "0731112217"),
        ("customer", "Jonas", "Vik", "jonasv", "jonas.vik@example.com", "0731112218"),
        ("customer", "Erik", "Blom", "erikb", "erik.blom@example.com", "0731112219"),
        ("customer", "Helena", "Nord", "helenan", "helena.nord@example.com", "0731112220"),
        ("customer", "Maria", "Gran", "mariag", "maria.gran@example.com", "0731112221"),
        ("customer", "Isak", "Månsson", "isakm", "isak.mansson@example.com", "0731112222"),
        ("customer", "Sanna", "Holmqvist", "sannah", "sanna.holmqvist@example.com", "0731112223"),
        ("customer", "Victor", "Eliasson", "victore", "victor.eliasson@example.com", "0731112224"),
    ]

    admin_data = [
        ("admin", "Admin", "User", "admin1", "admin1@example.com", "0700000001"),
        ("admin", "Support", "Admin", "support", "support@example.com", "0700000002"),
    ]

    provider_ids = []
    customer_ids = []
    admin_ids = []

    for row in provider_data:
        cursor.execute(
            """
            INSERT INTO users (role, firstname, lastname, username, email, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            row,
        )
        provider_ids.append(cursor.fetchone()[0])

    for row in customer_data:
        cursor.execute(
            """
            INSERT INTO users (role, firstname, lastname, username, email, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            row,
        )
        customer_ids.append(cursor.fetchone()[0])

    for row in admin_data:
        cursor.execute(
            """
            INSERT INTO users (role, firstname, lastname, username, email, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            row,
        )
        admin_ids.append(cursor.fetchone()[0])

    # ---------------- BUSINESSES ----------------
    businesses_data = [
        # owner_index, main_category_name, name, description, street_name, street_number, city, postal_code
        (0, "Massage", "Stockholm Massagecenter", "Avslappnande massage i hjärtat av Stockholm.", "Sveavägen", "12", "Stockholm", "11134"),
        (1, "Frisör", "City Hair Studio", "Modern frisörsalong nära Centralen.", "Kungsgatan", "45", "Stockholm", "11156"),
        (2, "Hudvård", "Göteborg Hud & Spa", "Skönhet och återhämtning vid Avenyn.", "Kungsportsavenyen", "3B", "Göteborg", "41136"),
        (3, "Naglar", "Malmö Nail Lounge", "Nagelbar med fokus på design.", "Södra Förstadsgatan", "21", "Malmö", "21143"),
        (4, "Massage", "Uppsala Relax", "Massage och avslappning nära Fyrisån.", "Drottninggatan", "7", "Uppsala", "75310"),
        (5, "Frisör", "Västerås Klipp & Färg", "Personlig frisörsalong i city.", "Stora Gatan", "9", "Västerås", "72212"),
        (6, "Träning", "FitLab Stockholm", "Personlig träning och PT-grupper.", "Vasagatan", "18", "Stockholm", "11120"),
        (7, "Hudvård", "Norrköping Skin Clinic", "Hudvårdsklinik med medicinska behandlingar.", "Kungsgatan", "2", "Norrköping", "60220"),
    ]

    business_ids = []
    business_main_cat_name_by_id = {}

    for i, (owner_index, cat_name, b_name, desc, street, number, city, postal) in enumerate(businesses_data):
        owner_id = provider_ids[owner_index % len(provider_ids)]
        main_cat_id = categories_by_name[cat_name]
        cursor.execute(
            """
            INSERT INTO businesses (owner_id, main_category_id, name, description, street_name, street_number, city, postal_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (owner_id, main_cat_id, b_name, desc, street, number, city, postal),
        )
        b_id = cursor.fetchone()[0]
        business_ids.append(b_id)
        business_main_cat_name_by_id[b_id] = cat_name

    # ---------------- STAFF MEMBERS ----------------
    staff_firstnames = ["Maria", "Oskar", "Linda", "Kevin", "Elin", "Patrik", "Sofia", "Mattias", "Jenny", "Tobias"]
    staff_lastnames = ["Andersson", "Johansson", "Karlsson", "Berg", "Sundqvist", "Lund", "Holm", "Nyberg", "Dahl", "Öhman"]
    staff_roles_by_category = {
        "Massage": "Massör",
        "Frisör": "Frisör",
        "Hudvård": "Hudterapeut",
        "Naglar": "Nagelterapeut",
        "Träning": "Personlig tränare",
    }

    staff_ids_by_business = {}

    for idx, b_id in enumerate(business_ids):
        cat_name = business_main_cat_name_by_id[b_id]
        role = staff_roles_by_category.get(cat_name, "Personal")
        staff_ids = []
        for j in range(3):  # 3 staff per business
            fn = staff_firstnames[(idx + j) % len(staff_firstnames)]
            ln = staff_lastnames[(idx * 2 + j) % len(staff_lastnames)]
            full_name = f"{fn} {ln}"
            email = f"{fn.lower()}.{ln.lower()}_{b_id}@example.com"
            phone = f"0709{idx}{j}00{j}"
            cursor.execute(
                """
                INSERT INTO staffmembers (business_id, name, email, phone_number, role)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (b_id, full_name, email, phone, role),
            )
            staff_ids.append(cursor.fetchone()[0])
        staff_ids_by_business[b_id] = staff_ids

    # ---------------- BUSINESS IMAGES ----------------
    for b_id in business_ids:
        slug = f"business_{b_id}"
        cursor.execute(
            """
            INSERT INTO business_images (business_id, image_url, is_logo, sort_order)
            VALUES 
                (%s, %s, TRUE, 0),
                (%s, %s, FALSE, 1),
                (%s, %s, FALSE, 2);
            """,
            (
                b_id, f"https://example.com/images/{slug}_logo.png",
                b_id, f"https://example.com/images/{slug}_interior1.jpg",
                b_id, f"https://example.com/images/{slug}_interior2.jpg",
            ),
        )

    # ---------------- BUSINESS OPENING HOURS ----------------
    for b_id in business_ids:
        # Mon-Fri: 09–18, Sat: 10–16
        for weekday in range(1, 6):
            cursor.execute(
                """
                INSERT INTO business_opening_hours (business_id, weekday, open_time, closing_time)
                VALUES (%s, %s, %s, %s);
                """,
                (b_id, weekday, "09:00", "18:00"),
            )
        cursor.execute(
            """
            INSERT INTO business_opening_hours (business_id, weekday, open_time, closing_time)
            VALUES (%s, %s, %s, %s);
            """,
            (b_id, 6, "10:00", "16:00"),
        )

    # ---------------- SERVICES ----------------
    service_templates_by_main_cat = {
        "Massage": [
            ("Klassisk massage 30 min", "Kortare avslappnande massage.", 30, 450, ["Massage", "Klassisk massage"]),
            ("Klassisk massage 60 min", "Helkroppsmassage.", 60, 650, ["Massage", "Klassisk massage"]),
            ("Djupgående massage 60 min", "Behandlande massage för spända muskler.", 60, 750, ["Massage", "Djupgående massage"]),
            ("Gravidmassage 60 min", "Skonsam massage för gravida.", 60, 795, ["Massage", "Gravidmassage"]),
        ],
        "Frisör": [
            ("Klippning dam", "Klippning och styling för dam.", 45, 550, ["Frisör", "Klippning dam"]),
            ("Klippning herr", "Herrklippning.", 30, 400, ["Frisör", "Klippning herr"]),
            ("Färg & klipp", "Färgning och klippning.", 90, 1200, ["Frisör", "Färg & klipp"]),
        ],
        "Hudvård": [
            ("Ansiktsbehandling", "Rengöring och återfuktning.", 50, 695, ["Hudvård", "Ansiktsbehandling"]),
            ("Ansiktsbehandling lyx", "Lyxigare kur med mask.", 80, 995, ["Hudvård", "Ansiktsbehandling lyx"]),
        ],
        "Naglar": [
            ("Spa-manikyr", "Manikyr med handmassage.", 60, 550, ["Naglar", "Spa-manikyr"]),
            ("Spa-pedikyr", "Pedikyr med fotmassage.", 60, 595, ["Naglar", "Spa-pedikyr"]),
        ],
        "Träning": [
            ("Personlig träning 60 min", "PT-pass en-till-en.", 60, 795, ["Träning", "Personlig träning"]),
            ("Gruppträning 45 min", "Träning i liten grupp.", 45, 295, ["Träning", "Gruppträning"]),
        ],
    }

    service_ids_by_business = {}
    service_price_by_id = {}

    for b_id in business_ids:
        main_cat_name = business_main_cat_name_by_id[b_id]
        templates = service_templates_by_main_cat.get(main_cat_name, [])
        s_ids = []
        for (s_name, s_desc, dur, price, cat_names) in templates:
            cursor.execute(
                """
                INSERT INTO services (business_id, name, description, duration_minutes, price)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (b_id, s_name, s_desc, dur, price),
            )
            s_id = cursor.fetchone()[0]
            s_ids.append(s_id)
            service_price_by_id[s_id] = price

            # service_categories links
            for cname in cat_names:
                cat_id = categories_by_name.get(cname)
                if cat_id:
                    cursor.execute(
                        """
                        INSERT INTO service_categories (service_id, category_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING;
                        """,
                        (s_id, cat_id),
                    )

            # Also always add main category
            main_cat_id = categories_by_name[main_cat_name]
            cursor.execute(
                """
                INSERT INTO service_categories (service_id, category_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (s_id, main_cat_id),
            )

        service_ids_by_business[b_id] = s_ids

    # ---------------- BOOKINGS, PAYMENTS, REVIEWS ----------------
    statuses = ["pending", "confirmed", "cancelled", "completed"]
    payment_methods = ["card", "swish", "klarna", "gift_card", "cash"]

    booking_infos = []  # to use later for payments + reviews

    # create ~8 bookings per business
    for b_index, b_id in enumerate(business_ids):
        s_ids = service_ids_by_business[b_id]
        staff_ids = staff_ids_by_business[b_id]
        for k in range(8):
            customer_id = customer_ids[(b_index * 3 + k) % len(customer_ids)]
            service_id = s_ids[k % len(s_ids)]
            staff_id = staff_ids[k % len(staff_ids)]
            status = statuses[(b_index + k) % len(statuses)]

            # Simple date pattern: March 10–31 2025
            day = 10 + (b_index * 2 + k) % 20
            start_hour = 9 + (k % 6)  # 09–14
            starttime = f"2025-03-{day:02d} {start_hour:02d}:00"
            end_hour = start_hour + 1
            endtime = f"2025-03-{day:02d} {end_hour:02d}:00"

            notes = None
            if status == "cancelled":
                notes = "Avbokad av kund."
            elif status == "completed":
                notes = "Genomförd behandling."

            cursor.execute(
                """
                INSERT INTO bookings (customer_id, business_id, service_id, staff_id, starttime, endtime, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (customer_id, b_id, service_id, staff_id, starttime, endtime, status, notes),
            )
            booking_id = cursor.fetchone()[0]
            booking_infos.append(
                {
                    "id": booking_id,
                    "business_id": b_id,
                    "customer_id": customer_id,
                    "service_id": service_id,
                    "status": status,
                }
            )

        import random

    # Realistic weight-based payment method selection
    payment_method_weights = {
        "card": 0.55,
            "swish": 0.25,
        "klarna": 0.10,
        "gift_card": 0.05,
        "cash": 0.05,
    }

    def choose_weighted_method():
        r = random.random()
        cumulative = 0
        for method, weight in payment_method_weights.items():
            cumulative += weight
            if r <= cumulative:
                return method
        return "card"  # fallback


    # ---- PAYMENTS ----
    for i, b in enumerate(booking_infos):

        status = b["status"]
        service_id = b["service_id"]
        booking_id = b["id"]
        amount = service_price_by_id[service_id]

        # --- Pending bookings: No payment yet ---
        if status == "pending":
            continue

        # --- Cancelled bookings ---
        if status == "cancelled":
            # 50% get a refund, 50% no payment created
            if random.random() < 0.5:
                cursor.execute(
                    """
                    INSERT INTO payments (booking_id, amount, payment_method, status)
                    VALUES (%s, %s, %s, %s);
                    """,
                    (booking_id, amount, choose_weighted_method(), "refunded"),
                )
            continue

        # --- Confirmed bookings ---
        if status == "confirmed":
            r = random.random()
            if r < 0.5:
                payment_status = "pending"
            elif r < 0.9:
                payment_status = "paid"
            else:
                payment_status = "failed"

            cursor.execute(
                """
                INSERT INTO payments (booking_id, amount, payment_method, status)
                VALUES (%s, %s, %s, %s);
                """,
                (booking_id, amount, choose_weighted_method(), payment_status),
            )
            continue

        # --- Completed bookings ---
        if status == "completed":
            r = random.random()
            if r < 0.80:
                payment_status = "paid"
            elif r < 0.90:
                payment_status = "pending"
            else:
                payment_status = "refunded"

            cursor.execute(
                """
                INSERT INTO payments (booking_id, amount, payment_method, status)
                VALUES (%s, %s, %s, %s);
                """,
                (booking_id, amount, choose_weighted_method(), payment_status),
            )
            continue


    # REVIEWS: for some completed bookings
    review_texts = [
        ("Fantastiskt!", "Mycket nöjd, kommer tillbaka."),
        ("Bra upplevelse", "Proffsig personal och trevlig lokal."),
        ("Helt okej", "Bra behandling men lite lång väntetid."),
        ("Supernöjd", "Precis vad jag behövde."),
        ("Rekommenderas", "Skulle absolut rekommendera till vänner."),
    ]

    review_index = 0
    for b in booking_infos:
        if b["status"] == "completed" and review_index < 80:  # cap number of reviews
            rating = 3 + (review_index % 3)  # 3,4,5
            title, comment = review_texts[review_index % len(review_texts)]
            cursor.execute(
                """
                INSERT INTO reviews (booking_id, business_id, customer_id, rating, title, comment)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (b["id"], b["business_id"], b["customer_id"], rating, title, comment),
            )
            review_index += 1

    connection.commit()
    cursor.close()
    connection.close()
    print("Seed data inserted successfully.")
    
if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    seed_data()
    print("Seed data inserted into tables.")
