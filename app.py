#Proyecto Final Integrador

#### Importar modulos ####
import funciones

##### Variables ########
opcion_seleccionada =0 #opciones de menu
inventario =[] #lista de inventario

###### Bucle principal ############
funciones.crear_base()
while opcion_seleccionada != 7:
    funciones.mostrar_menu()  # Llamada a la función para mostrar el menú
    
    # Verificación que la opción ingresada sea numérica
    try:
        opcion_seleccionada = int(input("\nIngrese una opcion: "))
    except ValueError:
        opcion_seleccionada = 0

    # Opciones del menú
    if opcion_seleccionada == 1:
        funciones.agregar_producto()
        
    elif opcion_seleccionada == 2:
        funciones.mostrar_productos()  
    
    elif opcion_seleccionada == 3:
        funciones.actualizar_producto()

    elif opcion_seleccionada == 4:
        funciones.eliminar_producto()
        
    elif opcion_seleccionada == 5:
        funciones.buscar_producto()
    
    elif opcion_seleccionada == 6:
        funciones.bajo_stock()
    
    elif opcion_seleccionada == 7:
        print("Muchas gracias por utilizar nuestro sistema\nAdios!")
        break

    else:
        print("Opción incorrecta, por favor intente nuevamente\n")
