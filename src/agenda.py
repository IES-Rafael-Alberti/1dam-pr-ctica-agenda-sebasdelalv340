"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

OPCIONES_MENU = {1, 2, 3, 4, 5, 6, 7, 8}



def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def cargar_contactos(contactos: list) -> list:
    """ Carga los contactos iniciales de la agenda desde un fichero
    ...
    
    Args:
        contactos (list): Lista de contactos vacía.

    Returns:
        list: una lista con los contactos.
    """

    # Recorre dos listas (nombres_clave y cada línea del fichero), guardando en diccionarios los datos de cada contacto para ir añadiendolo a una lista
    
    nombres_clave = ["nombre", "apellido", "email", "telefonos"]
    with open(RUTA_FICHERO, 'r') as fichero:
        for linea in fichero:
            valores = linea.split(";")
            contacto_info = {}
            for i in range(len(nombres_clave)):
                if nombres_clave[i] == "telefonos":
                    contacto_info[nombres_clave[i]] = list(valores[i:])
                else:
                    contacto_info[nombres_clave[i]] = valores[i]
            
            contactos.append(contacto_info)
            
    return contactos


def agregar_contacto(contactos:list) -> list:
    """ Agrega un nuevo contacto a la lista
    ...
    
    Args:
        contactos (list): Lista de contactos vacía.

    Returns:
        list: la lista de contactos con el nuevo contacto añadido.
    """

    nombre = pedir_nombre()
    apellido = pedir_apellido()
    email = pedir_email(contactos)
    telefonos = pedir_telefono()

    contacto_info = {"nombre": nombre, "apellido": apellido, "email": email, "telefonos": telefonos}

    contactos.append(contacto_info)

    return contactos


def pedir_nombre() -> str:
    """ Pide el nombre del nuevo contacto.

    Returns:
        str: el nombre del contacto.
    """

    try:
        nombre = input("Ingrese un nombre: ")
        return nombre.title()
    except ValueError:
        print("Error - entrada no válida.")

    return nombre


def pedir_apellido() -> str:
    """ Pide el apellido del nuevo contacto.

    Returns:
        str: el apellido del contacto.
    """

    try:
        apellido = input("Ingrese un apellido: ")
        return apellido.capitalize()
    except ValueError:
        print("Error - entrada no válida.")


def pedir_email(contactos: list) -> str:
    """ Pide el email del nuevo contacto.

    Args:
        contactos (list): lista de contactos

    Returns:
        str: el email del contacto.
    """
    entrada = False
    while not entrada:
        try:
            email = input("Ingrese un email: ")
            validar_email(contactos, email)
            entrada = True
        except ValueError:
            if email == "":
                print("el email no puede ser una cadena vacía")
            elif email.find("@") == -1:
                print("el email no es un correo válido") 
            for diccionario in contactos:
                if email in diccionario.values():
                    print("el email ya existe en la agenda")

    return email


def validar_email(contactos: list, email: str) -> bool:
    """ Controla los posibles errores del email del nuevo contacto.

    Args:
        contactos (list): lista de contactos
        email (str): email introducido por el usurio
    Returns:
        bool: controla errores o si el contacto ya existe.
    """
    if email == "":
        raise ValueError("el email no puede ser una cadena vacía")
    elif email.find("@") == -1:
        raise ValueError("el email no es un correo válido") 
    for diccionario in contactos:
        if email in diccionario.values():
            raise ValueError("el email ya existe en la agenda")


def pedir_telefono() -> list:
    """ Pide el teléfono del nuevo contacto.

    Returns:
        list: lista de teléfonos del contacto.
    """

    telefonos = []
    entrada = False
    print("Ingrese un teléfono: ", end="")
    while not entrada:
        telefono = input()
        telefono = telefono.replace(" ", "")
        if validar_telefono(telefono):
            telefonos.append(telefono)
        elif telefono == "":
            entrada = True
    
    return telefonos


