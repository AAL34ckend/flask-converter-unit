import pymysql
from conversion import LENGTH, LENGTH_IMPERIAL, MASS, MASS_IMPERIAL, VOLUME, VOLUME_IMPERIAL, VOLUME_US, TEMPERATURE, TIME

# Koneksi ke database
def get_db_connection():
    try:
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="1234", #sesuaikan dengan punya anda
            database="converter" #sesuaikan dengan nama database anda
        )
        return db
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None
    

# Fungsi untuk menyisipkan kategori dan unit ke database
def insert_categories_and_units():
    db = get_db_connection()
    if db is None:
        return

    cursor = db.cursor()

    # Kategori dari data
    categories = {
        "length": [LENGTH, LENGTH_IMPERIAL],
        "mass": [MASS, MASS_IMPERIAL],
        "volume": [VOLUME, VOLUME_IMPERIAL, VOLUME_US],
        "temperature": [TEMPERATURE],
        "time": [TIME]
    }

    # Insert kategori ke tabel
    for category_name in categories.keys():
        cursor.execute("INSERT INTO categories (name) VALUES (%s) ON DUPLICATE KEY UPDATE id=id", (category_name,))
    db.commit()

    # Insert unit ke tabel
    for category_name, unit_dicts in categories.items():
        # Ambil ID kategori
        cursor.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
        category_id = cursor.fetchone()[0]

        for unit_dict in unit_dicts:
            for unit_name, details in unit_dict.items():
                system = details[0]
                abbreviation = details[1]
                factor = details[2]
                note = details[3] if len(details) > 3 else None

                # Insert unit
                cursor.execute("""
                    INSERT INTO units (category_id, name, abbreviation, conversion_factor, measurement_system, note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (category_id, unit_name, abbreviation, factor, system, note))
    db.commit()

    # Tutup koneksi
    cursor.close()
    db.close()

if __name__ == "__main__":
    insert_categories_and_units()


