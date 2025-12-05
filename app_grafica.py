import tkinter as tk
from gestor_turnos import GestorTurnos

class SalonApp:
    def __init__(self, master):
        self.gestor = GestorTurnos()

        self.master = master
        master.title("Gestion de Peluqueria")

        self.setup_ui()
    
    def setup_ui(self):

        self.label_titulo = tk.Label(self.master, text="Menu Principal", font=("Arial", 15))
        self.label_titulo.pack(pady=10)

        self.btn_registro = tk.Button(self.master, text="1. Registrar Cliente", command= self.open_registro_cliente)
        self.btn_registro.pack(pady=5)
    
    def open_registro_cliente(self):
        self.ventana_registro = tk.Toplevel(self.master)
        self.ventana_registro.title("Registrar Nuevo Cliente")
        self.ventana_registro.geometry("300x300")

        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_telofono = tk.StringVar()

        #campo nombre
        tk.Label(self.ventana_registro, text="Nombre:").pack(padx=5)
        tk.Entry(self.ventana_registro, textvariable= self.var_nombre).pack(pady=5)
        #campo apellido
        tk.Label(self.ventana_registro, text="Apellido:").pack(pady=5)
        tk.Entry(self.ventana_registro, textvariable= self.var_apellido).pack(pady=5)
        #campo telefono
        tk.Label(self.ventana_registro, text="Telefono:").pack(pady=5)
        tk.Entry(self.ventana_registro, textvariable= self.var_telofono).pack(pady=5)

        btn_guardar = tk.Button(self.ventana_registro, text="Guardar Cliente", command= self.accion_guardar_cliente)
        btn_guardar.pack(pady=20)
    
    def accion_guardar_cliente(self):
        
        print("Botón presionado. Implementar lógica aquí.")
    
if __name__ == "__main__":
    root = tk.Tk()       # Crea la ventana base
    app = SalonApp(root) # Inicia tu App dentro de esa ventana
    root.mainloop()  