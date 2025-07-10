import json
from typing import List
from models.tarea import Tarea
from models.usuario import Usuario
from models.asignacion import Asignacion

class DataHandler:
    def __init__(self, filename='data.json'):
        self.filename = filename
        self.task_bump_id = 0
        self.tasks: List[Tarea] = []
        self.assignments: List[Asignacion] = []
        self.users: List[Usuario] = []
        self.load_data()

    def save_data(self):
        data = {
            'tasks': [task.to_dict() for task in self.tasks],
            'users': [user.to_dict() for user in self.users]
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.users = [self._user_from_dict(u) for u in data.get('users', [])]
                self.tasks = [self._task_from_dict(t) for t in data.get('tasks', [])]
        except FileNotFoundError:
            self.tasks = []
            self.users = []
    
    def create_task_id(self) -> str:
        obtained = self.task_bump_id
        self.task_bump_id += 1
        return str(obtained)
    
    def get_user_by_alias(self, alias: str) -> Usuario:
        for user in self.users:
            if alias == user.alias:
                return user
        return None

    def get_task_by_id(self, id: str) -> Tarea:
        for task in self.tasks:
            if id == task.id:
                return task
        return None
    
    def _user_from_dict(self, data_dict):
        user = Usuario(
            alias=data_dict['alias'],
            nombre=data_dict['nombre']
        )
        asignaciones = data_dict["asignaciones"]
        for asignacion in asignaciones:
            current = Asignacion(user, asignacion["rol"])
            current.asignar_tarea(asignacion["tarea"])
            self.assignments.append(current)
        return user

    def _task_from_dict(self, data_dict):
        tarea = Tarea(
            id=data_dict['id'],
            nombre=data_dict['nombre'],
            descripcion=data_dict['descripcion']
        )
        tarea.estado = data_dict.get('estado', 'nueva')
        for asignacion in self.assignments:
            if asignacion.tarea_id == tarea.id:
                tarea.adicionar_asignacion(asignacion)
        return tarea