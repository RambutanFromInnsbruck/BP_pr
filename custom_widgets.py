import tkinter as tk
from tkinter import ttk


class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            CustomNotebook.__initialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""
        element = self.identify(event.x, event.y)
        if "close" in element:
            index = self.index(f"@{event.x},{event.y}")
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']) or self._active is None:
            self.state(["!pressed"])
            self._active = None
            return

        # Close the tab regardless of cursor position
        self.forget(self._active)
        self.event_generate("<<NotebookTabClosed>>")
        self.state(["!pressed"])
        self._active = None

    def _draw_x_on_image(self, img, color):
        """Draw a thick X shape on a PhotoImage with the specified color"""

        start = 4

        for i in range(7):
            # First diagonal (top-left to bottom-right) - main line
            img.put(color, to=(start + i, start + i, start + i + 1, start + i + 1))
            # First diagonal - thickness (parallel lines)
            img.put(color, to=(start + i + 1, start + i, start + i + 2, start + i + 1))
            # Second diagonal (top-right to bottom-left) - main line
            img.put(color, to=(start + 7 - i, start + i, start + 8 - i, start + i + 1))
            # Second diagonal - thickness (parallel lines)
            img.put(color, to=(start + 6 - i, start + i, start + 7 - i, start + i + 1))

    def _create_close_button_images(self):
        """Create close button images programmatically"""
        size = 16

        # Create the three states with different colors
        img_close = tk.PhotoImage("img_close", width=size, height=size)
        self._draw_x_on_image(img_close, "#666666")  # Normal state - gray

        img_closeactive = tk.PhotoImage("img_closeactive", width=size, height=size)
        self._draw_x_on_image(img_closeactive, "#A19D37")  # Active state - yellow

        img_closepressed = tk.PhotoImage("img_closepressed", width=size, height=size)
        self._draw_x_on_image(img_closepressed, "#FF0000")  # Pressed state - red

        return (img_close, img_closeactive, img_closepressed)

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = self._create_close_button_images()

        style.element_create("close", "image", "img_close",
                             ("active", "pressed", "!disabled", "img_closepressed"),
                             ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.close", {"side": "right", "sticky": ''}),
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])


class AutocompleteEntry(tk.Entry):
    """
    Subclass of Tkinter.Entry that features autocompletion.

    To enable autocompletion use set_completion_list(list) to define
    a list of possible strings to hit.
    To cycle through hits use down and up arrow keys.
    """

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
        """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):  # Match case-insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position = self.position - 1  # delete one character
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        if event.keysym == "Down":
            self.autocomplete(1)  # cycle to next hit
        if event.keysym == "Up":
            self.autocomplete(-1)  # cycle to previous hit
        if len(event.keysym) == 1:
            self.autocomplete()


class ToggleButton(ttk.Frame):
    """New ttk ToggleButton class"""
    def __init__(self, parent, width=50, height=30, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.width = width
        self.height = height
        self.state = False

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            highlightthickness=0,
            relief='flat',
            bg=self["style"] if "style" in kwargs else '#f0f0f0'
        )
        self.canvas.pack()

        self.padding = 3
        self.radius = (height - 2 * self.padding) // 2
        self.track_height = height - 2 * self.padding
        self.slider_pos = self.padding + self.radius

        self.on_color = "#d92b18"
        self.off_color = "#2e39d9"
        self.slider_color = "#ffffff"

        self.draw_track()
        self.draw_slider()

        self.canvas.bind("<Button-1>", self.toggle)
        self.bind("<Button-1>", self.toggle)

    def draw_track(self):
        self.canvas.delete("track")
        self.bg_color = self.on_color if self.state else self.off_color

        track_x1 = self.padding
        track_y1 = (self.height - self.track_height) / 2
        track_x2 = self.width - self.padding
        track_y2 = track_y1 + self.track_height

        self.canvas.create_arc(
            track_x1,
            track_y1,
            track_x1 + self.track_height,
            track_y2,
            start=90,
            extent=180,
            fill=self.bg_color,
            outline=self.bg_color,
            width=1,
            tags="track"
        )
        self.canvas.create_arc(
            track_x2 - self.track_height,
            track_y1,
            track_x2,
            track_y2,
            start=270,
            extent=180,
            fill=self.bg_color,
            outline=self.bg_color,
            width=1,
            tags="track"
        )
        self.canvas.create_rectangle(
            track_x1 + self.track_height / 2,
            track_y1,
            track_x2 - self.track_height / 2,
            track_y2,
            fill=self.bg_color,
            outline=self.bg_color,
            width=1,
            tags="track"
        )

    def draw_slider(self):
        self.canvas.delete("slider")
        self.canvas.create_oval(
            self.slider_pos - self.radius,
            self.padding,
            self.slider_pos + self.radius,
            self.height - self.padding,
            fill=self.slider_color,
            outline=self.slider_color,
            width=1,
            tags="slider"
        )

    def toggle(self, event=None):
        """Switching state with animation"""
        self.state = not self.state

        if self.state:
            new_pos = self.width - self.padding - self.radius
        else:
            new_pos = self.padding + self.radius

        self.draw_track()
        self.animate_slider(self.slider_pos, new_pos)
        self.slider_pos = new_pos

        if hasattr(self, "command"):
            self.command()

    def animate_slider(self, start, end):
        steps = 15
        step_size = (end - start) / steps

        def move(step):
            nonlocal start
            if (step_size > 0 and start < end) or (step_size < 0 and start > end):
                start += step_size
                self.slider_pos = start
                self.draw_slider()
                self.after(20, move, step + 1)

        move(1)

    def set_command(self, command):
        """Setting up a callback function"""
        self.command = command

    def get_state(self):
        """Returns the current state"""
        return self.state
