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
#  Notes:
#    This project was created for learning purposes.
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
    "warn":     "#ffcf66",
}

# ------------------------------ Capacities (match CLI) ------------------------------ #
MAX_WATER = 2000
MAX_MILK = 1000
MAX_BEANS = 500
MAX_CUPS = 100


# ----------------------------------- GUI ----------------------------------- #
class CoffeeMachineApp(tk.Tk):
    """
    GUI that mirrors the CLI functionality:
    - Order Coffee
    - Fill the Machine (water/milk/beans/cups or fill all)
    - Withdraw Money (with donation flow)
    - Show Data (stock + sales history)
    - Exit
    """
    def __init__(self):
        super().__init__()
        self.title("☕ Coffee Machine — Sofia & Ximena")
        self.geometry("980x640")
        self.minsize(940, 600)
        self.configure(bg=PALETTE["bg"])

        # State from CLI main()
        self.money = 0.0
        self.sells = []            # list of tuples: (coffee_type, size)
        self.sells_unit_cost = []  # list of floats: unit prices
        self.stock = StockIngredients()  # expects keys: water, milk, coffee_beans, cups

        # Selection state for ordering
        self.var_type = tk.StringVar(value="espresso")  # espresso / latte / capuccino
        self.var_size = tk.StringVar(value="small")     # small / medium / large

        # Build UI
        self._build_style()
        self._build_layout()
        self._render_all()

        # Welcome
        self._log("👋 Welcome! Initial stock loaded.", tag="ok")

    # ------------------------------ Styling ------------------------------ #
    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(".", background=PALETTE["bg"], foreground=PALETTE["text"])
        style.configure("TFrame", background=PALETTE["bg"])
        style.configure("TLabel", background=PALETTE["bg"], foreground=PALETTE["text"])

        style.configure("Title.TLabel",
                        background=PALETTE["bg"],
                        foreground=PALETTE["text"],
                        font=("Segoe UI", 20, "bold"))

        style.configure("Section.TLabelframe",
                        background=PALETTE["surface"],
                        borderwidth=0,
                        relief="flat",
                        padding=14)
        style.configure("Section.TLabelframe.Label",
                        background=PALETTE["surface"],
                        foreground=PALETTE["muted"],
                        font=("Segoe UI", 11, "bold"))

        style.configure("TButton",
                        background=PALETTE["surface2"],
                        foreground=PALETTE["text"],
                        padding=10,
                        borderwidth=0)

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

        style.configure("Treeview",
                        background=PALETTE["surface"],
                        fieldbackground=PALETTE["surface"],
                        foreground=PALETTE["text"],
                        rowheight=26,
                        borderwidth=0)
        style.map("Treeview",
                  background=[("selected", PALETTE["accent"])],
                  foreground=[("selected", "#ffffff")])
        style.configure("Treeview.Heading",
                        background=PALETTE["surface2"],
                        foreground=PALETTE["text"],
                        relief="flat",
                        font=("Segoe UI", 10, "bold"))

        style.configure("TRadiobutton",
                        background=PALETTE["surface"],
                        foreground=PALETTE["text"],
                        padding=6)

        style.configure("Status.TLabel",
                        background=PALETTE["bg"],
                        foreground=PALETTE["muted"],
                        font=("Segoe UI", 10))

    # ------------------------------ Layout ------------------------------ #
    def _build_layout(self):
        # Header
        header = ttk.Frame(self)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=18, pady=(16, 10))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="☕ Coffee Machine", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        tk.Frame(header, bg=PALETTE["accent"], height=3).grid(row=1, column=0, sticky="ew", pady=(8, 0))

        # Left side: Order + Fill Machine
        left = ttk.Frame(self)
        left.grid(row=1, column=0, sticky="nsew", padx=(18, 9), pady=(0, 16))
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)

        # Right side: Sales/Data + Log
        right = ttk.Frame(self)
        right.grid(row=1, column=1, sticky="nsew", padx=(9, 18), pady=(0, 16))
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # --- Order Section ---
        order = ttk.Labelframe(left, text=" Order Coffee ", style="Section.TLabelframe")
        order.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        order.columnconfigure(0, weight=1)
        order.columnconfigure(1, weight=1)

        # Type
        type_box = ttk.Labelframe(order, text=" Type ", style="Section.TLabelframe")
        type_box.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        for i, (val, label) in enumerate([
            ("espresso", "☄️ Espresso"),
            ("latte", "🥛 Latte"),
            ("capuccino", "🌫️ Capuccino"),
        ]):
            ttk.Radiobutton(type_box, text=label, value=val, variable=self.var_type).grid(
                row=i, column=0, sticky="w", padx=6, pady=4
            )

        # Size
        size_box = ttk.Labelframe(order, text=" Size ", style="Section.TLabelframe")
        size_box.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        for i, (val, label) in enumerate([
            ("small", "🫖 Small"),
            ("medium", "🍶 Medium"),
            ("large", "🧃 Large"),
        ]):
            ttk.Radiobutton(size_box, text=label, value=val, variable=self.var_size).grid(
                row=i, column=0, sticky="w", padx=6, pady=4
            )

        # Action buttons for order
        order_actions = ttk.Frame(order, style="Section.TLabelframe")
        order_actions.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        order_actions.columnconfigure(0, weight=1)
        order_actions.columnconfigure(1, weight=1)
        order_actions.columnconfigure(2, weight=1)

        ttk.Button(order_actions, text="Brew ☕", style="Accent.TButton", command=self._brew).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(order_actions, text="Show Price 💵", command=self._show_price).grid(
            row=0, column=1, sticky="ew", padx=6
        )
        ttk.Button(order_actions, text="Need Cups?", command=self._need_cups_hint).grid(
            row=0, column=2, sticky="ew", padx=(6, 0)
        )

        # --- Fill Machine Section ---
        fill = ttk.Labelframe(left, text=" Fill the Machine ", style="Section.TLabelframe")
        fill.grid(row=1, column=0, sticky="nsew")
        fill.columnconfigure(1, weight=1)

        # Stock overview (numbers + progress bars)
        self._mk_stock_row(fill, 0, "Water (ml)", "water", MAX_WATER)
        self._mk_stock_row(fill, 1, "Milk (ml)", "milk", MAX_MILK)
        self._mk_stock_row(fill, 2, "Coffee Beans (g)", "coffee_beans", MAX_BEANS)
        self._mk_stock_row(fill, 3, "Cups (units)", "cups", MAX_CUPS)

        # Refill buttons
        btns = ttk.Frame(fill, style="Section.TLabelframe")
        btns.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(12, 0))
        for i in range(5):
            btns.columnconfigure(i, weight=1)

        ttk.Button(btns, text="Refill Water", command=self._refill_water).grid(row=0, column=0, sticky="ew", padx=4)
        ttk.Button(btns, text="Refill Milk", command=self._refill_milk).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(btns, text="Refill Beans", command=self._refill_beans).grid(row=0, column=2, sticky="ew", padx=4)
        ttk.Button(btns, text="Refill Cups", command=self._refill_cups).grid(row=0, column=3, sticky="ew", padx=4)
        ttk.Button(btns, text="Fill All ♻️", style="Accent.TButton", command=self._fill_all).grid(row=0, column=4, sticky="ew", padx=4)

        # --- Sales / Data Section ---
        data = ttk.Labelframe(right, text=" Data & Sales ", style="Section.TLabelframe")
        data.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        data.rowconfigure(1, weight=1)
        data.columnconfigure(0, weight=1)

        # Money quick actions (withdraw/donate)
        money_bar = ttk.Frame(data, style="Section.TLabelframe")
        money_bar.grid(row=0, column=0, sticky="ew")
        money_bar.columnconfigure(1, weight=1)
        ttk.Label(money_bar, text="Balance:").grid(row=0, column=0, sticky="w")
        self.lbl_money = ttk.Label(money_bar, text="$0.00")
        self.lbl_money.grid(row=0, column=1, sticky="w", padx=(6, 0))
        ttk.Button(money_bar, text="Withdraw", style="Danger.TButton", command=self._withdraw_money).grid(row=0, column=2, padx=6)
        ttk.Button(money_bar, text="Donate", style="Accent.TButton", command=self._donate_money).grid(row=0, column=3)

        # Sales history table
        self.tree = ttk.Treeview(data, columns=("coffee", "size", "price"), show="headings", height=10)
        self.tree.heading("coffee", text="Coffee")
        self.tree.heading("size", text="Size")
        self.tree.heading("price", text="Unit Price")
        self.tree.column("coffee", width=160, anchor="w")
        self.tree.column("size", width=100, anchor="center")
        self.tree.column("price", width=120, anchor="e")
        self.tree.grid(row=1, column=0, sticky="nsew", pady=(8, 0))

        # Totals
        totals = ttk.Frame(data, style="Section.TLabelframe")
        totals.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        totals.columnconfigure(1, weight=1)
        ttk.Label(totals, text="Total sales:").grid(row=0, column=0, sticky="w")
        self.lbl_total_sales = ttk.Label(totals, text="0")
        self.lbl_total_sales.grid(row=0, column=1, sticky="w", padx=(6, 0))
        ttk.Label(totals, text="Total revenue:").grid(row=0, column=2, sticky="w", padx=(12, 0))
        self.lbl_total_revenue = ttk.Label(totals, text="$0.00")
        self.lbl_total_revenue.grid(row=0, column=3, sticky="w", padx=(6, 0))

        # --- Log Section ---
        log = ttk.Labelframe(right, text=" Messages ", style="Section.TLabelframe")
        log.grid(row=1, column=0, sticky="nsew")
        log.rowconfigure(0, weight=1)
        log.columnconfigure(0, weight=1)

        self.txt_log = tk.Text(
            log, height=8, wrap="word", font=("Consolas", 10),
            bg="#0f1115", fg=PALETTE["text"], insertbackground=PALETTE["text"],
            highlightthickness=0, bd=0
        )
        self.txt_log.grid(row=0, column=0, sticky="nsew")
        sbr = ttk.Scrollbar(log, command=self.txt_log.yview)
        sbr.grid(row=0, column=1, sticky="ns")
        self.txt_log.config(yscrollcommand=sbr.set)
        # Log tags
        self.txt_log.tag_configure("ok", foreground=PALETTE["ok"])
        self.txt_log.tag_configure("warn", foreground=PALETTE["warn"])
        self.txt_log.tag_configure("err", foreground=PALETTE["danger"])
        self.txt_log.tag_configure("muted", foreground=PALETTE["muted"])

        # Footer status
        self.status = ttk.Label(self, style="Status.TLabel", anchor="w")
        self.status.grid(row=2, column=0, columnspan=2, sticky="ew", padx=18, pady=(0, 12))

    # ----------------------------- Helpers (stock rows) ----------------------------- #
    def _mk_stock_row(self, parent, row, title, key, max_value):
        """Create a labeled row with current value and a progress bar for a stock key."""
        ttk.Label(parent, text=title).grid(row=row, column=0, sticky="w", pady=4)
        lbl = ttk.Label(parent, text="0")
        lbl.grid(row=row, column=1, sticky="w", pady=4)
        bar = ttk.Progressbar(parent, orient="horizontal", mode="determinate", maximum=max_value, length=220)
        bar.grid(row=row, column=2, sticky="w", pady=4, padx=(12, 0))
        setattr(self, f"lbl_{key}", lbl)
        setattr(self, f"bar_{key}", bar)

    # ----------------------------- Actions: Order ----------------------------- #
    def _show_price(self):
        """Show price using Coffee.price (or .precio) for the current selection."""
        try:
            coffee = Coffee(self.var_type.get(), self.var_size.get())
            price = getattr(coffee, "price", None)
            if price is None:
                price = getattr(coffee, "precio", None)
            if price is None:
                self._log("ℹ️ Price not available on Coffee object.", tag="warn")
                messagebox.showinfo("Price", "Price not available.")
            else:
                self._log(f"💵 Price: {price} u", tag="ok")
                messagebox.showinfo("Price", f"{self.var_size.get().title()} {self.var_type.get().title()}: {price} u")
        except Exception as e:
            self._log(f"Could not get price: {e}", tag="err")
            messagebox.showerror("Price", f"Could not get price:\n{e}")

    def _need_cups_hint(self):
        self._log("Remember: each coffee uses one cup. Refill cups if needed.", tag="muted")
        messagebox.showinfo("Cups", "Each coffee uses one cup.\nRefill cups if needed.")

    def _brew(self):
        """Mimic the CLI logic for ordering coffee."""
        coffee_type = self.var_type.get()
        size = self.var_size.get()

        # Cup availability (CLI behavior)
        if self.stock.stock.get("cups", 0) <= 0:
            self._log("No cups available. Please refill the machine.", tag="err")
            messagebox.showwarning("Cups", "No cups available. Please refill the machine.")
            return
        else:
            self.stock.stock["cups"] -= 1

        # Create Coffee object
        try:
            coffee = Coffee(coffee_type, size)
        except Exception as e:
            self._log(f"Could not create coffee: {e}", tag="err")
            messagebox.showerror("Order", f"Could not create coffee:\n{e}")
            return

        # Record sale (like CLI)
        unit_price = getattr(coffee, "price", None)
        if unit_price is None:
            unit_price = getattr(coffee, "precio", None)
        if unit_price is None:
            unit_price = 0.0
        self.sells.append((coffee_type, size))
        self.sells_unit_cost.append(unit_price)
        self.money += float(unit_price)

        self._log(f"You selected a {size} {coffee_type}.", tag="muted")

        # Ingredient check & deduction
        ingredients_needed = getattr(coffee, "ingredients", None)
        if ingredients_needed is None:
            ingredients_needed = getattr(coffee, "ingredientes", None)

        available, output = self.stock.check_ingredients(ingredients_needed)
        self._log(output, tag=("ok" if available else "warn"))

        if available:
            self._log(f"Preparing your {size} {coffee_type}...", tag="muted")
            self.stock.take_ingredients(ingredients_needed)
            self._log(f"Your {size} {coffee_type} is ready! ✅", tag="ok")
        else:
            self._log("Not enough ingredients. Please refill or choose another drink.", tag="err")
            messagebox.showwarning("Order", "Not enough ingredients. Please refill or choose another drink.")

        # Refresh UI
        self._render_all()

    # ----------------------------- Actions: Fill Machine ----------------------------- #
    def _refill_water(self):
        current = self.stock.stock.get("water", 0)
        if current >= MAX_WATER:
            self._log("Water tank is already full.", tag="warn")
            return
        add = MAX_WATER - current
        self.stock.stock["water"] = MAX_WATER
        self._log(f"Refilled water by {add} ml.", tag="ok")
        self._render_all()

    def _refill_milk(self):
        current = self.stock.stock.get("milk", 0)
        if current >= MAX_MILK:
            self._log("Milk tank is already full.", tag="warn")
            return
        add = MAX_MILK - current
        self.stock.stock["milk"] = MAX_MILK
        self._log(f"Refilled milk by {add} ml.", tag="ok")
        self._render_all()

    def _refill_beans(self):
        current = self.stock.stock.get("coffee_beans", 0)
        if current >= MAX_BEANS:
            self._log("Coffee beans tank is already full.", tag="warn")
            return
        add = MAX_BEANS - current
        self.stock.stock["coffee_beans"] = MAX_BEANS
        self._log(f"Refilled coffee beans by {add} g.", tag="ok")
        self._render_all()

    def _refill_cups(self):
        current = self.stock.stock.get("cups", 0)
        if current >= MAX_CUPS:
            self._log("Cups tank is already full.", tag="warn")
            return
        add = MAX_CUPS - current
        self.stock.stock["cups"] = MAX_CUPS
        self._log(f"Refilled cups by {add} units.", tag="ok")
        self._render_all()

    def _fill_all(self):
        self._refill_water()
        self._refill_milk()
        self._refill_beans()
        self._refill_cups()
        self._log("All ingredients refill complete.", tag="ok")

    # ----------------------------- Actions: Money ----------------------------- #
    def _withdraw_money(self):
        """Implements the same flow as CLI (no donation branch)."""
        if self.money <= 0:
            self._log("No money to withdraw.", tag="warn")
            messagebox.showinfo("Withdraw", "No money to withdraw.")
            return

        # Ask if they want to withdraw
        amount_str = simpledialog.askstring("Withdraw", f"Current balance: ${self.money:.2f}\nEnter amount to withdraw:")
        if amount_str is None:
            return
        try:
            amount = float(amount_str)
        except ValueError:
            self._log("Invalid input, please enter a number.", tag="err")
            messagebox.showerror("Withdraw", "Invalid input, please enter a number.")
            return

        if amount > self.money:
            self._log("Insufficient funds.", tag="err")
            messagebox.showwarning("Withdraw", "Insufficient funds.")
            return
        if amount < 0:
            self._log("Please enter a positive number.", tag="err")
            messagebox.showwarning("Withdraw", "Please enter a positive number.")
            return

        self.money -= amount
        self._log(f"Withdrew ${amount:.2f}. Current amount: ${self.money:.2f}", tag="ok")
        self._render_money()

    def _donate_money(self):
        """Donation branch (matches CLI donate path)."""
        if self.money <= 0:
            self._log("No money available to donate.", tag="warn")
            messagebox.showinfo("Donate", "No money available to donate.")
            return

        amount_str = simpledialog.askstring("Donate", f"Current balance: ${self.money:.2f}\nEnter donation amount:")
        if amount_str is None:
            return
        try:
            amount = float(amount_str)
        except ValueError:
            self._log("Invalid input, please enter a number.", tag="err")
            messagebox.showerror("Donate", "Invalid input, please enter a number.")
            return

        if amount > self.money:
            self._log("Insufficient funds for donation.", tag="err")
            messagebox.showwarning("Donate", "Insufficient funds for donation.")
            return
        if amount < 0:
            self._log("Please enter a positive number.", tag="err")
            messagebox.showwarning("Donate", "Please enter a positive number.")
            return

        self.money -= amount
        self._log(f"Thank you for your donation of ${amount:.2f}.", tag="ok")
        self._render_money()

    # ----------------------------- Actions: Show Data ----------------------------- #
    def _render_sales(self):
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Insert sales
        for coffee, size, price in zip(self.sells, [s for s in self.sells], self.sells_unit_cost):
            # coffee is tuple (type, size); we will rely on self.sells directly below
            pass  # placeholder (we will fill using enumerate)

        for i, ((coffee_type, size), price) in enumerate(zip(self.sells, self.sells_unit_cost), start=1):
            self.tree.insert("", "end", values=(coffee_type.title(), size.title(), f"{price:.2f} u"))

        # Totals
        total_sales = len(self.sells_unit_cost)
        total_revenue = sum(self.sells_unit_cost) if self.sells_unit_cost else 0.0
        self.lbl_total_sales.config(text=str(total_sales))
        self.lbl_total_revenue.config(text=f"${total_revenue:.2f}")

    # ----------------------------- Rendering helpers ----------------------------- #
    def _render_stock(self):
        # Labels and progress bars
        w = self.stock.stock.get("water", 0)
        m = self.stock.stock.get("milk", 0)
        b = self.stock.stock.get("coffee_beans", 0)
        c = self.stock.stock.get("cups", 0)
        self.lbl_water.config(text=f"{w} ml")
        self.lbl_milk.config(text=f"{m} ml")
        self.lbl_coffee_beans.config(text=f"{b} g")
        self.lbl_cups.config(text=f"{c} units")
        self.bar_water["value"] = min(w, MAX_WATER)
        self.bar_milk["value"] = min(m, MAX_MILK)
        self.bar_coffee_beans["value"] = min(b, MAX_BEANS)
        self.bar_cups["value"] = min(c, MAX_CUPS)

    def _render_money(self):
        self.lbl_money.config(text=f"${self.money:.2f}")

    def _render_all(self):
        self._render_stock()
        self._render_money()
        self._render_sales()
        self._update_status()

    def _update_status(self):
        self.status.config(
            text=f"Selection: {self.var_size.get().title()} {self.var_type.get().title()}   |   "
                 f"Balance: ${self.money:.2f}   |   Cups: {self.stock.stock.get('cups', 0)}"
        )

    # ----------------------------- Logging ----------------------------- #
    def _log(self, text, tag=None):
        if tag:
            self.txt_log.insert("end", text.strip() + "\n", tag)
        else:
            self.txt_log.insert("end", text.strip() + "\n")
        self.txt_log.see("end")


# -------------------------------- Entry Point -------------------------------- #
def main():
    app = CoffeeMachineApp()
    # Add a top-level "Exit" menu, to mirror CLI "Exit" option elegantly
    menubar = tk.Menu(app)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=app.destroy)
    menubar.add_cascade(label="File", menu=filemenu)
    app.config(menu=menubar)
    app.mainloop()

if __name__ == "__main__":
    main()
