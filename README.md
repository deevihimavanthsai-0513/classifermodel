# 🌾 GrainPalette — AI Rice Intelligence Platform

An end-to-end AI-powered web application that classifies **5 rice varieties** from grain images using **MobileNet CNN**, provides **Grad-CAM explainability**, stores predictions in **SQLite**, and supports **batch inference**, **analytics**, **CSV/PDF reports**, **Docker**, and **GitHub Actions CI**.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![CI](https://img.shields.io/badge/GitHub_Actions-CI-success)

---

## 📌 Overview

GrainPalette helps identify rice varieties from uploaded images and provides cultivation guidance such as water and fertilizer recommendations.

The application combines **Deep Learning**, **Explainable AI**, **FastAPI**, and **Data Analytics** into a production-style architecture.

### Supported Rice Varieties

- Arborio
- Basmati
- Ipsala
- Jasmine
- Karacadag

---

## ✨ Features

- 🔍 AI rice classification using MobileNet Transfer Learning
- 🎯 Top-3 prediction probabilities
- 🔥 Grad-CAM visualization for model explainability
- 💧 Water & fertilizer recommendations
- 📁 Batch prediction for multiple images
- 🗂 Prediction history with SQLite
- 📊 Analytics dashboard with statistics
- 📄 Export prediction history to CSV
- 📑 Generate professional PDF reports
- 🐳 Docker containerization
- ⚙ GitHub Actions CI workflow

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Backend | FastAPI |
| Deep Learning | TensorFlow / Keras |
| CNN | MobileNet |
| Explainability | Grad-CAM |
| Database | SQLite + SQLAlchemy |
| Frontend | HTML, CSS, Jinja2 |
| Reports | Pandas, ReportLab |
| DevOps | Docker, GitHub Actions |

---

## 🏗 System Architecture

```text
User Upload
     │
     ▼
 FastAPI Backend
     │
     ├── Image Preprocessing
     ├── MobileNet Prediction
     ├── Grad-CAM Heatmap
     ├── SQLite Storage
     └── HTML Response
            │
            ▼
 Analytics • History • CSV • PDF
```

---

## 📸 Screenshots

> Replace these images with screenshots from your project.

### Home Page

![Home](screenshots/home.png)

### Prediction Result

![Prediction](screenshots/result.png)

### Analytics Dashboard

![Analytics](screenshots/analytics.png)

### Batch Prediction

![Batch](screenshots/batch.png)

---

## 📂 Project Structure

```text
GrainPalette/
│
├── app/
│   ├── database/
│   ├── models/
│   ├── services/
│   └── main.py
│
├── templates/
├── static/
├── reports/
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🚀 Local Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/GrainPalette.git
cd GrainPalette
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000
```

---

## 🐳 Run with Docker

Build the image:

```bash
docker build -t grainpalette .
```

Run the container:

```bash
docker run -p 8000:8000 grainpalette
```

Open:

```
http://localhost:8000
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Home page |
| POST | `/upload` | Single image prediction |
| GET | `/history` | Prediction history |
| GET | `/batch` | Batch prediction page |
| POST | `/batch` | Batch inference |
| GET | `/analytics` | Analytics dashboard |
| GET | `/export/csv` | Download CSV |
| GET | `/export/pdf` | Download PDF |

---

## 📈 Model Information

- **Architecture:** MobileNet (Transfer Learning)
- **Classes:** 5 Rice Varieties
- **Input Size:** 224 × 224
- **Output:** Softmax probabilities
- **Explainability:** Grad-CAM
- **Inference:** Real-time FastAPI API

---

## ⚙ CI/CD

GitHub Actions automatically:

- Install dependencies
- Verify project compilation
- Validate FastAPI imports
- Run on every push to `main`

Workflow file:

```text
.github/workflows/ci.yml
```

---

## 🔮 Future Improvements

- EfficientNetB0 for higher accuracy
- User authentication
- PostgreSQL support
- Cloud deployment (Render/AWS)
- REST API documentation with Swagger

---

## 👨‍💻 Author

**Himavanth Sai**

B.Tech Artificial Intelligence & Data Science

GitHub: https://github.com/YOUR_USERNAME
