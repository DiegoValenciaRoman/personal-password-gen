import main
import sys
import errors
main.check_connectivity()
secret = "123"
arguments = []


def assign_arguments():
    global arguments
    arguments = sys.argv
    if len(arguments) < 3:
        raise errors.CliArgumentsError(
            "Debes iniciar el programa con al menos 2 parametros. Ej:'python3 cli.py run login'")


def main_command_controller(maincom, secondcom):
    if maincom != "run":
        raise errors.CliArgumentsError(
            "Debes iniciar el programa con 'python3 cli.py run login o python3 cli.py run create'")
    if secondcom == "create":
        main.create_user_db()
    if secondcom == "login":
        login_status, pw, name = main.login()
        if login_status:
            main.logged_in_menu(pw, name)
        else:
            print("Error de password.")
            return


if __name__ == "__main__":
    assign_arguments()
    main_command_controller(arguments[1], arguments[2])
