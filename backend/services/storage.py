from backend.db.database import get_db


def persist_pipeline_result(event_data, plates):
    db_gen = get_db()
    conn = next(db_gen)

    try:
        cur = conn.cursor()

        # Insert event and get ID
        cur.execute(
            """
            INSERT INTO events
            (helmet_violation, helmet_confidence, helmet_count, image_path)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (
                event_data["helmet_violation"],
                event_data["helmet_confidence"],
                event_data["helmet_count"],
                event_data["image_path"],
            ),
        )

        event_id = cur.fetchone()["id"]

        for p in plates:
            cur.execute(
                """
                INSERT INTO plate_violations
                (event_id, plate_text, is_hsrp, hsrp_confidence, ocr_confidence,
                 bbox_x1, bbox_y1, bbox_x2, bbox_y2)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    event_id,
                    p["ocr_text"],
                    p["is_hsrp"],
                    p["hsrp_confidence"],
                    p["ocr_confidence"],
                    p["bbox"][0],
                    p["bbox"][1],
                    p["bbox"][2],
                    p["bbox"][3],
                ),
            )

    finally:
        db_gen.close()
