import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from pynput import keyboard
import yaml
from datetime import datetime
import winsound

# Globale Variablen
recording = False
listener = None
file_path = "records.yml"
records = []
current_text = ""
is_dark_mode = True
current_language = "de"

# Design-Einstellungen
CORNER_RADIUS = 12
BUTTON_ANIMATION_MS = 150
SOUND_EFFECTS = {
    "start": None,
    "stop": None,
    "error": None,
    "click": None
}

# Übersetzungen
translations = {
    "de": {
        "title": "StarLog Tastenrecorder",
        "status_ready": "Status: Bereit",
        "status_recording": "Status: Aufnahme läuft ⚫",
        "start_btn": "⏺ Aufnahme starten (F1)",
        "stop_btn": "⏹ Aufnahme stoppen (F2)",
        "clear_btn": "🗑️ Historie löschen",
        "open_btn": "📂 Datei öffnen",
        "dark_mode_btn": "🌓 Design wechseln",
        "footer": "© 2025 Eministar Dev Group n.e.V. | Professionelle Tastenaufzeichnung",
        "info": "Info",
        "already_recording": "Die Aufnahme läuft bereits!",
        "not_recording": "Es läuft keine Aufnahme!",
        "confirm": "Bestätigung",
        "confirm_delete": "Möchten Sie wirklich die gesamte Aufzeichnungshistorie löschen?",
        "current_session": "Aktuelle Sitzung",
        "current_lang": "Deutsch",
        "error": "Fehler",
        "open_error": "Fehler beim Öffnen: {error}",
        "file_not_found": "Datei nicht gefunden"
    },
    "en": {
        "title": "StarLog Key Recorder",
        "status_ready": "Status: Ready",
        "status_recording": "Status: Recording ⚫",
        "start_btn": "⏺ Start Recording (F1)",
        "stop_btn": "⏹ Stop Recording (F2)",
        "clear_btn": "🗑️ Clear History",
        "open_btn": "📂 Open File",
        "dark_mode_btn": "🌓 Toggle Theme",
        "footer": "© 2025 Eministar Dev Group n.e.V. | Professional Key Logging",
        "info": "Information",
        "already_recording": "Recording is already in progress!",
        "not_recording": "No recording is active!",
        "confirm": "Confirmation",
        "confirm_delete": "Are you sure you want to delete the entire recording history?",
        "current_session": "Current Session",
        "current_lang": "English",
        "error": "Error",
        "open_error": "Open error: {error}",
        "file_not_found": "File not found"
    },
    "fr": {
        "title": "StarLog Enregistreur",
        "status_ready": "Statut: Prêt",
        "status_recording": "Statut: Enregistrement ⚫",
        "start_btn": "⏺ Démarrer (F1)",
        "stop_btn": "⏹ Arrêter (F2)",
        "clear_btn": "🗑️ Effacer l'historique",
        "open_btn": "📂 Ouvrir le fichier",
        "dark_mode_btn": "🌓 Changer de thème",
        "footer": "© 2025 Eministar Dev Group n.e.V. | Enregistrement professionnel",
        "info": "Information",
        "already_recording": "L'enregistrement est déjà en cours!",
        "not_recording": "Aucun enregistrement actif!",
        "confirm": "Confirmation",
        "confirm_delete": "Voulez-vous vraiment supprimer tout l'historique?",
        "current_session": "Session en cours",
        "current_lang": "Français",
        "error": "Erreur",
        "open_error": "Erreur d'ouverture: {error}",
        "file_not_found": "Fichier non trouvé"
    }
}

# Modernes Farbdesign
colors = {
    "dark": {
        "primary": "#1A1A1A",
        "secondary": "#252525",
        "text": "#FFFFFF",
        "accent": "#4CAF50",
        "accent_hover": "#66BB6A",
        "stop": "#F44336",
        "stop_hover": "#EF5350",
        "scroll": "#404040",
        "scroll_hover": "#606060",
        "timestamp": "#888888",
        "border": "#333333",
        "hover": "#2D2D2D"
    },
    "light": {
        "primary": "#F5F5F5",
        "secondary": "#FFFFFF",
        "text": "#212121",
        "accent": "#2196F3",
        "accent_hover": "#42A5F5",
        "stop": "#FF5252",
        "stop_hover": "#FF7043",
        "scroll": "#C0C0C0",
        "scroll_hover": "#A0A0A0",
        "timestamp": "#666666",
        "border": "#E0E0E0",
        "hover": "#EEEEEE"
    }
}

