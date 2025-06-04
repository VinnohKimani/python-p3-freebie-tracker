#!/usr/bin/env python3

# Script goes here!

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Company, Dev, Freebie

# Setuping up  the database
engine = create_engine("sqlite:///freebies.db")
Session = sessionmaker(bind=engine)
session = Session()

# Droping  and recreate all tables 
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# The Companies
google = Company(name="Google", founding_year=1998)
amazon = Company(name="Amazon", founding_year=1994)
netflix = Company(name="Netflix", founding_year=1997)


# The Devs
vincent = Dev(name="Vincent")
Kimani = Dev(name="Kimani")
Dennis = Dev(name="Dennis")


# The  Freebies
f1 = Freebie(item_name="Mug", value=10, dev=vincent, company=google)
f2 = Freebie(item_name="T-Shirt", value=15, dev=Kimani, company=amazon)
f3= Freebie(item_name="Water Bottle", value=8, dev=Dennis, company=netflix)



session.add_all([google, amazon, netflix, vincent, Kimani, Dennis, f1, f2, f3])
session.commit()

print(" Seed data inserted successfully!")
