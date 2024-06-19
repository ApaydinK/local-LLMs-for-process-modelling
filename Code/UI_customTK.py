#argilla.io
#no yapping!
#few shot prompts
#simulation

#from tkinter import filedialog
import customtkinter
import os
from dotenv import load_dotenv
import threading
import dotenv
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

total_number_of_processes = 100

last_nav_button = None
folder = "pm4py_generated_models_and_descriptions"
current_path= os.path.dirname(os.path.abspath(__file__))
print(current_path)
folder_path = os.path.join(os.path.dirname(current_path), folder)
print(folder_path)

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('Process trees with descriptions')
        # self.iconbitmap('images/codemy.ico')
        self.geometry("1200x750")  # Adjusted size for better visibility

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(1, weight=1)

        self.nav_rows_frame = customtkinter.CTkScrollableFrame(self)
        self.nav_rows_frame.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")
        self.nav_rows_frame.grid_columnconfigure(0, weight=1)
        self.nav_rows_frame.grid_rowconfigure(0, weight=1)

        """
        self.display_frame = customtkinter.CTkFrame(self)
        self.display_frame.grid(row=0, column=1, padx = 5, pady=5, sticky='nsew')
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)
        
        self.selected_process = {} # will trace the processes
        """
        self.add_all_process_nav_ids()

    def add_all_process_nav_ids(self):

        process_ids = [f"Process {i}" for i in range(total_number_of_processes)]
        for process_id in range(total_number_of_processes):
            nav_button = customtkinter.CTkButton(self.nav_rows_frame, text=f"process {process_id}", anchor="center",
                                                 font=("Maitree", 20), width=60, height=25)
            nav_button.configure(
                command=lambda btn=nav_button, p_id=process_id: self.activate_nav_item_and_display_graph_and_description(btn,p_id))  # Pass the button object to the lambda
            nav_button.grid(row=process_id, column=0, sticky="nsew", pady=5)

        global last_nav_button
        last_nav_button = nav_button


    def activate_nav_item_and_display_graph_and_description(self, button, process_id):
        self.change_color(button)
        if hasattr(self, 'info_frame') and self.info_frame.winfo_exists():
            self.info_frame.destroy()
        
        self.info_frame = MyInfoView(self, process_id=process_id)
        self.info_frame.grid(row=0, column=1, pady=10, sticky="nsew")
        self.info_frame.grid_rowconfigure(1, weight=1)



    def change_color(self, button): # button
        global last_nav_button
        last_nav_button.configure(fg_color=["#3a7ebf", "#1f538d"])
        button.configure(fg_color="blue")
        last_nav_button = button


    def process_selected(self, selected_value):
        process_id = int(selected_value.split()[-1])
        self.activate_nav_item_and_display_graph_and_description(self.choose_process, process_id)


def retrieve_file_path(kind, id):
    match kind:
        case "process_tree":
            return f"{folder_path}/{id}_process_tree.png"
        case "bpmn":
            return f"{folder_path}/{id}_bpmn.png"
        case "petri_net":
            return f"{folder_path}/{id}_petri_net.png"
        case "process_tree_description":
            return f"{folder_path}/{id}_process_tree_description.txt"
        case "petri_net_description":
            return f"{folder_path}/{id}_petri_net_description.txt"
        case _:
            return "error"


class MyInfoView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        # Extract 'item_id' from kwargs and assign a default if not provided
        process_id = kwargs.pop('process_id', None)  # Use None or another appropriate default

        super().__init__(master, **kwargs)

        self.configure(bg_color="white", fg_color="white")
        self.process_tree_image_path = retrieve_file_path("bpmn", process_id)
        self.image = Image.open(self.process_tree_image_path)
        self.process_tree_image = customtkinter.CTkImage(light_image=self.image, size=self.image.size) 
        self.process_tree_image_label = customtkinter.CTkLabel(self, text="Business Process Flow", image=self.process_tree_image, anchor="center", compound="bottom",
                                               bg_color="white", fg_color="white", padx= 0, pady=10,
                                               font=("Geogia", 20, 'bold'))
        self.process_tree_image_label.grid(row=0, column=0, sticky="ew")

        self.process_tree_description_path = retrieve_file_path("process_tree_description", process_id)
        with open(self.process_tree_description_path, "r") as file:
            process_description = file.read()
        #self.process_tree_description = customtkinter.CTkLabel(self, text="Process Description", image=self.process_tree_image, anchor="center", compound="top",
        #                                       bg_color="white", fg_color="white", padx= 0, pady=10,
        #                                       font=("Geogia", 20, 'bold'))
        #self.process_tree_description.grid(row=0, column=0, sticky="ew")

        self.textbox_process_description = customtkinter.CTkTextbox(self,
                                                          width=self.winfo_width(),
                                                          height=1000,#self.winfo_height(),  # Adjust the height as needed
                                                          wrap="word")
        self.textbox_process_description.insert("1.0", process_description)
        self.textbox_process_description.grid(row=1, column=0, sticky="ew")

        # Set the font size (and optionally the font family)
        font = ("Helvetica", 18)  # Example: "Helvetica" font with size 14
        self.textbox_process_description.configure(font=font)

        self.save_button = customtkinter.CTkButton(self, text="Save updated description", font=font, command=self.save_text)
        self.save_button.grid(row=2, column=0, sticky="ew")

        self.bind("<Configure>", self.on_resize)

    def save_text(self):
        updated_text = self.textbox_process_description.get("1.0", "end-1c")
        with open(self.process_tree_description_path, "w") as file:
            file.write(updated_text)

    def on_resize(self, event):
        # Get the size of the parent frame

        self.image = Image.open(self.process_tree_image_path)

        new_width = self.winfo_width() - 40  # Subtract padding
        new_height = self.winfo_height() - 40  # Subtract padding

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        if self.winfo_screenwidth() > 3000:
            screen_normalization = 0.5
            new_width = int(new_width * screen_normalization)
            new_height = int(new_width * screen_normalization)

        # Preserve aspect ratio
        aspect_ratio = self.image.width / self.image.height
        if new_width / new_height > aspect_ratio:
            new_width = int(new_height * aspect_ratio)
        else:
            new_height = int((new_width / aspect_ratio))

        # Resize the image using high-quality resizing algorithm
        resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)

        # Apply anti-aliasing filter
        #resized_image = resized_image.filter(ImageFilter.SMOOTH)

        # Enhance the image sharpness
        #enhancer = ImageEnhance.Sharpness(resized_image)
        #resized_image = enhancer.enhance(2.0)  # Increase sharpness (adjust factor as needed)

        self.process_tree_image = customtkinter.CTkImage(light_image=resized_image, size=(new_width, new_height))

        self.process_tree_image = customtkinter.CTkImage(light_image=resized_image, size=(new_width, new_height))

        # Update the label with the resized image
        self.process_tree_image_label.configure(image=self.process_tree_image)


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
