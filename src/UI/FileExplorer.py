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

        super(FileExplorer, self).__init__(master, border_width=2)
        self.expanded_paths = set()
        self.selected = None
        self.after_expand = self.after(0, lambda: None)
        self.drive_manager = drive_manager
        self.inspector = inspector
        self.inspector.explorer = self
        self.draw()

    def draw_item(self, frame, path, item_type):
        """
        draws a single element to the screen

        :param frame: master widget to draw to
        :param path: the path of the item
        :param item_type: the emoji to represent the type of element (drive, folder or file)
        """

        # creates widgets
        item = CTkFrame(frame, fg_color=self.cget("fg_color"))
        item.path = path
        item.type = item_type
        state = CTkLabel(item, text="▶", font=("Arial", 15))
        name = CTkLabel(item, text=f" {item_type}{path.drive if path.name == '' else path.name}", font=("Arial", 15))

        # binds functionality
        state.bind("<Button-1>", lambda e: self.expand_volume(item))
        name.bind("<Button-1>", lambda e: self.select_item(item))

        # adds metadata for volumes
        if item_type != "📄":
            item.state = state
            state.pack(side="left", anchor="n")

        # places widgets
        name.pack(anchor="w")
        item.pack(fill="x", expand=True, padx=5, ipady=2)
        if path in self.expanded_paths: self.expand_volume(item)

    def draw(self):
        """
        draws all the folders/files in the file explorer widget
        """

        # removes old widgets
        for widget in self.winfo_children():
            widget.destroy()

        # draws new file system
        CTkLabel(self, text="File Explorer", font=("Arial", 20, "bold")).pack()
        for drive in self.drive_manager.mounted_drives:
            self.draw_item(self, Path(drive).resolve(), "💾")

    def select_item(self, item):
        """
        handles when the user selects an item

        :param item: widget to highlight when selected
        """

        if self.selected: self.selected.configure(fg_color=self.cget("fg_color"))
        self.selected = item
        self.selected.configure(fg_color=ThemeManager.theme["CTkFrame"]["top_fg_color"])
        self.inspector.select_item(item.path, item.type == "💾")

    def expand_volume(self, volume):
        """
        opens a volume and displays all the files and folders in it

        :param volume: volume to expand
        """

        # expands the volume
        self.expanded_paths.add(volume.path)
        expanded = CTkFrame(volume, fg_color=self.cget("fg_color"))
        expanded.pack(side="left", fill="x", expand=True)
        volume.state.configure(text="▼")
        volume.state.unbind("<Button-1>")
        volume.state.bind("<Button-1>", lambda e: self.collapse_volume(volume, expanded))
        for item in sorted(volume.path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):

            # handles when folders are found
            if item.is_dir():
                self.draw_item(expanded, item, "📂")

            # handles when files are found
            elif item.is_file():
                self.draw_item(expanded, item, "📄")

    def collapse_volume(self, volume, expanded):
        """
        collapses all the files and folders in a volume

        :param volume: volume to collapse
        :param expanded: the frame containing the expanded volume
        """

        self.expanded_paths.remove(volume.path)
        expanded.destroy()
        volume.state.configure(text="▶")
        volume.state.unbind("<Button-1>")
        volume.state.bind("<Button-1>", lambda e: self.expand_volume(volume))

    def highlight_volume(self, event):
        """
        highlights the folder at the given mouse position

        :param event: the mouse event
        """

        def check_pos(widget):
            """
            recursively checks each widget's bbox to find which the mouse is hovering over

            :param widget: the widget to check

            :return: the "deepest" widget that mouse is hovering over, or None if mouse is not over any widgets
            """

            # gets bbox
            x1 = widget.winfo_rootx()
            y1 = widget.winfo_rooty()
            x2 = x1 + widget.winfo_width()
            y2 = y1 + widget.winfo_height()

            # recursively checks children if this widget is hovered over
            if x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2:
                for child in widget.winfo_children():
                    if result := check_pos(child):
                        return result
                return widget
            return None

        # gets the highest hovered frame for a volume
        hover = check_pos(self)
        while not (hover is None or hasattr(hover, "state")):
            hover = hover.master

        # highlights the volume frame that is hovered over
        if hover and hover != self.selected:
            if self.selected: self.selected.configure(fg_color=self.cget("fg_color"))
            self.selected = hover
            self.selected.configure(fg_color=ThemeManager.theme["CTkFrame"]["top_fg_color"])
            self.after_cancel(self.after_expand)
            self.after_expand = self.after(1000, lambda: self.expand_volume(hover) if hover.path not in self.expanded_paths else None)
