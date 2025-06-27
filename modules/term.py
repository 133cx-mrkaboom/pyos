from . import h as help
from . import server
import sys

# Initialize toggle state and server instance once
tgle = False

def main():
    global tgle

    while True:
        inp = input('[PYOS]>>> ').strip().lower()

        if inp == "help":
            help.main()

        elif inp == "port":
            new_port = input('Port: ')
            try:
                server.change_port(int(new_port))
                print("Port Changed")
            except ValueError:
                print("Invalid port number.")

        elif inp == "toggle":
            if not tgle:
                server.start()
                print("Server on")
                tgle = True
            else:
                server.stop()
                print("Server off")
                tgle = False

        elif inp == "dir":
            new_path = input("New Path: ")
            server.set_folder(new_path)
            print("Path Set")

        elif inp == "exit":
            print("Exiting")
            sys.exit()

        else:
            print("Unknown command. Type 'help' for options.")
