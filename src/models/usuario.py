from typing import List

class Usuario:
    def __init__(self, alias: str, nombre: str):
        self.alias = alias
        self.nombre = nombre
        self.asignaciones: List = []
    
    def to_dict(self):
        return {
            "alias": self.alias,
            "nombre": self.nombre,
            "asignaciones": [a.to_dict() for a in self.asignaciones]
        }