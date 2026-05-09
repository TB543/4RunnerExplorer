from customtkinter import CTkFrame, CTkLabel


class FileInspector(CTkFrame):
    """
    a class to represent a file explorer widget
    """

    def __init__(self, master):
        """
        initialize file explorer widget
        """

        super(FileInspector, self).__init__(master)
        CTkLabel(self, text="File Inspector", font=("Arial", 20, "bold")).pack()

    def select_item(self, path, drive):
        """
        handles when the user selects a file

        :param path: the path of the selected item
        :param drive: determines if the selected item is a drive
        """

        if drive:
            print("drive")

        elif path.is_dir():
            print("dir")

        # handles when files are found
        elif path.is_file():
            print("file")
