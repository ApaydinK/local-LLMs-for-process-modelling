# argilla.io
# no yapping!
# few shot prompts
# simulation
# from Generate import generate_describe_and_store_one_process_model
import Generate
import customtkinter
import os
import FileHandling
from FileHandling import retrieve_file_path
import asyncio
import threading
import dotenv
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import ctypes
from dotenv import load_dotenv
from FileHandling import update_dotenv

load_dotenv()

ctypes.windll.shcore.SetProcessDpiAwareness(2)

total_number_of_processes = int(os.environ.get("NUMBER_OF_PROCESS_MODELS"))

last_nav_button = None


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('Process trees with descriptions')
        # self.iconbitmap('images/codemy.ico')
        self.geometry("1200x750")  # Adjusted size for better visibility
        self.configure(fg_color="white")
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

        for process_id in range(total_number_of_processes):
            nav_button = customtkinter.CTkButton(self.nav_rows_frame, text=f"process {process_id}", anchor="center",
                                                 font=("Maitree", 20), width=60, height=25)
            nav_button.configure(
                command=lambda btn=nav_button,
                               p_id=process_id: self.activate_nav_item_and_display_graph_and_description(btn,
                                                                                                         p_id))  # Pass the button object to the lambda
            nav_button.grid(row=process_id, column=0, sticky="nsew", pady=5)

        global last_nav_button
        last_nav_button = nav_button

        self.add_generate_another_example_button(row=total_number_of_processes)

    def add_generate_another_example_button(self, row):
        self.generate_another_example_button = customtkinter.CTkButton(self.nav_rows_frame, text=f"+ Generate",
                                                                  anchor="center",
                                                                  font=("Maitree", 20), width=60, height=25,
                                                                  command=self.generate)
        self.generate_another_example_button.grid(row=row, column=0, sticky="nsew", pady=5)

    def activate_nav_item_and_display_graph_and_description(self, button, process_id):
        self.change_color(button)
        if hasattr(self, 'info_frame') and self.info_frame.winfo_exists():
            self.info_frame.destroy()

        self.info_frame = MyInfoView(self, process_id=process_id)
        self.info_frame.grid(row=0, column=1, pady=10, sticky="nsew")
        self.info_frame.grid_rowconfigure(1, weight=1)

    def change_color(self, button):  # button
        global last_nav_button
        last_nav_button.configure(fg_color=["#3a7ebf", "#1f538d"])
        button.configure(fg_color="blue")
        last_nav_button = button



    def generate(self):

        #TODO Display Loading
        #TODO Stop Freezing
        #TODO Display Progress Update Messages
        #TODO implement guidance e.g. accept Process Tree, next, cancel,
        #TODO accept label suggestion, regenerate, replace specific labels
        #TODO generate description,
        #self.change_color(button)
        if hasattr(self, 'info_frame') and self.info_frame.winfo_exists():
            self.info_frame.destroy()

        self.label_progress_updates = customtkinter.CTkLabel(self, text="Generation started", font=("Geogia", 20, 'bold'))
        self.label_progress_updates.grid(row=0, column=1, pady=10, sticky="nsew")

        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(Generate.generate_describe_and_store_one_process_model(self.updateProgressLabel))

        run_llm_thread = threading.Thread(target=Generate.generate_describe_and_store_one_process_model, args=(self.updateProgressLabel, self.generation_finished))
        run_llm_thread.start()

    def generation_finished(self):

        self.label_progress_updates.destroy()

        self.generate_another_example_button.destroy()
        load_dotenv(override=True)
        total_number_of_processes = int(os.environ.get("NUMBER_OF_PROCESS_MODELS"))
        nav_button = customtkinter.CTkButton(self.nav_rows_frame, text=f"process {total_number_of_processes}", anchor="center",
                                             font=("Maitree", 20), width=60, height=25)
        nav_button.configure(
            command=lambda btn=nav_button,
                           p_id=total_number_of_processes: self.activate_nav_item_and_display_graph_and_description(btn,
                                                                                                     p_id))  # Pass the button object to the lambda
        nav_button.grid(row=total_number_of_processes, column=0, sticky="nsew", pady=5)

        self.add_generate_another_example_button(total_number_of_processes + 1)

        update_dotenv("NUMBER_OF_PROCESS_MODELS", total_number_of_processes + 1)
        load_dotenv(override=True)
        # os.environ.get("NUMBER_OF_PROCESS_MODELS")

    def updateProgressLabel(self, update_text):
        self.label_progress_updates.configure(text=update_text)

    def process_selected(self, selected_value):
        process_id = int(selected_value.split()[-1])
        self.activate_nav_item_and_display_graph_and_description(self.choose_process, process_id)



