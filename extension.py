""" CS 5001 -Yijia Zhan - Project 10 extension
This defines the ConfigUI class, which creates a
GUI for entering and saving configuration parameters
for the woods simulation.
"""
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkbox
from extension1 import WoodConfig
import jsonpickle


class ConfigUI:
    """Creates GUI for entering and saving
    configuration parameters for the woods simulation
    """
    def __init__(self):
        """
        Initializes a new instance of the ConfigUI class.
        """
        self.root = tk.Tk()
        self.root.title("Woods Configuration")

        # Initialize enjoy_var
        self.enjoy_var = tk.BooleanVar()
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and organizes the GUI widgets.
        """
        my_frame = ttk.Frame(self.root, padding=10)
        my_frame.grid()

        self.tree_min_string = tk.StringVar()
        self.tree_max_string = tk.StringVar()
        self.baby_min_string = tk.StringVar()
        self.baby_max_string = tk.StringVar()
        self.bird_min_string = tk.StringVar()
        self.bird_max_string = tk.StringVar()
        self.move_interval_string = tk.StringVar()

        tkbox.showinfo("Input Ranges", "Please enter the following values:\n"
                       "Number of Trees: 6-10\n"
                       "Number of babies: 2-5\n"
                       "Number of bird Min: 3-6\n"
                       "Your desired move_interval: 1-10\n"
                       "Please enter valid integers\n")

        ttk.Label(my_frame, text="Minimum number of trees:").grid(row=0,
                                                                  column=0)
        ttk.Label(my_frame, text="Maximum number of trees:").grid(row=1,
                                                                  column=0)
        ttk.Label(my_frame, text="Minimum number of babies:").grid(row=2,
                                                                   column=0)
        ttk.Label(my_frame, text="Maximum number of babies:").grid(row=3,
                                                                   column=0)
        ttk.Label(my_frame, text="Minimum number of birds:").grid(row=4,
                                                                  column=0)
        ttk.Label(my_frame, text="Maximum number of birds:").grid(row=5,
                                                                  column=0)
        ttk.Label(my_frame, text="Move_interval:").grid(row=6, column=0)

        self.min_num_trees_entry = tk.Entry(my_frame,
                                            textvariable=self.tree_min_string)
        self.max_num_trees_entry = tk.Entry(my_frame,
                                            textvariable=self.tree_max_string)
        self.min_num_babies_entry = tk.Entry(my_frame,
                                             textvariable=self.baby_min_string)
        self.max_num_babies_entry = tk.Entry(my_frame,
                                             textvariable=self.baby_max_string)
        self.min_num_birds_entry = tk.Entry(my_frame,
                                            textvariable=self.bird_min_string)
        self.max_num_birds_entry = tk.Entry(my_frame,
                                            textvariable=self.bird_max_string)
        self.move_interval_entry = tk.Entry(
            my_frame,
            textvariable=self.move_interval_string)

        self.min_num_trees_entry.grid(row=0, column=1)
        self.max_num_trees_entry.grid(row=1, column=1)
        self.min_num_babies_entry.grid(row=2, column=1)
        self.max_num_babies_entry.grid(row=3, column=1)
        self.min_num_birds_entry.grid(row=4, column=1)
        self.max_num_birds_entry.grid(row=5, column=1)
        self.move_interval_entry.grid(row=6, column=1)

        ttk.Button(my_frame, text="Save", command=self.on_start).grid(
            row=7,
            column=0,
            columnspan=2)

        # Create a checkbutton to check whether user enjoy the wood simulation
        ttk.Checkbutton(my_frame, text="Did you enjoy the woods simulation?",
                        variable=self.enjoy_var).grid(row=8, column=0,
                                                      columnspan=2)

    def on_start(self):
        """
        Event handler for the "Save" button click.
        """
        try:
            tree_min = str_to_int(self.tree_min_string.get())
            tree_max = str_to_int(self.tree_max_string.get())
            baby_min = str_to_int(self.baby_min_string.get())
            baby_max = str_to_int(self.baby_max_string.get())
            bird_min = str_to_int(self.bird_min_string.get())
            bird_max = str_to_int(self.bird_max_string.get())
            move_interval = str_to_int(self.move_interval_string.get())

            self.validate_ranges(tree_min, tree_max, baby_min, baby_max,
                                 bird_min, bird_max, move_interval)

            # Get the state of the enjoy checkbox
            enjoy = self.enjoy_var.get()

            config = WoodConfig(tree_min=tree_min, tree_max=tree_max,
                                baby_min=baby_min, baby_max=baby_max,
                                bird_min=bird_min, bird_max=bird_max,
                                move_interval=move_interval)

            with open('woodconfig.json', 'w') as config_file:
                config_json = jsonpickle.encode(config)
                config_file.write(config_json)
                print("File Made")

            # Give feedback based on user choices
            if enjoy:
                print("Hope to see you next time!")
            else:
                print("Sorry to hear that. We'll try to improve.")

                self.root.destroy()
        except ValueError as e:
            tkbox.showerror("Error", f"Invalid input: {str(e)}")

    def validate_ranges(self, tree_min, tree_max, baby_min, baby_max,
                        bird_min, bird_max, move_interval):
        """
        Validates the input ranges for trees, babies, birds,
        and move intervals.

        Raises ValueError if any of the input ranges is invalid.

        Args:
            - tree_min (int): Minimum number of trees.
            - tree_max (int): Maximum number of trees.
            - baby_min (int): Minimum number of babies.
            - baby_max (int): Maximum number of babies.
            - bird_min (int): Minimum number of birds.
            - bird_max (int): Maximum number of birds.
            - move_interval (int): Desired move interval.

        Raises:
            ValueError:  If any of the input ranges is invalid.
            Provides a descriptive message about the specific
            invalid range encountered.
        """
        if not (6 <= tree_min <= tree_max <= 10):
            raise ValueError("Invalid range for trees.\
Must be between 6 and 10.")
        if not (2 <= baby_min <= baby_max <= 5):
            raise ValueError("Invalid range for babies.\
Must be between 2 and 5.")
        if not (3 <= bird_min <= bird_max <= 6):
            raise ValueError("Invalid range for birds.\
 Must be between 3 and 6.")
        if not (1 <= move_interval <= 10):
            raise ValueError("Invalid range for move_interval.\
Must be between 1 and 10.")

    def run(self):
        """
        Enters the Tkinter main loop to run the GUI.
        """
        self.root.mainloop()


def str_to_int(entry):
    """
    Converts a string entry to an integer.

    Args:
        - entry (str): Entry in Tkinter fields.

    Returns:
        - int: Integer conversion of entry.
    """
    return int(entry)


if __name__ == "__main__":
    config_ui = ConfigUI()
    config_ui.run()
