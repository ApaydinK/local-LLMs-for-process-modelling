#from tkinter import filedialog
import customtkinter
import os
from dotenv import load_dotenv
import threading
import dotenv
from PIL import Image

load_dotenv()  # This loads the variables from .env
# TODO put into shared Resources Class TODO save as dotenv

total_number_of_processes = 18

last_nav_button = None
folder = "pm4py_generated_models_and_descriptions"

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('Process trees with descriptions')
        # self.iconbitmap('images/codemy.ico')
        self.geometry("1200x750")  # Adjusted size for better visibility

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.nav_rows_frame = customtkinter.CTkScrollableFrame(self)
        self.nav_rows_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.nav_rows_frame.grid_columnconfigure(0, weight=1)
        self.nav_rows_frame.grid_rowconfigure(0, weight=1)
        self.add_all_process_nav_ids()

    def add_all_process_nav_ids(self):

        for process_id in range(total_number_of_processes):
            nav_button = customtkinter.CTkButton(self.nav_rows_frame, text=f"process {process_id}", anchor="center",
                                                 font=("Maitree", 20), width=100, height=30)
            nav_button.configure(
                command=lambda btn=nav_button, p_id=process_id: self.activate_nav_item_and_display_graph_and_description(btn,p_id))  # Pass the button object to the lambda
            nav_button.grid(row=process_id, column=0, sticky="nsew", pady=5)

        global last_nav_button
        last_nav_button = nav_button


    def activate_nav_item_and_display_graph_and_description(self, button, process_id):
        self.change_color(button)
        self.info_frame = MyInfoView(self, process_id=process_id)
        self.info_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")


    def change_color(self, button):
        global last_nav_button
        last_nav_button.configure(fg_color=["#3a7ebf", "#1f538d"])
        button.configure(fg_color="blue")
        last_nav_button = button


def retrieve_file_path(kind, id):
    match kind:
        case "process_tree":
            return f"../{folder}/{id}_process_tree.png"
        case "bpmn":
            return f"../{folder}/{id}_bpmn.png"
        case "petri_net":
            return f"../{folder}/{id}_petri_net.png"
        case "process_tree_description":
            return f"../{folder}/{id}_process_tree_description.txt"
        case "petri_net_description":
            return f"../{folder}/{id}_petri_net_description.txt"
        case _:
            return "error"


class MyInfoView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        # Extract 'item_id' from kwargs and assign a default if not provided
        process_id = kwargs.pop('process_id', None)  # Use None or another appropriate default

        super().__init__(master, **kwargs)
        # create widgets
        self.configure(bg_color="white", fg_color="white")
        self.process_tree_image_path = retrieve_file_path("bpmn", process_id)
        image = Image.open(self.process_tree_image_path)
        self.process_tree_image = customtkinter.CTkImage(light_image=image, size=image.size)
        self.my_label = customtkinter.CTkLabel(self, text="", image=self.process_tree_image, anchor="n", compound="center",
                                               bg_color="white", fg_color="white")
        self.my_label.grid(row=0, column=0, padx=20, sticky="ew")

        process_tree_description_path = retrieve_file_path("process_tree_description", process_id)
        with open(process_tree_description_path, "r") as file:
            process_description = file.read()


        self.label_process_description = customtkinter.CTkLabel(self,
                                                                text=process_description,
                                                                anchor="w",
                                                                compound="left",
                                                                bg_color="white",
                                                                fg_color="white",
                                                                wraplength= self.winfo_width(),
                                                                font=("Maitree", 18)
                                                                )
        self.label_process_description.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        # Bind the update function to the <Configure> event of the frame
        self.bind("<Configure>", self.update_wraplength)
        self.label_process_description.configure(anchor="w")  # Re-emphasize text alignment

    def update_wraplength(self, event):
        # Set the wraplength to the current width of the frame
        new_width = self.winfo_width()
        self.label_process_description.configure(wraplength=new_width - 100)  # Subtract some padding if necessary
        self.label_process_description.configure(anchor="w")  # Re-emphasize text alignment

def count_files(directory):
    #Count the number of files in the given directory.
    total_files = 0
    for entry in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, entry)):
            total_files += 1
    return total_files


def update_dotenv(key, new_value):
    # Read the current contents of the .env file
    if not os.path.isfile('.env'):
        with open('.env', 'w'): pass

    with open('.env', 'r') as file:
        lines = [line.strip() for line in file]

    # Check if the key already exists in the file
    key_exists = False
    with open('.env', 'w') as file:
        for line in lines:
            if line.startswith(f"{key}="):
                file.write(f"{key}={new_value}\n")
                key_exists = True
            else:
                file.write(line + '\n')

        # If the key does not exist in the file, add it
        if not key_exists:
            file.write(f"{key}={new_value}\n")



if __name__ == "__main__":
    #customtkinter.set_appearance_mode("light")
    app = GUI()
    app.mainloop()
