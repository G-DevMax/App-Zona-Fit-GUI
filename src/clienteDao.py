from conexion import Conexion
from cliente import Cliente
class ClienteDAO:
    SELECT = "SELECT * FROM clientes ORDER BY id_clientes"
    SELECT_BY_NAME = "SELECT * FROM clientes WHERE nombre LIKE '%s%'"
    INSERT = "INSERT INTO clientes(nombre, apellido, membresia) VALUES (%s, %s, %s)"
    UPDATE = "UPDATE clientes SET nombre=%s, apellido=%s, membresia=%s WHERE id_clientes = %s"
    DELETE = "DELETE FROM clientes WHERE id_clientes=%s"

    @classmethod
    def seleccionar(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECT)
            registros = cursor.fetchall()
            clientes = []
            for regisro in registros:
                cliente = Cliente(regisro[0], regisro[1], regisro[2], regisro[3])
                clientes.append(cliente)
            return clientes
        except Exception as e:
            print(f"Ocurrio un error al seleccionar clientes: {e}")
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
    
    @classmethod
    def insertar(cls, cliente):
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente._nombre, cliente._apellido, cliente._membresia)
            cursor.execute(cls.INSERT, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Ocurrio un error al insertar el cliente: {e}")
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
    
    @classmethod
    def actualizar(cls, cliente):
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente._nombre, cliente._apellido, cliente._membresia, cliente._id)
            cursor.execute(cls.UPDATE, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Ocurrio un error al actulizar el cliente: {e}")
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
    
    @classmethod
    def eliminar(cls, cliente):
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente._id,)
            cursor.execute(cls.DELETE, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Ocurrio un error al eliminar el cliente: {e}")
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
        


if __name__ == "__main__": # entorno de pruebas rapido
    # eliminar cliente
    # clienteDelete = Cliente(id="2")
    # eliminar_cliente = ClienteDAO.eliminar(clienteDelete)
    # print(f"Cliente con ID: {clienteDelete._id} fue eliminado")

    # actualizar cliente
    # clienteUpdate = Cliente(nombre="Carlos", apellido="Pedrozza", membresia="120", id="2")
    # update_cliente = ClienteDAO.actualizar(clienteUpdate)
    # print(f"Cliente con ID: {clienteUpdate._id}, Actualizado")

    # insertar clientes
    # cliente1 = Cliente(nombre="Bianca", apellido="Montiel", membresia=200)
    # nuevo_cliente = ClienteDAO.insertar(cliente1)
    # print(f"Cliente agregado con exito")

    # seleccionar clientes
    clientes = ClienteDAO.seleccionar()
    for cliente in clientes:
        print(cliente)