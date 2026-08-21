import sqlite3

connection = sqlite3.connect("consultbae.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT person_id, name, email, phone, city
    FROM people
    ORDER BY person_id
""")

rows = cursor.fetchall()

print("\n===== PEOPLE IN DATABASE =====\n")

for row in rows:
    print(row)

print("\nTotal:", len(rows))

connection.close()