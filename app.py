from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from models import get_db_connection
import conversion

app = Flask(__name__)
app.secret_key = '8fa3edfb2524493fbf42f09c37d8a13a' 

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print('email : ', email, 'password : ', password)
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT id, username, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print('request form get',request.form)
        username = request.form.get("username")
        email = request.form.get("email")
        print(email);
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('register.html')

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()
        cursor = connection.cursor()
        print(username)
        try:
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Email already registered.", "warning")
                return render_template('register.html')
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                           (username, email, hashed_password))
            connection.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            print("Error during registration:", e) 
            flash("An error occurred. Please try again.", "danger")
        finally:
            cursor.close()
            connection.close()

    return render_template('register.html')


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/home', methods=["GET"])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == "GET":
        return render_template('home.html')

@app.route('/length/', methods=['POST', 'GET'])
def length():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Ambil data units dari database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Ambil ID kategori 'length' dari database
    cursor.execute("SELECT id FROM categories WHERE name = 'length'")
    category_id = cursor.fetchone()[0]

    # Query unit berdasarkan kategori ID
    cursor.execute("SELECT name, abbreviation, conversion_factor FROM units WHERE category_id = %s", (category_id,))
    units = cursor.fetchall()  # Mengambil data unit dari database
    cursor.close()
    connection.close()

    units_dict = {unit[0]: {'abbreviation': unit[1], 'factor': unit[2]} for unit in units}

    if request.method == "POST":
        unit_to_convert = request.form.get("unit_to_convert")
        unit_to_convert_to = request.form.get("unit_to_convert_to")

        # Cek apakah unit yang dipilih valid
        if not unit_to_convert or not unit_to_convert_to:
            return render_template('length.html', units=units_dict, invalid_input_warning=True)
        try:
            value_to_convert = float(request.form.get("value_to_convert"))
        except ValueError:
            return render_template('length.html', units=units_dict, invalid_input_warning=True)

        converter = conversion.Converter(
            "length", unit_to_convert, unit_to_convert_to, value_to_convert)
        
        if unit_to_convert not in units_dict or unit_to_convert_to not in units_dict:
            return render_template('length.html', units=units_dict, invalid_input_warning=True)
        
        converter.set_base()  # Ini memeriksa dan mengatur konversi dasar
        output = converter.return_output()[0]
        warnings = converter.return_output()[1]

        return render_template('length.html', output=output, warnings=warnings, units=units_dict, method=request.method)

    return render_template('length.html', units=units_dict)



@app.route('/mass/', methods=['POST', 'GET'])
def mass():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT id FROM categories WHERE name = 'mass'")
    category_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT name, abbreviation, conversion_factor FROM units WHERE category_id = %s", (category_id,))
    units = cursor.fetchall() 
    cursor.close()
    connection.close()

    units_dict = {unit[0]: {'abbreviation': unit[1], 'factor': unit[2]} for unit in units}
    if request.method == "POST":
        unit_to_convert = request.form.get("unit_to_convert")
        unit_to_convert_to = request.form.get("unit_to_convert_to")
        if not unit_to_convert or not unit_to_convert_to:
                return render_template('mass.html', units=units_dict, invalid_input_warning=True)
        try:
            value_to_convert = float(request.form.get("value_to_convert"))
        except ValueError:
            return render_template('mass.html', units=units_dict, invalid_input_warning=True)
        converter = conversion.Converter(
            "mass", unit_to_convert, unit_to_convert_to, value_to_convert)
    
        if unit_to_convert not in units_dict or unit_to_convert_to not in units_dict:
            return render_template('mass.html', units=units_dict, invalid_input_warning=True)
    
        converter.set_base()  # Ini memeriksa dan mengatur konversi dasar
        output = converter.return_output()[0]
        warnings = converter.return_output()[1]

        return render_template('mass.html', output=output, warnings=warnings, units=units_dict, method=request.method)

    return render_template('mass.html', units=units_dict)

@app.route('/volume/', methods=['POST', 'GET'])
def volume():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    connection = get_db_connection()
    cursor = connection.cursor()

    # Ambil ID kategori 'volume' dari database
    cursor.execute("SELECT id FROM categories WHERE name = 'volume'")
    category_id = cursor.fetchone()[0]

    # Query unit berdasarkan kategori ID
    cursor.execute("SELECT name, abbreviation, conversion_factor FROM units WHERE category_id = %s", (category_id,))
    units = cursor.fetchall()  # Mengambil data unit dari database
    cursor.close()
    connection.close()

    units_dict = {unit[0]: {'abbreviation': unit[1], 'factor': unit[2]} for unit in units}

    if request.method == "POST":
        unit_to_convert = request.form.get("unit_to_convert")
        unit_to_convert_to = request.form.get("unit_to_convert_to")

        # Cek apakah unit yang dipilih valid
        if not unit_to_convert or not unit_to_convert_to:
            return render_template('volume.html', units=units_dict, invalid_input_warning=True)
        try:
            value_to_convert = float(request.form.get("value_to_convert"))
        except ValueError:
            return render_template('volume.html', units=units_dict, invalid_input_warning=True)

        converter = conversion.Converter(
            "volume", unit_to_convert, unit_to_convert_to, value_to_convert)
        
        if unit_to_convert not in units_dict or unit_to_convert_to not in units_dict:
            return render_template('volume.html', units=units_dict, invalid_input_warning=True)
        
        converter.set_base()  # Ini memeriksa dan mengatur konversi dasar
        output = converter.return_output()[0]
        warnings = converter.return_output()[1]

        return render_template('volume.html', output=output, warnings=warnings, units=units_dict, method=request.method)

    return render_template('volume.html', units=units_dict)

