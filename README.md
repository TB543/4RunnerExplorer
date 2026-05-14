# 4RunnerExplorer

A lightweight touchscreen-friendly file explorer built for the 4RunnerDash ecosystem.

4RunnerExplorer automatically mounts connected drives, displays their file structure in a simple GUI, and provides quick access to common file operations such as opening, copying, deleting, and ejecting removable storage.

---

## Features

* Automatic mounting of removable drives
* Expandable file tree explorer
* File and folder inspection panel
* Open supported media files directly from the UI
* Copy and delete file operations
* Drive eject/unmount support
* Simple fullscreen-friendly layout designed for automotive use
* Built with Python and CustomTkinter

---

## Requirements

### System Requirements

* Linux-based operating system
* Python 3.10+
* `sudo` access for mounting/unmounting drives
* `lsblk` utility installed
* VLC media player installed (optional, for video playback)

### Python Dependencies

Dependencies are listed in:

```text
resources/requirements.txt
```

Current dependencies:

```text
customtkinter==5.2.2
darkdetect==0.8.0
packaging==26.2
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/4RunnerExplorer.git
cd 4RunnerExplorer
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r resources/requirements.txt
```

### 4. Run the Application

```bash
python src/main.py
```

---

## How It Works

### Drive Detection

`DriveManager` uses:

```bash
lsblk -J -o NAME,MOUNTPOINT,TYPE
```

to detect available block devices.

Unmounted drives are automatically mounted into:

```text
mounts/<drive_name>
```

Example:

```text
mounts/sda1
```

---

## User Interface

### File Explorer

The left panel displays:

* Connected drives
* Folders
* Files

Folders can be expanded and collapsed dynamically.

### File Inspector

The right panel displays metadata for the selected item:

* Name
* Size
* Creation date

Available actions depend on the selected item:

| Item Type | Actions            |
| --------- | ------------------ |
| Drive     | Eject              |
| Folder    | Copy, Delete       |
| File      | Open, Copy, Delete |

---

## Supported File Types

Currently supported media playback:

| Extension | Application |
| --------- | ----------- |
| `.mp4`    | VLC         |
| `.mov`    | VLC         |

Additional file handlers can be added in:

```python
FileInspector.OPEN_COMMANDS
```

Example:

```python
OPEN_COMMANDS = {
    ".mp3": lambda path: run(["vlc", path]),
    ".png": lambda path: run(["feh", path])
}
```

---

## License

This project is licensed under the terms of the included LICENSE file.

---

## Author

Created for the 4RunnerDash project ecosystem.
