import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class SalesData(Base):
    __tablename__ = 'sales_data'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    product_category = Column(String)
    region = Column(String)
    price = Column(Numeric)
    quantity = Column(Integer)
    order_date = Column(DateTime)

class UserEvent(Base):
    __tablename__ = 'user_events'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    event_type = Column(String)
    event_date = Column(DateTime)
    session_id = Column(String)
    device_type = Column(String)

def seed_data():
    try:
        # Create tables
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        
        session = Session()
        
        # Seed Sales Data
        categories = ['Electronics', 'Clothing', 'Home', 'Beauty', 'Sports']
        regions = ['North', 'South', 'East', 'West', 'Central']
        
        print("Seeding 1000 rows of sales data...")
        for _ in range(1000):
            sale = SalesData(
                user_id=random.randint(100, 500),
                product_category=random.choice(categories),
                region=random.choice(regions),
                price=random.uniform(10.0, 500.0),
                quantity=random.randint(1, 5),
                order_date=datetime.now() - timedelta(days=random.randint(0, 365))
            )
            session.add(sale)
        
        # Seed User Events
        event_types = ['login', 'page_view', 'add_to_cart', 'purchase', 'logout']
        devices = ['desktop', 'mobile', 'tablet']
        
        print("Seeding 500 rows of user event data...")
        for _ in range(500):
            event = UserEvent(
                user_id=random.randint(100, 500),
                event_type=random.choice(event_types),
                event_date=datetime.now() - timedelta(days=random.randint(0, 30)),
                session_id=f"sess_{random.randint(1000, 9999)}",
                device_type=random.choice(devices)
            )
            session.add(event)
        
        session.commit()
        print("Seeding completed successfully.")
        session.close()
    except Exception as e:
        print(f"Seeding failed: {e}")

if __name__ == "__main__":
    seed_data()
