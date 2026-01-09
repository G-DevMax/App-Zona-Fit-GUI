class Cliente:
    def __init__(self, id=None, nombre=None, apellido=None, membresia=None):
        self._id = id
        self._nombre = nombre
        self._apellido = apellido
        self._membresia = membresia
    
    def __str__(self):
        return f"id: {self._id}, nombre: {self._nombre}, apellido: {self._apellido}, membresia: {self._membresia}"
    