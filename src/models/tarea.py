from typing import List
from models.asignacion import Asignacion

ESTADOS_VALIDOS = ["nueva", "en_progreso", "finalizada"]

class StateError(ValueError):
    def __init__(self, current, next):
        super().__init__(f"Transicion invalida: {current} -> {next}")

class Tarea:
    def __init__(self, id: str, nombre: str, descripcion: str):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = "nueva"
        self.usuarios_asignados: List[Asignacion] = []
        self.dependencias: List[Tarea] = []
    
    def cambiar_estado(self, siguiente: str):
        if siguiente not in ESTADOS_VALIDOS:
            raise TypeError("Estado invalido!")
        
        if self.estado == "nueva":
            if siguiente != "en_progreso":
                raise StateError(self.estado, siguiente)
        
        elif self.estado == "en_progreso":
            if siguiente == "en_progreso":
                raise StateError(self.estado, siguiente)
        
        elif self.estado == "finalizada":
            raise StateError(self.estado, siguiente)

        self.estado = siguiente

    def adicionar_asignacion(self, asignacion: Asignacion):
        asignacion.asignar_tarea(self.id)
        self.usuarios_asignados.append(asignacion)
    
    def remover_asignacion(self, usuario_alias: str):
        for index, asignacion in enumerate(self.usuarios_asignados):
            current_alias = asignacion.usuario_asignado.alias
            if usuario_alias == current_alias:
                self.usuarios_asignados.pop(index)
                asignacion.remover_tarea()
                return
        raise ValueError("El usuario a remover no existe!")

    def adicionar_dependencia(self, tarea):
        self.dependencias.append(tarea)
    
    def remover_dependencia(self, tarea_id: str):
        for index, dependencia in enumerate(self.dependencias):
            current_id = dependencia.id
            if tarea_id == current_id:
                self.dependencias.pop(index)
                return
        raise ValueError("La dependencia a remover no existe!")
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "usuarios_asignados": [a.usuario_asignado.to_dict() for a in self.usuarios_asignados],
            "dependencias": [d.id for d in self.dependencias]
        }