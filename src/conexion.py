import os
from dotenv import load_dotenv

from mysql.connector import pooling
from mysql.connector import Error

load_dotenv()

class Conexion:
    DATABASE = os.getenv("DB_NAME")
    USERNAME = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASS")
    PORT = "3306"
    HOST = os.getenv("DB_HOST")
    POOL_SIZE = 5
    POOL_NAME = "zona_fit_pool"
    pool = None

    @classmethod
    def obtener_pool(cls):
        if cls.pool == None:
            try:
                cls.pool = pooling.MySQLConnectionPool(
                    pool_name = cls.POOL_NAME,
                    pool_size = cls.POOL_SIZE,
                    host = cls.HOST,
                    port = cls.PORT,
                    database = cls.DATABASE,
                    user = cls.USERNAME,
                    password = cls.PASSWORD
                )
                return cls.pool
            except Error as e:
                print(f"Ocurrio un error al obtener el pool: {e}")
                raise
        else:
            return cls.pool
    
    @classmethod
    def obtener_conexion(cls):
        return cls.obtener_pool().get_connection()
    
    @classmethod
    def liberar_conexion(cls, conexion):
        conexion.close()

if __name__ == "__main__":
    # creamos un objeto de prueba pool
    pool = Conexion.obtener_pool()
    print(pool)
    conexion1 = pool.get_connection()
    print(conexion1)
    Conexion.liberar_conexion(conexion1)
    print("Se libero el objeto conexion1")
