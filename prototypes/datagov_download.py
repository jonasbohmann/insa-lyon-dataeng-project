import requests
import pandas as pd


# URL for CSV-file on crime data in Los Angeles from 2010 to 2019
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


# merge the two CSV-files

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