def validar_telefono(telefono: str) -> bool:
    """ Controla los posibles errores del teléfono del nuevo contacto.

    Args:
        telefono (str): teléfono introducido por el usurio

    Returns:
        bool: True si es correcto y False si es incorrecto.
    """

    telefono = telefono.replace(" ", "")
    
    if telefono.startswith("+34"):
        if len(telefono) == 12:
            return True
        else:
            return False
    elif len(telefono) == 9:
        if telefono[:-1].isdigit:
            return True
        else:
            return False
    elif len(telefono) < 9:
        return False

    return False
    

def buscar_contactos_params(contactos: list) -> str:
    """ Muestra el menú de criterios de búsqueda y busca un contacto.

    Args:
        contactos (list): lista de contactos

    Returns:
        str: toda la información del contacto
    """

    print("\nCriterios:")
    print("1. Nombre")
    print("2. Apellido")
    print("3. Email")
    print("4. Teléfono\n")

    entrada = False
    while not entrada:
        try:
            opcion = int(input("Seleccione un criterio: "))
            if 1 <= opcion <= 4:
                entrada = True
        except ValueError:
            print("Opción no válida.")
        
    borrar_consola()
    if opcion == 1:
        buscar_nombre(contactos)
    if opcion == 2:
        buscar_apellido(contactos)
    elif opcion == 3:
        buscar_email(contactos)
    elif opcion == 4:
        buscar_telefono(contactos)


def buscar_nombre(contactos: list):
    """ Busca el nombre del contacto y muestra la info del contacto.

    Args:
        contactos (list): lista de contactos

    Returns:
        print: toda la info del contacto
    """

    valor = input("\nIngresa el valor de búsqueda: ")
    borrar_consola()
    valor = valor.lower()
    for contacto in contactos:
        if valor == contacto.get("nombre")[0].lower():
            print("Nombre: ", end="")           
            print(f"{contacto.get("nombre")}", end= " ")                
            print(f"{contacto.get("apellido")}", end= " ")
            print(f"({contacto.get("email")})")                
            print(f"Teléfonos: {" / ".join(contacto.get("telefonos"))}")
            print("." * 6)


def buscar_apellido(contactos: list):
    """ Busca el apellido del contacto y muestra la info del contacto.

    Args:
        contactos (list): lista de contactos

    Returns:
        print: toda la info del contacto
    """

    valor = input("Ingresa el valor de búsqueda: ")
    borrar_consola()
    valor = valor.lower()
    for contacto in contactos:
        if valor == contacto.get("apellido")[0].lower():
            print("Nombre: ", end="")           
            print(f"{contacto.get("nombre")}", end= " ")                
            print(f"{contacto.get("apellido")}", end= " ")
            print(f"({contacto.get("email")})")                
            print(f"Teléfonos: {" / ".join(contacto.get("telefonos"))}")
            print("." * 6)


def buscar_email(contactos: list):
    """ Busca el email del contacto y muestra la info del contacto.

    Args:
        contactos (list): lista de contactos

    Returns:
        print: toda la info del contacto
    """

    valor = input("Ingresa un email: ")
    borrar_consola()
    valor = valor.lower().split("@")
    for contacto in contactos:
        if valor[0] in contacto.get("email").lower():
            print("Nombre: ", end="")           
            print(f"{contacto.get("nombre")}", end= " ")                
            print(f"{contacto.get("apellido")}", end= " ")
            print(f"({contacto.get("email")})")                
            print(f"Teléfonos: {" / ".join(contacto.get("telefonos"))}")
            print("." * 6)


def buscar_telefono(contactos: list):
    """ Busca el teléfono del contacto y muestra la info del contacto.

    Args:
        contactos (list): lista de contactos

    Returns:
        print: toda la info del contacto
    """

    valor = input("Ingresa un telefono: ")
    borrar_consola()
    valor = valor.replace("+34", "")
    for contacto in contactos:
        for tel in contacto.get("telefonos"):
            if valor in tel:
                print("Nombre: ", end="")           
                print(f"{contacto.get("nombre")}", end= " ")                
                print(f"{contacto.get("apellido")}", end= " ")
                print(f"({contacto.get("email")})")                
                print(f"Teléfonos: {" / ".join(contacto.get("telefonos"))}")
                print("." * 6)


