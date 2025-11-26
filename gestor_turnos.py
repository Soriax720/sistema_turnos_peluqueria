from datetime import datetime
from modelos import Cliente, Peluquero, Turno, TIPOS_SERVICIO
from persistencia import PersistenceCsv


class GestorTurnos:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GestorTurnos, cls).__new__(cls)

        return cls._instance
    
    def __init__(self):
        try:
            _ = self._initialized
        except AttributeError:
            self._initialized = True

            self.clientes = []
            self.peluqueros = []
            self.turnos = []

            self.persistence = PersistenceCsv("turno.csv")
            
            self.cargar_datos()
    
    def cargar_datos(self):
        raw_data = self.persistence.load()

        for d in raw_data:
            try:
                turno_id = int(d['id_turno'])
                cliente_id = int(d['cliente_id'])
                peluquero_id = int(d['peluquero_id'])

                date_object = datetime.strptime(d['fecha_hora'],"%Y-%m-%d %H:%M")

                client_placeholder = Cliente(
                    nombre="Cliente",
                    apellido="Recuperado",
                    telefono="",
                    id_cliente= cliente_id
                )
                hairdresser_placeholder = Peluquero(
                    nombre="Peluquero",
                    apellido="recuperado",
                    telefono="",
                    id_peluquero= peluquero_id,
                    especialidad= d['servicio'],
                    

                )
                new_appointment = Turno(
                    cliente = client_placeholder,
                    peluquero= hairdresser_placeholder,
                    id_turno= turno_id,
                    servicio=d['servicio'],
                    fecha_hora= date_object

                )

                self.clientes.append(client_placeholder)
                self.peluqueros.append(hairdresser_placeholder)
                self.turnos.append(new_appointment)
            except Exception as e:
                print(f"Error al cargar turno del archivo: {e}")
                continue
    
    def registrar_cliente(self, nombre, apellido, telefono):
        if not self.clientes:
            new_id = 1
        else:
            max_id = 0
            for n in self.clientes:
                if n.id_cliente > max_id:
                    max_id = n.id_cliente
            
            new_id = max_id + 1

        new_client = Cliente(
            nombre = nombre,
            apellido= apellido,
            telefono= telefono,
            id_cliente= new_id
        )

        self.clientes.append(new_client)

        self.guadar_datos()
        return new_client.id_cliente
    
    def guardar_datos(self):
        data_to_save = []
        for appo_obj in self.turnos:
            appoint_dict = appo_obj.get_datos()
            data_to_save.append(appoint_dict)
        self.persistence.save(data_to_save)
        try:
            self.persistencia.save(data_to_save)
            print("Datos guardados con éxito.")
        except Exception as e:
            print(f"El sistema no pudo guardar los cambios en el archivo CSV.")
            print(f"Razon: {e}")
