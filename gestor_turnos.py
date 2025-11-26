from datetime import datetime
from modelos import Cliente, Peluquero, Turno, TIPOS_SERVICIO
from persistencia import PersistenceCsv


class GestorTurnos:
    _instance = None
    #Singleton: Garantiza la existencia de una única instancia del Gestor en todo el sistema.
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GestorTurnos, cls).__new__(cls)

        return cls._instance
    
    def __init__(self):
         
        try: #Evita que se borren las listas si se llama a GestorTurnos() de nuevo.
            _ = self._initialized
        except AttributeError:
            self._initialized = True

            self.clientes = []
            self.peluqueros = []
            self.turnos = []

            self.persistence = PersistenceCsv("turno.csv")
            
            self.cargar_datos()
            
            # Arreglo: Si el sistema arranca vacío, creamos peluqueros por defecto para poder probar
            if not self.peluqueros:
                p1 = Peluquero("Jorge", "Muñoz", "111-222", 101, "Corte")
                p2 = Peluquero("Maria", "Gomez", "333-444", 102, "Color")
                p3 = Peluquero("Luis", "Vera", "555-666", 103, "Barba")
                
                self.peluqueros.append(p1)
                self.peluqueros.append(p2)
                self.peluqueros.append(p3)
    
    def cargar_datos(self):
        raw_data = self.persistence.load()

        for d in raw_data:
            try:
                #conversion a int y datetime
                turno_id = int(d['id_turno'])
                cliente_id = int(d['cliente_id'])
                peluquero_id = int(d['peluquero_id'])

                date_object = datetime.strptime(d['fecha_hora'],"%Y-%m-%d %H:%M")
                

                # Reconstrucción con Placeholders:
                # Creacion de objetos temporales solo con el ID correcto para satisfacer al constructor de Turno
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
        #generacion de id de autoincremento
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

        self.guardar_datos()
        return new_client.id_cliente
    
    def guardar_datos(self):
        data_to_save = []
        #convertir los objetos Turno a dict antes de guardar
        for appo_obj in self.turnos:
            appoint_dict = appo_obj.get_datos()
            data_to_save.append(appoint_dict)
        self.persistence.save(data_to_save)
        try:
            self.persistence.save(data_to_save)
            print("Datos guardados con éxito.")
        except Exception as e:
            print(f"El sistema no pudo guardar los cambios en el archivo CSV.")
            print(f"Razon: {e}")

    def solicitar_turno(self, id_cliente, id_peluquero, servicio, fecha_hora):
        #Búsqueda de Instancias Reales
        client_found = None
        for c in self.clientes:
            if c.id_cliente == id_cliente:
                client_found = c
                break
        
        hairdresser_found = None
        for h in self.peluqueros:
            if h.id_peluquero == id_peluquero:
                hairdresser_found = h
                break

        if not client_found or not hairdresser_found:
            raise ValueError("El cliente o peluquero no fue encontrado")
        
        if hairdresser_found.especialidad != servicio:
             raise ValueError(f"El peluquero {hairdresser_found.nombre} (ID {id_peluquero}) no realiza '{servicio}'. Su especialidad es: {hairdresser_found.especialidad}")
        
        #Evitar turnos duplicados
        for turn_existent in self.turnos:
            if turn_existent.peluquero.id_peluquero == hairdresser_found.id_peluquero and turn_existent.fecha_hora == fecha_hora:
                raise ValueError("El peluquero ya tiene un turno asignado en esa fecha y hora")
        
        #Generación de ID y Creación
        if not self.turnos:
            new_id = 1
        else:
            max_id = 0
            for n in self.turnos:
                if n.id_turno > max_id:
                    max_id = n.id_turno
            
            new_id = max_id + 1

        new_turn = Turno(
            cliente = client_found,
            peluquero= hairdresser_found,
            id_turno= new_id,
            servicio= servicio,
            fecha_hora= fecha_hora
        )

        self.turnos.append(new_turn)
        self.guardar_datos()

        return new_turn.mostrar_turno()
    
    def listar_turnos(self):
        if not self.turnos:
            return "No hay turnos registrados en el sistema"
        
        final_report = "\n--- LISTADO DE TURNOS ---\n"

        for t in self.turnos:
            final_report = final_report + t.mostrar_turno() + "\n"
        
        return final_report
    
    def cancelar_turno(self, appointment_id):

        appointment_to_remove = None

        for appointment in self.turnos:
            if appointment.id_turno == appointment_id:
                appointment_to_remove = appointment
                break
        if appointment_to_remove:
            self.turnos.remove(appointment_to_remove)
            self.guardar_datos()

            return f"El tuno {appointment_id} fue elimnado correctamente"
        else:
            return f"Error: No se encontro ningun turno con el id {appointment_id}"