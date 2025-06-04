#!/usr/bin/env python3
from models import Dev, Company, Freebie
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    import ipdb; ipdb.set_trace()

Session = sessionmaker(bind=engine)
session = Session()



vincent = session.query(Dev).filter_by(name="Vincent").first()
print([company.name for company in vincent.companies])

freebie = session.query(Freebie).filter_by(item_name="Mug").first()
print(freebie.print_details())

oldest = Company.oldest_company(session)
print(f"Oldest company is: {oldest.name}")
