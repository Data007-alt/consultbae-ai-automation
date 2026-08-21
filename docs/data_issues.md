# Data Quality Issues

## Source 2 — Gig Workers

### 1. Blank row
Source 2 contained one completely blank row.

Action:
The ingestion pipeline removes completely empty rows before processing.

### 2. Malformed shifted row
One Source 2 row had its values shifted across columns.

The row appeared in the form:

skills | email | name | rate | city | status

instead of:

email | name | rate | city | status | skills

Action:
The pipeline detects this structural pattern and repositions the values into the correct columns before normalization and database insertion.

## Source 3 — CBNexus

### 3. Repeated header row
Source 3 contained a second header row in the middle of the dataset.

Action:
The pipeline detects rows where the Name field equals "Name" and removes them before processing.



# Data Quality Issues Report

## Overview

The three source CSV files came from different systems and contained
inconsistent formatting, duplicate people, missing values, and malformed data.

The pipeline cleans and normalizes the data before inserting it into SQLite.

---

## Source 1 — Naukri Applicants

### 1. Different city capitalization and formatting

Examples:

- Pune
- PUNE
- pune
- New Delhi
- new delhi
- NOIDA
- Noida
- GURGAON
- gurugram

Action:

City values were normalized for matching so that differences in capitalization
and whitespace do not prevent records from being matched.

---

### 2. Different phone number formats

Examples:

- 9000000131
- 919000000131
- +91-9000000131

Action:

Phone numbers were normalized by removing formatting characters and handling
the Indian country-code prefix so equivalent phone numbers can be compared.

---

### 3. Different name representations

Example:

- R. Verma
- Rohit Verma

These records had the same email address and phone number.

Action:

The records were treated as the same person because email and phone provided
strong matching evidence.

---

### 4. Duplicate person records

Some people appeared more than once in the source data.

Example:

Rohit Verma / R. Verma had the same email and phone.

Action:

Duplicate person records were merged into a single person in the database.

---

### 5. Inconsistent CTC formats

The Current CTC column contains different representations such as:

- 417964
- 5.1
- 10
- 11.2
- 1195422

Action:

The original source value is preserved rather than assuming that every numeric
value has the same unit. CTC values require source-specific interpretation
before being safely converted into one unit.

---

## Source 2 — Gig Workers

### 6. Completely blank row

Source 2 contained one completely blank row.

Action:

Completely empty rows are removed during ingestion.

---

### 7. Malformed shifted row

One Source 2 row had its values shifted into the wrong columns.

The malformed row effectively appeared as:

skills | email | name | rate | city | status

instead of:

email | name | rate | city | status | skills

Action:

The pipeline detects the structural pattern and moves the values back into
their expected columns before further processing.

---

### 8. Repeated / malformed records

Some people appeared more than once in the Gig Worker source.

Example:

Deepak Nair appeared with:

- DEEPAK.NAIR44@EXAMPLE.COM
- DEEPAK.NAIR57@EXAMPLE.IN

The first record matches the Naukri record by email and the CBNexus record
by phone. The second record has a conflicting email and different city.

Action:

The conflicting record is not automatically merged solely because the name
matches. This avoids incorrectly combining potentially different records.

---

### 9. Inconsistent status capitalization

Examples:

- Active
- active
- ACTIVE
- Inactive
- paused

Action:

Status values were normalized for consistency.

---

### 10. Inconsistent skill formatting

Skills appear in different capitalization and formatting:

- SQL
- sql
- REST APIs
- rest apis
- FastAPI
- fastapi

Action:

Skills are normalized for comparison and categorization while preserving
the underlying skill information.

---

## Source 3 — CBNexus Contacts

### 11. Repeated header row

The file contained a second header row inside the data.

Example:

Name | Phone Number | City | Verified | Projects Completed

Action:

The repeated header row is detected and removed before processing.

---

### 12. Different phone number formats

Examples:

- 9000000268
- 919000000268
- +91-9000000268
- +91-9000000131

Action:

Phone numbers are normalized before matching.

---

### 13. Different city capitalization and formatting

Examples:

- Gurgaon
- GURGAON
- Noida
- NOIDA
- Pune
- pune
- Bengaluru
- Bangalore

Action:

City values are normalized for matching.

---

### 14. Different representations of verification status

Examples:

- Y
- Yes
- yes
- N
- No

Action:

Verification values are normalized to a consistent representation.

---

## Matching Decisions

The pipeline does not rely only on names to identify people.

The matching process gives stronger weight to:

1. Exact normalized phone number
2. Exact normalized email
3. Matching name with supporting information such as city

Conflicting email/phone information is not automatically merged only because
the person's name is the same.

Example:

Arjun Mehta had different email addresses between Naukri and Gig Workers,
but his normalized phone number matched the CBNexus record and the name/city
also matched. Therefore the records were treated as the same person.

Deepak Nair had one Gig Worker record matching the Naukri email and another
Gig Worker record with a different email and city. The conflicting record was
not automatically treated as the same person.

---

## Final Database Result

After cleaning, normalization and matching:

- Naukri source records: 42
- Gig Worker source records: 31
- CBNexus source records: 30
- Unique people in database: 61