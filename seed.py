import bcrypt
from sqlmodel import Session, SQLModel
from app.models import User, LivestockItem
from app.database import engine
from datetime import datetime, timedelta

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def seed_db():
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Check if we already have users
        if session.query(User).first():
            print("Database already seeded.")
            return

        # Create a test farmer
        farmer = User(
            firstName="Tinashe",
            lastName="Chikwanha",
            email="farmer@example.com",
            phone="0771234567",
            password_hash=hash_password("password"), # matches verify_password logic
            verified=True,
            location="Harare"
        )
        session.add(farmer)
        session.commit()
        session.refresh(farmer)

        # Create some livestock items
        items = [
            LivestockItem(
                title="Prime Brahman Bull",
                breed="Brahman",
                age="3 years",
                weight="850kg",
                location="Harare",
                startingPrice=1500.0,
                currentBid=1650.0,
                category="cattle",
                description="Excellent breeding bull with proven genetics",
                imageUrl="https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=800",
                auctionEndDate=datetime.utcnow() + timedelta(days=2),
                seller_id=farmer.id
            ),
            LivestockItem(
                title="Boer Goat Buck",
                breed="Boer",
                age="2 years",
                weight="85kg",
                location="Gweru",
                startingPrice=200.0,
                currentBid=250.0,
                category="goats",
                description="Quality Boer goat buck for breeding",
                imageUrl="https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800",
                auctionEndDate=datetime.utcnow() + timedelta(days=3),
                seller_id=farmer.id
            )
        ]
        session.add_all(items)
        session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_db()
