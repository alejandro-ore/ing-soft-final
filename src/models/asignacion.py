from models.usuario import Usuario

ROLES_VALIDOS = ["analisis", "disenho", "programacion", "infra"]

class Asignacion:
    def __init__(self, usuario_asignado: Usuario, rol: str):
        usuario_asignado.asignaciones.append(self) # se añade asignacion al usuario
        self.usuario_asignado = usuario_asignado
        self.rol = rol
        self.tarea_id = ""

    def asignar_tarea(self, tarea_id: str):
        self.tarea_id = tarea_id

    def remover_tarea(self):
        self.tarea_id = ""
        for index, asignacion in enumerate(self.usuario_asignado.asignaciones):
            if asignacion == self:
                self.usuario_asignado.asignaciones.pop(index)
                return
        raise ValueError("No se pudo remover la asignacion")

    def to_dict(self):
        return {
            "usuario_asignado": self.usuario_asignado.alias,
            "rol": self.rol,
            "tarea": self.tarea_id
        }
