from datetime import datetime, timedelta
from abc import ABC, abstractmethod 


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
        if especialidad not in TIPOS_SERVICIO:
            raise ValueError(f"Especialidad no valida: {especialidad}, Validas: {TIPOS_SERVICIO}")

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

class Turno:
    def __init__(self,cliente,peluquero,id_turno,servicio,fecha_hora):
        if servicio not in TIPOS_SERVICIO:
            raise ValueError(f"El servicio '{servicio}' no es valido. Servicios validos: {TIPOS_SERVICIO}")

        self.cliente = cliente
        self.peluquero = peluquero
        self.id_turno = id_turno
        self.servicio = servicio
        self.fecha_hora = fecha_hora
        
    def mostrar_turno(self):
        formato_lectura = "%d/%m/%Y a las %H:%M"
        fecha_formateada = self.fecha_hora.strftime(formato_lectura)
        reporte = (
            f"\n=== DETALLE DEL TURNO #{self.id_turno} === \n"
            f"Servicio: {self.servicio} \n"
            f"Fecha y Hora: {fecha_formateada}\n"
            f"---------------------------------\n"
            f"Datos del Cliente: {self.cliente.mostrar_info()}\n"
            f"Datos Del Peluquero: {self.peluquero.mostrar_info()}\n"
            f"=========================================\n"
        )
        return reporte
    
    def get_datos(self):
        formato_lectura = "%Y-%m-%d %H:%M"
        fecha_formateada = self.fecha_hora.strftime(formato_lectura)
        return{
            "id_turno": self.id_turno,
            "fecha_hora": fecha_formateada,
            "cliente_id": self.cliente.id_cliente,
            "peluquero_id": self.peluquero.id_peluquero,
            "servicio": self.servicio

        }



