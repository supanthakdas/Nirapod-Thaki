import tkinter as tk
from tkinter import simpledialog, messagebox

import nirapod_thaki_backend as backend

user_info          = backend.user_info
emergency_contacts = backend.emergency_contacts
comfort_zones      = backend.comfort_zones
nearest_facilities = backend.nearest_facilities
live_location      = backend.live_location

# =====================================================================
# THEME
# =====================================================================

BG_DARK    = "#D5D5DD"
BG_PANEL   = "#CEC6C6"
BG_CARD    = "#DFDBEA"

ACCENT     = "#723DED"
ACCENT_DIM = "#5F21CC"

DANGER     = "#B45E5E"
DANGER_DIM = "#B92323"

TEXT_PRI   = "#242228"
TEXT_SEC   = "#626169"

BORDER     = "#E5E1F0"
SEPARATOR  = "#D8D3E8"
# =====================================================================
# ROUNDED BUTTON  (Canvas-based, the only way in pure tkinter)
# =====================================================================

def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    """Draw a rounded rectangle on a canvas."""
    pts = [
        x1+r, y1,   x2-r, y1,
        x2,   y1,   x2,   y1+r,
        x2,   y2-r, x2,   y2,
        x2-r, y2,   x1+r, y2,
        x1,   y2,   x1,   y2-r,
        x1,   y1+r, x1,   y1,
        x1+r, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kwargs)


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command,
                 bg_color=None, hover_color=None, fg_color=None,
                 radius=10, font=("Helvetica", 11, "bold"),
                 height=44, icon="", **kwargs):

        bg_color    = bg_color    or BG_PANEL
        hover_color = hover_color or BORDER
        fg_color    = fg_color    or TEXT_PRI

        # Canvas background must match the parent background so the
        # rounded corners look correct (no rectangular outline shows).
        super().__init__(parent,
                         height=height,
                         bg=parent["bg"],          # transparent border zone
                         highlightthickness=0,
                         bd=0,
                         cursor="hand2",
                         **kwargs)

        self._bg      = bg_color
        self._hover   = hover_color
        self._fg      = fg_color
        self._radius  = radius
        self._cmd     = command
        self._font    = font
        self._text    = (icon + "  " + text) if icon else text
        self._rect    = None
        self._label   = None

        self.bind("<Configure>",  self._draw)
        self.bind("<Enter>",      self._on_enter)
        self.bind("<Leave>",      self._on_leave)
        self.bind("<Button-1>",   self._on_click)

    def _draw(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 2 or h < 2:
            return
        r = self._radius
        self._rect = rounded_rect(self, 0, 0, w, h, r, fill=self._bg,
                                  outline="")
        self._label = self.create_text(
            14, h // 2,
            text=self._text,
            font=self._font,
            fill=self._fg,
            anchor="w"
        )

    def _set_bg(self, color):
        self._bg = color
        if self._rect:
            self.itemconfig(self._rect, fill=color)

    def _on_enter(self, _):
        self._set_bg(self._hover)

    def _on_leave(self, _):
        self._set_bg(self._bg if self._bg != self._hover else
                     (DANGER if "e63946" in self._hover else BG_PANEL))
        # Restore the stored original bg directly
        self.itemconfig(self._rect, fill=self._orig_bg)

    def _on_click(self, _):
        if self._cmd:
            self._cmd()

    def pack(self, **kw):
        # Capture the true original bg before first pack
        self._orig_bg = self._bg
        super().pack(**kw)

    def grid(self, **kw):
        self._orig_bg = self._bg
        super().grid(**kw)


def make_rounded_btn(parent, text, command,
                     is_sos=False, is_sub=False, icon="›"):
    """
    Factory that creates and packs a RoundedButton into parent.
    """
    if is_sos:
        bg, hover, fg = DANGER, DANGER_DIM, "white"
        font = ("Helvetica", 11, "bold")
        h = 46
    elif is_sub:
        bg, hover, fg = BG_CARD, BORDER, TEXT_SEC
        font = ("Helvetica", 9, "normal")
        h = 38
        icon = ""
    else:
        bg, hover, fg = BG_PANEL, BORDER, TEXT_PRI
        font = ("Helvetica", 11, "bold")
        h = 46

    btn = RoundedButton(
        parent, text=text, command=command,
        bg_color=bg, hover_color=hover, fg_color=fg,
        font=font, height=h, icon=icon, radius=10
    )
    # Fix _on_leave by storing orig_bg at creation time
    btn._orig_bg = bg
    btn.pack(fill=tk.X, pady=(0, 7))
    return btn


# =====================================================================
# POPUP FACTORY
# =====================================================================

def make_popup(title, width=480, height=440):
    popup = tk.Toplevel(app_window)
    popup.title("")
    popup.configure(bg=BG_CARD)
    popup.resizable(False, False)
    #popup.grab_set()

    app_window.update_idletasks()
    x = app_window.winfo_x() + (app_window.winfo_width()  - width)  // 2
    y = app_window.winfo_y() + (app_window.winfo_height() - height) // 2
    popup.geometry(f"{width}x{height}+{x}+{y}")

    popup.wait_visibility()
    popup.grab_set()

    # Top accent stripe
    tk.Frame(popup, bg=ACCENT, height=3).pack(fill=tk.X)

    # Title bar
    title_bar = tk.Frame(popup, bg=BG_CARD, pady=14)
    title_bar.pack(fill=tk.X, padx=24)
    tk.Label(title_bar, text=title, font=("Georgia", 13, "bold"),
             bg=BG_CARD, fg=TEXT_PRI).pack(side=tk.LEFT)

    tk.Frame(popup, bg=SEPARATOR, height=1).pack(fill=tk.X)

    # Scrollable body
    wrapper = tk.Frame(popup, bg=BG_CARD)
    wrapper.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(wrapper, bg=BG_CARD, highlightthickness=0, bd=0)
    vbar   = tk.Scrollbar(wrapper, orient=tk.VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=vbar.set)
    vbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    body = tk.Frame(canvas, bg=BG_CARD)
    body_id = canvas.create_window((0, 0), window=body, anchor="nw")

    def _on_canvas_resize(event):
        canvas.itemconfig(body_id, width=event.width)

    def _on_body_resize(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", _on_canvas_resize)
    body.bind("<Configure>",   _on_body_resize)

    def _on_mousewheel(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
        else:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>",   _on_mousewheel)
    canvas.bind_all("<Button-5>",   _on_mousewheel)

    def _on_close():
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", _on_close)

    # Close bar
    tk.Frame(popup, bg=SEPARATOR, height=1).pack(fill=tk.X)
    close_bar = tk.Frame(popup, bg=BG_PANEL, pady=8)
    close_bar.pack(fill=tk.X)
    close_btn = tk.Button(
        close_bar, text="Close", command=_on_close,
        font=("Helvetica", 10), bg=BG_PANEL, fg=TEXT_SEC,
        relief=tk.FLAT, bd=0, padx=20, pady=5, cursor="hand2",
        activebackground=BORDER, activeforeground=TEXT_PRI
    )
    close_btn.pack(side=tk.RIGHT, padx=16)

    return popup, body


# =====================================================================
# REUSABLE WIDGET HELPERS
# =====================================================================

def add_section_title(parent, text):
    tk.Frame(parent, bg=SEPARATOR, height=1).pack(fill=tk.X, pady=(12, 0))
    tk.Label(parent, text=text.upper(),
             font=("Helvetica", 8, "bold"),
             bg=BG_CARD, fg=ACCENT, anchor="w",
             padx=24).pack(fill=tk.X, pady=(4, 0))


def add_label_row(parent, label, value,
                  label_color=TEXT_SEC, value_color=TEXT_PRI,
                  row_bg=BG_CARD):
    row = tk.Frame(parent, bg=row_bg, pady=4)
    row.pack(fill=tk.X, padx=24)
    tk.Label(row, text=label, font=("Helvetica", 10),
             bg=row_bg, fg=label_color,
             width=16, anchor="w").pack(side=tk.LEFT)
    tk.Label(row, text=value, font=("Helvetica", 10, "bold"),
             bg=row_bg, fg=value_color,
             anchor="w", wraplength=260,
             justify=tk.LEFT).pack(side=tk.LEFT, padx=(6, 0))


def add_facility_row(parent, name, distance):
    row = tk.Frame(parent, bg=BG_PANEL, pady=6, padx=14)
    row.pack(fill=tk.X, pady=2, padx=24)
    tk.Label(row, text=name, font=("Helvetica", 10),
             bg=BG_PANEL, fg=TEXT_PRI, anchor="w").pack(side=tk.LEFT)
    tk.Label(row, text=distance, font=("Helvetica", 9),
             bg=BG_PANEL, fg=ACCENT, anchor="e").pack(side=tk.RIGHT)


# =====================================================================
# POPUP SCREENS
# =====================================================================

def popup_view_data():
    popup, body = make_popup("User Profile & Contacts", width=480, height=500)

    add_section_title(body, "Personal Information")
    for key, value in user_info.items():
        add_label_row(body, key, value)

    add_section_title(body, "Emergency Contacts")
    for relation, number in emergency_contacts.items():
        add_label_row(body, relation, number, value_color=ACCENT)

    add_section_title(body, "Comfort Zones")
    for zone in comfort_zones:
        add_label_row(body, zone["name"], zone["distance"],
                      label_color=TEXT_PRI, value_color=TEXT_SEC)

    tk.Frame(body, bg=BG_CARD, height=10).pack()


def popup_edit_profile():
    popup, body = make_popup("Edit User Data", width=460, height=360)

    def btn_action(action):
        popup.destroy()
        action()

    def _edit_field():
        field = simpledialog.askstring(
            "Edit Profile",
            "Which field to edit?\n\nOptions:  Name  |  Blood Type  |  Allergies",
            parent=app_window
        )
        if not field:
            return
        field = field.strip().title()
        if field in user_info:
            new_val = simpledialog.askstring(
                "Edit Profile", f"New value for '{field}':",
                parent=app_window
            )
            if new_val:
                user_info[field] = new_val.strip()
                _confirm(f"'{field}' updated to '{new_val.strip()}'.")
        else:
            messagebox.showerror(
                "Not Found",
                f"'{field}' is not a recognised field.\n\n"
                "Please type one of:  Name  |  Blood Type  |  Allergies",
                parent=app_window
            )

    def _edit_contact():
        relation = simpledialog.askstring(
            "Edit / Add Contact",
            "Enter relation name\n(e.g. Father, Sister, Uncle):",
            parent=app_window
        )
        if not relation:
            return
        number = simpledialog.askstring(
            "Edit / Add Contact", f"Enter phone number for '{relation}':",
            parent=app_window
        )
        if number:
            emergency_contacts[relation.strip()] = number.strip()
            _confirm(f"Contact '{relation.strip()}' saved.")

    def _add_zone():
        zone = simpledialog.askstring(
            "Add Comfort Zone", "Enter the new comfort zone location:",
            parent=app_window
        )
        if zone:
            comfort_zones.append({
                "name": zone.strip(),
                "distance": backend.get_static_dist()
            })
            _confirm(f"Comfort zone '{zone.strip()}' added.")

    def _confirm(msg):
        win, b = make_popup("Done", width=340, height=160)
        tk.Label(b, text="✓", font=("Helvetica", 26),
                 bg=BG_CARD, fg=ACCENT).pack(pady=(8, 2))
        tk.Label(b, text=msg, font=("Helvetica", 10),
                 bg=BG_CARD, fg=TEXT_PRI, wraplength=280).pack()

    tk.Frame(body, bg=BG_CARD, height=8).pack()

    for label, action in [
        ("Edit Profile Field  (Name / Blood Type / Allergies)", _edit_field),
        ("Edit or Add Emergency Contact",                       _edit_contact),
        ("Add New Comfort Zone",                                _add_zone),
    ]:
        make_rounded_btn(body, label, lambda a=action: btn_action(a),
                         icon="›")

    tk.Frame(body, bg=BG_CARD, height=10).pack()


def popup_nearest_facilities():
    popup, body = make_popup("Nearest Facilities", width=500, height=520)

    pill = tk.Frame(body, bg=ACCENT, padx=12, pady=5)
    pill.pack(anchor="w", padx=24, pady=(8, 4))
    tk.Label(pill, text=f"  Live Location:  {live_location}  ",
             font=("Helvetica", 9, "bold"),
             bg=ACCENT, fg=BG_DARK).pack()

    ICONS = {
        "First Aid Zones":    "＋",
        "Hospitals":          "H",
        "Police Station":     "P",
        "Fire Service":       "F",
        "Emergency Helplines":"#"
    }

    for category, places in nearest_facilities.items():
        icon = ICONS.get(category, "•")
        tk.Frame(body, bg=SEPARATOR, height=1).pack(fill=tk.X, padx=24,
                                                     pady=(10, 2))
        tk.Label(body, text=f"  {icon}  {category.upper()}",
                 font=("Helvetica", 8, "bold"),
                 bg=BG_CARD, fg=ACCENT, anchor="w",
                 padx=24).pack(fill=tk.X)
        for place in places:
            add_facility_row(body, place["name"], place["distance"])

    tk.Frame(body, bg=BG_CARD, height=10).pack()


def popup_sos(trigger_type):
    popup, body = make_popup("SOS Alert Dispatched", width=480, height=340)

    badge = tk.Frame(body, bg=DANGER, width=70, height=70)
    badge.pack_propagate(False)
    badge.pack(pady=(12, 6))
    tk.Label(badge, text="SOS", font=("Helvetica", 18, "bold"),
             bg=DANGER, fg="white").place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(body, text=trigger_type,
             font=("Helvetica", 10, "bold"),
             bg=BG_CARD, fg=DANGER).pack()

    tk.Frame(body, bg=SEPARATOR, height=1).pack(fill=tk.X, padx=24, pady=10)

    contact_str = ", ".join(emergency_contacts.keys())
    for lbl, val in [
        ("Location",    live_location),
        ("Sent To",     contact_str),
        ("Authorities", "999  ·  Rajpara Police Station"),
    ]:
        add_label_row(body, lbl, val)

    tk.Frame(body, bg=BG_CARD, height=6).pack()
    tk.Label(body, text="All contacts notified successfully.",
             font=("Helvetica", 9), bg=BG_CARD, fg=ACCENT).pack()
    tk.Frame(body, bg=BG_CARD, height=10).pack()


def popup_stealth_capture():
    popup, body = make_popup("Stealth Media Capture", width=420, height=300)

    tk.Label(body, text="◉", font=("Helvetica", 40),
             bg=BG_CARD, fg=DANGER).pack(pady=(12, 2))
    tk.Label(body, text="Stealth Mode Active",
             font=("Helvetica", 12, "bold"),
             bg=BG_CARD, fg=TEXT_PRI).pack()

    tk.Frame(body, bg=SEPARATOR, height=1).pack(fill=tk.X, padx=24, pady=10)

    for step in [
        "Screen dimmed to 0% brightness  (blacked out)",
        "Recording audio & capturing background photos",
        "Recording background video",
        "Media saved to encrypted local vault",
    ]:
        row = tk.Frame(body, bg=BG_CARD, pady=2)
        row.pack(fill=tk.X, padx=24)
        tk.Label(row, text="›", font=("Helvetica", 12),
                 bg=BG_CARD, fg=ACCENT).pack(side=tk.LEFT)
        tk.Label(row, text=step, font=("Helvetica", 10),
                 bg=BG_CARD, fg=TEXT_PRI, anchor="w").pack(side=tk.LEFT,
                                                             padx=(8, 0))
    tk.Frame(body, bg=BG_CARD, height=10).pack()


def popup_sms_fallback():
    popup, body = make_popup("SMS Fallback", width=440, height=310)

    tk.Label(body, text="⚠", font=("Helvetica", 36),
             bg=BG_CARD, fg="#f4a261").pack(pady=(10, 2))
    tk.Label(body, text="No Internet Connection Detected",
             font=("Helvetica", 11, "bold"),
             bg=BG_CARD, fg=TEXT_PRI).pack()

    tk.Frame(body, bg=SEPARATOR, height=1).pack(fill=tk.X, padx=24, pady=10)

    contact_str = ", ".join(emergency_contacts.keys())
    for lbl, val in [
        ("Status",   "SMS Fallback Activated"),
        ("GPS Data", live_location),
        ("Sent To",  contact_str),
        ("Result",   "Fallback SMS Delivered  ✓"),
    ]:
        color = ACCENT if "✓" in val else TEXT_PRI
        add_label_row(body, lbl, val, value_color=color)

    tk.Frame(body, bg=BG_CARD, height=10).pack()


# =====================================================================
# MAIN WINDOW
# =====================================================================

app_window = tk.Tk()
app_window.title("NIRAPOD THAKI")
app_window.geometry("420x620")
app_window.configure(bg=BG_DARK)
app_window.resizable(True, True)

# ── Fixed Header (does NOT scroll) ───────────────────────────────────
header = tk.Frame(app_window, bg=BG_PANEL)
header.pack(fill=tk.X)

tk.Frame(header, bg=ACCENT, height=3).pack(fill=tk.X)

tk.Label(header, text="NIRAPOD THAKI",
         font=("Georgia", 22, "bold"),
         bg=BG_PANEL, fg=TEXT_PRI).pack(pady=(18, 2))
tk.Label(header, text="Personal Safety System",
         font=("Helvetica", 9),
         bg=BG_PANEL, fg=TEXT_SEC).pack()

loc_pill = tk.Frame(header, bg=BG_CARD, padx=14, pady=5)
loc_pill.pack(pady=(10, 16))
tk.Label(loc_pill, text=f"  {live_location}  ",
         font=("Helvetica", 9), bg=BG_CARD, fg=ACCENT).pack()

tk.Frame(header, bg=ACCENT, height=3).pack(fill=tk.X)

# ── Fixed Footer (does NOT scroll) ───────────────────────────────────
footer = tk.Frame(app_window, bg=BG_PANEL)
footer.pack(fill=tk.X, side=tk.BOTTOM)
tk.Frame(footer, bg=SEPARATOR, height=1).pack(fill=tk.X)
exit_btn = tk.Button(
    footer, text="Exit Application",
    command=app_window.quit,
    font=("Helvetica", 9), bg=BG_PANEL, fg=TEXT_SEC,
    relief=tk.FLAT, bd=0, pady=9, cursor="hand2",
    activebackground=BORDER, activeforeground=TEXT_PRI
)
exit_btn.pack()
exit_btn.bind("<Enter>", lambda e: exit_btn.configure(bg=BORDER))
exit_btn.bind("<Leave>", lambda e: exit_btn.configure(bg=BG_PANEL))

# ── Scrollable Button Area ────────────────────────────────────────────
# Canvas + scrollbar between the fixed header and fixed footer.
scroll_wrapper = tk.Frame(app_window, bg=BG_DARK)
scroll_wrapper.pack(fill=tk.BOTH, expand=True)

main_canvas = tk.Canvas(scroll_wrapper, bg=BG_DARK,
                         highlightthickness=0, bd=0)
main_vbar   = tk.Scrollbar(scroll_wrapper, orient=tk.VERTICAL,
                             command=main_canvas.yview)
main_canvas.configure(yscrollcommand=main_vbar.set)

# Scrollbar only appears when needed — pack it last so it's on the right
main_vbar.pack(side=tk.RIGHT, fill=tk.Y)
main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Inner frame that holds all buttons
btn_area = tk.Frame(main_canvas, bg=BG_DARK, padx=28, pady=16)
btn_area_id = main_canvas.create_window((0, 0), window=btn_area,
                                         anchor="nw")

# Keep inner frame width in sync with canvas width
def _main_canvas_resize(event):
    main_canvas.itemconfig(btn_area_id, width=event.width)

# Update scrollregion whenever btn_area changes height
def _btn_area_resize(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

main_canvas.bind("<Configure>", _main_canvas_resize)
btn_area.bind("<Configure>",    _btn_area_resize)

# Mouse-wheel on the main window
def _main_mousewheel(event):
    if event.num == 4:
        main_canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        main_canvas.yview_scroll(1, "units")
    else:
        main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

main_canvas.bind("<MouseWheel>", _main_mousewheel)
main_canvas.bind("<Button-4>",   _main_mousewheel)
main_canvas.bind("<Button-5>",   _main_mousewheel)
btn_area.bind("<MouseWheel>",    _main_mousewheel)
btn_area.bind("<Button-4>",      _main_mousewheel)
btn_area.bind("<Button-5>",      _main_mousewheel)

# ── Section label helper ──────────────────────────────────────────────
def section_label(parent, text):
    tk.Label(parent, text=text.upper(),
             font=("Helvetica", 7, "bold"),
             bg=BG_DARK, fg=TEXT_SEC).pack(anchor="w", pady=(12, 4))

# ── Build the button list ─────────────────────────────────────────────
section_label(btn_area, "Profile")
make_rounded_btn(btn_area, "View User Data & Contacts",  popup_view_data)
make_rounded_btn(btn_area, "Edit Profile / Contacts / Zones",
                 popup_edit_profile, is_sub=True)

section_label(btn_area, "Environment")
make_rounded_btn(btn_area, "Nearest Facilities & Helplines",
                 popup_nearest_facilities)

section_label(btn_area, "SOS Triggers")
make_rounded_btn(btn_area, "SOS  —  Hardware / Smartwatch",
                 lambda: popup_sos("HARDWARE BUTTON PRESS"), is_sos=True)
make_rounded_btn(btn_area, 'SOS  —  Voice: "Dattebayo"',
                 lambda: popup_sos("VOICE ACTIVATION  (Dattebayo)"),
                 is_sos=True)

section_label(btn_area, "Utilities")
make_rounded_btn(btn_area, "Stealth Media Capture",     popup_stealth_capture)
make_rounded_btn(btn_area, "No-Internet SMS Fallback",  popup_sms_fallback)

# Bottom breathing room
tk.Frame(btn_area, bg=BG_DARK, height=12).pack()

# ── Launch ────────────────────────────────────────────────────────────
app_window.mainloop()