class ModernButton(tk.Canvas):
    def __init__(self, master, text, command, color_type="accent", width=140, height=40):
        super().__init__(master, width=width, height=height, highlightthickness=0)
        self.command = command
        self.text = text
        self.color_type = color_type
        self.width = width
        self.height = height
        self.text_id = None
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
        self.draw()

    def draw(self, hover=False):
        self.delete("all")
        current_colors = colors["dark" if is_dark_mode else "light"]
        bg_color = current_colors[self.color_type + ("_hover" if hover else "")]
        
        # Hintergrund
        self.create_rectangle(
            0, 0, self.width, self.height,
            fill=bg_color,
            outline="",
            width=0
        )
        
        # Text
        self.text_id = self.create_text(
            self.width/2,
            self.height/2,
            text=self.text,
            fill=current_colors["text"],
            font=("Segoe UI", 11, "bold")
        )
        
    def on_enter(self, event):
        self.draw(hover=True)
        self.config(cursor="hand2")
        
    def on_leave(self, event):
        self.draw()
        
    def on_click(self, event):
        self.command()
        play_sound("click")

def play_sound(sound_type):
    if sound_type in SOUND_EFFECTS and SOUND_EFFECTS[sound_type]:
        try:
            winsound.PlaySound(SOUND_EFFECTS[sound_type], winsound.SND_ASYNC)
        except:
            pass

def set_language(lang):
    global current_language
    current_language = lang
    update_ui_texts()

def update_ui_texts():
    tr = translations[current_language]
    root.title(tr['title'])
    status_label.config(text=tr['status_ready'])
    start_btn.itemconfig(start_btn.text_id, text=tr['start_btn'])
    stop_btn.itemconfig(stop_btn.text_id, text=tr['stop_btn'])
    clear_btn.itemconfig(clear_btn.text_id, text=tr['clear_btn'])
    open_btn.itemconfig(open_btn.text_id, text=tr['open_btn'])
    dark_mode_btn.itemconfig(dark_mode_btn.text_id, text=tr['dark_mode_btn'])
    footer_label.config(text=tr['footer'])
    lang_combobox.set(tr['current_lang'])

def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    update_styles()

def update_styles():
    current_colors = colors["dark" if is_dark_mode else "light"]
    
    # Hauptfenster
    root.config(bg=current_colors["primary"])
    header_frame.config(bg=current_colors["primary"])
    main_frame.config(bg=current_colors["secondary"])
    button_frame.config(bg=current_colors["primary"])
    footer_label.config(bg=current_colors["primary"], fg=current_colors["timestamp"])
    
    # Textbereich
    text_display.config(
        bg=current_colors["secondary"],
        fg=current_colors["text"],
        insertbackground=current_colors["text"]
    )
    text_frame.config(highlightbackground=current_colors["border"])
    
    # Status Label
    status_label.config(
        bg=current_colors["primary"],
        fg=current_colors["timestamp"]
    )
    
    # Buttons neu zeichnen
    for btn in [start_btn, stop_btn, clear_btn, open_btn, dark_mode_btn]:
        btn.draw()
    
    update_display()

