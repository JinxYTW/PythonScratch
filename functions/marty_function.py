from martypy import Marty
from models.labyrinthe import Labyrinth
import threading

class MartyFunction:
    def __init__(self, marty_ip):
        self.marty_ip = marty_ip
        self.my_marty = None
        self.labyrinth = Labyrinth()

    def connect(self):
        """Connect to Marty"""
        self.my_marty = Marty("wifi", self.marty_ip)
        self.my_marty.stand_straight(1000, None)
        self.labyrinth.my_marty = self.my_marty

    def dance(self):
        """Make Marty dance."""
        if self.my_marty:
            self.my_marty.dance()
        else:
            print("Marty is not connected")

    def stand_straight(self):
        """Make Marty stand straight."""
        if self.my_marty:
            self.my_marty.stand_straight(1000, None)
        else:
            print("Marty is not connected")

    def read_color(self):
        """Read color from Marty's obstacle sensor."""
        try:
            if self.my_marty:
                return self.my_marty.get_obstacle_sensor_reading('left')
            else:
                print("Marty is not connected")
        except Exception as e:
            print(f"Error reading color: {e}")
            return None

    def walk(self, steps=2, direction='auto', turn=0, step_length=35, step_time=1500):
        """Make Marty walk."""
        if self.my_marty:
            print("Marty is walking")
            self.my_marty.walk(steps, direction, turn, step_length, step_time, None)
        else:
            print("Marty is not connected")

    def sidestep(self, direction='right', steps=2, step_length=35, step_time=1000):
        """Make Marty sidestep."""
        if self.my_marty:
            self.my_marty.sidestep(direction, steps, step_length, step_time, None)
        else:
            print("Marty is not connected")

    def turn(self, direction='right', steps=2, turn_amount=25, step_time=1500):
        """Make Marty turn."""
        if self.my_marty:
            if direction == 'right':
                self.my_marty.walk(steps, 'auto', -15, turn_amount, step_time, None)
            else:
                self.my_marty.walk(steps, 'auto', 15, turn_amount, step_time, None)
        else:
            print("Marty is not connected")

    def auto_walk(self):
        """Make Marty walk automatically."""
        if self.my_marty:
            self.labyrinth.auto_walk()
        else:
            print("Marty is not connected")

    def play_music(self, mp3_file):
        """Play an MP3 file."""
        if self.my_marty:
            try:
                print(f"Playing music: {mp3_file}")
                self.my_marty.play_mp3(mp3_file)
            except Exception as e:
                print(f"Error playing music: {e}")
        else:
            print("Marty is not connected")

    def wait(self, seconds=2):
        """Make Marty wait."""
        if self.my_marty:
            self.my_marty.wait(seconds)
        else:
            print("Marty is not connected")

    def get_ground_sensor_reading(self, foot='left'):
        """Get the ground sensor reading."""
        if self.my_marty:
            return self.my_marty.get_ground_sensor_reading(foot)
        else:
            print("Marty is not connected")
            return None

    def calibrate(self):
        """Calibrate the labyrinth."""
        if self.my_marty:
            self.labyrinth.calibrate()
        else:
            print("Marty is not connected")

    def recon_labyrinth(self, other_marty_function):
        """Recon the labyrinth with two Martys in parallel."""
        if self.my_marty and other_marty_function.my_marty:
            # Create threads for reconning the labyrinth for each Marty
            thread1 = threading.Thread(target=self._recon_labyrinth, args=(self.labyrinth,))
            thread2 = threading.Thread(target=other_marty_function._recon_labyrinth, args=(other_marty_function.labyrinth,))
            # Start the threads
            thread1.start()
            thread2.start()
            # Wait for both threads to finish
            thread1.join()
            thread2.join()
        else:
            print("One or both Martys are not connected")

    def _recon_labyrinth(self, labyrinth):
        """Private method for reconning the labyrinth."""
        labyrinth.recon()
