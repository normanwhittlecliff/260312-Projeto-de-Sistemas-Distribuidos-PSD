from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import tkinter as tk

def showMessage(message, title="Message"):
    messagebox.showinfo(title, message)

def showError(message, title="Error"):
    messagebox.showerror(title, message)

def showInput(message, title="Enter"):
    return simpledialog.askstring(title, message)

def showConfirm(message, title="Confirm"):
    return messagebox.askyesno(title, message)

"""
FILE TIPES

[("Text Files", "*.txt"), ("All Files", "*.*")]
"""
def openFile(title="Select File", fileTypes=[("All Files", "*.*")], initialPath=""):
    return filedialog.askopenfilename(
        initialdir=initialPath,
        title=title,
        filetypes=fileTypes)


def showSelectOptions(options, title="Select", message="Select an option:"):
    """
    Shows a dialog that lets the user choose
    P1, P2, P3, P4, or P5.

    Returns:
        str -> "P1", "P2", "P3", "P4", or "P5"
        None -> if the window is closed
    """

    root = tk.Tk()
    root.withdraw()  # Hide root window

    result = None

    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.geometry(f"400x{150 + len(options) * 30}")
    dialog.resizable(False, True)

    selected = tk.StringVar(value=options[0])

    tk.Label(
        dialog,
        text=message
    ).pack(pady=14)

    for option in options:
        tk.Radiobutton(
            dialog,
            text=option,
            variable=selected,
            value=option
        ).pack(anchor="w", padx=(20))

    def confirm():
        nonlocal result
        result = selected.get()
        dialog.destroy()

    tk.Button(
        dialog,
        text="OK",
        command=confirm
    ).pack(pady=(10))

    dialog.grab_set()      # Makes the dialog modal
    dialog.wait_window()   # Wait until closed

    return result


# ==========
# FUNCTIONS FOR 1

def createvariationselector(parent):

    selected = tk.StringVar()

    selected.set("P1")

    menu = tk.OptionMenu(
        parent,
        selected,
        "P1",
        "P2",
        "P3",
        "P4",
        "P5"
    )

    menu.pack()

    return selected
