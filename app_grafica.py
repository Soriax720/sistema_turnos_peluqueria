import tkinter as tk
from tkinter import ttk
from tkinter import messagebox # ventanas emergentes de alerta
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

        self.btn_listar = tk.Button(self.master , text="3. Listar turnos", command= self.open_listar_turnos)
        self.btn_listar.pack(pady=5)
    
    def open_registro_cliente(self):
        self.ventana_registro = tk.Toplevel(self.master)
        self.ventana_registro.title("Registrar Nuevo Cliente")
        self.ventana_registro.geometry("300x300")

        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_telefono = tk.StringVar()

        #campo nombre
        tk.Label(self.ventana_registro, text="Nombre:").pack(padx=5)
        tk.Entry(self.ventana_registro, textvariable= self.var_nombre).pack(pady=5)
        #campo apellido
        tk.Label(self.ventana_registro, text="Apellido:").pack(pady=5)
        tk.Entry(self.ventana_registro, textvariable= self.var_apellido).pack(pady=5)
        #campo telefono
        tk.Label(self.ventana_registro, text="Telefono:").pack(pady=5)
        tk.Entry(self.ventana_registro, textvariable= self.var_telefono).pack(pady=5)

        btn_guardar = tk.Button(self.ventana_registro, text="Guardar Cliente", command= self.accion_guardar_cliente)
        btn_guardar.pack(pady=20)
    
    def accion_guardar_cliente(self):
        nombre = self.var_nombre.get().strip()
        apellido = self.var_apellido.get().strip()
        telefono = self.var_telefono.get().strip()

        if not nombre or not apellido or not telefono:
            messagebox.showwarning("Faltan Datos", "Por favor complete todos los campos.")
            return

        #llamada al gestor
        try:
            nuevo_id = self.gestor.registrar_cliente(nombre, apellido, telefono)
            messagebox.showinfo("Éxito", f"Cliente registrado correctamente.\nID Asignado: {nuevo_id}")
            self.ventana_registro.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente.\nDetalle: {e}")


    def open_listar_turnos(self):
        self.ventana_lista = tk.Toplevel(self.master)
        self.ventana_lista.title("Listado de Turnos")
        self.ventana_lista.geometry("800x400")

        columns = ("id", "fecha", "servicio", "cliente", "peluquero")

        #widget treeview
        tree = ttk.Treeview(self.ventana_lista, columns=columns, show="headings")

        tree.heading("id", text="ID Turno")
        tree.heading("fecha", text="Fecha y Hora")
        tree.heading("servicio", text="Servicio")
        tree.heading("cliente", text="Cliente (ID)")
        tree.heading("peluquero", text="Peluquero (ID)")

        tree.column("id", width=50, anchor="center")
        tree.column("fecha", width=150, anchor="center")
        tree.column("servicio", width=100)
        tree.column("cliente", width=100)
        tree.column("peluquero", width=100)

        for turno in self.gestor.turnos:
            fecha_str = turno.fecha_hora.strftime("%d/%m/%Y %H:%M")
            #insertar fila en tabla
            tree.insert("", tk.END, values=(
                turno.id_turno,
                fecha_str,
                turno.servicio,
                f"ID: {turno.cliente.id_cliente}",
                f"ID: {turno.peluquero.id_peluquero}"
            ))
            #empaquetar tabla
            scrollbar = ttk.Scrollbar(self.ventana_lista, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)

            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()       # Crea la ventana base
    app = SalonApp(root) # Inicia tu App dentro de esa ventana
    root.mainloop()  