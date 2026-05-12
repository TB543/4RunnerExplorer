from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, set_default_color_theme, set_widget_scaling
from Managers.DriveManager import DriveManager
from UI.FileExplorer import FileExplorer
from UI.FileInspector import FileInspector
from UI.ConfirmationFrame import ConfirmationFrame


class MainMenu(CTk):
    """
    the main menu of the application
    """

    set_default_color_theme("green")
    set_widget_scaling(1.375)

    def __init__(self):
        """
        initialize the main menu of the application
        draw all the elements to the screen
        """

        super(MainMenu, self).__init__()
        self.drive_manager = DriveManager()
        self.geometry("1024x600+0+0")
        # self.configure(cursor="none") todo
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # creates title frame
        title = CTkFrame(self)
        title.columnconfigure(0, weight=1)
        title.columnconfigure(1, weight=0)
        title.columnconfigure(2, weight=1)
        CTkLabel(title, text="4RunnerExplorer", font=("Arial", 25, "bold")).grid(row=0, column=1, padx=10, pady=10)
        CTkButton(title, text="↻", width=12, font=("Arial", 20), command=self.refresh_drives).grid(row=0, column=2, sticky="w", padx=10, pady=10)
        CTkButton(title, text="X", width=12, font=("Arial", 20), command=self.destroy).grid(row=0, column=2, sticky="e", padx=10, pady=10)
        title.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # places file management tool widgets
        confirmation = ConfirmationFrame(self)
        inspector = FileInspector(self, self.drive_manager, confirmation)
        self.explorer = FileExplorer(self, self.drive_manager, inspector)
        self.explorer.grid(row=1, column=0, sticky="nsew")
        confirmation.lift()
        inspector.grid(row=1, column=1, sticky="nsew")

    def refresh_drives(self):
        """
        mounts all un mounted drives and refreshes the display
        """

        self.drive_manager.mount_drives()
        self.explorer.draw()

    def destroy(self):
        """
        overrides the destroy function to also unmount all files
        """

        self.drive_manager.unmount_drives()
        super(MainMenu, self).destroy()
