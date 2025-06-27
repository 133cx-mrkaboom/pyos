# server

from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import os

class WebServer:
    def __init__(self, port=8080, folder='.'):
        self.port = port
        self.folder = os.path.abspath(folder)
        self.server = None
        self.thread = None
        self.is_running = False

    def _create_server(self):
        # Create a custom handler with specified directory
        handler_class = self._make_handler_with_directory(self.folder)
        return HTTPServer(('', self.port), handler_class)

    def _make_handler_with_directory(self, directory):
        # Dynamically create a handler class with the directory
        class CustomHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=directory, **kwargs)
        return CustomHandler

    def start(self):
        if self.is_running:
            print("Server is already running.")
            return
        self.server = self._create_server()
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.is_running = True
        print(f"Server started on port {self.port}, serving folder: {self.folder}")

    def stop(self):
        if self.server:
            print("Stopping server...")
            self.server.shutdown()
            self.server.server_close()
            self.thread.join()
            self.is_running = False
            self.server = None
            self.thread = None
            print("Server stopped.")

    def toggle(self):
        if self.is_running:
            self.stop()
        else:
            self.start()

    def change_port(self, new_port):
        was_running = self.is_running
        if was_running:
            self.stop()
        self.port = new_port
        if was_running:
            self.start()
        print(f"Port changed to {self.port}.")

    def set_folder(self, folder_path):
        abs_path = os.path.abspath(folder_path)
        if not os.path.isdir(abs_path):
            print(f"Error: '{folder_path}' is not a valid directory.")
            return
        was_running = self.is_running
        if was_running:
            self.stop()
        self.folder = abs_path
        if was_running:
            self.start()
        print(f"Folder changed to: {self.folder}")
