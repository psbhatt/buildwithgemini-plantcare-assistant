import datetime
from typing import Any, Dict, List, Optional
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-f2446fdf298c"

def _get_db() -> firestore.Client:
    return firestore.Client(project=PROJECT_ID)

def list_plants() -> List[Dict[str, Any]]:
    """List all tracked houseplants and their care schedules and health status.

    Returns:
        A list of plant records containing species, care requirements, watering status, and notes.
    """
    db = _get_db()
    docs = db.collection("plants").stream()
    plants = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        plants.append(data)
    return plants

def get_plant(plant_id_or_name: str) -> Dict[str, Any]:
    """Retrieve detailed information and care guide for a specific houseplant.

    Args:
        plant_id_or_name: The plant document ID or the common name/nickname (e.g. 'Monty', 'monstera-deliciosa', 'snake-plant').

    Returns:
        The plant record dictionary or an error message if not found.
    """
    db = _get_db()
    plants_ref = db.collection("plants")
    
    # Try direct ID lookup
    doc = plants_ref.document(plant_id_or_name.lower().strip().replace(" ", "-")).get()
    if doc.exists:
        data = doc.to_dict()
        data["id"] = doc.id
        return data

    # Try name or species search
    for d in plants_ref.stream():
        data = d.to_dict()
        name = data.get("name", "").lower()
        species = data.get("species", "").lower()
        query = plant_id_or_name.lower().strip()
        if query in name or query in species or query in d.id:
            data["id"] = d.id
            return data

    return {"error": f"Plant '{plant_id_or_name}' not found in your collection."}

def log_watering(plant_id_or_name: str, notes: Optional[str] = None) -> Dict[str, Any]:
    """Log that a plant was watered today and update its watering records.

    Args:
        plant_id_or_name: The plant document ID or name (e.g. 'Monty', 'monstera-deliciosa').
        notes: Optional observation or care notes during watering.

    Returns:
        Status message with updated watering date and next due date.
    """
    db = _get_db()
    plant = get_plant(plant_id_or_name)
    if "error" in plant:
        return plant

    plant_id = plant["id"]
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    
    update_data = {
        "last_watered": today_str,
        "health_status": "Recently watered"
    }
    if notes:
        existing_notes = plant.get("notes", "")
        update_data["notes"] = f"{existing_notes} [{today_str}]: {notes}".strip()

    db.collection("plants").document(plant_id).update(update_data)
    
    watering_interval = plant.get("watering_interval_days", 7)
    next_watering = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=watering_interval)).strftime("%Y-%m-%d")
    
    return {
        "status": "success",
        "message": f"Successfully logged watering for {plant.get('name', plant_id)} ({plant.get('species', '')}).",
        "last_watered": today_str,
        "next_watering_due": next_watering
    }

def add_plant(
    name: str,
    species: str,
    location: str,
    light_requirement: str,
    watering_interval_days: int,
    notes: Optional[str] = "",
    care_guide: Optional[str] = ""
) -> Dict[str, Any]:
    """Add a new houseplant to the user's collection in Firestore.

    Args:
        name: Common name or nickname (e.g. 'Monty', 'Spike').
        species: Botanical/species name (e.g. 'Monstera Deliciosa', 'Chlorophytum Comosum').
        location: Where the plant is placed (e.g. 'Living Room windowsill', 'Balcony').
        light_requirement: Lighting needs (e.g. 'Bright indirect light', 'Low light').
        watering_interval_days: Recommended watering frequency in days.
        notes: Initial observations or notes.
        care_guide: Care recommendations (humidity, soil, pruning).

    Returns:
        Success message and the created plant document ID.
    """
    db = _get_db()
    doc_id = name.lower().replace(" ", "-").strip()
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    plant_data = {
        "id": doc_id,
        "name": name,
        "species": species,
        "location": location,
        "light_requirement": light_requirement,
        "watering_interval_days": watering_interval_days,
        "last_watered": today_str,
        "health_status": "Healthy",
        "notes": notes or "",
        "care_guide": care_guide or ""
    }

    db.collection("plants").document(doc_id).set(plant_data)
    return {
        "status": "success",
        "message": f"Added {name} ({species}) to your plant collection.",
        "plant_id": doc_id
    }
