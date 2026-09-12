const API_BASE = "http://localhost:8000";

// Handle form submissions for prediction (Tumor or Stroke)
async function submitPredictionForm(e, type) {
    e.preventDefault();
    const form = e.target;
    const loader = document.getElementById('loader');
    const resultBox = document.getElementById('result-box');
    const submitBtn = document.getElementById('submit-btn');
    
    loader.style.display = 'block';
    resultBox.style.display = 'none';
    submitBtn.disabled = true;

    try {
        const formData = new FormData(form);
        const response = await fetch(`${API_BASE}/${type}/predict`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        if (response.ok) {
            // According to PredictionResponse schema
            // Typically includes patient_id, prediction, confidence, etc.
            resultBox.innerHTML = `
                <h3>Analysis Complete</h3>
                <p><strong>Patient ID:</strong> ${data.patient_id || data.id || 'N/A'}</p>
                <p><strong>Diagnosis/Prediction:</strong> ${data.prediction || 'Unknown'}</p>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 10px;">
                    Record safely stored in database. You can view it in the database section.
                </p>
            `;
            resultBox.style.display = 'block';
            form.reset();
            document.getElementById('file-name').textContent = "Upload MRI Image";
        } else {
            let errorMsg = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
            alert("API Error: " + errorMsg);
        }
    } catch (error) {
        console.error(error);
        alert("Failed to connect to API. Is the backend running on http://localhost:8000?");
    } finally {
        loader.style.display = 'none';
        submitBtn.disabled = false;
    }
}

// Fetch and render patients database
async function loadDatabase(type) {
    const tableBody = document.getElementById('table-body');
    const loader = document.getElementById('loader');
    
    tableBody.innerHTML = '';
    loader.style.display = 'block';

    try {
        const response = await fetch(`${API_BASE}/${type}/patients`);
        if (!response.ok) throw new Error("Failed to fetch data");
        const data = await response.json();
        
        if (data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No records found.</td></tr>';
            return;
        }

        data.forEach(patient => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${patient.id || patient.patient_id}</td>
                <td>${patient.name}</td>
                <td>${patient.age} / ${patient.gender}</td>
                <td>${patient.prediction || '-'}</td>
                <td>
                    <div class="action-btns">
                        <button class="btn outline" onclick="viewImage('${type}', '${patient.id || patient.patient_id}')">View MRI</button>
                        <button class="btn danger" onclick="deletePatient('${type}', '${patient.id || patient.patient_id}')">Delete</button>
                    </div>
                </td>
            `;
            tableBody.appendChild(tr);
        });
    } catch (error) {
        console.error(error);
        tableBody.innerHTML = '<tr><td colspan="6" style="text-align:center; color: var(--accent);">Error connecting to API.</td></tr>';
    } finally {
        loader.style.display = 'none';
    }
}

// View Patient Image in new tab
function viewImage(type, patientId) {
    window.open(`${API_BASE}/${type}/image/${patientId}`, '_blank');
}

// Delete patient record
async function deletePatient(type, patientId) {
    if (!confirm("Are you sure you want to delete this record?")) return;

    try {
        const response = await fetch(`${API_BASE}/${type}/patient/${patientId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            // refresh data
            loadDatabase(type);
        } else {
            const data = await response.json();
            alert("Error: " + (data.detail || "Failed to delete"));
        }
    } catch (error) {
        alert("Failed to delete record.");
    }
}

// Update file upload UI
function updateFileName(input) {
    if (input.files && input.files[0]) {
        document.getElementById('file-name').textContent = input.files[0].name;
    }
}

// Search patient by ID
async function searchPatient(type) {
    const searchInput = document.getElementById('search-id').value.trim();
    if (!searchInput) {
        loadDatabase(type);
        return;
    }

    const tableBody = document.getElementById('table-body');
    const loader = document.getElementById('loader');
    
    tableBody.innerHTML = '';
    loader.style.display = 'block';

    try {
        const response = await fetch(`${API_BASE}/${type}/patient/${searchInput}`);
        if (response.status === 404) {
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Patient not found.</td></tr>';
            return;
        }
        if (!response.ok) throw new Error("Failed to fetch data");
        const patient = await response.json();
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${patient.id || patient.patient_id || searchInput}</td>
            <td>${patient.name}</td>
            <td>${patient.age} / ${patient.gender}</td>
            <td>${patient.prediction || '-'}</td>
            <td>
                <div class="action-btns">
                    <button class="btn outline" onclick="viewImage('${type}', '${patient.id || patient.patient_id || searchInput}')">View MRI</button>
                    <button class="btn danger" onclick="deletePatient('${type}', '${patient.id || patient.patient_id || searchInput}')">Delete</button>
                </div>
            </td>
        `;
        tableBody.appendChild(tr);
    } catch (error) {
        console.error(error);
        tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color: var(--accent);">Error connecting to API.</td></tr>';
    } finally {
        loader.style.display = 'none';
        document.getElementById('search-id').value = '';
    }
}
