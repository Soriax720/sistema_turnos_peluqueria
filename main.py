from datetime import datetime
from gestor_turnos import GestorTurnos
from modelos import TIPOS_SERVICIO

def mostrar_menu():
    print("\n========================================")
    print("   SISTEMA DE GESTIÓN DE PELUQUERÍA")
    print("========================================")
    print("1. Registrar nuevo Cliente")
    print("2. Solicitar Turno")
    print("3. Listar Turnos existentes")
    print("4. Cancelar Turno")
    print("5. Guardar Cambios Manualmente")
    print("6. Salir")
    print("========================================")

def main():
    manager = GestorTurnos()

    while True:
        mostrar_menu()
        option = input("Ingrese una opcion (1-6): ").strip()

        try:
            if option == '1':
                print("\n--- NUEVO CLIENTE ---")
                name = input("Nombre: ")
                last_name = input("Apellido: ")
                phone = input("Telefono: ")
            
                new_id = manager.registrar_cliente( name, last_name, phone)
                print(f"El cliente se a registrado con exito. Nro de ID: {new_id}")
            elif option == '2':
                print("\n--- SOLICITAR TURNO ---")

                try:
                    id_client = int(input("Ingre ID del cliente: "))
                    id_hairdresser = int(input("Ingrese ID del Peluquero: "))
                except ValueError:
                    print("Erro: los id deben ser numeros enteros")
                    continue #vuelve al menu

                print(f"Servicios disponibles: {TIPOS_SERVICIO}")
                service = input("Ingrese el servicio: ").strip()

                if service not in TIPOS_SERVICIO:
                    print(f"Error: Servicio no valido, debe ser uno de: {TIPOS_SERVICIO}")
                    continue
                
                date_str = input("Ingrese Fecha y Hora (Formato AAAA-MM-DD HH:MM: ")
                try:
                    date_str = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("Error: formato de fecha incorrecto")
                    continue

                result = manager.solicitar_turno(id_client, id_hairdresser, service, date_str)
                print("Turno agendado")
                print(result)

            elif option == '3':
                print(manager.listar_turnos())
            
            elif option == '4':
                print("\n--- CANCELAR TURNO ---")
                try:
                    id_turn = int(input("Ingrasar el ID del turno que desea cancelar: "))
                    msj = manager.cancelar_turno(id_turn)
                    print(msj)
                except ValueError:
                    print("Error: el ID debe ser un numero")
            
            elif option == '5':
                manager.guardar_datos()
                print("Datos guardados correctamente")
            
            elif option == '6':
                print("Saliendo del sistema")
                break

            else:
                print("opcion no valida intente de vuelta")
        except ValueError as e:
            print(f"Error de operacion: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()