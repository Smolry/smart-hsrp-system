from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import numpy as np
import cv2

from backend.core.pipeline import run_pipeline
from backend.db.database import get_db
from backend.services.storage import persist_pipeline_result

router = APIRouter()


@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    contents = await file.read()
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    return run_pipeline(img, force_save=False)


@router.get("/violations")
def get_violations(db=Depends(get_db)):
    cur = db.cursor()

    # 1️⃣ Fetch events
    cur.execute(
        """
        SELECT
            id,
            helmet_violation,
            helmet_confidence,
            helmet_count,
            image_path,
            created_at
        FROM events
        ORDER BY created_at DESC
        LIMIT 100
        """
    )

    events = cur.fetchall()
    response = []

    # 2️⃣ Fetch plates per event
    for event in events:
        cur.execute(
            """
            SELECT
                plate_text,
                is_hsrp,
                hsrp_confidence,
                ocr_confidence
            FROM plate_violations
            WHERE event_id = %s
            """,
            (event["id"],)
        )

        plates = cur.fetchall()

        response.append({
            "id": event["id"],
            "helmet_violation": bool(event["helmet_violation"]),
            "helmet_confidence": event["helmet_confidence"],
            "helmet_count": event["helmet_count"],
            "image_path": event["image_path"],
            "created_at": event["created_at"],
            "plates": [
                {
                    "ocr_text": p["plate_text"],
                    "is_hsrp": bool(p["is_hsrp"]),
                    "hsrp_confidence": p["hsrp_confidence"],
                    "ocr_confidence": p["ocr_confidence"],
                }
                for p in plates
            ],
        })

    return response


@router.post("/save")
async def save_record(payload: dict):
    event = payload.get("event")
    plates = payload.get("plates")

    if not event or plates is None:
        raise HTTPException(status_code=400, detail="Invalid payload")

    persist_pipeline_result(event, plates)
    return {"status": "saved"}
