import tkinter as tk
from tkinter import ttk, messagebox
import math


class SinglePhaseEnergyMeter:

    def __init__(self, root):

        self.root = root
        self.root.title("1-Phase Energy Meter Calculator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # ==========================
        # INPUT VARIABLES
        # ==========================

        self.voltage = tk.StringVar(value="230")
        self.current = tk.StringVar(value="5")
        self.pf = tk.StringVar(value="0.8")
        self.time = tk.StringVar(value="3600")
        self.md_interval = tk.StringVar(value="15")

        # ==========================
        # RESULT VARIABLES
        # ==========================

        self.active_power = tk.StringVar()
        self.reactive_power = tk.StringVar()
        self.apparent_power = tk.StringVar()

        self.active_energy = tk.StringVar()
        self.reactive_energy = tk.StringVar()
        self.apparent_energy = tk.StringVar()

        self.active_md = tk.StringVar()
        self.reactive_md = tk.StringVar()
        self.apparent_md = tk.StringVar()

        self.create_gui()

    # ============================================================
    # GUI
    # ============================================================

    def create_gui(self):

        canvas = tk.Canvas(self.root, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=scrollable_frame,
            anchor="nw"
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                canvas_window,
                width=event.width
            )
        )

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.columnconfigure(1, weight=1)

        title = ttk.Label(
            scrollable_frame,
            text="1-PHASE ENERGY METER CALCULATOR",
            font=("Arial", 15, "bold")
        )

        title.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=10
        )

        # ========================================================
        # INPUT FRAME
        # ========================================================

        input_frame = ttk.LabelFrame(
            scrollable_frame,
            text="Meter Input",
            padding=8
        )

        input_frame.grid(
            row=1,
            column=0,
            padx=(15, 7),
            pady=10,
            sticky="nsew"
        )

        # Voltage

        ttk.Label(
            input_frame,
            text="Voltage (V):"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        ttk.Entry(
            input_frame,
            textvariable=self.voltage,
            width=20
        ).grid(row=0, column=1, padx=10, pady=5)

        # Current

        ttk.Label(
            input_frame,
            text="Current (A):"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        ttk.Entry(
            input_frame,
            textvariable=self.current,
            width=20
        ).grid(row=1, column=1, padx=10, pady=5)

        # Power Factor

        ttk.Label(
            input_frame,
            text="Power Factor:"
        ).grid(row=2, column=0, padx=10, pady=5, sticky="w")

        ttk.Entry(
            input_frame,
            textvariable=self.pf,
            width=20
        ).grid(row=2, column=1, padx=10, pady=5)

        # Time

        ttk.Label(
            input_frame,
            text="Time (Seconds):"
        ).grid(row=3, column=0, padx=10, pady=5, sticky="w")

        ttk.Entry(
            input_frame,
            textvariable=self.time,
            width=20
        ).grid(row=3, column=1, padx=10, pady=5)

        # IP time

        ttk.Label(
            input_frame,
            text="IP Time (minutes):"
        ).grid(row=4, column=0, padx=10, pady=5, sticky="w")

        md_combo = ttk.Combobox(
            input_frame,
            textvariable=self.md_interval,
            values=["15", "30", "60"],
            state="readonly",
            width=17
        )

        md_combo.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(
            input_frame,
            text="Seconds"
        ).grid(row=4, column=2, padx=5)

        # Calculate Button

        ttk.Button(
            input_frame,
            text="CALCULATE",
            command=self.calculate
        ).grid(
            row=5,
            column=0,
            columnspan=3,
            pady=15
        )

        # ========================================================
        # POWER FRAME
        # ========================================================

        power_frame = ttk.LabelFrame(
            scrollable_frame,
            text="Power Calculation",
            padding=8
        )

        power_frame.grid(
            row=1,
            column=1,
            padx=(7, 12),
            pady=10,
            sticky="nsew"
        )

        ttk.Label(
            power_frame,
            text="Active Power"
        ).grid(row=0, column=0, padx=12, pady=4)

        ttk.Label(
            power_frame,
            textvariable=self.active_power,
            font=("Arial", 11, "bold")
        ).grid(row=0, column=1, padx=15, pady=5)

        ttk.Label(
            power_frame,
            text="Reactive Power"
        ).grid(row=1, column=0, padx=15, pady=5)

        ttk.Label(
            power_frame,
            textvariable=self.reactive_power,
            font=("Arial", 11, "bold")
        ).grid(row=1, column=1, padx=15, pady=5)

        ttk.Label(
            power_frame,
            text="Apparent Power"
        ).grid(row=2, column=0, padx=15, pady=5)

        ttk.Label(
            power_frame,
            textvariable=self.apparent_power,
            font=("Arial", 11, "bold")
        ).grid(row=2, column=1, padx=15, pady=5)

        # ========================================================
        # ENERGY FRAME
        # ========================================================

        energy_frame = ttk.LabelFrame(
            scrollable_frame,
            text="Energy Calculation",
            padding=10
        )

        energy_frame.grid(
            row=2,
            column=0,
            padx=(15, 7),
            pady=3,
            sticky="nsew"
        )

        ttk.Label(
            energy_frame,
            text="Active Energy"
        ).grid(row=0, column=0, padx=15, pady=5)

        ttk.Label(
            energy_frame,
            textvariable=self.active_energy,
            font=("Arial", 11, "bold")
        ).grid(row=0, column=1, padx=15, pady=5)

        ttk.Label(
            energy_frame,
            text="Reactive Energy"
        ).grid(row=1, column=0, padx=15, pady=5)

        ttk.Label(
            energy_frame,
            textvariable=self.reactive_energy,
            font=("Arial", 11, "bold")
        ).grid(row=1, column=1, padx=15, pady=5)

        ttk.Label(
            energy_frame,
            text="Apparent Energy"
        ).grid(row=2, column=0, padx=15, pady=5)

        ttk.Label(
            energy_frame,
            textvariable=self.apparent_energy,
            font=("Arial", 11, "bold")
        ).grid(row=2, column=1, padx=15, pady=5)

        # ========================================================
        # MD FRAME
        # ========================================================

        md_frame = ttk.LabelFrame(
            scrollable_frame,
            text="Maximum Demand",
            padding=10
        )

        md_frame.grid(
            row=2,
            column=1,
            padx=(7, 12),
            pady=5,
            sticky="nsew"
        )

        ttk.Label(
            md_frame,
            text="Active MD"
        ).grid(row=0, column=0, padx=15, pady=5)

        ttk.Label(
            md_frame,
            textvariable=self.active_md,
            font=("Arial", 11, "bold")
        ).grid(row=0, column=1, padx=15, pady=5)

        ttk.Label(
            md_frame,
            text="Reactive MD"
        ).grid(row=1, column=0, padx=15, pady=5)

        ttk.Label(
            md_frame,
            textvariable=self.reactive_md,
            font=("Arial", 11, "bold")
        ).grid(row=1, column=1, padx=15, pady=5)

        ttk.Label(
            md_frame,
            text="Apparent MD"
        ).grid(row=2, column=0, padx=15, pady=5)

        ttk.Label(
            md_frame,
            textvariable=self.apparent_md,
            font=("Arial", 11, "bold")
        ).grid(row=2, column=1, padx=15, pady=5)

        # ========================================================
        # FORMULAS
        # ========================================================

        formula_frame = ttk.LabelFrame(
            scrollable_frame,
            text="Formulas",
            padding=10
        )

        formula_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=15,
            pady=5,
            sticky="ew"
        )

        formulas = (
            "Active Power     P = V × I × PF\n"
            "Apparent Power   S = V × I\n"
            "Reactive Power   Q = √(S² − P²)\n"
            "Energy           E = Power × (Time / 3600)\n"
            "MD               MD = Power × (Running Time / IP Time)"
        )

        ttk.Label(
            formula_frame,
            text=formulas,
            font=("Arial", 9)
        ).pack(fill="x")

    # ============================================================
    # CALCULATION
    # ============================================================

    def calculate(self):

        try:

            # Read inputs

            V = float(self.voltage.get())
            I = float(self.current.get())
            PF = float(self.pf.get())
            running_time_seconds = float(self.time.get())
            md_minutes = float(self.md_interval.get())

            # Validation

            if V <= 0:
                raise ValueError("Voltage must be greater than 0.")

            if I < 0:
                raise ValueError("Current cannot be negative.")

            if PF < -1 or PF > 1:
                raise ValueError(
                    "Power Factor must be between -1 and +1."
                )

            if running_time_seconds < 0:
                raise ValueError(
                    "Time cannot be negative."
                )

            if md_minutes <= 0:
                raise ValueError(
                    "MD interval must be greater than 0."
                )

            time_hours = running_time_seconds / 3600

            # ====================================================
            # POWER
            # ====================================================

            # Apparent Power
            S = V * I

            # Active Power
            P = S * PF

            # Reactive Power
            Q = math.sqrt(
                max(0, S**2 - P**2)
            )

            # ====================================================
            # ENERGY
            # ====================================================

            P_kW = abs(P) / 1000
            Q_kVAR = Q / 1000
            S_kVA = S / 1000

            active_E = P_kW * time_hours
            reactive_E = Q_kVAR * time_hours
            apparent_E = S_kVA * time_hours

            # ====================================================
            # MAXIMUM DEMAND
            # ====================================================

            ip_time_seconds = md_minutes * 60
            running_time_ratio = running_time_seconds / ip_time_seconds

            active_MD = P_kW * running_time_ratio
            reactive_MD = Q_kVAR * running_time_ratio
            apparent_MD = S_kVA * running_time_ratio

            # ====================================================
            # DISPLAY POWER
            # ====================================================

            self.active_power.set(
                f"{P:.3f} W   ({P_kW:.3f} kW)"
            )

            self.reactive_power.set(
                f"{Q:.3f} VAR   ({Q_kVAR:.3f} kVAR)"
            )

            self.apparent_power.set(
                f"{S:.3f} VA   ({S_kVA:.3f} kVA)"
            )

            # ====================================================
            # DISPLAY ENERGY
            # ====================================================

            self.active_energy.set(
                f"{active_E:.6f} kWh"
            )

            self.reactive_energy.set(
                f"{reactive_E:.6f} kVARh"
            )

            self.apparent_energy.set(
                f"{apparent_E:.6f} kVAh"
            )

            # ====================================================
            # DISPLAY MD
            # ====================================================

            self.active_md.set(
                f"{active_MD:.3f} kW"
            )

            self.reactive_md.set(
                f"{reactive_MD:.3f} kVAR"
            )

            self.apparent_md.set(
                f"{apparent_MD:.3f} kVA"
            )

        except ValueError as error:

            messagebox.showerror(
                "Input Error",
                str(error)
            )


# ================================================================
# MAIN PROGRAM
# ================================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SinglePhaseEnergyMeter(root)

    root.mainloop()