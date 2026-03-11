"""
Seed script for Supabase — populates livestock_items with sample data.
Requires SUPABASE_URL and SUPABASE_KEY in .env.

Usage:
    python seed.py
"""
from datetime import datetime, timedelta
from db import supabase


SAMPLE_ITEMS = [
    {
        "title": "Prime Brahman Bull",
        "breed": "Brahman",
        "age": "3 years",
        "weight": "850kg",
        "location": "Harare",
        "startingPrice": 1500.0,
        "currentBid": 1650.0,
        "category": "cattle",
        "description": "Excellent breeding bull with proven genetics",
        "imageUrl": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=800&fit=crop&crop=center",
        "healthStatus": "verified",
        "auctionEndDate": (datetime.utcnow() + timedelta(days=2)).isoformat(),
    },
    {
        "title": "Productive Dairy Cow",
        "breed": "Holstein Friesian",
        "age": "4 years",
        "weight": "650kg",
        "location": "Bulawayo",
        "startingPrice": 700.0,
        "currentBid": 950.0,
        "category": "cattle",
        "description": "High-yielding dairy cow with excellent health records",
        "imageUrl": "https://images.unsplash.com/photo-1546445317-29f4545e9d53?w=800&fit=crop&crop=center",
        "healthStatus": "verified",
        "auctionEndDate": (datetime.utcnow() + timedelta(days=3)).isoformat(),
    },
    {
        "title": "Boer Goat Buck",
        "breed": "Boer",
        "age": "2 years",
        "weight": "85kg",
        "location": "Gweru",
        "startingPrice": 200.0,
        "currentBid": 285.0,
        "category": "goats",
        "description": "Quality Boer goat buck for breeding",
        "imageUrl": "https://images.unsplash.com/photo-1524024973431-2ad916746881?w=800&fit=crop&crop=center",
        "healthStatus": "verified",
        "auctionEndDate": (datetime.utcnow() + timedelta(days=5)).isoformat(),
    },
    {
        "title": "Free Range Chickens (10)",
        "breed": "Rhode Island Red",
        "age": "8 months",
        "weight": "2kg each",
        "location": "Mutare",
        "startingPrice": 80.0,
        "currentBid": 120.0,
        "category": "chickens",
        "description": "Healthy free-range chickens ready for laying",
        "imageUrl": "https://images.unsplash.com/photo-1612170153139-6f881ff067e0?w=800&fit=crop&crop=center",
        "healthStatus": "verified",
        "auctionEndDate": (datetime.utcnow() + timedelta(days=1)).isoformat(),
    },
    {
        "title": "Dorper Sheep Ram",
        "breed": "Dorper",
        "age": "2.5 years",
        "weight": "95kg",
        "location": "Masvingo",
        "startingPrice": 300.0,
        "currentBid": 420.0,
        "category": "sheep",
        "description": "Premium Dorper ram with excellent meat quality",
        "imageUrl": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=800&fit=crop&crop=center",
        "healthStatus": "verified",
        "auctionEndDate": (datetime.utcnow() + timedelta(days=4)).isoformat(),
    },
    {
        "title": "Large White Pigs (2)",
        "breed": "Large White",
        "age": "1 year",
        "weight": "120kg each",
        "location": "Chinhoyi",
        "startingPrice": 250.0,
        "currentBid": 380.0,
        "category": "pigs",
        "description": "Healthy Large White pigs ready for breeding",
        "imageUrl": "https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=800&fit=crop&crop=center",
        "healthStatus": "verified",
        "auctionEndDate": (datetime.utcnow() + timedelta(days=7)).isoformat(),
    },
]


def seed():
    if not supabase:
        print("ERROR: Supabase not configured. Set SUPABASE_URL and SUPABASE_KEY in .env")
        return

    existing = supabase.table("livestock_items").select("id").limit(1).execute()
    if existing.data:
        print("Database already has items -- skipping seed.")
        return

    res = supabase.table("livestock_items").insert(SAMPLE_ITEMS).execute()
    print(f"Seeded {len(res.data)} livestock items.")


if __name__ == "__main__":
    seed()
