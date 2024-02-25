"""construct data models"""

from enum import Enum
from sqlalchemy import Column, Integer, String, inspect
from app.__init__ import Base


class TypeOfOrganizationEnum(Enum):
    """types of organization map to integer value in the database"""

    UNKNOWN = 0
    GOV = 1 # Governmental Organizations
    NGO = 2 # Non-Governmental Organizations
    EDU = 3  # Educational and Research Institutions
    HLT = 4  # Healthcare Organizations
    COM = 5  # Community Centers and Libraries 
    FP = 6  # For-Profit Businesses
    ART = 7  # Arts and Cultural Organizations
    SPO = 8 # Sports and Recreational Organizations
    OTH = 9 # Other


class Partner(Base):
    """partner database schema"""

    __tablename__ = "partners"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, default="", unique=True)
    email = Column(String(120), nullable=False, default="", unique=True)
    organization = Column(String(120), nullable=False, default="")
    type_of_organization = Column(Integer, nullable=False, default="")

    def __init__(self,
                 name=None,
                 email=None,
                 organization=None,
                 type_of_organization=TypeOfOrganizationEnum.UNKNOWN.value):
        self.name = name
        self.email = email
        self.organization = organization
        self.type_of_organization = type_of_organization

    def as_dict(self):
        """convert partner object into a dictionary"""
        
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


partner_inspector = inspect(Partner).columns
partner_columns = [c.name for c in partner_inspector]
