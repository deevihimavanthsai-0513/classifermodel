from app.database.db import Base, engine, SessionLocal
from app.database.models import RiceInfo

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Prevent duplicate inserts
if db.query(RiceInfo).count() == 0:
    rice_data = [
        RiceInfo(
            variety="Arborio",
            water="High (flooded fields)",
            fertilizer="High nitrogen, phosphorus and potassium"
        ),
        RiceInfo(
            variety="Basmati",
            water="Moderate to high",
            fertilizer="Balanced NPK with organic fertilizer"
        ),
        RiceInfo(
            variety="Ipsala",
            water="High",
            fertilizer="Nitrogen-rich fertilizer"
        ),
        RiceInfo(
            variety="Jasmine",
            water="Moderate",
            fertilizer="Moderate NPK with compost"
        ),
        RiceInfo(
            variety="Karacadag",
            water="Low to moderate",
            fertilizer="Minimal slow-release fertilizer"
        ),
    ]

    db.add_all(rice_data)
    db.commit()
    print("Database seeded successfully!")
else:
    print("Rice data already exists.")

db.close()