import pandas as pd

source1 = pd.read_csv("data/source1_naukri_applicants.csv")
source2 = pd.read_csv("data/source2_gig_workers.csv")
source3 = pd.read_csv("data/source3_cbnexus_contacts.csv")

def normalize_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def normalize_phone(value):
    if pd.isna(value):
        return ""

    digits = "".join(char for char in str(value) if char.isdigit())

    if len(digits) > 10:
        digits = digits[-10:]

    return digits

source1["normalized_name"] = source1["Full Name"].apply(normalize_text)
source2["normalized_name"] = source2["worker_name"].apply(normalize_text)
source3["normalized_name"] = source3["Name"].apply(normalize_text)

source1["normalized_email"] = source1["Email"].apply(normalize_text)
source2["normalized_email"] = source2["email_id"].apply(normalize_text)

source1["normalized_phone"] = source1["Phone"].apply(normalize_phone)
source3["normalized_phone"] = source3["Phone Number"].apply(normalize_phone)

common_names = (
    set(source1["normalized_name"])
    & set(source2["normalized_name"])
    & set(source3["normalized_name"])
)

print("Names appearing in all three sources:")
print(sorted(common_names))



def compare_person(name):
    print("\n" + "=" * 60)
    print("MATCH:", name)
    print("=" * 60)

    naukri = source1[source1["normalized_name"] == name]
    gig = source2[source2["normalized_name"] == name]
    cbnexus = source3[source3["normalized_name"] == name]

    if not naukri.empty:
        print("\nNaukri:")
        print(
            naukri[
                ["Full Name", "Email", "Phone", "City"]
            ].to_string(index=False)
        )

    if not gig.empty:
        print("\nGig Worker:")
        print(
            gig[
                ["worker_name", "email_id", "location"]
            ].to_string(index=False)
        )

    if not cbnexus.empty:
        print("\nCBNexus:")
        print(
            cbnexus[
                ["Name", "Phone Number", "City"]
            ].to_string(index=False)
        )

for name in sorted(common_names):
    compare_person(name)