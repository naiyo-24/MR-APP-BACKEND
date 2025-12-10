from sqlalchemy import Column, Integer, String
from db import Base

class Headquarter(Base):
    __tablename__ = "headquarters"

    headquarter_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=True)
    area_sales_manager_name = Column(String(255), nullable=False)
    contact_no = Column(String(15), nullable=True)
