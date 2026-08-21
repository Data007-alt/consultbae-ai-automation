import sqlite3
import pandas as pd

DATABASE_PATH = "consultbae.db"

SOURCE1 = "data/source1_naukri_applicants.csv"
SOURCE2 = "data/source2_gig_workers.csv"
SOURCE3 = "data/source3_cbnexus_contacts.csv"

def normalize_text(value):
    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def normalize_email(value):
    return normalize_text(value)


def normalize_phone(value):
    if pd.isna(value):
        return ""

    digits = "".join(
        character for character in str(value)
        if character.isdigit()
    )

    if len(digits) > 10:
        digits = digits[-10:]

    return digits


def normalize_city(value):
    city = normalize_text(value)

    city_mapping = {
        "new delhi": "delhi",
        "delhi ncr": "delhi",
        "gurgaon": "gurugram",
        "bangalore": "bengaluru",
    }

    return city_mapping.get(city, city)

def load_data():
    source1 = pd.read_csv(SOURCE1)
    source2 = pd.read_csv(SOURCE2)
    source3 = pd.read_csv(SOURCE3)

    return source1, source2, source3

def clean_data(source1, source2, source3):

# Remove completely blank rows
    source1 = source1.dropna(how="all").copy()
    source2 = source2.dropna(how="all").copy()
    source3 = source3.dropna(how="all").copy()

# Remove repeated header rows that appear inside the data
    source1 = source1[
    source1["Full Name"].astype(str).str.strip().str.lower()
    != "full name"
].copy()

    source2 = source2[
    source2["worker_name"].astype(str).str.strip().str.lower()
    != "worker_name"
].copy()

    source3 = source3[
    source3["Name"].astype(str).str.strip().str.lower()
    != "name"
].copy() 


# Fix malformed Source 2 rows where the columns are shifted.
    source2 = source2.copy()

    for index in source2.index:

        first_value = str(source2.loc[index, "email_id"]).strip()
        second_value = str(source2.loc[index, "worker_name"]).strip()
        third_value = str(source2.loc[index, "rate"]).strip()
        fourth_value = str(source2.loc[index, "location"]).strip()
        fifth_value = str(source2.loc[index, "status"]).strip()
        sixth_value = str(source2.loc[index, "skill_tags"]).strip()

    # Detect a row where:
    # skills | email | name | rate | city | status
    # was incorrectly placed instead of:
    # email | name | rate | city | status | skills

    if (
        "," in first_value
        and "@" in second_value
        and not "@" in third_value
        and "/" in fourth_value
    ):

        source2.loc[index, "email_id"] = second_value
        source2.loc[index, "worker_name"] = third_value
        source2.loc[index, "rate"] = fourth_value
        source2.loc[index, "location"] = fifth_value
        source2.loc[index, "status"] = sixth_value
        source2.loc[index, "skill_tags"] = first_value




    # Normalize names
    source1["normalized_name"] = (
        source1["Full Name"].apply(normalize_text)
    )

    source2["normalized_name"] = (
        source2["worker_name"].apply(normalize_text)
    )

    source3["normalized_name"] = (
        source3["Name"].apply(normalize_text)
    )

    # Normalize email
    source1["normalized_email"] = (
        source1["Email"].apply(normalize_email)
    )

    source2["normalized_email"] = (
        source2["email_id"].apply(normalize_email)
    )

    # Normalize phone
    source1["normalized_phone"] = (
        source1["Phone"].apply(normalize_phone)
    )

    source3["normalized_phone"] = (
        source3["Phone Number"].apply(normalize_phone)
    )

    # Normalize cities
    source1["normalized_city"] = (
        source1["City"].apply(normalize_city)
    )

    source2["normalized_city"] = (
        source2["location"].apply(normalize_city)
    )

    source3["normalized_city"] = (
        source3["City"].apply(normalize_city)
    )

    return source1, source2, source3


def calculate_score(
    name1,
    email1,
    phone1,
    city1,
    name2,
    email2,
    phone2,
    city2
):
    score = 0

    if name1 and name2 and name1 == name2:
        score += 20

    if email1 and email2 and email1 == email2:
        score += 50

    if phone1 and phone2 and phone1 == phone2:
        score += 50

    if city1 and city2 and city1 == city2:
        score += 10

    return score

def classify_match(score):
    if score >= 70:
        return "strong_match"

    if score >= 40:
        return "possible_match"

    return "no_match"


def find_person(connection, name, email, phone, city):

    cursor = connection.cursor()

    cursor.execute("""
        SELECT person_id, name, email, phone, city
        FROM people
    """)

    people = cursor.fetchall()

    best_person = None
    best_score = 0
    best_reason = ""

    for person in people:

        person_id, person_name, person_email, person_phone, person_city = person

        person_name = normalize_text(person_name)
        person_email = normalize_email(person_email)
        person_phone = normalize_phone(person_phone)
        person_city = normalize_city(person_city)

        score = calculate_score(
            name,
            email,
            phone,
            city,
            person_name,
            person_email,
            person_phone,
            person_city
        )

        if score > best_score:

            best_score = score
            best_person = person_id

            reasons = []

            if name and name == person_name:
                reasons.append("name")

            if email and email == person_email:
                reasons.append("email")

            if phone and phone == person_phone:
                reasons.append("phone")

            if city and city == person_city:
                reasons.append("city")

            best_reason = ", ".join(reasons)

    if best_score >= 70:
        return best_person, best_score, "strong_match"

    if best_score >= 40:
        return best_person, best_score, "possible_match"

    return None, best_score, "no_match"


