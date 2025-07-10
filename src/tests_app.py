import unittest
import json
from controller import app, data_handler
from models.usuario import Usuario

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        # Preparar entorno de test
        self.client = app.test_client()
        data_handler.users.clear()
        data_handler.tasks.clear()

    def test_crear_usuario(self):
        response = self.client.post("/usuarios", json={
            "alias": "juan123",
            "nombre": "Juan Pérez"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_handler.users[0].alias, "juan123")

    def test_crear_tarea_con_usuario(self):
        # Primero crear un usuario
        self.client.post("/usuarios", json={
            "alias": "ana456",
            "nombre": "Ana Gómez"
        })

        # Luego crear una tarea con ese usuario
        response = self.client.post("/tasks", json={
            "nombre": "Tarea prueba",
            "descripcion": "Descripción de prueba",
            "usuario": "ana456",
            "rol": "tester"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data_handler.tasks), 1)
        self.assertEqual(data_handler.tasks[0].usuarios_asignados[0].rol, "tester")

    def test_agregar_usuario_a_tarea(self):
        self.client.post("/usuarios", json={"alias": "luisa", "nombre": "Luisa"})
        self.client.post("/usuarios", json={"alias": "pablo", "nombre": "Pablo"})

        self.client.post("/tasks", json={
            "nombre": "Tarea X",
            "descripcion": "desc",
            "usuario": "luisa",
            "rol": "manager"
        })

        task_id = data_handler.tasks[0].id

        response = self.client.post(f"/tasks/{task_id}/users", json={
            "usuario": "pablo",
            "rol": "dev",
            "accion": "adicionar"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data_handler.tasks[0].usuarios_asignados), 2)

    def test_adicionar_dependencia(self):
        # Crear tarea A
        self.client.post("/usuarios", json={"alias": "pedro", "nombre": "Pedro"})
        self.client.post("/tasks", json={
            "nombre": "Tarea A",
            "descripcion": "desc",
            "usuario": "pedro",
            "rol": "admin"
        })

        # Crear tarea B
        self.client.post("/tasks", json={
            "nombre": "Tarea B",
            "descripcion": "desc",
            "usuario": "pedro",
            "rol": "admin"
        })

        tarea_a = data_handler.tasks[0]
        tarea_b = data_handler.tasks[1]

        # Adicionar B como dependencia de A
        response = self.client.post(f"/tasks/{tarea_a.id}/dependencies", json={
            "dependencytaskid": tarea_b.id,
            "accion": "adicionar"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(tarea_b, tarea_a.dependencias)

if __name__ == '__main__':
    unittest.main()
