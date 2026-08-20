import pandas as pd

source1 = pd.read_csv("data/source1_naukri_applicants.csv")
source2 = pd.read_csv("data/source2_gig_workers.csv")
source3 = pd.read_csv("data/source3_cbnexus_contacts.csv")

sources = {
    "Source 1 - Naukri Applicants": source1,
    "Source 2 - Gig Workers": source2,
    "Source 3 - CBNexus Contacts": source3
}

for name, df in sources.items():

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print("Rows:", len(df))
    print("Columns:", list(df.columns))

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate complete rows:", df.duplicated().sum())

    print("\nFirst 5 rows:")
    print(df.head())

    #check duplicates emails and phones
    def check_duplicates(df, column):
        if column in df.columns:
         duplicates = df[df[column].duplicated(keep=False)]

        if len(duplicates) > 0:
            print(f"\nDuplicate values in '{column}':")
            print(duplicates[[column]].to_string(index=False))
        else:
            print(f"\nNo duplicates found in '{column}'.")

            print(df.head())

        for column in ["Email", "email_id", "Phone", "Phone Number"]:
            check_duplicates(df, column)
