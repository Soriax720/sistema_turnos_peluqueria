
from abc import ABC, abstractmethod 

"""class TipoServicio(Enum):
    CORTE = "Corte"
    COLOR = "Color"
    BARBA = "Barba" """
TIPOS_SERVICIO = ["Corte", "Color", "Barba"]

class Persona(ABC):
    def __init__(self,nombre,apellido,telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
    @abstractmethod
    def mostrar_info(self):
        pass

class Peluquero(Persona):

    

    def __init__(self, nombre, apellido, telefono,id_peluquero,especialidad):
        super().__init__(nombre, apellido, telefono)
        self.id_peluquero = id_peluquero
        if especialidad not in Peluquero.TIPOS_SERVICIO:
            raise ValueError(f"Especialidad no valida: {especialidad}, Validas: {Peluquero.TIPOS_SERVICIO}")

        self.especialidad = especialidad

    def mostrar_info(self):
        return (f"Peluquero: {self.nombre} {self.apellido}, "
                f"Teléfono: {self.telefono}, "
                f"ID: {self.id_peluquero}, "
                f"Especialidad: {self.especialidad}")
    
    def get_datos(self):
        return {
            "id_peluquero": self.id_peluquero,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "especialidad": self.especialidad
        }



class Cliente(Persona):
    def __init__(self, nombre, apellido, telefono,id_cliente):
        super().__init__(nombre, apellido, telefono)
        self.id_cliente = id_cliente
    
    def mostrar_info(self):
        return (f"Cliente: {self.nombre} {self.apellido}, "
                f"Teléfono: {self.telefono}, "
                f"ID: {self.id_cliente}")
    def get_datos(self):
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono
        }