def modificar_contacto(contactos: list) -> list:
    """ Modifica la info de un contacto.

    Args:
        contactos (list): lista de contactos

    Returns:
        list: lista de contactos actualizada
    """

    print("1. Nombre")
    print("2. Apellido")
    print("3. Email")
    print("4. Teléfono\n")

    try: 
        opcion = input("Ingrese el campo que desea cambiar (1-4): ")
        valor_actual = input("Ingrese el valor que desea cambiar: ")
        valor_nuevo = input("Ingrese el nuevo valor: ")
    except ValueError:
        print("error en la entrada")

    if opcion == 1:
        modificar_nombre(contactos, valor_actual, valor_nuevo)
    if opcion == 2:
        modificar_apellido(contactos, valor_actual, valor_nuevo)
    if opcion == 3:
        modificar_email(contactos, valor_actual, valor_nuevo)
    if opcion == 4:
        modificar_telefono(contactos, valor_actual, valor_nuevo)

    borrar_consola()
    return contactos


def modificar_nombre(contactos: list, valor_actual: str, valor_nuevo: str) ->list:
    """ Modifica el nombre de un contacto.

    Args:
        contactos (list): lista de contactos
        valor_actual (str): nombre a modificar del contacto
        valor_nuevo (str): nuevo nombre

    Returns:
        list: lista de contactos modificada
    """
    
    for contacto in contactos:
        if valor_actual == contacto.get("nombre"):
            contacto["nombre"] = valor_nuevo

    return contactos


def modificar_apellido(contactos: list, valor_actual: str, valor_nuevo: str) ->list:
    """ Modifica el apellido de un contacto.

    Args:
        contactos (list): lista de contactos
        valor_actual (str): apellido a modificar del contacto
        valor_nuevo (str): nuevo apellido

    Returns:
        list: lista de contactos modificada
    """

    for contacto in contactos:
        if valor_actual == contacto.get("apellido"):
            contacto["apellido"] = valor_nuevo

    return contactos


def modificar_email(contactos: list, valor_actual: str, valor_nuevo: str) ->list:
    """ Modifica el email de un contacto.

    Args:
        contactos (list): lista de contactos
        valor_actual (str): email a modificar del contacto
        valor_nuevo (str): nuevo email

    Returns:
        list: lista de contactos modificada
    """

    for contacto in contactos:
        if valor_actual == contacto.get("email"):
            contacto["email"] = valor_nuevo

    return contactos


def modificar_telefono(contactos: list, valor_actual: str, valor_nuevo: str) ->list:
    """ Modifica el teléfono de un contacto.

    Args:
        contactos (list): lista de contactos
        valor_actual (str): teléfono a modificar del contacto
        valor_nuevo (str): nuevo teléfono

    Returns:
        list: lista de contactos modificada
    """

    for contacto in contactos:
        if valor_actual in contacto.get("telefonos"):
            contacto.get("telefonos").remove(valor_actual)
            contacto.get("telefonos").append(valor_nuevo)

    return contactos


def buscar_contacto(contactos: list, email: str) -> int:
    """ Busca la posición de un email concreto.

    Args:
        contactos (list): lista de contactos
        email (str): rciruelo@gmail.com
        
    Returns:
        int: posición del contacto
    """
    
    cont = 0
    for contacto in contactos:
        valor = contacto.get("email")
        if valor == email:
            pos = cont
            return pos
        else:
            pos = contacto.get("edad")
            cont += 1
            
    return pos


def eliminar_contacto_concreto(contactos: list) -> list:
    """ Elimina un contacto concreto de la agenda
    ...

    Args:
        contactos (list): lista de contactos

    Returns:
        list: lista actualizada
    """

    try:
        #TODO: Crear función buscar_contacto para recuperar la posición de un contacto con un email determinado
        email = "rciruelo@gmail.com"
        pos = buscar_contacto(contactos, email)
        if pos != None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")
    
    return contactos


