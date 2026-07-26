import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_path = os.path.join(project_root, "backend", "database.db")

engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    provider = Column(String, default="email")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True, nullable=False)
    city = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)
    sqft_living = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Float, nullable=False)
    estimated_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# Initialize Database Tables
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def find_or_create_user(email, name="User", picture=None, provider="google"):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                name=name,
                picture=picture,
                provider=provider
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            if name and user.name != name:
                user.name = name
            if picture and user.picture != picture:
                user.picture = picture
            db.commit()
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "picture": user.picture,
            "provider": user.provider
        }
    finally:
        db.close()


def save_prediction(user_email, city, zipcode, sqft_living, bedrooms, bathrooms, estimated_price):
    db = SessionLocal()
    try:
        pred = Prediction(
            user_email=user_email,
            city=city,
            zipcode=zipcode,
            sqft_living=sqft_living,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            estimated_price=estimated_price
        )
        db.add(pred)
        db.commit()
        db.refresh(pred)
        return {
            "id": pred.id,
            "user_email": pred.user_email,
            "city": pred.city,
            "zipcode": pred.zipcode,
            "sqft_living": pred.sqft_living,
            "bedrooms": pred.bedrooms,
            "bathrooms": pred.bathrooms,
            "estimated_price": pred.estimated_price,
            "created_at": pred.created_at.strftime("%Y-%m-%d %H:%M")
        }
    finally:
        db.close()


def get_user_predictions(user_email, limit=20):
    db = SessionLocal()
    try:
        preds = db.query(Prediction).filter(
            Prediction.user_email == user_email
        ).order_by(Prediction.created_at.desc()).limit(limit).all()

        return [
            {
                "id": p.id,
                "city": p.city,
                "zipcode": p.zipcode,
                "sqft_living": p.sqft_living,
                "bedrooms": p.bedrooms,
                "bathrooms": p.bathrooms,
                "estimated_price": p.estimated_price,
                "created_at": p.created_at.strftime("%b %d, %Y %H:%M")
            }
            for p in preds
        ]
    finally:
        db.close()
