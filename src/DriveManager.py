from subprocess import run
from json import loads


class DriveManager:
    """
    A class that manages the drives on the system. It can mount and unmount drives
    """

    def __init__(self):
        """
        initializes the DriveManager class. It mounts all drives that are currently un mounted to the mounts folder.
        """

        self.mounted_drives = []
        self.mount_drives()

    def mount_drives(self):
        """
        mounts all drives that are currently un mounted to the mounts folder. 
        Each drive is mounted to a folder with the same name as the drive. 
        For example, if the drive is /dev/sda1, it will be mounted to mounts/sda1.
        """

        # gets all un mounted drives
        drives = loads(run(["lsblk", "-J", "-o", "NAME,MOUNTPOINT,TYPE"], capture_output=True, text=True).stdout)
        for blockdevice in drives.get("blockdevices", []):
            for child in blockdevice.get("children", []):
                if child.get("mountpoint") == None:

                    # creates folders for each drive and mounts them to the folders
                    run(["sudo", "mkdir", "-p", f"mounts/{child.get('name')}"])
                    run(["sudo", "mount", f"/dev/{child.get('name')}", f"mounts/{child.get('name')}"])
                    self.mounted_drives.append(f"mounts/{child.get('name')}")

    def unmount_drives(self):
        """
        unmounts all drives that are currently mounted to the mounts folder. 
        """

        for drive in self.mounted_drives:
            run(["sudo", "umount", drive])
            run(["sudo", "rm", "-rf", drive])
        self.mounted_drives = []

    def unmount_drive(self, drive):
        """
        unmounts a specific drive that is currently mounted to the mounts folder. 

        :param drive: the drive to unmount. It should be in the format of "mounts/sda1" where sda1 is the name of the drive.
        """

        if drive in self.mounted_drives:
            run(["sudo", "umount", drive])
            run(["sudo", "rm", "-rf", drive])
            self.mounted_drives.remove(drive)
