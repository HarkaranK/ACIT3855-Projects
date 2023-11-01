from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime
import uuid

class WeightRecord(Base):
    """ Return Weight Class """

    __tablename__ = "weight_logging"

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, nullable=False)
    weight = Column(Float, nullable=False)
    note = Column(String(250))
    trace_id = Column(String(36), nullable=False)
    
    
    def __init__(self,trace_id,weight, note=None):
        """ Initializes a weight record """
        self.weight = weight
        self.note = note
        self.date_created = datetime.datetime.now()
        self.trace_id = trace_id #str(uuid.uuid4())

    def to_dict(self):
        """ Dictionary Representation of a return weight record """
        dict = {}
        dict['id'] = self.id
        dict['weight'] = self.weight
        dict['note'] = self.note
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict
