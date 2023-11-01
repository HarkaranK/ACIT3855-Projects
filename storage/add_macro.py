from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime
import uuid

class MacroRecord(Base):
    """ Return Macro Class """

    __tablename__ = "macro_logging"

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, nullable=False)
    protein = Column(Float)
    carbohydrate = Column(Float)
    fats = Column(Float)
    vitamin_A = Column(Float)
    vitamin_B = Column(Float)
    vitamin_C = Column(Float)
    vitamin_D = Column(Float)
    vitamin_E = Column(Float)
    vitamin_K = Column(Float)
    calcium = Column(Float)
    sodium = Column(Float)
    iron = Column(Float)
    potassium = Column(Float)
    magnesium = Column(Float)
    zinc = Column(Float)
    omega_3 = Column(Float)
    omega_6 = Column(Float)
    trace_id = Column(String(36), nullable=False)
    
    
    def __init__(self, protein, carbohydrate, fats, vitamin_A, vitamin_B, vitamin_C, vitamin_D, vitamin_E, vitamin_K, calcium, sodium, iron, potassium, magnesium, zinc, omega_3, omega_6, trace_id):
        """ Initializes a macro logging record """
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.protein = protein
        self.carbohydrate = carbohydrate
        self.fats = fats
        self.vitamin_A = vitamin_A
        self.vitamin_B = vitamin_B
        self.vitamin_C = vitamin_C
        self.vitamin_D = vitamin_D
        self.vitamin_E = vitamin_E
        self.vitamin_K = vitamin_K
        self.calcium = calcium
        self.sodium = sodium
        self.iron = iron
        self.potassium = potassium
        self.magnesium = magnesium
        self.zinc = zinc
        self.omega_3 = omega_3
        self.omega_6 = omega_6
        self.trace_id = trace_id #str(uuid.uuid4())

    def to_dict(self):
        """ Dictionary Representation of a return book record """
        dict = {}
        dict['id'] = self.id
        dict['date_created'] = self.date_created
        dict['protein'] = self.protein
        dict['carbohydrate'] = self.carbohydrate
        dict['fats'] = self.fats
        dict['vitamin_A'] = self.vitamin_A
        dict['vitamin_B'] = self.vitamin_B
        dict['vitamin_C'] = self.vitamin_C
        dict['vitamin_D'] = self.vitamin_D
        dict['vitamin_E'] = self.vitamin_E
        dict['vitamin_K'] = self.vitamin_K
        dict['calcium'] = self.calcium
        dict['sodium'] = self.sodium
        dict['iron'] = self.iron
        dict['potassium'] = self.potassium
        dict['magnesium'] = self.magnesium
        dict['zinc'] = self.zinc
        dict['omega_3'] = self.omega_3
        dict['omega_6'] = self.omega_6
        dict['trace_id'] = self.trace_id


        return dict