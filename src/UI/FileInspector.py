from customtkinter import CTkFrame, CTkLabel, CTkButton, StringVar
from datetime import datetime
from shutil import disk_usage
from subprocess import run


class FileInspector(CTkFrame):
    """
    a class to represent a file explorer widget
    """

    # maps file types to open commands, key is the file extension, value is the command to open the file taking the path as a parameter
    OPEN_COMMANDS = {
        ".mp3": lambda path: run(["echo", "mp3", path]),
        ".mov": lambda path: run(["echo", "mov", path]),
        ".txt": lambda path: run(["notepad", path]),
    }

    def __init__(self, master, drive_manager, confirmation):
        """
        initialize file explorer widget

        :param master: master widget
        :param drive_manager: reference to the drive manager
        :param confirmation: reference to the confirmation frame
        """

        # creates fields
        super(FileInspector, self).__init__(master, border_width=2)
        self.drive_manager = drive_manager
        self.confirmation = confirmation
        self.explorer = None  # will be set by file explorer
        self.path = None
        self.pack_propagate(False)
        self.name = StringVar(self, "Name:")
        self.size = StringVar(self, "Size:")
        self.created_at = StringVar(self, "Created At:")

        # places labels
        CTkLabel(self, text="File Inspector", font=("Arial", 20, "bold")).pack()
        CTkLabel(self, textvariable=self.name, font=("Arial", 15)).pack(anchor="w", padx=20, pady=10)
        CTkLabel(self, textvariable=self.size, font=("Arial", 15)).pack(anchor="w", padx=20, pady=10)
        CTkLabel(self, textvariable=self.created_at, font=("Arial", 15)).pack(anchor="w", padx=20, pady=10)

        # creates buttons
        self.unmount_button = CTkButton(self, text="Eject", command=self.unmount)
        self.open_button = CTkButton(self, text="Open", command=self.open)
        self.copy_button = CTkButton(self, text="Copy", command=self.copy)
        self.delete_button = CTkButton(self, text="Delete", command=self.delete)

        # sets up drag and drop for copy command
        self.dragging = False
        self.drag_text = CTkLabel(self.winfo_toplevel(), font=("Arial", 15), bg_color=self.cget("fg_color"))
        self.winfo_toplevel().bind("<B1-Motion>", self.drag)
        self.winfo_toplevel().bind("<ButtonRelease-1>", self.end_drag)

    @staticmethod
    def get_size(path, drive):
        """
        gets the size of an item in the file system

        :param path: the path to the file object
        :param drive: determines if the item is a drive

        :return: the size of the file object on the disk formated in human-readable format
        """

        # gets the size of the file system
        if drive:
            size = disk_usage(path).total
        else:
            size = path.stat().st_size if path.is_file() else 0
            size += sum(f.stat().st_size for f in path.rglob("*") if f.is_file())

        # generates a string a readable format
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

    def select_item(self, path, drive):
        """
        handles when the user selects a file

        :param path: the path of the selected item
        :param drive: determines if the selected item is a drive
        """

        # sets metadata values
        self.path = path
        self.name.set(f"Name: {path.name}")
        self.size.set(f"Size: {FileInspector.get_size(path, drive)}")
        self.created_at.set(f"Created At: {datetime.fromtimestamp(path.stat().st_ctime).strftime("%b %d, %Y %I:%M%p")}")

        # removes old action buttons
        self.unmount_button.pack_forget()
        self.open_button.pack_forget()
        self.copy_button.pack_forget()
        self.delete_button.pack_forget()

        # places action buttons for drives
        if drive:
            self.name.set(f"Name: {path.drive}")
            self.unmount_button.pack(side="bottom", fill="x", pady=10, padx=10)

        # places action buttons for paths
        elif path.is_file():
            self.delete_button.pack(side="bottom", fill="x", pady=10, padx=10)
            self.copy_button.pack(side="bottom", fill="x", pady=10, padx=10)
            self.open_button.pack(side="bottom", fill="x", pady=10, padx=10)

        # places action buttons for folders
        elif path.is_dir():
            self.delete_button.pack(side="bottom", fill="x", pady=10, padx=10)
            self.copy_button.pack(side="bottom", fill="x", pady=10, padx=10)

    def unmount(self):
        """
        handles when the user unmounts a drive
        """

        self.confirmation.ask("Eject Disk?", self.path.drive, lambda: print("eject"))

    def open(self):
        """
        handles when the user opens a file
        """

        self.winfo_toplevel().withdraw()
        FileInspector.OPEN_COMMANDS[self.path.suffix.lower()](self.path)
        self.winfo_toplevel().deiconify()

    def copy(self):
        """
        handles when the user copies a file/folder
        """

        self.dragging = self.explorer.selected
        self.drag_text.configure(text=self.path.name)
        self.drag_text.lift()

    def delete(self):
        """
        handles when the user deletes a file/folder
        """

        # gets the title of the confirmation popup
        title = None
        if self.path.is_file():
            title = "Delete File?"
        elif self.path.is_dir():
            title = "Delete Folder?"

        # creates confirmation popup
        self.confirmation.ask(title, self.path.name, lambda: print("deleted"))

    def drag(self, event):
        """
        handles when the user drags a file/folder

        :param event: the drag event
        """

        # does nothing if not in a drag event
        if not self.dragging:
            return

        # highlights folder hovered over and places label at mouse position
        self.explorer.highlight_volume(event)
        x = (event.x_root - self.winfo_toplevel().winfo_rootx()) / 1.375 # divide by widget scaling set in main menu
        y = (event.y_root - self.winfo_toplevel().winfo_rooty()) / 1.375
        self.drag_text.place(x=x, y=y, anchor="center")

    def end_drag(self, event):
        """
        handles when the user stops dragging a file/folder

        :param event: the end drag event
        """

        # does nothing if not in a drag event
        if not self.dragging:
            return

        # checks if drag was ended over the selected folder
        x1 = self.explorer.selected.winfo_rootx()
        y1 = self.explorer.selected.winfo_rooty()
        x2 = x1 + self.explorer.selected.winfo_width()
        y2 = y1 + self.explorer.selected.winfo_height()
        if x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2:
            print(self.explorer.selected.path)  # todo copy command here

        # ends the drag event
        self.explorer.select_item(self.dragging)
        self.dragging = False
        self.drag_text.place_forget()
