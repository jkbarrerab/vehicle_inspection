from flask import Flask, send_from_directory, request, jsonify, render_template, send_file
import csv
import os

app = Flask(__name__)

CSV_FILE = "inspection_data.csv"


DB_FILE = "vehicle_db.csv"  # Updated path to the newly uploaded vehicle database

# Function to fetch vehicle details from CSV based on plate number
def get_vehicle_data(plate_number):
    try:
        with open(DB_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)  # Read CSV as dictionary
            for row in reader:
                if row["PLACA"].strip().upper() == plate_number.strip().upper():
                    return {
                        "plate": row["PLACA"],
                        "brand": row["MARCA"],
                        "driver": row["CONDUCTOR"],
                        "model": row["MODELO"],
                        "OT": row["OT"],
                    }
        return None  # Return None if plate is not found
    except Exception as e:
        return {"error": f"Error reading CSV: {str(e)}"}

# Ensure the CSV file has a header
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Plate", "Mileage", "Date", "Interior Cleaning", "Exterior Cleaning", "Final Remarks", 
            "Tarjeta de Gasolina", "Licencia", "Tarjeta de Circulacion", "Verificacion", "Automatico",
            "Damage Reports"
        ])

@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to fetch vehicle data
@app.route("/get_vehicle_data", methods=["GET"])
def fetch_vehicle_data():
    plate = request.args.get("plate")
    if not plate:
        return jsonify({"error": "Plate number is required"}), 400
    
    vehicle_info = get_vehicle_data(plate)
    if vehicle_info:
        return jsonify(vehicle_info)
    else:
        return jsonify({"error": "Vehicle not found"}), 404


@app.route('/submit_inspection', methods=['POST'])
def submit_inspection():
    data = request.json
    print(data)
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
    damage_reports = "; ".join([f"{d['part']}: {d['observation']}" for d in data.get("damageReports", [])])
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
