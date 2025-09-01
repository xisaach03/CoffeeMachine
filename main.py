# ============================================================
#  Project: Coffee Machine Simulation
#  File: main.py
#
#  Author(s): Sofia Vanessa and Ximena Isaac
#
#  Credits:
#    - Functional design and logic implemented by both authors.
#    - GUI layout, dark theme styling, and interactive enhancements
#      by ChatGPT (OpenAI Assistant).
#
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from coffeeprep import Coffee, StockIngredients

# ------------------------------ Color Palette ------------------------------ #
PALETTE = {
    "bg":       "#0e0f13",  # app background
    "surface":  "#171923",  # primary card
    "surface2": "#1f2230",  # secondary card / stripes
    "text":     "#e7e7ea",
    "muted":    "#b0b3c5",
    "accent":   "#7c5cff",  # purple
    "accent2":  "#00d1b2",  # teal
    "danger":   "#ff5c5c",
    "ok":       "#72e06a",
}


# ----------------------------------- GUI ----------------------------------- #
class CoffeeApp(tk.Tk):
    """
    Graphical user interface for the coffee machine.
    Integrates with Coffee and StockIngredients from coffeeprep.py
    """
    def __init__(self):
        super().__init__()
        self.title("☕ Coffee Machine — Sofia & Ximena")
        self.geometry("860x600")
        self.minsize(820, 560)
        self.configure(bg=PALETTE["bg"])

        # State
        self.stock = StockIngredients()
        self.var_tipo = tk.StringVar(value="espresso")   # espresso, latte, capuccino
        self.var_tamano = tk.StringVar(value="small")    # small, medium, large

        # Build UI
        self._build_style()
        self._build_layout()
        self._render_stock()

        # Welcome log
        self._log("👋 Welcome. Initial stock ready.", tag="ok")
        self._log(f"Inventory: {self.stock.stock}", tag="muted")

    # ------------------------------ Styling ------------------------------ #
    def _build_style(self):
        style = ttk.Style(self)

        # Use a theme that respects color configuration
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Base colors
        style.configure(".", background=PALETTE["bg"], foreground=PALETTE["text"])
        style.configure("TFrame", background=PALETTE["bg"])
        style.configure("TLabel", background=PALETTE["bg"], foreground=PALETTE["text"])

        # Title
        style.configure("Title.TLabel",
                        background=PALETTE["bg"],
                        foreground=PALETTE["text"],
                        font=("Segoe UI", 18, "bold"))

        # Section cards (Labelframes)
        style.configure("Section.TLabelframe",
                        background=PALETTE["surface"],
                        borderwidth=0,
                        relief="flat",
                        padding=14)
        style.configure("Section.TLabelframe.Label",
                        background=PALETTE["surface"],
                        foreground=PALETTE["muted"],
                        font=("Segoe UI", 11, "bold"))

        # Buttons
        style.configure("TButton",
                        background=PALETTE["surface2"],
                        foreground=PALETTE["text"],
                        padding=10,
                        borderwidth=0,
                        focusthickness=0)
        style.map("TButton",
                  background=[("active", "#242736"), ("pressed", "#26293a")],
                  foreground=[("disabled", "#7b7f91")])

        style.configure("Accent.TButton",
                        background=PALETTE["accent"],
                        foreground="#ffffff",
                        padding=10,
                        font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton",
                  background=[("active", "#6e4cf5"), ("pressed", "#633fe9")])

        style.configure("Danger.TButton",
                        background=PALETTE["danger"],
                        foreground="#ffffff",
                        padding=10,
                        font=("Segoe UI", 10, "bold"))
        style.map("Danger.TButton",
                  background=[("active", "#e55353"), ("pressed", "#d84a4a")])

        # Radio buttons
        style.configure("TMenubutton", background=PALETTE["surface"])
        style.configure("TRadiobutton",
                        background=PALETTE["surface"],
                        foreground=PALETTE["text"],
                        padding=6)
        style.map("TRadiobutton",
                  foreground=[("active", "#ffffff")])

        # Treeview (stock table)
        style.configure("Treeview",
                        background=PALETTE["surface"],
                        fieldbackground=PALETTE["surface"],
                        foreground=PALETTE["text"],
                        rowheight=28,
                        borderwidth=0)
        style.map("Treeview",
                  background=[("selected", PALETTE["accent"])],
                  foreground=[("selected", "#ffffff")])

        style.configure("Treeview.Heading",
                        background=PALETTE["surface2"],
                        foreground=PALETTE["text"],
                        relief="flat",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview.Heading",
                  background=[("active", PALETTE["surface2"])])

        # Scrollbar (optional minimal tweak)
        style.configure("Vertical.TScrollbar",
                        background=PALETTE["surface2"],
                        troughcolor=PALETTE["surface"],
                        bordercolor=PALETTE["surface"],
                        lightcolor=PALETTE["surface2"],
                        darkcolor=PALETTE["surface2"])

    # ------------------------------ Layout ------------------------------ #
    def _build_layout(self):
        # Grid skeleton
        self.columnconfigure(0, weight=1, uniform="half")
        self.columnconfigure(1, weight=1, uniform="half")
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        # Header area with accent underline
        header = ttk.Frame(self)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 8))
        header.columnconfigure(0, weight=1)

        lbl_title = ttk.Label(header, text="☕ Coffee Machine", style="Title.TLabel")
        lbl_title.grid(row=0, column=0, sticky="w")
        # Accent bar
        bar = tk.Frame(header, bg=PALETTE["accent"], height=3)
        bar.grid(row=1, column=0, sticky="ew", pady=(8, 0))

        # --- Selection card ---
        frm_select = ttk.Labelframe(self, text=" Selection ", style="Section.TLabelframe")
        frm_select.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=(8, 16))
        frm_select.columnconfigure(0, weight=1)
        frm_select.columnconfigure(1, weight=1)

        # Coffee type radios
        lf_tipo = ttk.Labelframe(frm_select, text=" Coffee type ", style="Section.TLabelframe")
        lf_tipo.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))
        for i, (value, label) in enumerate([
            ("espresso", "☄️ Espresso"),
            ("latte", "🥛 Latte"),
            ("capuccino", "🌫️ Capuccino"),
        ]):
            ttk.Radiobutton(lf_tipo, text=label, value=value, variable=self.var_tipo).grid(
                row=i, column=0, sticky="w", padx=6, pady=4
            )

        # Coffee size radios
        lf_tamano = ttk.Labelframe(frm_select, text=" Size ", style="Section.TLabelframe")
        lf_tamano.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 8))
        for i, (value, label) in enumerate([
            ("small", "🫖 Small"),
            ("medium", "🍶 Medium"),
            ("large", "🧃 Large"),
        ]):
            ttk.Radiobutton(lf_tamano, text=label, value=value, variable=self.var_tamano).grid(
                row=i, column=0, sticky="w", padx=6, pady=4
            )

        # Action buttons
        frm_actions = ttk.Frame(frm_select, style="Section.TLabelframe")
        frm_actions.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        for col in range(3):
            frm_actions.columnconfigure(col, weight=1)

        ttk.Button(frm_actions, text="Brew ☕", style="Accent.TButton", command=self._prepare).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(frm_actions, text="Show Price 💵", command=self._show_price).grid(
            row=0, column=1, sticky="ew", padx=6
        )
        ttk.Button(frm_actions, text="Reset Stock ♻️", style="Danger.TButton", command=self._reset_stock).grid(
            row=0, column=2, sticky="ew", padx=(6, 0)
        )

        # --- Stock & log card ---
        frm_stock = ttk.Labelframe(self, text=" Stock ", style="Section.TLabelframe")
        frm_stock.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=(8, 16))
        frm_stock.rowconfigure(1, weight=1)
        frm_stock.columnconfigure(0, weight=1)

        # Stock table
        self.tree = ttk.Treeview(frm_stock, columns=("ingredient", "amount"), show="headings", height=9)
        self.tree.heading("ingredient", text="Ingredient")
        self.tree.heading("amount", text="Amount")
        self.tree.column("ingredient", width=160, anchor="w")
        self.tree.column("amount", width=100, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Configure striped rows for the Treeview
        self.tree.tag_configure("oddrow", background=PALETTE["surface"])
        self.tree.tag_configure("evenrow", background=PALETTE["surface2"])

        # Messages / log (dark console look)
        lf_log = ttk.Labelframe(frm_stock, text=" Messages ", style="Section.TLabelframe")
        lf_log.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        lf_log.rowconfigure(0, weight=1)
        lf_log.columnconfigure(0, weight=1)

        self.txt_log = tk.Text(
            lf_log,
            height=8,
            wrap="word",
            font=("Consolas", 10),
            bg="#0f1115",
            fg=PALETTE["text"],
            insertbackground=PALETTE["text"],
            highlightthickness=0,
            bd=0,
        )
        self.txt_log.grid(row=0, column=0, sticky="nsew")
        sbr = ttk.Scrollbar(lf_log, command=self.txt_log.yview)
        sbr.grid(row=0, column=1, sticky="ns")
        self.txt_log.config(yscrollcommand=sbr.set)

        # Define text tags for colored log lines
        self.txt_log.tag_configure("ok", foreground=PALETTE["ok"])
        self.txt_log.tag_configure("warn", foreground="#ffcf66")
        self.txt_log.tag_configure("err", foreground=PALETTE["danger"])
        self.txt_log.tag_configure("muted", foreground=PALETTE["muted"])

        # Status bar
        self.status = ttk.Label(self, anchor="w", foreground=PALETTE["muted"])
        self.status.grid(row=2, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))
        self._update_status()

        # React to selection changes
        self.var_tipo.trace_add("write", lambda *args: self._update_status())
        self.var_tamano.trace_add("write", lambda *args: self._update_status())

    # ------------------------------ Actions ------------------------------ #
    def _prepare(self):
        """Try to brew the selected coffee, validate stock and deduct ingredients."""
        coffee_type = self.var_tipo.get()
        size = self.var_tamano.get()

        try:
            coffee = Coffee(coffee_type, size)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create coffee:\n{e}")
            self._log(f"❌ Error creating coffee: {e}", tag="err")
            return

        ingredients = getattr(coffee, "ingredients", None) or getattr(coffee, "ingredientes", None)
        if not isinstance(ingredients, dict):
            self._log("⚠️ No ingredients found in Coffee object (.ingredients or .ingredientes).", tag="warn")
            return

        available, text = self.stock.check_ingredients(ingredients)
        self._log(text, tag=("ok" if available else "warn"))

        if available:
            self._log(f"🛠️ Brewing {self._pretty_label(size)} {self._pretty_label(coffee_type)} …", tag="muted")
            self.stock.take_ingredients(ingredients)
            self._render_stock()
            self._log(f"✅ Your {self._pretty_label(size)} {self._pretty_label(coffee_type)} is ready!", tag="ok")
            self._show_price(inline=True, coffee=coffee)
        else:
            self._log("🚫 Not enough ingredients. Try another coffee/size or reset stock.", tag="err")

    def _show_price(self, inline=False, coffee=None):
        """Show price using Coffee.price / Coffee.precio if available."""
        try:
            if coffee is None:
                coffee = Coffee(self.var_tipo.get(), self.var_tamano.get())
            price = getattr(coffee, "price", None)
            if price is None:
                price = getattr(coffee, "precio", None)
            if price is None:
                message = "ℹ️ Coffee object has no price attribute (.price/.precio)."
                tag = "warn"
            else:
                message = f"💵 Price: {price} u"
                tag = "ok"
        except Exception as e:
            message = f"⚠️ Could not get price: {e}"
            tag = "err"

        if inline:
            self._log(message, tag=tag)
        else:
            messagebox.showinfo("Price", message)
            self._log(message, tag=tag)

    def _reset_stock(self):
        """Restore stock to its initial values."""
        if messagebox.askyesno("Reset stock", "Are you sure you want to reset stock to initial values?"):
            self.stock = StockIngredients()
            self._render_stock()
            self._log("♻️ Stock reset to initial values.", tag="ok")

    # ----------------------------- UI Utilities ----------------------------- #
    def _render_stock(self):
        """Refresh the stock table with current values (striped rows)."""
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Read items
        try:
            items = sorted(self.stock.stock.items(), key=lambda kv: kv[0])
        except Exception:
            items = []

        # Insert with stripes
        for idx, (ingredient, amount) in enumerate(items):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(ingredient, amount), tags=(tag,))

    def _log(self, text, tag=None):
        """Append a colored line to the message log."""
        if tag:
            self.txt_log.insert("end", text.strip() + "\n", tag)
        else:
            self.txt_log.insert("end", text.strip() + "\n")
        self.txt_log.see("end")

    def _update_status(self):
        """Update the footer with the current selection."""
        self.status.config(
            text=f"Selection: {self._pretty_label(self.var_tamano.get())}  {self._pretty_label(self.var_tipo.get())}"
        )

    @staticmethod
    def _pretty_label(s):
        mapping = {
            "espresso": "Espresso",
            "latte": "Latte",
            "capuccino": "Capuccino",
            "small": "Small",
            "medium": "Medium",
            "large": "Large",
        }
        return mapping.get(s, s.capitalize())


# -------------------------------- Entry Point -------------------------------- #
def main():
    app = CoffeeApp()
    app.mainloop()

if __name__ == "__main__":
    main()
