from customtkinter import CTkFrame, CTkLabel, CTkButton, StringVar
from datetime import datetime
from shutil import disk_usage


class FileInspector(CTkFrame):
    """
    a class to represent a file explorer widget
    """

    def __init__(self, master):
        """
        initialize file explorer widget
        """

        # creates fields
        super(FileInspector, self).__init__(master, border_width=2)
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
        self.unmount = CTkButton(self, text="Eject")
        self.open = CTkButton(self, text="Open")
        self.copy = CTkButton(self, text="Copy")
        self.delete = CTkButton(self, text="Delete")

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
        self.unmount.pack_forget()
        self.open.pack_forget()
        self.copy.pack_forget()
        self.delete.pack_forget()

        # places action buttons for drives
        if drive:
            self.name.set(f"Name: {path.drive}")
            self.unmount.pack(side="bottom", fill="x", pady=10, padx=10)

        # places action buttons for paths
        elif path.is_file():
            self.delete.pack(side="bottom", fill="x", pady=10, padx=10)
            self.copy.pack(side="bottom", fill="x", pady=10, padx=10)
            self.open.pack(side="bottom", fill="x", pady=10, padx=10)

        # places action buttons for folders
        elif path.is_dir():
            self.delete.pack(side="bottom", fill="x", pady=10, padx=10)
            self.copy.pack(side="bottom", fill="x", pady=10, padx=10)