def eliminar_contacto(contactos: list) -> list:
    """ Elimina un contacto de la agenda
    ...

    Args:
        contactos (list): lista de contactos

    Returns:
        list: lista de contactos modificada
    """

    try:
        nombre = input("Ingrese el nombre del contacto: ")
        pos = buscar_name(contactos, nombre)
        if pos != None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")

    return contactos


def buscar_name(contactos: list, nombre: str) -> int:
    """ Busca la posición de un contacto con un nombre
    ...

    Args:
        contactos (list): lista de contactos
        nombre (str): nombre a buscar

    Returns:
        int: posición del contacto con dicho nombre
    """

    nombre = nombre.lower()
    cont = 0
    for contacto in contactos:
        if nombre == contacto.get("nombre").lower():
            pos = cont
            return pos
        else:
            pos = contacto.get("edad")
            cont += 1
            
    return pos


def vaciar_agenda(contactos: list) -> list:
    """ Borra todos los contactos de la agenda
    ...

    Args:
        contactos (list): lista de contactos

    Returns:
        list: lista vacía
    """
    for contacto in contactos:
        del contacto

    return contactos


def cargar_agenda_inicial(contactos: list) -> list:
    """ Carga los contactos de la agenda inicial
    ...

    Args:
        contactos (list): lista de contactos
        
    Returns:
        list: lista de contactos
    """
    contactos = cargar_contactos(contactos)
    return contactos


def mostrar_contactos(contactos: list):
    """ Muestra todos los contactos de la agenda
    ...

    Args:
        contactos (list): lista de contactos

    Returns:
        print: agenda completa
    """

    print(f"AGENDA ({len(contactos)})\n")
    print("-" * 6)

    for contacto in contactos:
        print("Nombre: ", end="")
        for valor in contacto.keys():
            if valor == "nombre":
                print(f"{contacto.get("nombre")}", end= " ")
            elif valor == "apellido":
                print(f"{contacto.get("apellido")}", end= " ")
            if valor == "email":
                print(f"({contacto.get("email")})")
            elif valor == "telefonos":
                print(f"Teléfonos: {" / ".join(contacto.get("telefonos"))}")
                print("." * 6)


def pedir_opcion():
    """Devuelve el número del menú."""

    opcion = 0
    while opcion not in OPCIONES_MENU:
        try:
            opcion = int(input())
        except ValueError:           
            print("Opción incorrecta.")
            
    return opcion


def mostrar_menu():
    print("\nMenú:")
    print("1. Nuevo contacto")
    print("2. Modificar contacto")
    print("3. Eliminar contacto")
    print("4. Vaciar agenda")
    print("5. Cargar agenda inicial")
    print("6. Mostrar contactos por criterio")
    print("7. Mostrar la agenda completa")
    print("8. Salir")   
    print ("\n>> Seleccione una opción:", end= " ")


def agenda(contactos: list):
    """ Ejecuta el menú de la agenda con varias opciones
    ...

    Args:
        contactos (list): lista de contactos
    """

    opcion = 0
    while opcion != 8:
        mostrar_menu()
        opcion = pedir_opcion()

        borrar_consola()
        
        if opcion in OPCIONES_MENU ^ {8}:
            if opcion == 1:
                agregar_contacto(contactos)
            elif opcion == 2:
                modificar_contacto(contactos)
            elif opcion == 3:
                eliminar_contacto(contactos)
            elif opcion == 4:
                vaciar_agenda(contactos)
            elif opcion == 5:
                cargar_agenda_inicial(contactos)
            elif opcion == 6:
                buscar_contactos_params(contactos)
            elif opcion == 7:
                mostrar_contactos(contactos)
            
    if opcion == 8:
                print("¡Hasta pronto!")

def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    os.system("pause")


def main():
    """ Función principal del programa
    """

    borrar_consola()

    contactos = []

    cargar_contactos(contactos)

    agregar_contacto(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()
    
    eliminar_contacto_concreto(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    mostrar_contactos(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    agenda(contactos)


if __name__ == "__main__":
    main()