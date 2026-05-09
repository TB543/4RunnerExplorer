from customtkinter import CTkScrollableFrame, CTkFrame, CTkLabel, ThemeManager
from pathlib import Path


class FileExplorer(CTkScrollableFrame):
    """
    a class to represent a file explorer widget
    """

    def __init__(self, master, drive_manager, inspector):
        """
        initialize file explorer widget

        :param master: master widget
        :param drive_manager: drive manager instance
        :param inspector: file inspector widget
        """

        super(FileExplorer, self).__init__(master)
        self.expanded_paths = set()
        self.selected = None
        self.drive_manager = drive_manager
        self.inspector = inspector
        CTkLabel(self, text="File Explorer", font=("Arial", 20, "bold")).pack()
        self.draw()

    def draw_item(self, frame, path, item_type):
        """
        draws a single element to the screen

        :param frame: master widget to draw to
        :param path: the path of the item
        :param item_type: the emoji to represent the type of element (drive, folder or file)
        """

        # creates widgets
        frame = CTkFrame(frame, fg_color=self.cget("fg_color"))
        state = CTkLabel(frame, text="⯈", font=("Arial", 15))
        name = CTkLabel(frame, text=f" {item_type}{path.drive if path.name == '' else path.name}", font=("Arial", 15))

        # binds functionality
        state.bind("<Button-1>", lambda e: self.expand_volume(path, frame, state))
        name.bind("<Button-1>", lambda e: self.select_item(frame, path, item_type == "💾"))

        # places widgets
        if item_type != "📄": state.pack(side="left", anchor="n")
        name.pack(anchor="w")
        frame.pack(fill="x", expand=True, padx=5, ipady=2)
        if path in self.expanded_paths: self.expand_volume(path, frame, state)

    def draw(self):
        """
        draws all the folders/files in the file explorer widget
        """

        # removes old widgets
        for widget in self.winfo_children():
            widget.destroy()

        # draws new file system
        for drive in self.drive_manager.mounted_drives:
            self.draw_item(self, Path(drive).resolve(), "💾")

    def select_item(self, frame, path, drive):
        """
        handles when the user selects an item

        :param frame: widget to highlight when selected
        :param path: the path of the item
        :param drive: determines if the item is a drive or not
        """

        if self.selected: self.selected.configure(fg_color=self.cget("fg_color"))
        self.selected = frame
        frame.configure(fg_color=ThemeManager.theme["CTkFrame"]["top_fg_color"])
        self.inspector.select_item(path, drive)

    def expand_volume(self, volume, frame, label):
        """
        opens a volume and displays all the files and folders in it

        :param volume: volume to expand
        :param frame: frame used to display the volume
        :param label: label used to display the volume state (⯈ or ⯆)
        """

        # expands the volume
        self.expanded_paths.add(volume)
        expanded = CTkFrame(frame, fg_color=self.cget("fg_color"))
        expanded.pack(side="left", fill="x", expand=True)
        label.configure(text="⯆")
        label.unbind("<Button-1>")
        label.bind("<Button-1>", lambda e: self.collapse_volume(volume, frame, label, expanded))
        for item in sorted(volume.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):

            # handles when folders are found
            if item.is_dir():
                self.draw_item(expanded, item, "📂")

            # handles when files are found
            elif item.is_file():
                self.draw_item(expanded, item, "📄")

    def collapse_volume(self, volume, frame, label, expanded):
        """
        collapses all the files and folders in a volume

        :param volume: volume to collapse
        :param frame: frame used to display the volume
        :param label: label used to display the volume state (⯈ or ⯆)
        :param expanded: the frame containing the expanded volume
        """

        self.expanded_paths.remove(volume)
        expanded.destroy()
        label.configure(text="⯈")
        label.unbind("<Button-1>")
        label.bind("<Button-1>", lambda e: self.expand_volume(volume, frame, label))
