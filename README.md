# How to Run and Install
- Install pymysql -> pip install pymysql
- create database and configurate the connection in models.py
- run models.py -> py models.py
- run flask run in terminal
- open browser and go to http://127.0.0.1:5000/
- you can see the result in the browser

# Apps
-Flask
-Jinja
-MySQL

## How it Works
This program handles a wide variety of units, spanning metric, imperial, and US volume measurement systems. It currently supports 5 measurement types:
- Length
- Mass
- Volume
- Temperature
- Time

### Under the Hood: Multiple Dictionaries for Precision
To achieve accurate conversions, the program uses a base-oriented approach to data storage and representation. Instead of having a single dictionary for each measurement type (e.g. a length dictionary and a mass dictionary), it utilizes multiple dictionaries with different bases. Here's why:

- **Base Units and Accuracy:** Each dictionary has a designated "base unit" with a value of 1. The values of other units are expressed relative to this     base. 
    - This structure ensures maximum accuracy when converting between units within the same system.
- **System-Specific Dictionaries:** For example, there are separate dictionaries for metric length units (using meters as the base) and imperial length units (using inches as the base). This separation allows for precise conversions within each system.

### Choosing the Right Base

The program automatically selects the appropriate dictionary based on the units involved in the conversion. For simplicity, the following list only talks about metric and imperial systems (not US systems), because this is just meant to demonstrate understanding of the program:

- **Metric to Metric:** If both units are metric, the metric dictionary is used.
- **Imperial to Imperial:** If both units are imperial, the imperial dictionary is used.
- **Metric to Imperial (or vice versa):** In these cases, the metric base is used as a default, offering the best possible accuracy for conversions between systems.

#### Example: Metric vs. Imperial Base for Length

- **Metric Base (meter as base):** - kilometer = 1000 - meter = 1 - decimeter = 0.1 - centimeter = 0.01 - inch = 0.0254 - foot = 0.3048
- **Imperial Base (inch as base):** - kilometer = 39370.1 - meter = 39.3701 - decimeter = 3.93701 - centimeter = 0.393701 - inch = 1 - foot = 12

This approach ensures optimal accuracy for all conversions, regardless of the measurement systems involved.

# flask-converter-unit
