import sqlite3

connection = sqlite3.connect("consultbae.db")

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM people")
people_count = cursor.fetchone()[0]

print("Total people:", people_count)

cursor.execute("SELECT COUNT(*) FROM naukri_records")
print("Naukri records:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM gig_worker_records")
print("Gig Worker records:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM cbnexus_records")
print("CBNexus records:", cursor.fetchone()[0])

connection.close()