# temperature
def convert_temperature(value, from_unit, to_unit, conversion_factor):
    if from_unit == "celsius" and to_unit == "fahrenheit":
        # Celsius to Fahrenheit: (C * 1.8) + 32
        return (value * conversion_factor) + 32
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        # Fahrenheit to Celsius: (F - 32) / 1.8
        return (value - 32) / conversion_factor
    elif from_unit == "celsius" and to_unit == "kelvin":
        # Celsius to Kelvin: C + 273.15
        return value + 273.15
    elif from_unit == "kelvin" and to_unit == "celsius":
        # Kelvin to Celsius: K - 273.15
        return value - 273.15
    elif from_unit == "fahrenheit" and to_unit == "kelvin":
        # Fahrenheit to Kelvin: ((F - 32) / 1.8) + 273.15
        return ((value - 32) / conversion_factor) + 273.15
    elif from_unit == "kelvin" and to_unit == "fahrenheit":
        # Kelvin to Fahrenheit: ((K - 273.15) * 1.8) + 32
        return ((value - 273.15) * conversion_factor) + 32
    else:
        return value
@app.route('/temperature/', methods=['POST', 'GET'])
def temperature():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    cursor = connection.cursor()

    # Ambil ID kategori 'temperature' dari database
    cursor.execute("SELECT id FROM categories WHERE name = 'temperature'")
    category_id = cursor.fetchone()[0]

    # Query unit berdasarkan kategori ID
    cursor.execute("SELECT name, abbreviation, conversion_factor, unit_symbol FROM units WHERE category_id = %s", (category_id,))
    units = cursor.fetchall()  # Mengambil data unit dari database
    cursor.close()
    connection.close()

    units_dict = {unit[0].lower(): {'abbreviation': unit[1], 'conversion_factor': unit[2], 'unit_symbol': unit[3]} for unit in units}

    if request.method == "POST":
        unit_to_convert = request.form.get("unit_to_convert")
        unit_to_convert_to = request.form.get("unit_to_convert_to")

        # Cek apakah unit yang dipilih valid
        if not unit_to_convert or not unit_to_convert_to:
            return render_template('temperature.html', units=units_dict, invalid_input_warning=True)
        try:
            value_to_convert = float(request.form.get("value_to_convert"))
        except ValueError:
            return render_template('temperature.html', units=units_dict, invalid_input_warning=True)

        # Cek apakah unit yang dipilih valid
        if unit_to_convert.lower() not in units_dict or unit_to_convert_to.lower() not in units_dict:
            return render_template('temperature.html', units=units_dict, invalid_input_warning=True)

        # Ambil conversion_factor untuk unit yang dipilih
        from_unit = unit_to_convert.lower()
        to_unit = unit_to_convert_to.lower()
        conversion_factor = float(units_dict[from_unit]['conversion_factor'])

        # Lakukan konversi suhu
        output = convert_temperature(value_to_convert, from_unit, to_unit, conversion_factor)

        # Ambil abbreviation untuk unit yang dipilih
        from_unit_abbreviation = units_dict[from_unit]['abbreviation']
        to_unit_abbreviation = units_dict[to_unit]['abbreviation']

        # Format output dengan menghilangkan angka 0 jika ada
        if output.is_integer():  # Jika hasil konversi adalah integer
            formatted_output = f"{int(value_to_convert)} {from_unit_abbreviation} = {int(output)} {to_unit_abbreviation}"
        else:
            formatted_output = f"{int(value_to_convert)} {from_unit_abbreviation} = {output:.2f} {to_unit_abbreviation}"

        print(formatted_output)
        return render_template('temperature.html', output=formatted_output, units=units_dict, method=request.method)

    return render_template('temperature.html', units=units_dict)



@app.route('/time/', methods=['POST', 'GET'])
def time():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    connection = get_db_connection()
    cursor = connection.cursor()

    # Ambil ID kategori 'time' dari database
    cursor.execute("SELECT id FROM categories WHERE name = 'time'")
    category_id = cursor.fetchone()[0]

    # Query unit berdasarkan kategori ID
    cursor.execute("SELECT name, abbreviation, conversion_factor FROM units WHERE category_id = %s", (category_id,))
    units = cursor.fetchall()  # Mengambil data unit dari database
    cursor.close()
    connection.close()

    units_dict = {unit[0]: {'abbreviation': unit[1], 'factor': unit[2]} for unit in units}

    if request.method == "POST":
        unit_to_convert = request.form.get("unit_to_convert")
        unit_to_convert_to = request.form.get("unit_to_convert_to")

        # Cek apakah unit yang dipilih valid
        if not unit_to_convert or not unit_to_convert_to:
            return render_template('time.html', units=units_dict, invalid_input_warning=True)
        try:
            value_to_convert = float(request.form.get("value_to_convert"))
        except ValueError:
            return render_template('time.html', units=units_dict, invalid_input_warning=True)

        converter = conversion.Converter(
            "time", unit_to_convert, unit_to_convert_to, value_to_convert)
        
        if unit_to_convert not in units_dict or unit_to_convert_to not in units_dict:
            return render_template('time.html', units=units_dict, invalid_input_warning=True)
        
        converter.set_base()  # Ini memeriksa dan mengatur konversi dasar
        output = converter.return_output()[0]
        warnings = converter.return_output()[1]

        return render_template('time.html', output=output, warnings=warnings, units=units_dict, method=request.method)

    return render_template('time.html', units=units_dict)

if __name__ == '__main__':
    app.run(debug=True)
