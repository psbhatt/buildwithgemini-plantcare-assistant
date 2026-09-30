import datetime
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-f2446fdf298c"

def seed_plants():
    db = firestore.Client(project=PROJECT_ID)
    plants_ref = db.collection("plants")
    
    sample_plants = [
        {
            "id": "monstera-deliciosa",
            "name": "Monty",
            "species": "Monstera Deliciosa",
            "location": "Living Room (East window)",
            "light_requirement": "Bright indirect light",
            "watering_interval_days": 7,
            "last_watered": (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            "health_status": "Thriving",
            "notes": "Large fenestrated leaves; likes moderate humidity.",
            "care_guide": "Allow top 2-3 inches of soil to dry out between waterings. Wipe leaves occasionally."
        },
        {
            "id": "snake-plant",
            "name": "Ziggy",
            "species": "Sansevieria Trifasciata",
            "location": "Bedroom (Low light)",
            "light_requirement": "Low to bright indirect light",
            "watering_interval_days": 21,
            "last_watered": (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=18)).strftime("%Y-%m-%d"),
            "health_status": "Needs watering soon",
            "notes": "Very hardy, air-purifying, drought tolerant.",
            "care_guide": "Let soil dry completely between waterings. Water sparingly in winter."
        },
        {
            "id": "fiddle-leaf-fig",
            "name": "Fiona",
            "species": "Ficus Lyrata",
            "location": "Home Office (South-facing window)",
            "light_requirement": "Bright, consistent direct/indirect light",
            "watering_interval_days": 10,
            "last_watered": (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=9)).strftime("%Y-%m-%d"),
            "health_status": "Slight browning on lower leaf tip",
            "notes": "Sensitive to drafts and sudden changes in position.",
            "care_guide": "Water when top 1-2 inches are dry. Rotate weekly to promote even growth."
        },
        {
            "id": "golden-pothos",
            "name": "Penny",
            "species": "Epipremnum Aureum",
            "location": "Kitchen Shelf",
            "light_requirement": "Moderate indirect light",
            "watering_interval_days": 8,
            "last_watered": (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "health_status": "Vibrant and trailing",
            "notes": "Fast growing trailing vine; easy propagation.",
            "care_guide": "Tolerates low light and missed waterings. Droops visibly when thirsty."
        }
    ]

    print(f"Seeding plants to project: {PROJECT_ID}...")
    for plant in sample_plants:
        doc_id = plant["id"]
        plants_ref.document(doc_id).set(plant)
        print(f"  ✓ Seeded: {plant['name']} ({plant['species']}) -> document id: {doc_id}")

    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed_plants()