def create_person(connection, name, email, phone, city):

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO people
        (name, email, phone, city)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        city
    ))

    connection.commit()

    return cursor.lastrowid

def process_naukri(connection, source1):

    cursor = connection.cursor()

    for index, row in source1.iterrows():

        name = row["Full Name"]
        email = row["Email"]
        phone = row["Phone"]
        city = row["City"]

        normalized_name = row["normalized_name"]
        normalized_email = row["normalized_email"]
        normalized_phone = row["normalized_phone"]
        normalized_city = row["normalized_city"]

        person_id, score, match_type = find_person(
            connection,
            normalized_name,
            normalized_email,
            normalized_phone,
            normalized_city
        )

        if person_id is None:

            person_id = create_person(
                connection,
                name,
                email,
                phone,
                city
            )

            match_type = "new_person"
            score = 0

        cursor.execute("""
            INSERT INTO naukri_records
            (
                person_id,
                source_row,
                experience_years,
                current_ctc,
                applied_date,
                skills
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            person_id,
            index + 2,
            row["Experience (Years)"],
            str(row["Current CTC"]),
            str(row["Applied Date"]),
            str(row["Skills"])
        ))

        cursor.execute("""
            INSERT INTO match_log
            (
                person_id,
                source,
                source_row,
                match_score,
                match_type,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            person_id,
            "naukri",
            index + 2,
            score,
            match_type,
            "Processed from Naukri Applicants"
        ))

    connection.commit()

def process_gig_workers(connection, source2):

    cursor = connection.cursor()

    for index, row in source2.iterrows():

        name = row["worker_name"]
        email = row["email_id"]

        city = row["location"]

        normalized_name = row["normalized_name"]
        normalized_email = row["normalized_email"]
        normalized_city = row["normalized_city"]

        # Source 2 does not contain phone numbers
        person_id, score, match_type = find_person(
            connection,
            normalized_name,
            normalized_email,
            "",
            normalized_city
        )

        if person_id is None:

            person_id = create_person(
                connection,
                name,
                email,
                "",
                city
            )

            match_type = "new_person"
            score = 0

        cursor.execute("""
            INSERT INTO gig_worker_records
            (
                person_id,
                source_row,
                rate,
                status,
                skill_tags
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            person_id,
            index + 2,
            str(row["rate"]),
            str(row["status"]),
            str(row["skill_tags"])
        ))

        cursor.execute("""
            INSERT INTO match_log
            (
                person_id,
                source,
                source_row,
                match_score,
                match_type,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            person_id,
            "gig_workers",
            index + 2,
            score,
            match_type,
            "Processed from Gig Workers"
        ))

    connection.commit()

def process_cbnexus(connection, source3):

    cursor = connection.cursor()

    for index, row in source3.iterrows():

        name = row["Name"]
        phone = row["Phone Number"]
        city = row["City"]

        normalized_name = row["normalized_name"]
        normalized_phone = row["normalized_phone"]
        normalized_city = row["normalized_city"]

        # Source 3 does not contain email
        person_id, score, match_type = find_person(
            connection,
            normalized_name,
            "",
            normalized_phone,
            normalized_city
        )

        if person_id is None:

            person_id = create_person(
                connection,
                name,
                "",
                phone,
                city
            )

            match_type = "new_person"
            score = 0

        cursor.execute("""
            INSERT INTO cbnexus_records
            (
                person_id,
                source_row,
                verified,
                projects_completed
            )
            VALUES (?, ?, ?, ?)
        """, (
            person_id,
            index + 2,
            str(row["Verified"]),
            int(row["Projects Completed"])
        ))

        cursor.execute("""
            INSERT INTO match_log
            (
                person_id,
                source,
                source_row,
                match_score,
                match_type,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            person_id,
            "cbnexus",
            index + 2,
            score,
            match_type,
            "Processed from CBNexus Contacts"
        ))

    connection.commit()  

def run_pipeline():

    print("Loading CSV files...")

    source1, source2, source3 = load_data()

    print("Cleaning and normalizing data...")

    source1, source2, source3 = clean_data(
        source1,
        source2,
        source3
    )

    connection = sqlite3.connect(DATABASE_PATH)

    print("Processing Naukri Applicants...")
    process_naukri(connection, source1)

    print("Processing Gig Workers...")
    process_gig_workers(connection, source2)

    print("Processing CBNexus Contacts...")
    process_cbnexus(connection, source3)

    connection.close()

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()


