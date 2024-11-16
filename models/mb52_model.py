import mysql.connector
from bs4 import BeautifulSoup

def process_mb52_data(file_path):
    """Parse HTML file for MB52, delete old data, and insert new data."""
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    tbody = soup.find('tbody')

    conn = mysql.connector.connect(
        host="36.94.112.123",  # IP server database
        user="it",             # Username database
        password="ITIMS321",   # Password database
        database="dashboard",  # Nama database
        port=3306              # Port MySQL (default: 3306)
    )
    cursor = conn.cursor()

    # Hapus semua data lama di tabel MB52
    cursor.execute("DELETE FROM `MB52`")
    conn.commit()

    is_first_row = True  # Variabel untuk melacak baris pertama

    for row in tbody.find_all('tr'):
        columns = row.find_all('td')

        # Abaikan baris pertama jika itu adalah header
        if is_first_row:
            is_first_row = False
            continue

        # Pastikan kolom minimal sesuai dengan jumlah yang diinginkan
        if len(columns) >= 9:  # Pastikan ada cukup kolom
            data = {
                'Material': columns[0].get_text(strip=True),
                'Plnt': columns[1].get_text(strip=True),
                'SLoc': columns[2].get_text(strip=True),
                'S': columns[3].get_text(strip=True),
                'WBS_Element': columns[5].get_text(strip=True) if columns[5].get_text(strip=True) else None,  # Handle empty value
                'BUn': columns[8].get_text(strip=True),
                'Unrestricted': columns[9].get_text(strip=True),
                'Crcy': columns[10].get_text(strip=True),
                'Value_Unrestricted': columns[11].get_text(strip=True)
            }

            placeholders = ', '.join(['%s'] * len(data))
            columns = ', '.join([f'`{key}`' for key in data.keys()])
            sql = f"INSERT INTO `MB52` ({columns}) VALUES ({placeholders})"

            try:
                cursor.execute(sql, tuple(data.values()))
            except mysql.connector.Error as e:
                print(f"Error inserting row: {e}")
                print(f"SQL Query: {sql}")
                print(f"Row values: {list(data.values())}")

    conn.commit()
    cursor.close()
    conn.close()