class MyInfoView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        # Extract 'item_id' from kwargs and assign a default if not provided
        self.process_id = kwargs.pop('process_id', None)  # Use None or another appropriate default

        super().__init__(master, **kwargs)

        self.configure(bg_color="white", fg_color="white")
        self.process_tree_image_path = retrieve_file_path("bpmn", self.process_id)
        self.image = Image.open(self.process_tree_image_path)
        self.process_tree_image = customtkinter.CTkImage(light_image=self.image, size=self.image.size)
        self.process_tree_image_label = customtkinter.CTkLabel(self, text="Business Process Flow",
                                                               image=self.process_tree_image, anchor="center",
                                                               compound="bottom",
                                                               bg_color="white", fg_color="white", padx=10, pady=10,
                                                               font=("Geogia", 20, 'bold'))
        self.process_tree_image_label.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.process_tree_description_path = retrieve_file_path("process_tree_description", self.process_id)
        with open(self.process_tree_description_path, "r") as file:
            process_description = file.read()
        # self.process_tree_description = customtkinter.CTkLabel(self, text="Process Description", image=self.process_tree_image, anchor="center", compound="top",
        #                                       bg_color="white", fg_color="white", padx= 0, pady=10,
        #                                       font=("Geogia", 20, 'bold'))
        # self.process_tree_description.grid(row=0, column=0, sticky="ew")

        self.textbox_process_description = customtkinter.CTkTextbox(self,
                                                                    width=self.winfo_width(),
                                                                    height=1000,
                                                                    # self.winfo_height(),  # Adjust the height as needed
                                                                    wrap="word")
        self.textbox_process_description.insert("1.0", process_description)
        self.textbox_process_description.grid(row=1, column=0, padx=10, columnspan=3, sticky="ew")

        # Set the font size (and optionally the font family)
        font = ("Helvetica", 18)  # Example: "Helvetica" font with size 14
        self.textbox_process_description.configure(font=font)

        self.save_button = customtkinter.CTkButton(self, text="Save updated description", font=font,
                                                   command=self.save_text)
        self.save_button.grid(row=2, column=0, columnspan=2, padx=10, sticky="ew")

        self.change_visualization_dropdown = customtkinter.CTkOptionMenu(self,
                                                                         values=["bpmn", "process_tree", "petri_net"],
                                                                         command=self.optionmenu_callback, font=font)
        self.change_visualization_dropdown.grid(row=2, column=2, padx=10, sticky="ew")
        self.change_visualization_dropdown.set("bpmn")  # set initial value
        self.bind("<Configure>", self.on_resize)

    def optionmenu_callback(self, choice):
        self.process_tree_image_path = retrieve_file_path(choice, self.process_id)
        self.on_resize(None)
        print("optionmenu dropdown clicked:", choice)

    def save_text(self):
        updated_text = self.textbox_process_description.get("1.0", "end-1c")
        with open(self.process_tree_description_path, "w") as file:
            file.write(updated_text)

    def on_resize(self, event):
        # Get the size of the parent frame

        self.image = Image.open(self.process_tree_image_path)

        new_width = self.winfo_width() - 20  # Subtract padding
        new_height = self.winfo_height() - 20  # Subtract padding

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        if self.winfo_screenwidth() > 3000:
            screen_normalization = 0.5  # 0.66
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
        # resized_image = resized_image.filter(ImageFilter.SMOOTH)

        # Enhance the image sharpness
        # enhancer = ImageEnhance.Sharpness(resized_image)
        # resized_image = enhancer.enhance(2.0)  # Increase sharpness (adjust factor as needed)

        self.process_tree_image = customtkinter.CTkImage(light_image=resized_image, size=(new_width, new_height))

        self.process_tree_image = customtkinter.CTkImage(light_image=resized_image, size=(new_width, new_height))

        # Update the label with the resized image
        self.process_tree_image_label.configure(image=self.process_tree_image)


def count_files(directory):
    # Count the number of files in the given directory.
    total_files = 0
    for entry in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, entry)):
            total_files += 1
    return total_files


if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    app = GUI()
    # windll.shcore.SetProcessDpiAwareness(2)
    customtkinter.set_appearance_mode("light")
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    app.mainloop()
