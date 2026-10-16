"""Collection ledger for a dairy cooperative.

Records each farmer's milk deliveries, totals a day's collection, finds the
top supplier, flags low-fat milk and prints collection slips.
"""

import hashlib
import sqlite3

LOW_FAT_THRESHOLD = 3.5


def create_ledger():
    """Create an in-memory database with the milk table."""
    db = sqlite3.connect(":memory:")
    db.execute(
        "CREATE TABLE milk (id INTEGER PRIMARY KEY, farmer TEXT, "
        "litres REAL, fat REAL, day TEXT)"
    )
    return db


def record_milk(db, farmer, litres, fat, day):
    """Store one milk delivery for a farmer."""
    db.execute(
        "INSERT INTO milk (farmer, litres, fat, day) VALUES (?, ?, ?, ?)",
        (farmer, litres, fat, day),
    )
    db.commit()


def farmer_token(farmer):
    """Return a stable SHA-256 token identifying a farmer."""
    return hashlib.sha256(farmer.encode()).hexdigest()


def daily_total(db, day):
    """Return a formatted total of litres collected on the given day."""
    rows = db.execute(
        "SELECT litres FROM milk WHERE day = ?", (day,)
    ).fetchall()
    return f"Total: {sum(r[0] for r in rows):.1f} litres"


def top_farmer(db):
    """Return the farmer who supplied the most litres, or None if empty."""
    rows = db.execute(
        "SELECT farmer, SUM(litres) FROM milk GROUP BY farmer"
    ).fetchall()
    if not rows:
        return None
    top = max(rows, key=lambda r: r[1])
    return top[0]


def print_slip(farmer):
    """Print a collection slip for a farmer."""
    print(f"printing slip for {farmer}")


def low_fat(db):
    """Return farmers whose milk fat is missing or below the threshold."""
    rows = db.execute("SELECT farmer, fat FROM milk").fetchall()
    return [f for f, fat in rows if fat is None or fat < LOW_FAT_THRESHOLD]


def main():
    """Run a short demonstration of the ledger."""
    db = create_ledger()
    record_milk(db, "Gopal", 12.5, 4.1, "Mon")
    record_milk(db, "Lata", 20.0, 3.2, "Mon")
    print(daily_total(db, "Mon"), top_farmer(db), low_fat(db))
    print_slip("Gopal")
    print(farmer_token("Lata"))
    db.close()


if __name__ == "__main__":
    main()
