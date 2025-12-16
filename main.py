# main.py
import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from transformer_engine import design_transformer
from pdf_generator import generate_transformer_pdf

app = FastAPI(title="Transformer Design Cloud API", version="1.0")

@app.get("/")
def home():
    return {
        "message": "Transformer Design Cloud API",
        "endpoints": {
            "/design": "Get JSON design result",
            "/design/pdf": "Download PDF report"
        }
    }

@app.get("/design/")
def design(kva: float, v1: float, v2: float, f: float = 50.0):
    # Add compliance check
    result = design_transformer(kva, v1, v2, f)
    
    # Simple compliance: check no-load loss limit (IS 1180 example)
    loss_limits = {100: 300, 250: 500, 500: 850, 1000: 1500}
    max_loss = loss_limits.get(kva, float('inf'))
    result["compliant_with_iec"] = result["no_load_loss_w"] <= max_loss
    result["f"] = f
    
    return result

@app.get("/design/pdf/")
def design_pdf(
    kva: float,
    v1: float,
    v2: float,
    f: float = 50.0,
):
    # Generate design data
    result = design_transformer(kva, v1, v2, f)
    loss_limits = {100: 300, 250: 500, 500: 850, 1000: 1500}
    max_loss = loss_limits.get(kva, float('inf'))
    result["compliant_with_iec"] = result["no_load_loss_w"] <= max_loss
    result["f"] = f

    # Generate unique filename
    filename = f"Transformer_{int(kva)}kVA_{int(v1/1000)}kV_{int(v2)}V.pdf"
    filepath = os.path.join("reports", filename)

    # Generate PDF
    generate_transformer_pdf(result, filepath)

    # Return file for download
    return FileResponse(
        path=filepath,
        media_type='application/pdf',
        filename=filename
    )