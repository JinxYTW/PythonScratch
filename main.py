from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from models.gamepad import GameController
import threading
from models.ip_manager import IPManager  

def start_game_controller():
    marty_ip = IPManager.get_instance().get_ip_address1()
    marty_ip2 = IPManager.get_instance().get_ip_address2()
    
    game_controller = GameController(marty_ip,marty_ip2)
    game_controller.run()

if __name__ == "__main__":
    app = QApplication([])

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    # Définir les adresses IP dans IPManager
    IPManager.get_instance().add_ip_address("192.168.0.100") # Addresse IP du Marty 1
    IPManager.get_instance().add_ip_address("192.168.0.100") # Addresse IP du Marty 2

    window = MainWindow()
    window.show()

    # Démarrer le contrôleur de jeu dans un thread séparé pour ne pas bloquer l'UI
    game_controller_thread = threading.Thread(target=start_game_controller)
    game_controller_thread.daemon = True  # Permet de terminer le thread lorsque l'application se ferme
    game_controller_thread.start()

    app.exec()
