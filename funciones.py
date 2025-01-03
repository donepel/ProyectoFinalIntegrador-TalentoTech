#### IMPORTAR MODULOS ####
import sqlite3
import colorama
import datetime

#### DEFINICION DE COLORES ###
MAGENTA="\033[35m"
RED="\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

####DEFINICION DE FUNCIONES######

# Función para mostrar el menú
def mostrar_menu():
    print()
    print(f"{GREEN}#", "+"*40, "#")
    print(f"{GREEN}#     Sistema de gestión de inventario     #")
    print(f"{GREEN}#      Version 0.2, Entrega Final          #")
    print(f"{GREEN}#", "+"*40, "#")
    print("")
    print(f"{MAGENTA}Opciones: ")
    print("1. Agregar producto")
    print("2. Mostrar productos")
    print("3. Actualizar cantidad de producto")
    print("4. Eliminar producto")
    print("5. Buscar producto")
    print("6. Reporte de bajo stock")
    print("7. Salir")
    print(f"{RESET}")

##### Conexion con la base de datos
def crear_base():
    conexion = sqlite3.connect("inventario.db") #conecta o crea la base de datos
    cursor = conexion.cursor() # Crea un cursor para interactuar con la db

    cursor.execute ("""CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    descripcion TEXT,
                    cantidad INTEGER,
                    precio FLOAT,
                    categoria TEXT,
                    create_date TEXT,
                    modify_date TEXT

                    )
                """)
    conexion.commit() #Guarda cambios
    conexion.close() #Cierra la conexion

# Funcion para verificar si un producto existe en la base de datos

