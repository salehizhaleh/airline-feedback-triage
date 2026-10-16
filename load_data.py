import csv
import random

import models
from database import SessionLocal, engine


CSV_PATH = "data/Tweets.csv"
LIMIT = 500

models.Base.metadata.create_all(bind=engine)


def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    random.seed(42)
    random.shuffle(rows)

    db = SessionLocal()
    added = 0
    seen_ids = set()

    try:
        for row in rows:
            if added >= LIMIT:
                break

            tweet_id = row["tweet_id"]

            if tweet_id in seen_ids:
                continue

            seen_ids.add(tweet_id)

            exists = (
                db.query(models.Comment)
                .filter_by(tweet_id=tweet_id)
                .first()
            )

            if exists:
                continue

            comment = models.Comment(
                tweet_id=tweet_id,
                airline=row["airline"],
                text=row["text"],
                true_sentiment=row["airline_sentiment"],
                true_reason=row["negativereason"] or None,
            )

            db.add(comment)
            added += 1

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

    print(f"Added {added} comments")


if __name__ == "__main__":
    main()