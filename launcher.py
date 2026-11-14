#!/usr/bin/env python3
"""NEXUS AI desktop launcher.

A lightweight Tkinter UI for the NEXUS AI endpoint-discovery MVP.
Run with: python3 launcher.py
"""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk, messagebox

import nexus

BG = "#090d18"
PANEL = "#111827"
PANEL_ALT = "#172235"
BORDER = "#26364d"
TEXT = "#e8f0ff"
MUTED = "#8ea2bf"
ACCENT = "#48e5c2"
BLUE = "#68a7ff"
RED = "#ff6b81"


class NexusLauncher:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("NEXUS AI — Player Console")
        self.root.geometry("940x620")
        self.root.minsize(760, 520)
        self.root.configure(bg=BG)
        self.endpoints = []
        self.models = []
        self._build_style()
        self._build_layout()
        self.refresh()

    def _build_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", background=PANEL, foreground=TEXT,
                        fieldbackground=PANEL, rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", background=PANEL_ALT,
                        foreground=ACCENT, relief="flat", font=("TkDefaultFont", 9, "bold"))
        style.map("Treeview", background=[("selected", "#21445a")],
                  foreground=[("selected", TEXT)])

    def _label(self, parent, text, size=10, color=TEXT, bold=False):
        return tk.Label(parent, text=text, bg=parent.cget("bg"), fg=color,
                        font=("TkDefaultFont", size, "bold" if bold else "normal"))

    def _button(self, parent, text, command, primary=False):
        color = ACCENT if primary else PANEL_ALT
        fg = BG if primary else TEXT
        return tk.Button(parent, text=text, command=command, bg=color, fg=fg,
                         activebackground=BLUE, activeforeground=BG,
                         relief="flat", bd=0, padx=14, pady=9,
                         cursor="hand2", font=("TkDefaultFont", 9, "bold"))

    def _build_layout(self):
        header = tk.Frame(self.root, bg=BG, padx=24, pady=18)
        header.pack(fill="x")
        tk.Label(header, text="NEXUS", bg=BG, fg=ACCENT,
                 font=("TkDefaultFont", 23, "bold")).pack(side="left")
        tk.Label(header, text="  AI  /  PLAYER CONSOLE", bg=BG, fg=MUTED,
                 font=("TkDefaultFont", 10, "bold")).pack(side="left", pady=(8, 0))
        self.status_badge = tk.Label(header, text="● SCANNING", bg=BG, fg=BLUE,
                                     font=("TkDefaultFont", 9, "bold"))
        self.status_badge.pack(side="right", pady=(8, 0))

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        sidebar = tk.Frame(body, bg=PANEL, width=175, padx=12, pady=16)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self._label(sidebar, "SYSTEM MENU", 9, MUTED, True).pack(anchor="w", pady=(0, 14))
        self._button(sidebar, "⌂  Dashboard", lambda: self.show_page("dashboard"), True).pack(fill="x", pady=4)
        self._button(sidebar, "▦  My Models", lambda: self.show_page("models")).pack(fill="x", pady=4)
        self._button(sidebar, "+  Add Your LLM", self.add_llm).pack(fill="x", pady=4)
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", pady=16)
        self._label(sidebar, "NEXUS AI", 9, ACCENT, True).pack(anchor="w")
        self._label(sidebar, "EARLY ACCESS BUILD", 8, MUTED).pack(anchor="w", pady=(5, 0))
        self._label(sidebar, "Local-first • Lightweight", 8, MUTED).pack(anchor="w", pady=(3, 0))

        self.content = tk.Frame(body, bg=BG)
        self.content.pack(side="left", fill="both", expand=True, padx=(18, 0))
        self.show_page("dashboard")

        footer = tk.Frame(self.root, bg=BG, padx=24, pady=8)
        footer.pack(fill="x")
        self.footer_label = tk.Label(footer, text=f"CONFIG  {nexus.config_path()}",
                                     bg=BG, fg=MUTED, font=("TkDefaultFont", 8))
        self.footer_label.pack(anchor="w")

    def _clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def _card(self, parent, title, value, subtitle, accent=ACCENT):
        card = tk.Frame(parent, bg=PANEL, padx=16, pady=14,
                        highlightthickness=1, highlightbackground=BORDER)
        tk.Label(card, text=title.upper(), bg=PANEL, fg=MUTED,
                 font=("TkDefaultFont", 8, "bold")).pack(anchor="w")
        tk.Label(card, text=value, bg=PANEL, fg=accent,
                 font=("TkDefaultFont", 23, "bold")).pack(anchor="w", pady=(7, 2))
        tk.Label(card, text=subtitle, bg=PANEL, fg=MUTED,
                 font=("TkDefaultFont", 8)).pack(anchor="w")
        return card

    def show_page(self, page):
        self._clear_content()
        if page == "models":
            self._build_models_page()
        else:
            self._build_dashboard()

    def _build_dashboard(self):
        self._label(self.content, "PLAYER DETECTED", 9, ACCENT, True).pack(anchor="w")
        self._label(self.content, "Local AI System", 22, TEXT, True).pack(anchor="w", pady=(4, 2))
        self._label(self.content, "Manage your AI engines and model endpoints from one place.", 9, MUTED).pack(anchor="w")
        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", pady=20)
        self.online_card = self._card(cards, "Connected endpoints", "—", "Local and remote servers")
        self.online_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.model_card = self._card(cards, "Available models", "—", "Models exposed by servers", BLUE)
        self.model_card.pack(side="left", fill="both", expand=True, padx=8)
        self.engine_card = self._card(cards, "Configured servers", "—", "Saved in your user config", BLUE)
        self.engine_card.pack(side="left", fill="both", expand=True, padx=(8, 0))

        panel = tk.Frame(self.content, bg=PANEL, padx=16, pady=14,
                         highlightthickness=1, highlightbackground=BORDER)
        panel.pack(fill="both", expand=True)
        row = tk.Frame(panel, bg=PANEL)
        row.pack(fill="x")
        self._label(row, "ENGINE STATUS", 10, TEXT, True).pack(side="left")
        self._button(row, "↻ Refresh", self.refresh, True).pack(side="right")
        self.status_text = tk.Text(panel, bg=PANEL, fg=TEXT, insertbackground=TEXT,
                                   relief="flat", height=10, wrap="word",
                                   font=("TkFixedFont", 9), padx=2, pady=12)
        self.status_text.pack(fill="both", expand=True)
        self.status_text.insert("end", "Scanning configured endpoints…")
        self.status_text.configure(state="disabled")

    def _build_models_page(self):
        self._label(self.content, "MODEL LIBRARY", 9, ACCENT, True).pack(anchor="w")
        self._label(self.content, "Your connected models", 21, TEXT, True).pack(anchor="w", pady=(4, 12))
        toolbar = tk.Frame(self.content, bg=BG)
        toolbar.pack(fill="x", pady=(0, 10))
        self._button(toolbar, "+ Add LLM", self.add_llm, True).pack(side="left")
        self._button(toolbar, "↻ Refresh", self.refresh).pack(side="left", padx=8)
        table_frame = tk.Frame(self.content, bg=PANEL, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)
        columns = ("model", "provider")
        self.model_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.model_table.heading("model", text="MODEL ID")
        self.model_table.heading("provider", text="SERVER")
        self.model_table.column("model", width=350, anchor="w")
        self.model_table.column("provider", width=220, anchor="w")
        self.model_table.pack(fill="both", expand=True)
        self.model_hint = self._label(self.content, "Refresh to discover models exposed by connected endpoints.", 8, MUTED)
        self.model_hint.pack(anchor="w", pady=(8, 0))
        self._populate_models()

    def _populate_models(self):
        if not hasattr(self, "model_table") or not self.model_table.winfo_exists():
            return
        self.model_table.delete(*self.model_table.get_children())
        for provider, model in self.models:
            self.model_table.insert("", "end", values=(model, provider))
        if hasattr(self, "model_hint") and self.model_hint.winfo_exists():
            self.model_hint.configure(text=f"{len(self.models)} model(s) found. Model files remain managed by their own engine.")

    def refresh(self):
        self.status_badge.configure(text="● SCANNING", fg=BLUE)
        self._set_status_text("Scanning configured endpoints…")
        def worker():
            endpoints = nexus.configured_endpoints()
            states = []
            found_models = []
            for name, url in endpoints:
                ok, detail = nexus.check_endpoint(name, url)
                states.append((name, url, ok, detail))
                if ok:
                    try:
                        data = nexus.request_json(url)
                        entries = data.get("models") or data.get("data") or []
                        for item in entries:
                            model = (item.get("name") or item.get("id") or "Unknown") if isinstance(item, dict) else str(item)
                            found_models.append((name, model))
                    except Exception:
                        pass
            self.root.after(0, lambda: self._refresh_done(states, found_models))
        threading.Thread(target=worker, daemon=True).start()

    def _set_status_text(self, text):
        if hasattr(self, "status_text") and self.status_text.winfo_exists():
            self.status_text.configure(state="normal")
            self.status_text.delete("1.0", "end")
            self.status_text.insert("end", text)
            self.status_text.configure(state="disabled")

    def _refresh_done(self, states, found_models):
        self.endpoints = states
        self.models = found_models
        online = sum(1 for item in states if item[2])
        self.status_badge.configure(text=f"● {online} ONLINE / {len(states)} CHECKED",
                                    fg=ACCENT if online else RED)
        lines = []
        for name, url, ok, detail in states:
            lines.append(f"[{'ONLINE' if ok else 'OFFLINE'}] {name}\n  {url}\n  {detail}\n")
        if not lines:
            lines = ["No endpoints configured. Add your own LLM server to get started."]
        self._set_status_text("\n".join(lines))
        if hasattr(self, "online_card"):
            self._update_card(self.online_card, str(online), "Reachable endpoints")
            self._update_card(self.model_card, str(len(found_models)), "Discovered model IDs")
            self._update_card(self.engine_card, str(len(states)), "Saved server endpoints")
        self._populate_models()

    def _update_card(self, card, value, subtitle):
        labels = [child for child in card.winfo_children() if isinstance(child, tk.Label)]
        if len(labels) >= 3:
            labels[1].configure(text=value)
            labels[2].configure(text=subtitle)

    def add_llm(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add your own LLM")
        dialog.configure(bg=PANEL)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        box = tk.Frame(dialog, bg=PANEL, padx=22, pady=20)
        box.pack(fill="both", expand=True)
        tk.Label(box, text="CONNECT YOUR LLM", bg=PANEL, fg=ACCENT,
                 font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(0, 12))
        tk.Label(box, text="Display name", bg=PANEL, fg=TEXT).pack(anchor="w")
        name_entry = tk.Entry(box, bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat", width=48)
        name_entry.pack(fill="x", pady=(5, 12), ipady=7)
        tk.Label(box, text="Models endpoint URL", bg=PANEL, fg=TEXT).pack(anchor="w")
        url_entry = tk.Entry(box, bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat", width=48)
        url_entry.pack(fill="x", pady=(5, 8), ipady=7)
        tk.Label(box, text="Example: http://127.0.0.1:1234/v1/models",
                 bg=PANEL, fg=MUTED, font=("TkDefaultFont", 8)).pack(anchor="w")
        def save():
            name, url = name_entry.get().strip(), url_entry.get().strip()
            if not name or not url.startswith(("http://", "https://")):
                messagebox.showerror("Invalid endpoint", "Enter a name and a valid http:// or https:// URL.", parent=dialog)
                return
            try:
                nexus.add_endpoint(name, url)
            except Exception as exc:
                messagebox.showerror("Could not save endpoint", str(exc), parent=dialog)
                return
            dialog.destroy()
            self.refresh()
            messagebox.showinfo("NEXUS AI", f"Added {name}. NEXUS will now check the endpoint.", parent=self.root)
        actions = tk.Frame(box, bg=PANEL)
        actions.pack(fill="x", pady=(18, 0))
        self._button(actions, "Cancel", dialog.destroy).pack(side="right")
        self._button(actions, "Save endpoint", save, True).pack(side="right", padx=8)
        name_entry.focus_set()

def main():
    root = tk.Tk()
    NexusLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
