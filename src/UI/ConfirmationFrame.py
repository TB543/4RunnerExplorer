from customtkinter import CTkFrame, CTkLabel, CTkButton, StringVar


class ConfirmationFrame(CTkFrame):
    """
    a class to represent a confirmation frame
    """

    def __init__(self, master):
        """
        initialize the frame

        :param master: the parent widget
        """

        super(ConfirmationFrame, self).__init__(master, border_width=2)
        self.title = StringVar(self, "Confirmation")
        self.description = StringVar(self, "Description")
        self.yes_command = None
        CTkLabel(self, textvariable=self.title, font=("Arial", 20, "bold")).pack(side="top", pady=10)
        CTkLabel(self, textvariable=self.description, font=("Arial", 15)).pack(expand=True)
        CTkButton(self, text="Yes", font=("Arial", 15), command=self.command).pack(side="left", fill="x", expand=True, pady=10, padx=10)
        CTkButton(self, text="No", font=("Arial", 15), command=self.place_forget).pack(side="left", fill="x", expand=True, pady=10, padx=10)

    def ask(self, title, description, command):
        """
        places the confirmation frame to the screen

        :param title: the title of the confirmation frame
        :param description: the description of the confirmation frame
        :param command: the command to execute if the user hits yes
        """

        self.title.set(title)
        self.description.set(description)
        self.yes_command = command
        self.place(relx=.5, rely=.5, relwidth=.75, relheight=.75, anchor="center")

    def command(self):
        """
        handles when the user presses the yes button
        """

        self.yes_command()
        self.place_forget()