def update_display():
    text_display.config(state=tk.NORMAL)
    text_display.delete(1.0, tk.END)
    
    current_colors = colors["dark" if is_dark_mode else "light"]
    
    for record in reversed(records):
        timestamp = record['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        text_display.insert(tk.END, f"{timestamp}\n", "timestamp")
        text_display.insert(tk.END, f"{record['content']}\n\n", "content")
    
    if current_text:
        text_display.insert(tk.END, f"{translations[current_language]['current_session']}:\n", "timestamp")
        text_display.insert(tk.END, f"{current_text}\n\n", "content")
    
    text_display.tag_config("timestamp", foreground=current_colors["timestamp"])
    text_display.tag_config("content", foreground=current_colors["text"])
    text_display.see(tk.END)
    text_display.config(state=tk.DISABLED)

def start_recording():
    global recording, listener, current_text
    if recording:
        messagebox.showinfo(translations[current_language]['info'], 
                          translations[current_language]['already_recording'])
        play_sound("error")
        return
    
    current_text = ""
    recording = True
    status_label.config(text=translations[current_language]['status_recording'], fg="#4CAF50")
    play_sound("start")
    
    def on_press(key):
        global current_text
        try:
            char = key.char
        except AttributeError:
            char = f"[{key}]"
        
        current_text += char
        root.after(0, update_display)
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    update_display()

def stop_recording():
    global recording, listener, records, current_text
    if not recording:
        messagebox.showinfo(translations[current_language]['info'], 
                          translations[current_language]['not_recording'])
        play_sound("error")
        return
    
    recording = False
    status_label.config(text=translations[current_language]['status_ready'], fg="#808080")
    play_sound("stop")
    
    if current_text:
        records.append({
            'timestamp': datetime.now(),
            'content': current_text
        })
        save_records()
    
    if listener:
        listener.stop()
        listener = None
    
    current_text = ""
    update_display()

def save_records():
    with open(file_path, 'w') as file:
        yaml.safe_dump(
            [{'timestamp': r['timestamp'].isoformat(), 'content': r['content']} 
             for r in records],
            file,
            allow_unicode=True,
            default_flow_style=False
        )

def load_records():
    global records
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            loaded = yaml.safe_load(file) or []
            records = [{
                'timestamp': datetime.fromisoformat(r['timestamp']),
                'content': r['content']
            } for r in loaded]
    else:
        records = []

def clear_history():
    if messagebox.askyesno(translations[current_language]['confirm'], 
                         translations[current_language]['confirm_delete']):
        global records
        records = []
        if os.path.exists(file_path):
            os.remove(file_path)
        update_display()
        play_sound("stop")

def open_file():
    if os.path.exists(file_path):
        try:
            if os.name == 'nt':
                os.startfile(file_path)
            elif sys.platform == 'darwin':
                os.system(f'open "{file_path}"')
            else:
                os.system(f'xdg-open "{file_path}"')
        except Exception as e:
            messagebox.showerror(
                translations[current_language]['error'],
                translations[current_language]['open_error'].format(error=str(e))
            )
            play_sound("error")
    else:
        messagebox.showerror(
            translations[current_language]['error'],
            translations[current_language]['file_not_found'])
        play_sound("error")

def create_gui():
    global root, header_frame, status_label, footer_label, text_display
    global lang_combobox, start_btn, stop_btn, clear_btn, open_btn, dark_mode_btn, text_frame, main_frame, button_frame
    
    root = tk.Tk()
    root.title("StarLog Recorder")
    root.geometry("1000x700")
    root.minsize(800, 600)
    
    # Hauptlayout
    main_container = tk.Frame(root, bg=colors["dark"]["primary"])
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Header
    header_frame = tk.Frame(main_container, bg=colors["dark"]["primary"])
    header_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Titel
    title_label = tk.Label(
        header_frame,
        text="StarLog Recorder",
        font=("Segoe UI", 24, "bold"),
        bg=colors["dark"]["primary"],
        fg=colors["dark"]["text"]
    )
    title_label.pack(side=tk.LEFT)
    
    # Sprachauswahl
    lang_frame = tk.Frame(header_frame, bg=colors["dark"]["primary"])
    lang_frame.pack(side=tk.RIGHT, padx=10)
    
    lang_combobox = ttk.Combobox(
        lang_frame,
        values=["Deutsch", "English", "Français"],
        state="readonly",
        width=12,
        style="TCombobox"
    )
    lang_combobox.current(0)
    lang_combobox.pack(side=tk.RIGHT)
    lang_combobox.bind("<<ComboboxSelected>>", lambda e: set_language(lang_combobox.get().lower()[:2]))
    
    # Status
    status_label = tk.Label(
        header_frame,
        text="Status: Bereit",
        font=("Segoe UI", 11),
        fg=colors["dark"]["timestamp"],
        bg=colors["dark"]["primary"]
    )
    status_label.pack(side=tk.RIGHT, padx=20)
    
    # Hauptbereich
    main_frame = tk.Frame(
        main_container,
        bg=colors["dark"]["secondary"],
        relief="flat"
    )
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Textbereich
    text_frame = tk.Frame(
        main_frame,
        bg=colors["dark"]["secondary"],
        highlightthickness=1
    )
    text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    text_display = tk.Text(
        text_frame,
        wrap=tk.WORD,
        font=("Segoe UI", 12),
        bg=colors["dark"]["secondary"],
        fg=colors["dark"]["text"],
        insertbackground=colors["dark"]["text"],
        padx=20,
        pady=20,
        state=tk.DISABLED
    )
    
    scrollbar = ttk.Scrollbar(text_frame, command=text_display.yview)
    text_display.configure(yscrollcommand=scrollbar.set)
    text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Button-Leiste
    button_frame = tk.Frame(main_container, bg=colors["dark"]["primary"])
    button_frame.pack(fill=tk.X, pady=15)
    
    start_btn = ModernButton(button_frame, "⏺ Start", start_recording, "accent")
    start_btn.pack(side=tk.LEFT, padx=10)
    
    stop_btn = ModernButton(button_frame, "⏹ Stop", stop_recording, "stop")
    stop_btn.pack(side=tk.LEFT, padx=10)
    
    clear_btn = ModernButton(button_frame, "🗑️ Löschen", clear_history, "accent")
    clear_btn.pack(side=tk.LEFT, padx=10)
    
    open_btn = ModernButton(button_frame, "📂 Öffnen", open_file, "accent")
    open_btn.pack(side=tk.LEFT, padx=10)
    
    dark_mode_btn = ModernButton(button_frame, "🌓 Design", toggle_dark_mode, "accent")
    dark_mode_btn.pack(side=tk.RIGHT, padx=10)
    
    # Footer
    footer_label = tk.Label(
        main_container,
        text="© 2025 Eministar Dev Group n.e.V. | Professionelle Tastenaufzeichnung",
        font=("Segoe UI", 9),
        fg=colors["dark"]["timestamp"],
        bg=colors["dark"]["primary"]
    )
    footer_label.pack(side=tk.BOTTOM, pady=(10, 0))
    
    # Initialisierung
    load_records()
    set_language("de")
    update_styles()
    
    # Tastenkürzel
    root.bind("<F1>", lambda e: start_recording())
    root.bind("<F2>", lambda e: stop_recording())
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()