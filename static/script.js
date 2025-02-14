let damageReports = [];

function openDamagePopup(partId) {
    document.getElementById('popup').style.display = 'block';
    document.getElementById('damagePart').value = partId;
}

function closeDamagePopup() {
    document.getElementById('popup').style.display = 'none';
}
function saveDamageReport() {
    const part = document.getElementById('damagePart').value;
    const observation = document.getElementById('damageObservation').value;
    damageReports.push({ part, observation });
    closeDamagePopup();
    console.log(`Damage reported on ${part}: ${observation}`);
}

function fetchVehicleData() {
    const plate = document.getElementById("plate").value;
    fetch(`/get_vehicle_data?plate=${plate}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("vehicle-info").innerHTML = 
                `<p>Type: ${data.type}</p><p>Brand: ${data.brand}</p><p>Driver: ${data.driver}</p><p>Model: ${data.model}</p>`;
        });
}

function reportDamage(event) {
    const target = event.target;
    const partId = target.id ? target.id : "Unknown Part";
    const sketch = document.getElementById("car-sketch");
    const rect = sketch.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const damageEntry = { part: partId, coordinates: { x, y } };
    damageReports.push(damageEntry);
    console.log(`Damage reported:`, damageEntry);
    alert(`Damage reported on part: ${partId} at coordinates: (${x}, ${y})`);
}


function submitInspection() {
    const data = {
        plate: document.getElementById("plate").value,
        mileage: document.getElementById("mileage").value,
        date: document.getElementById("date").value,
        interiorCleaning: document.getElementById("interiorCleaning").value,
        exteriorCleaning: document.getElementById("exteriorCleaning").value,
        finalRemarks: document.getElementById("finalRemarks").value,
        damageReports:damageReports
    };
    fetch("/submit_inspection", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    }).then(response => response.json())
              .then(result => console.log("Inspection submitted successfully:", result))
              .catch(error => console.error("Error submitting inspection:", error));
}

function loadCSVData() {
    fetch("/get_csv_data")
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById("csv-preview");
            table.innerHTML = ""; // Clear previous content

            // Add headers
            if (data.length > 0) {
                const headerRow = document.createElement("tr");
                Object.keys(data[0]).forEach(key => {
                    const th = document.createElement("th");
                    th.textContent = key;
                    headerRow.appendChild(th);
                });
                table.appendChild(headerRow);
            }

            // Add rows
            data.forEach(row => {
                const tr = document.createElement("tr");
                Object.values(row).forEach(value => {
                    const td = document.createElement("td");
                    td.textContent = value;
                    tr.appendChild(td);
                });
                table.appendChild(tr);
            });
        })
        .catch(error => console.error("Error loading CSV data:", error));
}

function downloadCSV() {
    window.location.href = "/download_csv";
        }

// Load CSV data when the page loads
document.addEventListener("DOMContentLoaded", loadCSVData);