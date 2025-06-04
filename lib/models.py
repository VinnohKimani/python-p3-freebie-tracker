# Code Interpretation

#Imports
from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
# backref a helper for creating reverse access to relationships
from sqlalchemy.ext.declarative import declarative_base

# naming convention for foreign keys to follow
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# This is how the relationship looks like:
# Company --< Freebie >-- Dev


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship("Freebie", back_populates="company")

    devs = relationship(
        "Dev",
        # use the freebies table as the link
        secondary="freebies",
        # matching Dev.companies
        back_populates="companies",
        # because we're not storing this directly
        viewonly=True,
    )

    # repr -->(representation)
    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        return Freebie(item_name=item_name, value=value, dev=dev, company=self)
    
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship("Freebie", back_populates="dev")
    
    companies = relationship(
        "Company",
        # linking via freebies
        secondary="freebies",
        # matching Company.devs
        back_populates="devs",
        # a read only
        viewonly=True,
    )

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, other_dev, freebie):
        if freebie.dev == self:
            freebie.dev = other_dev


# Freebie acts as the intermidiery class 

class Freebie(Base):
    __tablename__ = "freebies"

    id = Column(Integer(), primary_key = True)
    item_name = Column(String())
    value = Column(Integer())

    # convention = {
    #     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    # }
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))
    

    dev = relationship("Dev", back_populates="freebies")
    company = relationship("Company", back_populates="freebies")

# Rep -- method
    def __repr__(self):
       return f'<Freebie {self.item_name}, Value: {self.value}>'

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
      