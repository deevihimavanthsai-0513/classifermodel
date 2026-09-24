from typing import List
from fastapi import FastAPI, Request, UploadFile, File
from pathlib import Path
import shutil
from app.database import db
from app.database.db import SessionLocal
from app.database.models import PredictionHistory
from app.services.gradcam import generate_gradcam
from fastapi.responses import FileResponse
import pandas as pd
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database.db import SessionLocal, engine, Base
from typing import List
from sqlalchemy import func
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from app.services.predict import predict_image
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rice Intelligence Platform",
    description="AI-powered rice variety classification API",
    version="2.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    heatmap_name = f"gradcam_{file.filename}"
    heatmap_path = UPLOAD_DIR / heatmap_name
    result = predict_image(str(file_path))
    db = SessionLocal()
    history = PredictionHistory(
        image_name=file.filename,
        rice_type=result["rice_type"],
        confidence=result["confidence"]
    )
    db.add(history)
    db.commit()
    db.close()
    generate_gradcam(
        str(file_path),
        str(heatmap_path)
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "prediction": result["rice_type"],
            "confidence": result["confidence"],
            "water": result["water"],
            "fertilizer": result["fertilizer"],
            "image_url": f"/static/uploads/{file.filename}",
            "top3": result["top3"],
            "gradcam_url": f"/static/uploads/{heatmap_name}"
            
        }
    )
@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    db = SessionLocal()

    records = (
        db.query(PredictionHistory)
        .order_by(PredictionHistory.created_at.desc())
        .all()
    )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"records": records}
    )
@app.get("/batch", response_class=HTMLResponse)
async def batch_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="batch.html",
        context={}
    )
@app.post("/batch", response_class=HTMLResponse)
async def batch_predict(
    request: Request,
    files: List[UploadFile] = File(...)
):
    db = SessionLocal()

    results = []

    for file in files:

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        prediction = predict_image(str(file_path))

        history = PredictionHistory(
            image_name=file.filename,
            rice_type=prediction["rice_type"],
            confidence=prediction["confidence"]
        )

        db.add(history)

        results.append({
            "image": file.filename,
            "rice_type": prediction["rice_type"],
            "confidence": prediction["confidence"]
        })

    db.commit()
    db.close()

    average = round(
        sum(r["confidence"] for r in results) / len(results),
        2
    )

    return templates.TemplateResponse(
        request=request,
        name="batch.html",
        context={
            "results": results,
            "total": len(results),
            "average": average
        }
    )
@app.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    db = SessionLocal()

    total = db.query(PredictionHistory).count()

    avg_confidence = (
        db.query(func.avg(PredictionHistory.confidence))
        .scalar() or 0
    )

    counts = (
        db.query(
            PredictionHistory.rice_type,
            func.count(PredictionHistory.id)
        )
        .group_by(PredictionHistory.rice_type)
        .all()
    )

    most_common = max(counts, key=lambda x: x[1])[0] if counts else "N/A"

    db.close()

    chart_data = [
        {"name": name, "count": count}
        for name, count in counts
    ]

    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={
            "total": total,
            "average": round(avg_confidence, 2),
            "most_common": most_common,
            "chart_data": chart_data
        }
    )
@app.get("/export/pdf")
async def export_pdf():

    db = SessionLocal()

    records = db.query(PredictionHistory).all()

    db.close()

    pdf_path = "reports/rice_prediction_report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>Rice Intelligence Platform</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Prediction Analytics Report",
            styles["Heading2"]
        )
    )

    table_data = [
        ["Image", "Rice Type", "Confidence", "Timestamp"]
    ]

    for r in records:
        table_data.append([
            r.image_name,
            r.rice_type,
            f"{r.confidence}%",
            str(r.created_at)[:19]
        ])

    table = Table(table_data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.green),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 10),
    ]))

    elements.append(table)

    doc.build(elements)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="Rice_Prediction_Report.pdf"
    )