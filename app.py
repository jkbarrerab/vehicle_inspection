from flask import Flask, send_from_directory, request, jsonify, render_template, send_file
import csv
import os

app = Flask(__name__)

CSV_FILE = "inspection_data.csv"

# @app.route("/")
# def serve_frontend():
#     return send_from_directory(".", "index.html")


# Ensure the CSV file has a header
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Plate", "Mileage", "Date", "Interior Cleaning", "Exterior Cleaning", "Final Remarks", 
            "Tarjeta de Gasolina", "Licencia", "Tarjeta de Circulacion", "Verificacion", "Automatico",
            "Damage Reports"
        ])

VEHICLE_DATABASE = {
    "XYZ123": {"type": "SUV", "brand": "Toyota", "driver": "John Doe", "model": "Rav4"}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_vehicle_data')
def get_vehicle_data():
    plate = request.args.get('plate')
    return jsonify(VEHICLE_DATABASE.get(plate, {}))

@app.route('/submit_inspection', methods=['POST'])
def submit_inspection():
    data = request.json
    plate = data.get("plate", "N/A")
    mileage = data.get("mileage", "N/A")
    date = data.get("date", "N/A")
    interior_cleaning = data.get("interiorCleaning", "N/A")
    exterior_cleaning = data.get("exteriorCleaning", "N/A")
    final_remarks = data.get("finalRemarks", "N/A")

    gasolina = "SI" if data.get("gasolina", False) else "NO"
    licencia = "SI" if data.get("licencia", False) else "NO"
    circulacion = "SI" if data.get("circulacion", False) else "NO"
    verificacion = "SI" if data.get("verificacion", False) else "NO"
    automatico = "SI" if data.get("automatico", False) else "NO"

    # Convert damageReports list to a string
    damage_reports = "; ".join([f"{d['part']}" for d in data.get("damageReports", [])])
    # damage_reports = "; ".join([f"{d['part']} ({d['coordinates']['x']}, {d['coordinates']['y']})" for d in data.get("damageReports", [])])

    # Append data to the CSV file
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            plate, mileage, date, interior_cleaning, exterior_cleaning, final_remarks, 
            gasolina, licencia, circulacion, verificacion, automatico, damage_reports
        ])

    return jsonify({"status": "success", "message": "Inspection data saved successfully"}), 200

@app.route("/get_csv_data")
def get_csv_data():
    """Read and return CSV file content as JSON"""
    data = []
    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            data.append(dict(zip(headers, row)))
    return jsonify(data)

@app.route("/download_csv")
def download_csv():
    return send_file(CSV_FILE, as_attachment=True)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
