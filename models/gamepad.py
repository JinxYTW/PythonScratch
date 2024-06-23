from __future__ import print_function
from martypy import Marty
import inputs
import threading
from functions.marty_function import MartyFunction
from models.labyrinthe import Labyrinth

class GameController:
    def __init__(self, marty_ip, marty_ip2):
        self.marty_ip = marty_ip
        self.marty_ip2 = marty_ip2
        self.marty_functions = None
        self.marty_functions2 = None
        self.turning = False
        self.is_connected = False
        self.labyrinth = Labyrinth()

    def both_walk(self):
        if self.is_connected:
            # Create threads for walking
            thread1 = threading.Thread(target=self.marty_functions.walk)
            thread2 = threading.Thread(target=self.marty_functions2.walk)
            # Start the threads
            thread1.start()
            thread2.start()
            # Wait for both threads to finish
            thread1.join()
            thread2.join()
        else:
            print("Marty is not connected")

    def run(self):
        try:
            gamepad = inputs.devices.gamepads[0]
        except Exception:
            print("Couldn't find a proper controller.")
            return
        gamepad.led = 1  # Ne sert a rien mais faut pas le supprimer

        while True:
            events = inputs.get_gamepad()
            for event in events:
                self.handle_event(event)

    def connect_to_marty(self):
        """Attempt to connect to Marty."""
        if not self.is_connected:
            print("Trying to connect...")
            try:
                self.marty_functions = MartyFunction(self.marty_ip)
                self.marty_functions2 = MartyFunction(self.marty_ip2)
                self.marty_functions.connect()
                self.marty_functions2.connect()
                self.is_connected = True
                print("Connection established!")
            except Exception as e:
                print(f"Couldn't connect to Marty: {e}")

    def handle_event(self, event):
        if event.code == "BTN_THUMBR" and event.state == 1:  # Connect
            self.connect_to_marty()

        if event.code == "BTN_THUMBL" and event.state == 1:
            self.marty_functions.auto_walk()
            print("BTN_THUMBL pressed.")

        if event.code == "BTN_SOUTH" and event.state == 1:  # Dance
            print("B button pressed.")
            if self.is_connected:
                self.both_walk()

        if event.code == "BTN_EAST" and event.state == 1:  # Calibrate
            print("Calibrating labyrinth...")
            if self.is_connected:
                self.marty_functions.calibrate()
            else:
                print("Marty not connected!")

        if event.code == "BTN_NORTH" and event.state == 1:  # Recon
            print("Reconning labyrinth...")
            if self.is_connected:
                self.marty_functions.recon_labyrinth(self.marty_functions2)
            else:
                print("Marty not connected!")

        if event.code == "BTN_WEST" and event.state == 1:
            print("Y button released.")

        if event.code == "ABS_HAT0Y" and event.state == -1:  # Walk forward
            print("Going forwards.")
            if self.is_connected:
                self.marty_functions.walk()

        if event.code == "ABS_HAT0Y" and event.state == 0:
            print("Stopped.")

        if event.code == "ABS_HAT0Y" and event.state == 1:  # Walk backward
            print("Going backwards.")
            if self.is_connected:
                self.marty_functions.walk(turn=0, step_length=-35)

        if event.code == "ABS_HAT0X" and event.state == 1:  # Sidestep right
            print("Going right.")
            if self.is_connected:
                self.marty_functions.sidestep(direction='right')

        if event.code == "ABS_HAT0X" and event.state == -1:  # Sidestep left
            print("Going left.")
            if self.is_connected:
                self.marty_functions.sidestep(direction='left')

        if event.code == "BTN_TR" and event.state == 1 and not self.turning:  # Turn right
            print("Turning right...")
            if self.is_connected:
                self.marty_functions.turn(direction='right')
            self.turning = True

        if event.code == "BTN_TR" and event.state == 0 and self.turning:
            print("Done turning.")
            self.turning = False

        if event.code == "BTN_TL" and event.state == 1 and not self.turning:  # Turn left
            print("Turning left...")
            if self.is_connected:
                self.marty_functions.turn(direction='left')
            self.turning = True

        if event.code == "BTN_TL" and event.state == 0 and self.turning:
            print("Done turning.")
            self.turning = False

    def merge_directions(self, directions1, directions2):
        merged_directions = directions1 + directions2
        return merged_directions