# Funcion para agregar un producto al inventario (1)
def agregar_producto():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    try:
        nombre = input("Ingrese el nombre del producto: ").strip().upper()
        descripcion = input("Ingrese la descrpcion del producto: ").strip().upper()
        cantidad = int(input("Ingrese la cantidad del producto: "))
        precio = float(input("Ingrese el precio del producto: "))
        categoria = input("Ingrese la categoria del producto: ").strip().upper()
    except ValueError as e:
        print (f"Hay un error en el valor ingresado:\n Valor: {e} no admitido")
        return
    creado = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    modificado = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria, create_date, modify_date) 
        VALUES(?,?,?,?,?,?,?)""", (nombre, descripcion, cantidad, precio, categoria, creado, modificado))
    conexion.commit()

    last_id = cursor.lastrowid  # Obtiene el último ID insertado
    print(f"{GREEN}Se ha agregado exitosamente el siguiente producto:{RESET}")
    cursor.execute("SELECT * FROM productos WHERE id = ?", (last_id,))
    tabla = cursor.fetchall()
    for filas in tabla:
        print(f"{MAGENTA}| {RESET}{RED}ID: {RESET}{filas[0]} {MAGENTA}| {RESET}{GREEN}Nombre: {RESET}{filas[1]} {MAGENTA}| {RESET}{GREEN}Descripción: {RESET}{filas[2]} {MAGENTA}| {RESET}{GREEN}Cantidad: {RESET}{filas[3]} {MAGENTA}| {RESET}{GREEN}Precio:{RESET} ${filas[4]} {MAGENTA}| {RESET}{GREEN}Categoria: {RESET}{filas[5]} {MAGENTA}|")
    conexion.close()

#Funcion para mostrar todos los productos en el inventario en forma de tabla (2)
def mostrar_productos():
    conexion = sqlite3.connect("inventario.db") #conecta o crea la base de datos
    cursor = conexion.cursor() # Crea un cursor para interactuar con la db
    cursor.execute("SELECT * FROM productos ")
    print(f"{RED}Listado de articulos:{RESET}")
    tabla = cursor.fetchall()
    print(f"{MAGENTA}{'ID':<5} {'Nombre':<20} {'Descripción':<20} {'Cantidad':<10} {'Precio':<10} {'Categoría':<15}{'Create_date':<15}{'Modify_date':<15}{RESET}")
    print(f"{MAGENTA}{'-'*120}{RESET}")  # Separador

    for filas in tabla:
         print(f"{filas[0]:<5} {filas[1]:<20} {filas[2]:<20} {filas[3]:<10} {"$ "}{filas[4]:<10} {filas[5]:<15} {filas[6]:<15} {filas[7]:<15}")
    
    print()
    conexion.commit() #Guarda cambios
    conexion.close() #Cierra la conexion

#Funcion para actualizar cantidad de producto (3)
def actualizar_producto():
    conexion = sqlite3.connect("inventario.db") #conecta o crea la base de datos
    cursor = conexion.cursor() # Crea un cursor para interactuar con la db
    modificado = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    id=int(input("Ingrese el ID del producto a actualizar: "))
    nueva_cantidad=int(input("Ingrese la nueva cantidad de stock: "))
    
    cursor.execute("UPDATE productos SET cantidad = ?, modify_date = ? WHERE id = ?", (nueva_cantidad,modificado,id))

    conexion.commit() #Guarda cambios
    conexion.close() #Cierra la conexion

#Funcion para eliminar un producto (4)
def eliminar_producto():
    conexion = sqlite3.connect("inventario.db")  # Conecta o crea la base de datos
    cursor = conexion.cursor()  # Crea un cursor para interactuar con la db
    
    id = int(input("Ingrese el ID del producto a eliminar: "))
    
    # Verificar si el producto existe
    cursor.execute("SELECT nombre FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    
    if producto:  # Si el producto existe
        nombre_producto = producto[0]
        confirmacion = input(f"¿Está seguro que desea eliminar el artículo '{nombre_producto}'? (s/n): ").strip().lower()
        if confirmacion == 's':
            cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
            print(f"El producto '{nombre_producto}' ha sido eliminado.")
        else:
            print("Eliminación cancelada.")
    else:
        print("No existe un producto con ese ID.")
    
    conexion.commit()  # Guarda cambios
    conexion.close()  # Cierra la conexión

# Función Buscar producto(5)
def buscar_producto():
    conexion = sqlite3.connect("inventario.db")  # Conecta o crea la base de datos
    cursor = conexion.cursor()  # Crea un cursor para interactuar con la db

    id = int(input("\nIngrese el ID del producto: "))

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    
    if resultado == None:  # Verifica si el resultado está vacío
        print("El producto buscado no se encuentra en la base\n")
    else:
        print("\nProducto encontrado:\n")
        print(f"""
        ---------------------
        ID:          {resultado[0]}
        Nombre:      {resultado[1]}
        Descripción: {resultado[2]}
        Cantidad:    {resultado[3]}
        Precio:      ${resultado[4]}
        Categoría:   {resultado[5]}
        """)

    conexion.close()  # Cierra la conexión

#Función bajo stock (6)
def bajo_stock():
    conexion = sqlite3.connect("inventario.db")  # Conecta o crea la base de datos
    cursor = conexion.cursor()  # Crea un cursor para interactuar con la db
    minimo = input("Ingrese el valor minimo de stock a controlar: ")
    cursor.execute("SELECT * FROM productos WHERE cantidad <?",(minimo,))
    tabla = cursor.fetchall()
    print(f"{MAGENTA}{'ID':<5} {'Nombre':<20} {'Descripción':<20} {'Cantidad':<10} {'Precio':<10} {'Categoría':<15}{RESET}")
    print(f"{MAGENTA}{'-'*80}{RESET}")  # Separador

    for filas in tabla:
         print(f"{filas[0]:<5} {filas[1]:<20} {filas[2]:<20} {filas[3]:<10} {filas[4]:<10} {filas[5]:<15}")
    
    print()
    #tabla = cursor.fetchall()
    #for filas in tabla:
    #    print("ID: ",filas[0], "|","Nombre: ",filas[1],"|", "Descripción: ", filas[2],"|","Cantidad: ", filas[3],"|","Precio: $",filas[4], "|","Categoria: ",filas[5],"|")
    #print()
    conexion.commit()  # Guarda cambios
    conexion.close()  # Cierra la conexión    