import random
import time
import tkinter as tk
from tkinter import ttk
import threading
import logging

# Setup logging
logging.basicConfig(filename="traffic_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

class TrafficLight:
    def __init__(self, intersection_id):
        self.intersection_id = intersection_id
        self.state = 'RED'

    def update_state(self, new_state):
        logging.info(f"Intersection {self.intersection_id}: {self.state} -> {new_state}")
        self.state = new_state

class TrafficControllerGUI:
    def __init__(self, root, intersections=3):
        self.root = root
        self.root.title("Smart Traffic Light Controller")
        self.intersections = intersections

        self.lights = {i: TrafficLight(i) for i in range(intersections)}
        self.traffic_density = {i: 0 for i in range(intersections)}

        self.frames = {}
        self.labels = {}
        self.density_labels = {}

        self.setup_ui()
        self.running = False

    def setup_ui(self):
        for i in range(self.intersections):
            frame = ttk.LabelFrame(self.root, text=f"Intersection {i}")
            frame.grid(row=0, column=i, padx=10, pady=10)

            state_label = tk.Label(frame, text="RED", bg="red", fg="white", font=("Arial", 16), width=10)
            state_label.pack(padx=5, pady=5)
            self.labels[i] = state_label

            density_label = tk.Label(frame, text="Density: 0", font=("Arial", 10))
            density_label.pack(pady=5)
            self.density_labels[i] = density_label

        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=1, columnspan=self.intersections, pady=10)

    def simulate_traffic(self):
        for i in self.traffic_density:
            self.traffic_density[i] = random.randint(0, 10)

    def prioritize_intersections(self):
        return sorted(self.traffic_density, key=self.traffic_density.get, reverse=True)

    def update_gui_lights(self):
        for i in self.lights:
            self.labels[i].config(text="RED", bg="red")
            self.lights[i].update_state("RED")
            self.density_labels[i].config(text=f"Density: {self.traffic_density[i]}")

        priorities = self.prioritize_intersections()
        if priorities:
            self.labels[priorities[0]].config(text="GREEN", bg="green")
            self.lights[priorities[0]].update_state("GREEN")
        if len(priorities) > 1:
            self.labels[priorities[1]].config(text="YELLOW", bg="yellow")
            self.lights[priorities[1]].update_state("YELLOW")

    def run(self):
        while self.running:
            self.simulate_traffic()
            self.update_gui_lights()
            time.sleep(2)

    def start_simulation(self):
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self.run, daemon=True)
            thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficControllerGUI(root)
    root.mainloop()
()