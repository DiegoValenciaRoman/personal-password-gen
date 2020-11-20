import bcrypt
from tinydb import TinyDB, Query
import errors
from getpass import getpass
db = TinyDB('./db.json')


def create_hash(passw):
    hashed = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_pw(passw, hashed):
    return bcrypt.checkpw(passw.encode('utf-8'), hashed.encode('utf-8'))


def check_connectivity():
    print("\nok!\n")


def create_user_db():
    users_table = db.table('name')
    exiter = True
    while exiter:
        name = input("1.-Ingresa tu nombre (caracteres de largo 3 a 30): ")
        if name == "xxx":
            return
        if type(name) != str or len(name) < 3 or len(name) > 30:
            raise errors.CliUserNameError("Revisa el largo o tipo de nombre")
        print("\n*Analizando nombre...")
        results = users_table.search(Query().name == name)
        if len(results) == 0:
            exiter = False
        else:
            print(
                "Advertencia: El nombre que elegista ya existe (para salir ingresa xxx).")
    pssw = getpass("\n2.-Ingresa tu password principal: ")
    pssw = create_hash(pssw)
    secreto = getpass("\n3.-Ingresa tu secreto: ")
    users_table.insert({
        'name': name,
        'hashedmainpssw': pssw,
        'secreto': secreto,
        'apps': []
    })
    print("Usuario creado!")


def login():
    users_table = db.table('name')
    name = input("\nIngresa tu nombre de usuario: ")
    passw = getpass("\nIngresa tu password principal: ")
    results = users_table.search(Query().name == name)
    # mejorar
    if len(results) < 1:
        return (False, '', '')
    if check_pw(passw, results[0]['hashedmainpssw']):
        print("*Inicio de sesion exitoso!")
        return (True, passw, name)
    else:
        return (False, '', '')


def logged_in_menu(pw, name):
    users_table = db.table('name')
    secreto = users_table.search(Query().name == name)[0]['secreto']
    apps = users_table.search(Query().name == name)[0]['apps']
    opcion = input("1.-Agregar aplicacion\n2.-Obtener pass \n")
    if opcion != "1" and opcion != "2":
        print("error")
        return
    if opcion == "1":
        appname = input("\nIngrese nombre de la app: ")
        web = input("\nIngrese web de la app: ")
        final_pass = create_hash(pw+secreto+appname)
        apps.append({'appname': appname, 'web': web, 'finalpass': final_pass})
        users_table.update({'apps': apps}, Query().name == name)
        print("La nueva pass para tu app ", appname, " es: ", final_pass)
    if opcion == "2":
        appname = input("\nIngrese nombre de la app: ")
        for app in apps:
            if app['appname'] == appname:
                print('tu pass es: ', app['finalpass'])
                return
