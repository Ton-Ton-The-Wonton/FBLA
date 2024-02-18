"""models"""
from enum import Enum
from sqlalchemy import Column, Integer, String, inspect
from app.__init__ import Base


class TypeOfOrganizationEnum(Enum):
    """TypeOfOrganizationEnum"""

    UNKNOWN = 0
    GOV = 1
    NGO = 2
    EI = 3  # Educational Institutions
    HCO = 4  # Healthcare Organizations
    FND = 5  # Foundations
    FP = 6  # For-Profit


def get_enum_member_by_value(enum_class, value):
    """get enumerate member by value"""

    for member in enum_class:
        if member.value == value:
            return member

    return None


class Partner(Base):
    """Partner model"""

    __tablename__ = 'partners'
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

    def __repr__(self):
        return f'<Partner {self.name!r}>'

    def as_dict(self):
        """as_dict
        
        serialize obj
        """
        
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


partner_inspector = inspect(Partner).columns
partner_columns = [c.name for c in partner_inspector]
