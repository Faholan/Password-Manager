"""Password manager interface."""
import json
import tkinter as tk
from tkinter import font
import typing as t
from os import path

from .base import characters, core


class Interface:
    """Implementation of the interface."""

    def __init__(self) -> None:
        """Initialize self."""
        # Main window
        self.main = tk.Tk()
        self.main.title("Password manager")
        self.main.bind("<Button-3>", self.popup)
        self.main.protocol("WM_DELETE_WINDOW", self.on_close)

        # Configuration
        curconf = self.load_config()
        basefont = font.Font(self.main, "Helvetica", "16")
        self._togrid: t.List[t.Tuple[tk.Widget, t.Dict[str, t.Any]]] = []
        self.charselected: t.List[tk.BooleanVar] = []

        # Menus
        self.menu = tk.Menu(self.main, tearoff=0)
        self.password_menu = tk.Menu(self.menu, tearoff=0)
        self.copy_menu = tk.Menu(self.menu, tearoff=0)

        # All fields
        password_indicator = tk.Label(text="Password:", font=basefont)
        password_indicator.bind("<Button-3>", self.popup)
        self.password_input = tk.Entry(font=basefont)

        length_indicator = tk.Label(text="Length:", font=basefont)
        length_indicator.bind("<Button-3>", self.popup)
        self.length_input = tk.Entry(font=basefont)

        curlength = str(curconf.get("passlength", "10"))

        self.length_input.insert(
            0,
            curlength if self.validate_length(curlength) else "10",
        )  # type: ignore
        self.length_input.bind("<Button-3>", self.popup)

        vcmd = (self.main.register(self.validate_length), "%P")
        self.length_input.config(validate="key", validatecommand=vcmd)

        gen_button = tk.Button(text="Generate", command=self.passgen)
        gen_button.bind("<Button-3>", self.popup)

        # Gridding
        password_indicator.grid(column=0, row=0)
        length_indicator.grid(column=0, row=1)
        self.password_input.grid(column=1, row=0)
        self.length_input.grid(column=1, row=1)
        gen_button.grid(column=2, row=0, rowspan=2)

        self.init_menu(curconf)
        self.main.config(menu=self.menu)
        self.main.resizable(False, False)
        self.main.mainloop()

    def on_close(self) -> None:
        """Save config on window closing."""
        self.save_config()
        self.main.destroy()

    @staticmethod
    def load_config() -> t.Dict[t.Any, t.Any]:
        """Load the configuration."""
        _base = path.split(__file__)[0]
        try:
            with open(
                path.join(_base, "data", "config.json"),
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    return {}
                return data  # type: ignore
        except (FileNotFoundError, ValueError):
            return {}

    def save_config(self) -> None:
        """Save the current configuration."""
        _base = path.split(__file__)[0]

        data = {
            "charselected": tuple(
                characters.ALL[i].name
                for i, var in enumerate(self.charselected)
                if var.get()
            ),
            "passlength": self.length_input.get(),  # type: ignore
        }

        try:
            with open(
                path.join(_base, "data", "config.json"),
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(data, file)
        except ValueError:
            pass

    @staticmethod
    def validate_length(value: str) -> bool:
        """Validate integer input for the password length."""
        return value == "" or value.isdigit() and int(value) > 0

    def popup(self, event: t.Any) -> None:
        """Popup the configuration menu."""
        self.password_menu.post(event.x_root, event.y_root)  # type: ignore

    def to_clipboard(self) -> None:
        """Copy current password to clipboard."""
        self.main.clipboard_clear()
        self.main.clipboard_append(  # type: ignore
            self.password_input.get(),  # type: ignore
        )

    def check_all(self) -> None:
        """Check all boxes."""
        maxindex = self.password_menu.index(tk.END)  # type: ignore
        if maxindex is None:
            return
        for i in range(maxindex + 1):
            if self.password_menu.type(i) == "checkbutton":  # type: ignore
                lab = self.password_menu.entrycget(i, "label")  # type: ignore
                if lab in characters.REV_ALL:
                    if not self.charselected[characters.REV_ALL[lab]].get():
                        self.password_menu.invoke(i)  # type: ignore

    def check_none(self) -> None:
        """Uncheck all boxes."""
        maxindex = self.password_menu.index(tk.END)  # type: ignore
        if maxindex is None:
            return
        for i in range(maxindex + 1):
            if self.password_menu.type(i) == "checkbutton":  # type: ignore
                lab = self.password_menu.entrycget(i, "label")  # type: ignore
                if lab in characters.REV_ALL:
                    if self.charselected[characters.REV_ALL[lab]].get():
                        self.password_menu.invoke(i)  # type: ignore

    def init_menu(self, curconf: t.Dict[t.Any, t.Any]) -> None:
        """Initialize the menu used for Password generation."""
        self.password_menu.add_command(
            label="Copy password",
            command=self.to_clipboard,
        )
        self.password_menu.add_separator()

        for charrange in characters.ALL:
            rawconf = curconf.get("charselected")
            if isinstance(rawconf, tuple):
                conf: t.Tuple[t.Any, ...] = rawconf
            else:
                conf = ()
            self.charselected.append(
                tk.BooleanVar(value=charrange.name in conf),
            )
            self.password_menu.add_checkbutton(
                label=charrange.name,
                onvalue=True,
                offvalue=False,
                variable=self.charselected[-1],
            )

        self.password_menu.add_command(label="All", command=self.check_all)
        self.password_menu.add_command(label="None", command=self.check_none)
        self.menu.add_cascade(menu=self.password_menu, label="Password")

    def passgen(self) -> None:
        """Generate a password."""
        if self.length_input.get() == "":  # type: ignore
            return
        chars = characters.BASE
        for i, charrange in enumerate(characters.ALL):
            if self.charselected[i].get():
                chars |= charrange

        self.password_input.delete(0, tk.END)
        self.password_input.insert(
            0,
            core.gen_password(
                chars,
                int(self.length_input.get()),  # type: ignore
            ),
        )
