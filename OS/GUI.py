import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class CubeSatGroundStation:
    def __init__(self, root):
        self.root = root
        self.root.title("SNAC-Sat Ground Station")

        self.create_widgets()

    def create_widgets(self):
        # Image Display Frame
        image_frame = ttk.LabelFrame(self.root, text="Image Received")
        image_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.image_label = ttk.Label(image_frame)
        self.image_label.grid(row=0, column=0, padx=10, pady=10)

        # Past Image Timestamps Frame
        past_images_frame = ttk.LabelFrame(self.root, text="Past Image Timestamps")
        past_images_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.past_images_listbox = tk.Listbox(past_images_frame, height=10, width=25)
        self.past_images_listbox.grid(row=0, column=0, padx=10, pady=10)

        # Position and Yaw Data Frame
        data_frame = ttk.LabelFrame(self.root, text="SNAC-Sat Data")
        data_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.time_label = ttk.Label(data_frame, text="Time: N/A", justify=tk.LEFT)
        self.time_label.grid(row=0, column=0, padx=10, pady=5)

        self.position_label = ttk.Label(data_frame, text="Position: N/A", justify=tk.LEFT)
        self.position_label.grid(row=1, column=0, padx=10, pady=5)

        self.yaw_label = ttk.Label(data_frame, text="Yaw: N/A", justify=tk.LEFT)
        self.yaw_label.grid(row=2, column=0, padx=10, pady=5)

        self.leg_label = ttk.Label(data_frame, text="Leg: N/A", justify=tk.LEFT)
        self.leg_label.grid(row=3, column=0, padx=10, pady=5)

        self.illumination_label = ttk.Label(data_frame, text="Illumination Status: N/A", justify=tk.LEFT)
        self.illumination_label.grid(row=5, column=0, padx=10, pady=5)

        # CubeCity Data Frame

        data_values_frame = ttk.LabelFrame(self.root, text="CubeCity Data")
        data_values_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.red_LEDs = ttk.Label(data_values_frame, text="Red: N/A", justify=tk.LEFT)
        self.red_LEDs.grid(row=0, column=0, padx=10, pady=0)

        self.green_LEDs = ttk.Label(data_values_frame, text="Green: N/A", justify=tk.LEFT)
        self.green_LEDs.grid(row=1, column=0, padx=10, pady=0)

        self.blue_LEDs = ttk.Label(data_values_frame, text="Blue: N/A", justify=tk.LEFT)
        self.blue_LEDs.grid(row=2, column=0, padx=10, pady=0)

        self.yellow_LEDs = ttk.Label(data_values_frame, text="Yellow: N/A", justify=tk.LEFT)
        self.yellow_LEDs.grid(row=3, column=0, padx=10, pady=0)

        self.white_LEDs = ttk.Label(data_values_frame, text="White: N/A", justify=tk.LEFT)
        self.white_LEDs.grid(row=4, column=0, padx=10, pady=0)

        self.total_LEDs = ttk.Label(data_values_frame, text="Total: N/A", justify=tk.LEFT)
        self.total_LEDs.grid(row=5, column=0, padx=10, pady=0)

        self.average_brightness = ttk.Label(data_values_frame, text="Average Brightness: N/A", justify=tk.LEFT)
        self.average_brightness.grid(row=6, column=0, padx=10, pady=0)

        
    def update_telemetry(self, telemetry_data):
        self.telemetry_text.delete(1.0, tk.END)
        self.telemetry_text.insert(tk.END, telemetry_data)

    def update_image(self, image_path):
        try:
            image = Image.open(image_path)
            image.thumbnail((200, 200))  # Resize the image to fit the label
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference to avoid garbage collection
        except Exception as e:
            print("Error displaying image:", str(e))

    def update_data(self, position, yaw, leg, illumination):
        self.position_label.config(text="Position: {}".format(position))
        self.yaw_label.config(text="Yaw: {}".format(yaw))
        self.leg_label.config(text="Leg: {}".format(leg))
        self.illumination_label.config(text="Illumination Status: {}".format(illumination))

    def update_LED_data(self, data):
        self.red_LEDs.config(text="Red: {}".format(data["red"]))
        self.green_LEDs.config(text="Green: {}".format(data["green"]))
        self.blue_LEDs.config(text="Blue: {}".format(data["blue"]))
        self.yellow_LEDs.config(text="Yellow: {}".format(data["yellow"]))
        self.white_LEDs.config(text="White: {}".format(data["white"]))
        self.total_LEDs.config(text="Total: {}".format(data["total"]))
        self.average_brightness.config(text="Average Brightness: {}".format(data["average_brightness"]))
    
    def update_image_timestamps(self, timestamp):
        if self.past_images_listbox.size() == 10:
            self.past_images_listbox.delete(tk.END)
        self.past_images_listbox.insert(tk.TOP, timestamp)

if __name__ == "__main__":
    root = tk.Tk()
    app = CubeSatGroundStation(root)
    root.mainloop()
