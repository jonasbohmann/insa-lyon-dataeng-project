import requests
import pandas as pd
import psycopg2

# TO-DO: Delete last AREA column

"""# URL for CSV-file on crime data in Los Angeles from 2010 to 2019
url = "https://data.lacity.org/api/views/63jg-8b9z/rows.csv?accessType=DOWNLOAD"

# download file
response = requests.get(url)

if response.status_code == 200:

    # save data to the file
    csv_content = response.content.decode('utf-8')

    # save as local file
    with open("data1.csv", "w", encoding="utf-8") as file:
        file.write(csv_content)
    print("file successfully saved: data1.csv")


# URL for CSV-file on crime data in Los Angeles from 2020 to 2024
url = "https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD"

# download file
response = requests.get(url)

if response.status_code == 200:

    # save data to the file
    csv_content = response.content.decode('utf-8')

    # save as local file
    with open("data2.csv", "w", encoding="utf-8") as file:
        file.write(csv_content)
    print("file successfully saved: data2.csv")



# MERGING OF THE CSV FILES

# read CSV-files and load into Pandas DataFrames
csv1 = "data1.csv"
csv2 = "data2.csv"

df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)

# combine DataFrames
df_combined = pd.concat([df1, df2], ignore_index=True)

# save combines file
output_file = "combined_data.csv"
df_combined.to_csv(output_file, index=False)

print(f"The files were successfully combined and saved: {output_file}")



# DELETION OF REDUNDANT COLUMNS

combined_file = "combined_data.csv"
df = pd.read_csv(combined_file)

# clean data
columns_to_delete = ["Date Rptd", "AREA NAME", "Mocodes", "Vict Sex", "Vict Descent", "Premis Desc", 
                     "Weapon Used Cd", "Weapon Desc", "Status", "Status Desc", "Crm Cd 2", "Crm Cd 3", "Crm Cd 4", "Cross Street"]
df_cleaned = df.drop(columns=columns_to_delete)

# save cleaned data
output_file = "cleaned_data.csv"
df_cleaned.to_csv(output_file, index=False)

print(f"The file has been cleaned and saved: {output_file}")

"""

# UPLOAD DATA TO POSTGRES

# CSV-file with connection details
csv_file = "cleaned_data.csv"
db_user = "airflow"
db_password = "airflow"
db_host = "localhost"
db_port = "5432"
db_name = "airflow"

# load CSV-file into DataFrame
df = pd.read_csv(csv_file)

# establish connection to database
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

cursor = conn.cursor()

# create table
create_table_query = """
CREATE TABLE IF NOT EXISTS crime_data_la 
 (id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY, dr_no_file_number INTEGER, datetime TEXT, area TEXT, rpt_dist_no_sub_area TEXT, part1_2 TEXT,
  crime_code TEXT, crime_code_description TEXT, victim_age INTEGER, premis_cd_vehicle_or_location TEXT, crime_code_type TEXT,
  location_street_address TEXT, latitude INTEGER, longitude INTEGER)
"""
cursor.execute(create_table_query)
conn.commit()

print(f"Table 'crime_data_la' successfully created")

# prepare SQL-query for insertion
insert_query = f"""
INSERT INTO crime_data_la (dr_no_file_number, datetime, area, rpt_dist_no_sub_area, part1_2, crime_code, crime_code_description, 
victim_age, premis_cd_vehicle_or_location, crime_code_type, location_street_address, latitude, longitude)
VALUES ({', '.join(['%s'] * len(df.columns))});
"""

print(insert_query)

# extract & insert data rows from DataFrame
for row in df.itertuples(index=False, name=None):
    print(row)
    cursor.execute(insert_query, row)

# save changes and close connection
conn.commit()
cursor.close()
conn.close()

print(f"Data successfully inserted into 'crime_date_la'")