from sqlalchemy import Column, Float, Integer, String, DateTime
from Connections.connections import Base,engine
from datetime import datetime, UTC
from hashing import Harsher
from pydantic import BaseModel
import joblib

class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True, index=True)
    Nitrogen = Column(Float)
    Phosphorus = Column(Float)
    Potassium = Column(Float)
    timestamp = Column(DateTime, default=datetime.now(UTC))

    # addig data to the database
    @staticmethod
    def add_sensor_data(db_session, Nitrogen, Phosphorus, Potassium):
        sensor_data = SensorData(Nitrogen=Nitrogen, Phosphorus=Phosphorus, Potassium=Potassium)
        try:
            db_session.add(sensor_data)
            db_session.commit()
            db_session.refresh(sensor_data)
        except Exception as e:
            print(f"Error occurred: {e}")
            db_session.rollback()

    @staticmethod
    def get_predictions(Nitrogen, Phosphorus, Potassius, Ph):
        entered_data = [[Nitrogen, Phosphorus, Potassius, Ph]]
        loaded_model = joblib.load('D:\\UICT\\Backend\\Models\\model.pkl')
        predicted_crop = loaded_model.predict(entered_data)
        return {"predicted_crop": predicted_crop}

# Base.metadata.drop_all(engine) 

class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String)
    password = Column(String)
    email = Column(String)

    @staticmethod
    def get_admin(db_session):
        return db_session.query(Admin).all()
    
    @staticmethod
    def username_exists(db_session, username):
        return db_session.query(Admin).filter(Admin.username == username).first() is not None
    
    @staticmethod
    def get_username(db_session):
        return db_session.query(Admin.username).all()
    
    @staticmethod
    def get_userdata_by_username(db_session, username):
        return db_session.query(Admin).filter(Admin.username == username).first()

    @staticmethod
    def confirm_password_login(db_session, username, password):
       # username can be username or email
        return db_session.query(Admin).filter(Admin.username == username, Admin.password == password).first()
    
    def update_password(self, new_password):
        hashed_password = Harsher.get_hash_password(new_password)
        print(f"Updating password to: {hashed_password}") 
        self.password = hashed_password

    def update_username(self, new_username_prefix):
        self.username = f"{new_username_prefix}@Animex.ug"

class Receved_text(Base):
    __tablename__ = 'receved_text'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)

    @staticmethod
    def add_text(db,text):
        text = Receved_text(text=text)
        try:
            db.add(text)
            db.commit()
            db.refresh(text)
            return text
        except Exception as e:
            print(f"Error occurred: {e}")
            db.rollback()

    @staticmethod
    def get_text(db):
        return db.query(Receved_text).all()

class UsernameChangeRequest(BaseModel):
    current_username: str
    new_username_prefix: str


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

