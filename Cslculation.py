import tkinter as tk
from tkinter import ttk, messagebox
import math


class EnergyMeterCalculator:

    def __init__(self, root):

        self.root = root
        self.root.title("1-Phase Energy Meter Calculator")
        self.root.geometry("1250x850")
        self.root.minsize(1100, 750)

        # =========================================================
        # COLORS
        # =========================================================

        self.BLUE = "#0645AD"
        self.DARK_BLUE = "#073B8C"
        self.LIGHT_BLUE = "#EAF4FF"
        self.WHITE = "#FFFFFF"

        self.GREEN = "#DDF8E8"
        self.GREEN_TEXT = "#087A43"

        self.YELLOW = "#FFF5CC"
        self.YELLOW_TEXT = "#8A6500"

        self.PURPLE = "#F5E5FF"
        self.PURPLE_TEXT = "#7020A0"

        self.BORDER = "#B7D4F5"
        self.TEXT = "#172033"
        self.GRAY = "#667085"

        self.root.configure(bg="#F5F8FC")

        # =========================================================
        # INPUT VARIABLES
        # =========================================================

        self.voltage_var = tk.StringVar(value="230")
        self.current_var = tk.StringVar(value="5")

        self.pf_type_var = tk.StringVar(value="Direct PF")
        self.pf_value_var = tk.StringVar(value="0.8")

        self.time_var = tk.StringVar(value="3600")
        self.md_interval_var = tk.StringVar(value="900")

        # =========================================================
        # OUTPUT VARIABLES
        # =========================================================

        self.active_power_var = tk.StringVar(value="0.000 W")
        self.reactive_power_var = tk.StringVar(value="0.000 VAR")
        self.apparent_power_var = tk.StringVar(value="0.000 VA")

        self.pf_var = tk.StringVar(value="0.00000")
        self.angle_var = tk.StringVar(value="0.000°")

        self.active_energy_var = tk.StringVar(value="0.00000 kWh")
        self.reactive_energy_var = tk.StringVar(value="0.00000 kVARh")
        self.apparent_energy_var = tk.StringVar(value="0.00000 kVAh")

        self.active_md_var = tk.StringVar(value="0.000 kW")
        self.reactive_md_var = tk.StringVar(value="0.000 kVAR")
        self.apparent_md_var = tk.StringVar(value="0.000 kVA")

        self.create_styles()
        self.create_ui()

        self.calculate()

    # =========================================================
    # STYLES
    # =========================================================

    def create_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8)
        )

        style.configure(
            "TCombobox",
            font=("Segoe UI", 10)
        )

        style.configure(
            "TEntry",
            font=("Segoe UI", 10)
        )

    # =========================================================
    # MAIN UI
    # =========================================================

    def create_ui(self):

        # ======================================================
        # HEADER
        # ======================================================

        header = tk.Frame(
            self.root,
            bg=self.DARK_BLUE,
            height=105
        )

        header.pack(
            fill="x",
            side="top"
        )

        header.pack_propagate(False)

        # Meter icon
        icon = tk.Label(
            header,
            text="⚡",
            font=("Segoe UI", 38),
            fg="#FFD21F",
            bg=self.DARK_BLUE
        )

        icon.pack(
            side="left",
            padx=(30, 15)
        )

        title_frame = tk.Frame(
            header,
            bg=self.DARK_BLUE
        )

        title_frame.pack(
            side="left",
            pady=15
        )

        tk.Label(
            title_frame,
            text="1-PHASE ENERGY METER CALCULATOR",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg=self.DARK_BLUE
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_frame,
            text="Power  |  Energy  |  Maximum Demand (MD)",
            font=("Segoe UI", 12),
            fg="#A8D3FF",
            bg=self.DARK_BLUE
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # ======================================================
        # MAIN AREA
        # ======================================================

        main = tk.Frame(
            self.root,
            bg="#F5F8FC"
        )

        main.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18
        )

        # Left column
        left = tk.Frame(
            main,
            bg="#F5F8FC",
            width=390
        )

        left.pack(
            side="left",
            fill="y",
            padx=(0, 12)
        )

        # Right column
        right = tk.Frame(
            main,
            bg="#F5F8FC"
        )

        right.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.create_input_panel(left)

        self.create_power_panel(right)

        self.create_energy_panel(right)

        self.create_md_panel(right)

        self.create_formula_panel()

    # =========================================================
    # INPUT PANEL
    # =========================================================

    def create_input_panel(self, parent):

        panel = tk.Frame(
            parent,
            bg="white",
            highlightbackground=self.BLUE,
            highlightthickness=2
        )

        panel.pack(
            fill="both",
            expand=True
        )

        # Header
        header = tk.Frame(
            panel,
            bg=self.BLUE,
            height=52
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="⚙",
            font=("Segoe UI", 22),
            bg=self.BLUE,
            fg="white"
        ).pack(
            side="left",
            padx=(18, 8)
        )

        tk.Label(
            header,
            text="Meter Input",
            font=("Segoe UI", 16, "bold"),
            bg=self.BLUE,
            fg="white"
        ).pack(
            side="left"
        )

        body = tk.Frame(
            panel,
            bg="white"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=20
        )

        # ======================================================
        # Voltage
        # ======================================================

        self.create_input_row(
            body,
            "Voltage (V)",
            self.voltage_var,
            0,
            "V"
        )

        # ======================================================
        # Current
        # ======================================================

        self.create_input_row(
            body,
            "Current (A)",
            self.current_var,
            1,
            "A"
        )

        # ======================================================
        # PF TYPE
        # ======================================================

        tk.Label(
            body,
            text="Power Factor",
            font=("Segoe UI", 10),
            bg="white",
            fg=self.TEXT
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=8
        )

        pf_combo = ttk.Combobox(
            body,
            textvariable=self.pf_type_var,
            values=[
                "Direct PF",
                "Angle",
                "Quadrature PF"
            ],
            state="readonly",
            width=19
        )

        pf_combo.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=8
        )

        pf_combo.bind(
            "<<ComboboxSelected>>",
            self.update_pf_label
        )

        # ======================================================
        # PF VALUE
        # ======================================================

        self.pf_label = tk.Label(
            body,
            text="Value",
            font=("Segoe UI", 10),
            bg="white",
            fg=self.TEXT
        )

        self.pf_label.grid(
            row=3,
            column=0,
            sticky="w",
            pady=8
        )

        ttk.Entry(
            body,
            textvariable=self.pf_value_var,
            width=22
        ).grid(
            row=3,
            column=1,
            sticky="ew",
            pady=8
        )

        # ======================================================
        # TIME
        # ======================================================

        self.create_input_row(
            body,
            "Time",
            self.time_var,
            4,
            "Seconds"
        )

        # ======================================================
        # MD INTERVAL
        # ======================================================

        tk.Label(
            body,
            text="MD Interval",
            font=("Segoe UI", 10),
            bg="white",
            fg=self.TEXT
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=8
        )

        md_combo = ttk.Combobox(
            body,
            textvariable=self.md_interval_var,
            values=[
                "900",
                "1800",
                "3600"
            ],
            state="readonly",
            width=19
        )

        md_combo.grid(
            row=5,
            column=1,
            sticky="ew",
            pady=8
        )

        tk.Label(
            body,
            text="seconds",
            font=("Segoe UI", 9),
            fg=self.BLUE,
            bg="white"
        ).grid(
            row=5,
            column=2,
            padx=(6, 0)
        )

        # ======================================================
        # BUTTONS
        # ======================================================

        button_frame = tk.Frame(
            body,
            bg="white"
        )

        button_frame.grid(
            row=6,
            column=0,
            columnspan=3,
            pady=(25, 5)
        )

        calculate_button = tk.Button(
            button_frame,
            text="▣  CALCULATE",
            command=self.calculate,
            bg="#0969F5",
            fg="white",
            activebackground="#0757D4",
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=10
        )

        calculate_button.pack(
            side="left",
            padx=(0, 10)
        )

        reset_button = tk.Button(
            button_frame,
            text="↻  RESET",
            command=self.reset,
            bg="white",
            fg=self.BLUE,
            activebackground="#EEF6FF",
            font=("Segoe UI", 11, "bold"),
            relief="solid",
            borderwidth=1,
            cursor="hand2",
            padx=25,
            pady=9
        )

        reset_button.pack(
            side="left"
        )

        # ======================================================
        # INFO
        # ======================================================

        info = tk.Label(
            body,
            text=(
                "5–30 A  |  1-Phase 2-Wire\n"
                "Recommended MD interval: 900 seconds (15 min)"
            ),
            font=("Segoe UI", 9),
            fg=self.GRAY,
            bg="white",
            justify="center"
        )

        info.grid(
            row=7,
            column=0,
            columnspan=3,
            pady=(20, 0)
        )

        body.columnconfigure(1, weight=1)

    # =========================================================
    # INPUT ROW
    # =========================================================

    def create_input_row(
        self,
        parent,
        label,
        variable,
        row,
        unit
    ):

        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 10),
            bg="white",
            fg=self.TEXT
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=8
        )

        ttk.Entry(
            parent,
            textvariable=variable,
            width=22
        ).grid(
            row=row,
            column=1,
            sticky="ew",
            pady=8
        )

        tk.Label(
            parent,
            text=unit,
            font=("Segoe UI", 9),
            fg=self.BLUE,
            bg="white"
        ).grid(
            row=row,
            column=2,
            padx=(6, 0)
        )

    # =========================================================
    # POWER PANEL
    # =========================================================

    def create_power_panel(self, parent):

        panel = tk.Frame(
            parent,
            bg="white",
            highlightbackground=self.BLUE,
            highlightthickness=2
        )

        panel.pack(
            fill="x",
            pady=(0, 12)
        )

        header = self.section_header(
            panel,
            "⚡",
            "Power Calculation"
        )

        header.pack(
            fill="x"
        )

        cards = tk.Frame(
            panel,
            bg="white"
        )

        cards.pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.create_card(
            cards,
            "Active Power",
            self.active_power_var,
            "#DFF1FF",
            "#0B5CAD"
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.create_card(
            cards,
            "Reactive Power",
            self.reactive_power_var,
            "#EFE3FF",
            "#6D22A8"
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.create_card(
            cards,
            "Apparent Power",
            self.apparent_power_var,
            "#E2F2FF",
            "#07549A"
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        # PF row
        pf_frame = tk.Frame(
            panel,
            bg=self.GREEN
        )

        pf_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        tk.Label(
            pf_frame,
            text="⚡  Power Factor",
            font=("Segoe UI", 11, "bold"),
            fg=self.GREEN_TEXT,
            bg=self.GREEN
        ).pack(
            side="left",
            padx=15,
            pady=10
        )

        tk.Label(
            pf_frame,
            textvariable=self.pf_var,
            font=("Segoe UI", 13, "bold"),
            fg="#111827",
            bg=self.GREEN
        ).pack(
            side="left",
            padx=10
        )

        tk.Frame(
            pf_frame,
            bg="#8AD6AA",
            width=2,
            height=35
        ).pack(
            side="left",
            padx=25
        )

        tk.Label(
            pf_frame,
            text="∠  PF Angle",
            font=("Segoe UI", 11, "bold"),
            fg=self.GREEN_TEXT,
            bg=self.GREEN
        ).pack(
            side="left"
        )

        tk.Label(
            pf_frame,
            textvariable=self.angle_var,
            font=("Segoe UI", 13, "bold"),
            fg="#111827",
            bg=self.GREEN
        ).pack(
            side="left",
            padx=15
        )

    # =========================================================
    # ENERGY PANEL
    # =========================================================

    def create_energy_panel(self, parent):

        panel = tk.Frame(
            parent,
            bg="white",
            highlightbackground=self.BLUE,
            highlightthickness=2
        )

        panel.pack(
            fill="x",
            pady=(0, 12)
        )

        self.section_header(
            panel,
            "⚡",
            "Energy Calculation"
        ).pack(
            fill="x"
        )

        cards = tk.Frame(
            panel,
            bg="white"
        )

        cards.pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.create_card(
            cards,
            "Active Energy",
            self.active_energy_var,
            self.YELLOW,
            self.YELLOW_TEXT
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.create_card(
            cards,
            "Reactive Energy",
            self.reactive_energy_var,
            "#F1E4FF",
            self.PURPLE_TEXT
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.create_card(
            cards,
            "Apparent Energy",
            self.apparent_energy_var,
            "#FFF4D5",
            "#785400"
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

    # =========================================================
    # MD PANEL
    # =========================================================

    def create_md_panel(self, parent):

        panel = tk.Frame(
            parent,
            bg="white",
            highlightbackground=self.BLUE,
            highlightthickness=2
        )

        panel.pack(
            fill="x",
            pady=(0, 12)
        )

        self.section_header(
            panel,
            "▥",
            "Maximum Demand (MD)"
        ).pack(
            fill="x"
        )

        cards = tk.Frame(
            panel,
            bg="white"
        )

        cards.pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.create_card(
            cards,
            "Active MD",
            self.active_md_var,
            "#F8E6FF",
            "#76249F"
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.create_card(
            cards,
            "Reactive MD",
            self.reactive_md_var,
            "#F8E6FF",
            "#76249F"
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.create_card(
            cards,
            "Apparent MD",
            self.apparent_md_var,
            "#F8E6FF",
            "#76249F"
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

    # =========================================================
    # SECTION HEADER
    # =========================================================

    def section_header(
        self,
        parent,
        icon,
        title
    ):

        frame = tk.Frame(
            parent,
            bg=self.BLUE,
            height=48
        )

        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=icon,
            font=("Segoe UI", 20),
            bg=self.BLUE,
            fg="white"
        ).pack(
            side="left",
            padx=(15, 10)
        )

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 15, "bold"),
            bg=self.BLUE,
            fg="white"
        ).pack(
            side="left"
        )

        return frame

    # =========================================================
    # CARD
    # =========================================================

    def create_card(
        self,
        parent,
        title,
        variable,
        bg,
        title_color
    ):

        frame = tk.Frame(
            parent,
            bg=bg,
            highlightbackground="#C8D8EA",
            highlightthickness=1
        )

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 10, "bold"),
            fg=title_color,
            bg=bg
        ).pack(
            pady=(12, 5)
        )

        tk.Label(
            frame,
            textvariable=variable,
            font=("Segoe UI", 14, "bold"),
            fg="#101828",
            bg=bg
        ).pack(
            pady=(0, 12),
            padx=8
        )

        return frame

    # =========================================================
    # FORMULA PANEL
    # =========================================================

    def create_formula_panel(self):

        panel = tk.Frame(
            self.root,
            bg="white",
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        panel.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        header = tk.Frame(
            panel,
            bg=self.BLUE,
            height=42
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="ⓘ   Formulas",
            font=("Segoe UI", 13, "bold"),
            bg=self.BLUE,
            fg="white"
        ).pack(
            side="left",
            padx=15
        )

        body = tk.Frame(
            panel,
            bg="#F8FBFF"
        )

        body.pack(
            fill="x",
            padx=15,
            pady=10
        )

        left_text = (
            "Active Power (P):       P = V × I × PF\n"
            "Apparent Power (S):     S = V × I\n"
            "Reactive Power (Q):     Q = √(S² − P²)\n"
            "Angle PF:                PF = cos(θ)\n"
            "Quadrature PF:           PF = 1 / √(1 + (Q/P)²)"
        )

        right_text = (
            "Energy:\n"
            "E = Power × (Time / 3600)\n\n"
            "Maximum Demand:\n"
            "MD = Block Energy × (3600 / MD Interval)"
        )

        tk.Label(
            body,
            text=left_text,
            font=("Segoe UI", 9),
            bg="#F8FBFF",
            fg=self.TEXT,
            justify="left"
        ).pack(
            side="left",
            anchor="w",
            padx=10
        )

        separator = tk.Frame(
            body,
            bg="#BCD0E8",
            width=1,
            height=105
        )

        separator.pack(
            side="left",
            padx=35
        )

        tk.Label(
            body,
            text=right_text,
            font=("Segoe UI", 9),
            bg="#F8FBFF",
            fg=self.TEXT,
            justify="left"
        ).pack(
            side="left",
            anchor="w"
        )

    # =========================================================
    # UPDATE PF LABEL
    # =========================================================

    def update_pf_label(self, event=None):

        pf_type = self.pf_type_var.get()

        if pf_type == "Direct PF":
            self.pf_label.config(text="Value")

        elif pf_type == "Angle":
            self.pf_label.config(text="Angle (°)")

        elif pf_type == "Quadrature PF":
            self.pf_label.config(text="Q / P")

    # =========================================================
    # CALCULATE
    # =========================================================

    def calculate(self):

        try:

            V = float(self.voltage_var.get())
            I = float(self.current_var.get())
            value = float(self.pf_value_var.get())

            time_seconds = float(
                self.time_var.get()
            )

            md_interval = float(
                self.md_interval_var.get()
            )

            pf_type = self.pf_type_var.get()

            # --------------------------------------------------
            # VALIDATION
            # --------------------------------------------------

            if V <= 0:
                raise ValueError(
                    "Voltage must be greater than 0."
                )

            if I < 0:
                raise ValueError(
                    "Current cannot be negative."
                )

            if time_seconds <= 0:
                raise ValueError(
                    "Time must be greater than 0."
                )

            if md_interval <= 0:
                raise ValueError(
                    "MD interval must be greater than 0."
                )

            # --------------------------------------------------
            # POWER FACTOR
            # --------------------------------------------------

            if pf_type == "Direct PF":

                PF = value

                if PF < -1 or PF > 1:
                    raise ValueError(
                        "PF must be between -1 and +1."
                    )

            elif pf_type == "Angle":

                angle_input = value

                if angle_input < -180 or angle_input > 180:
                    raise ValueError(
                        "Angle must be between -180° and +180°."
                    )

                PF = math.cos(
                    math.radians(angle_input)
                )

            else:

                # Quadrature PF
                Q_by_P = value

                PF = 1 / math.sqrt(
                    1 + Q_by_P ** 2
                )

            # --------------------------------------------------
            # APPARENT POWER
            # --------------------------------------------------

            S = V * I

            # --------------------------------------------------
            # ACTIVE POWER
            # --------------------------------------------------

            P = S * PF

            # --------------------------------------------------
            # REACTIVE POWER
            # --------------------------------------------------

            Q = math.sqrt(
                max(
                    0,
                    S ** 2 - P ** 2
                )
            )

            # --------------------------------------------------
            # PF ANGLE
            # --------------------------------------------------

            angle = math.degrees(
                math.acos(
                    max(-1, min(1, abs(PF)))
                )
            )

            # --------------------------------------------------
            # TIME
            # --------------------------------------------------

            time_hours = (
                time_seconds / 3600
            )

            # --------------------------------------------------
            # ENERGY
            # --------------------------------------------------

            active_energy = (
                abs(P) / 1000
            ) * time_hours

            reactive_energy = (
                Q / 1000
            ) * time_hours

            apparent_energy = (
                S / 1000
            ) * time_hours

            # --------------------------------------------------
            # MD
            # --------------------------------------------------

            md_hours = (
                md_interval / 3600
            )

            # Energy consumed during ONE MD block
            active_block_energy = (
                abs(P) / 1000
            ) * md_hours

            reactive_block_energy = (
                Q / 1000
            ) * md_hours

            apparent_block_energy = (
                S / 1000
            ) * md_hours

            # Average power over block
            active_md = (
                active_block_energy /
                md_hours
            )

            reactive_md = (
                reactive_block_energy /
                md_hours
            )

            apparent_md = (
                apparent_block_energy /
                md_hours
            )

            # --------------------------------------------------
            # DISPLAY POWER
            # --------------------------------------------------

            self.active_power_var.set(
                f"{P:.3f} W\n({P/1000:.3f} kW)"
            )

            self.reactive_power_var.set(
                f"{Q:.3f} VAR\n({Q/1000:.3f} kVAR)"
            )

            self.apparent_power_var.set(
                f"{S:.3f} VA\n({S/1000:.3f} kVA)"
            )

            self.pf_var.set(
                f"{PF:.5f}"
            )

            self.angle_var.set(
                f"{angle:.3f}°"
            )

            # --------------------------------------------------
            # DISPLAY ENERGY
            # --------------------------------------------------

            self.active_energy_var.set(
                f"{active_energy:.5f} kWh"
            )

            self.reactive_energy_var.set(
                f"{reactive_energy:.5f} kVARh"
            )

            self.apparent_energy_var.set(
                f"{apparent_energy:.5f} kVAh"
            )

            # --------------------------------------------------
            # DISPLAY MD
            # --------------------------------------------------

            self.active_md_var.set(
                f"{active_md:.3f} kW"
            )

            self.reactive_md_var.set(
                f"{reactive_md:.3f} kVAR"
            )

            self.apparent_md_var.set(
                f"{apparent_md:.3f} kVA"
            )

        except Exception as e:

            messagebox.showerror(
                "Calculation Error",
                str(e)
            )

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.voltage_var.set("230")
        self.current_var.set("5")
        self.pf_type_var.set("Direct PF")
        self.pf_value_var.set("0.8")
        self.time_var.set("3600")
        self.md_interval_var.set("900")

        self.update_pf_label()

        self.calculate()


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = EnergyMeterCalculator(root)

    root.mainloop()
