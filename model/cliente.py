from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column("id", Integer, primary_key=True)
    nome = Column(String(100))
    email = Column(String(100))
    celular = Column(Integer)
    cidade = Column(String(100))


    def __init__(self, nome:str, email:str, celular:int, 
                 cidade:str):
        """
        Cria um Cliente

        Arguments:
            nome: nome do cliente.
            email: email do cliente
            celular: celular do cliente
            cidade: cidade do cliente
        """        
        self.nome = nome
        self.email = email
        self.celular = celular
        self.cidade = cidade    