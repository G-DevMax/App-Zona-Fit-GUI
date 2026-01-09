import tkinter as tk
from tkinter import ttk
from clienteDao import ClienteDAO
from cliente import Cliente
from tkinter.messagebox import showerror, showinfo

class App(tk.Tk):
    COLOR_VENTANA = "#1d2d44"

    def __init__(self):
        super().__init__()
        self.id_cliente = None
        self.configurar_ventana()
        self.configurar_grid()
        self.titulo_principal()
        self.formulario()
        self.tabla_clientes()
        self.botones()

    def configurar_ventana(self):
        self.geometry("700x500")
        self.title("Zona Fit App")
        self.configure(background=App.COLOR_VENTANA)
        self.estilos = ttk.Style()
        self.estilos.theme_use("clam")
        self.estilos.configure(self, background=App.COLOR_VENTANA, foreground="white", fieldbackground="black")

    def configurar_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def titulo_principal(self):
        titulo = ttk.Label(self, text="Zona Fit (GYM)", font=("Arial", 20), background=App.COLOR_VENTANA, foreground="white")
        titulo.grid(row=0, column=0, columnspan=2, pady=30) # se publica en la fila 0 y columna 0, y con columnspan=2 el titulo ocupa todo el espacio 

    def formulario(self):
        self.frame_formulario = ttk.Frame(self)

        # Formulario - Apartado de nombre
        nombre_L = ttk.Label(self.frame_formulario, text="Nombre: ")
        nombre_L.grid(row=0, column=0, sticky=tk.W, pady=30, padx=5)

        self.nombre_T = ttk.Entry(self.frame_formulario)
        self.nombre_T.grid(row=0, column=1)

        # formulario - Apartadp de apellido
        apellido_L = ttk.Label(self.frame_formulario, text="Apellido: ")
        apellido_L.grid(row=1, column=0, sticky=tk.W, pady=30, padx=5)

        self.apellido_T = ttk.Entry(self.frame_formulario)
        self.apellido_T.grid(row=1, column=1)

        # formulario, apartado de membresia
        membresia_L = ttk.Label(self.frame_formulario, text="Membresia: ")
        membresia_L.grid(row=2, column=0, sticky=tk.W, pady=30, padx=5)

        self.membresia_T = ttk.Entry(self.frame_formulario)
        self.membresia_T.grid(row=2, column=1)

        # publicar el formulario
        self.frame_formulario.grid(row=1, column=0)

    def tabla_clientes(self):
        self.frame_tabla = ttk.Frame(self)

        # configuramos el estilo de la tabla y las columnas
        self.estilos.configure("Treeview", background="black", foreground="white", fieldbackground="black", rowheight=20) 
        columnas = ("ID", "Nombre", "Apellido", "Membresia")

        # creamos la tabla
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")

        # columnas de la tabla
        self.tabla.column("ID", anchor=tk.CENTER, width=50)
        self.tabla.column("Nombre", anchor=tk.W, width=100)
        self.tabla.column("Apellido", anchor=tk.W, width=100)
        self.tabla.column("Membresia", anchor=tk.W, width=100)

        # cabeceros de la tabla
        self.tabla.heading("ID", text="ID", anchor=tk.CENTER)
        self.tabla.heading("Nombre", text="Nombre", anchor=tk.W)
        self.tabla.heading("Apellido", text="Apellido", anchor=tk.W)
        self.tabla.heading("Membresia", text="Membresia", anchor=tk.W)

        # cargamos los datos de la DB
        clientes = ClienteDAO.seleccionar()
        for cliente in clientes:
            self.tabla.insert(parent="", index=tk.END, values=(cliente._id, cliente._nombre, cliente._apellido, cliente._membresia)) # parent vacio ya que no usamos subregistros
        
        # configuramos el Scrollbar y lo establecemos
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # Asociamos el evento select
        self.tabla.bind("<<TreeviewSelect>>", self.cargar_cliente)

        # publicamos la tabla
        self.tabla.grid(row=0, column=0)
        self.frame_tabla.grid(row=1, column=1, padx=20)

    def botones(self):
        self.frame_botones = ttk.Frame(self)

        # creacion de botones
        guardar_btn = ttk.Button(self.frame_botones, text="Guardar", command=self.validar_cliente)

        eliminar_btn = ttk.Button(self.frame_botones, text="Eliminar", command=self.eliminar_cliente)

        limpiar_btn = ttk.Button(self.frame_botones, text="Limpiar", command=self.limpiar_datos)

        # publicacion del boton
        guardar_btn.grid(row=0, column=0, padx=30)

        eliminar_btn.grid(row=0, column=1, padx=30)

        limpiar_btn.grid(row=0, column=2, padx=30)

        # aplicando estilos a los botones
        self.estilos.configure("TButton", background="#005f73")
        self.estilos.map("TButton", background=[("active", "#0a9396")])

        # publicacion del frame
        self.frame_botones.grid(row=2, column=0, columnspan=2, pady=20)

    def validar_cliente(self):
        # se validan los campos
        if (self.nombre_T.get() and self.apellido_T.get() and self.membresia_T.get()):
            if self.validar_membresia():
                self.guardar_cliente()
            else:
                showerror(title="Error en Membresia", message="El valor de membresia debe de ser numerico para poder guardarlo en la base de datos")
                self.membresia_T.delete(0, tk.END) # se limpia el valor de membresia, desde el indice 0 hasta el final del indice
                self.membresia_T.focus_set() 
        else:
            showerror(title="Error en el Formulario", message="Debe de llenar todos los datos del formulario para poder guardar al cliente en la base de datos")
            self.nombre_T.focus_set()
        

    def eliminar_cliente(self):
        if self.id_cliente is None:
            showerror(title="Error", message="Debes seleccionar un cliente a eliminar primero")
        else:
            cliente = Cliente(id=self.id_cliente)
            ClienteDAO.eliminar(cliente)
            showinfo(title="Cliente Eliminado", message=f"El cliente con el ID ({self.id_cliente}) se ha eliminado con exito")
            self.recargar_datos()


    def validar_membresia(self):
        try:
            int(self.membresia_T.get())
            return True
        except:
            return False

    def guardar_cliente(self):
        # se recuperan los valores de los campos
        nombre = self.nombre_T.get()
        apellido = self.apellido_T.get()
        membresia = self.membresia_T.get()

        # Antes de insertar el cliente, primero validamos el id del cliente que se va a guardar
        if self.id_cliente is None: # Si no hay id registrado, se inserta el nuevo cliente
            cliente = Cliente(nombre=nombre, apellido=apellido, membresia=membresia)
            ClienteDAO.insertar(cliente)
            showinfo(title="Cliente guardado", message="El cliente se guardo correctamente en la base de datos")
        else: # si el id esta registrado, se actualiza el cliente con ese id
            actualizar_cliente = Cliente(self.id_cliente, nombre, apellido, membresia)
            ClienteDAO.actualizar(actualizar_cliente)
            showinfo(title="Cliente Actualizado", message=f"El cliente con ID ({self.id_cliente}) se actualizo corretamente")


        self.recargar_datos()

    def cargar_cliente(self, event):
        elemento_seleccionado = self.tabla.selection()[0]
        elemento = self.tabla.item(elemento_seleccionado)
        cliente_T = elemento["values"] # tupla de valores del cliente seleccionado
        # se recupera cada valor del cliente seleccionado
        self.id_cliente = cliente_T[0]
        nombre = cliente_T[1]
        apellido = cliente_T[2]
        membresia = cliente_T[3]

        self.limpiar_formulario()

        self.nombre_T.insert(0, nombre)
        self.apellido_T.insert(0, apellido)
        self.membresia_T.insert(0, membresia)

    def recargar_datos(self):
        # volvemos a mostar la tabla clientes, actualizandola con los datos cargados
        self.tabla_clientes()
        self.limpiar_datos() 

    def limpiar_datos(self):
        self.limpiar_formulario() # se llama al metodo para reniciar el formulario
        self.id_cliente = None
    
    def limpiar_formulario(self):
        self.nombre_T.delete(0, tk.END)
        self.apellido_T.delete(0, tk.END)
        self.membresia_T.delete(0, tk.END)

        


if __name__ == "__main__":
    app = App()
    app.mainloop()