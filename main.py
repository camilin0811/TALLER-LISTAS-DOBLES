import tkinter as tk
from tkinter import messagebox


BACKGROUND = "#0f172a"
PANEL = "#1e293b"
TEXT = "#e2e8f0"
ACCENT = "#f97316"
GREEN = "#16a34a"
RED = "#dc2626"
BLUE = "#2563eb"


class Node:

    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1
        return new_node

    def prepend(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.length += 1
        return new_node

    def traverse_to_index(self, index):
        if index < 0 or index >= self.length:
            return None
        if index <= self.length // 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self.length - 1 - index):
                current = current.prev
        return current

    def insert(self, index, value):
        if index <= 0:
            return self.prepend(value)
        if index >= self.length:
            return self.append(value)

        new_node = Node(value)
        leader = self.traverse_to_index(index - 1)
        follower = leader.next

        leader.next = new_node
        new_node.prev = leader
        new_node.next = follower
        follower.prev = new_node

        self.length += 1
        return new_node

    def remove(self, index):
        node = self.traverse_to_index(index)
        if node is None:
            return None

        if node.prev is None:
            self.head = node.next
        else:
            node.prev.next = node.next

        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev

        node.next = None
        node.prev = None
        self.length -= 1
        return node

    def print_list(self):
        values = []
        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values

    def print_list_reverse(self):
        values = []
        current = self.tail
        while current is not None:
            values.append(current.value)
            current = current.prev
        return values

    def index_of(self, node):
        current = self.head
        index = 0
        while current is not None:
            if current is node:
                return index
            current = current.next
            index += 1
        return -1


class AssemblyLineApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Línea de Ensamblaje Automotriz  -  Taller de Listas Dobles")
        self.geometry("1150x720")
        self.configure(bg=BACKGROUND)
        self.minsize(1000, 650)

        self.line = DoublyLinkedList()
        self.current = None
        self.plate = ""

        self.load_default_stations()
        self.build_interface()
        self.refresh()
        self.log("Sistema iniciado. La línea tiene " + str(self.line.length) + " estaciones.")

    def load_default_stations(self):
        stations = [
            "Recepción de chasis",
            "Montaje de motor",
            "Sistema eléctrico",
            "Pintura",
            "Interiores y tablero",
            "Ruedas y frenos",
            "Control de calidad",
        ]
        for station in stations:
            self.line.append(station)

    def build_interface(self):
        header = tk.Frame(self, bg=ACCENT)
        header.pack(fill="x")
        tk.Label(header,
                 text="PLANTA AUTOMOTRIZ   |   Línea de ensamblaje con Lista Doblemente Enlazada",
                 bg=ACCENT, fg="white",
                 font=("Segoe UI", 14, "bold")).pack(pady=14)

        body = tk.Frame(self, bg=BACKGROUND)
        body.pack(fill="both", expand=True, padx=14, pady=12)

        left = tk.LabelFrame(body, text=" LÍNEA DE PRODUCCIÓN (head -> tail) ",
                             bg=PANEL, fg=ACCENT, font=("Segoe UI", 10, "bold"),
                             padx=10, pady=10)
        left.pack(side="left", fill="both", expand=True)

        self.listbox = tk.Listbox(left, bg="#0b1220", fg=TEXT,
                                  font=("Consolas", 12), height=12,
                                  activestyle="none", borderwidth=0,
                                  highlightthickness=0)
        self.listbox.pack(fill="both", expand=True)

        self.summary_label = tk.Label(left, text="", bg=PANEL, fg="#94a3b8",
                                      font=("Consolas", 10), justify="left", anchor="w")
        self.summary_label.pack(fill="x", pady=(8, 0))

        log_frame = tk.LabelFrame(left, text=" BITÁCORA DE PRODUCCIÓN ",
                                  bg=PANEL, fg=ACCENT, font=("Segoe UI", 9, "bold"))
        log_frame.pack(fill="both", expand=True, pady=(10, 0))
        self.log_text = tk.Text(log_frame, height=8, bg="#0b1220", fg="#86efac",
                                font=("Consolas", 9), borderwidth=0,
                                highlightthickness=0, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=4, pady=4)

        right = tk.Frame(body, bg=BACKGROUND)
        right.pack(side="left", fill="y", padx=(14, 0))

        vehicle_frame = tk.LabelFrame(right, text=" VEHÍCULO EN PRODUCCIÓN ",
                                      bg=PANEL, fg=ACCENT, font=("Segoe UI", 10, "bold"),
                                      padx=10, pady=10)
        vehicle_frame.pack(fill="x")

        tk.Label(vehicle_frame, text="Placa / VIN:", bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")
        self.plate_entry = tk.Entry(vehicle_frame, width=14, font=("Consolas", 11))
        self.plate_entry.grid(row=0, column=1, padx=6)
        self.plate_entry.insert(0, "ABC-123")
        tk.Button(vehicle_frame, text="Iniciar producción", bg=BLUE, fg="white",
                  font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
                  command=self.start_vehicle).grid(row=0, column=2, padx=4)

        self.station_label = tk.Label(vehicle_frame, text="Sin vehículo en la línea",
                                      bg=PANEL, fg="#fbbf24",
                                      font=("Segoe UI", 12, "bold"))
        self.station_label.grid(row=1, column=0, columnspan=3, pady=(12, 2), sticky="w")

        pointer_frame = tk.LabelFrame(right, text=" PUNTEROS DEL NODO ACTUAL ",
                                      bg=PANEL, fg=ACCENT, font=("Segoe UI", 10, "bold"),
                                      padx=10, pady=10)
        pointer_frame.pack(fill="x", pady=10)
        self.prev_label = tk.Label(pointer_frame, text="prev  -> None", bg=PANEL,
                                   fg="#f87171", font=("Consolas", 10), anchor="w")
        self.value_label = tk.Label(pointer_frame, text="value -> None", bg=PANEL,
                                    fg="#fbbf24", font=("Consolas", 10, "bold"), anchor="w")
        self.next_label = tk.Label(pointer_frame, text="next  -> None", bg=PANEL,
                                   fg="#4ade80", font=("Consolas", 10), anchor="w")
        for widget in (self.prev_label, self.value_label, self.next_label):
            widget.pack(fill="x")

        move_frame = tk.LabelFrame(right, text=" MOVER EL VEHÍCULO ",
                                   bg=PANEL, fg=ACCENT, font=("Segoe UI", 10, "bold"),
                                   padx=10, pady=10)
        move_frame.pack(fill="x")

        tk.Button(move_frame, text="<<   DEVOLVER A REPROCESO\nusa el puntero  prev",
                  bg=RED, fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", cursor="hand2", width=26,
                  command=self.move_backward).pack(pady=4)
        tk.Button(move_frame, text="AVANZAR DE ESTACIÓN   >>\nusa el puntero  next",
                  bg=GREEN, fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", cursor="hand2", width=26,
                  command=self.move_forward).pack(pady=4)

        station_frame = tk.LabelFrame(right, text=" GESTIONAR ESTACIONES ",
                                      bg=PANEL, fg=ACCENT, font=("Segoe UI", 10, "bold"),
                                      padx=10, pady=10)
        station_frame.pack(fill="x", pady=10)

        tk.Label(station_frame, text="Nombre:", bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(station_frame, width=20, font=("Consolas", 10))
        self.name_entry.grid(row=0, column=1, padx=6, pady=3, sticky="w")

        tk.Label(station_frame, text="Posición:", bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w")
        self.index_entry = tk.Entry(station_frame, width=6, font=("Consolas", 10))
        self.index_entry.grid(row=1, column=1, padx=6, pady=3, sticky="w")

        buttons = [
            ("append   (al final)", self.add_to_end),
            ("prepend  (al inicio)", self.add_to_start),
            ("insert   (en posición)", self.insert_at_index),
            ("remove   (eliminar)", self.remove_at_index),
        ]
        for position, (label, action) in enumerate(buttons):
            tk.Button(station_frame, text=label, bg=BLUE, fg="white", relief="flat",
                      font=("Consolas", 9, "bold"), cursor="hand2", anchor="w",
                      command=action).grid(row=2 + position, column=0, columnspan=2,
                                           pady=2, sticky="we")

        extra_frame = tk.Frame(right, bg=BACKGROUND)
        extra_frame.pack(fill="x")
        tk.Button(extra_frame, text="Recorrer en reversa (tail -> head)", bg="#475569",
                  fg="white", relief="flat", font=("Segoe UI", 9), cursor="hand2",
                  command=self.show_reverse).pack(fill="x", pady=2)
        tk.Button(extra_frame, text="Reiniciar línea de producción", bg="#475569",
                  fg="white", relief="flat", font=("Segoe UI", 9), cursor="hand2",
                  command=self.reset_line).pack(fill="x", pady=2)

    def log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", "> " + message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def refresh(self):
        self.listbox.delete(0, "end")

        node = self.line.head
        index = 0
        while node is not None:
            marker = ">>" if node is self.current else "  "
            tag = ""
            if node is self.line.head:
                tag += "  [head]"
            if node is self.line.tail:
                tag += "  [tail]"
            self.listbox.insert("end", " {} {:>2}. {}{}".format(marker, index, node.value, tag))
            if node is self.current:
                self.listbox.itemconfig(index, bg=ACCENT, fg="white")
            node = node.next
            index += 1

        head_value = self.line.head.value if self.line.head else "None"
        tail_value = self.line.tail.value if self.line.tail else "None"
        self.summary_label.config(text="head   = {}\ntail   = {}\nlength = {}".format(
            head_value, tail_value, self.line.length))

        if self.current is None:
            self.station_label.config(text="Sin vehículo en la línea")
            self.prev_label.config(text="prev  -> None")
            self.value_label.config(text="value -> None")
            self.next_label.config(text="next  -> None")
        else:
            self.station_label.config(text="{}  en:  {}".format(self.plate, self.current.value))
            previous_value = self.current.prev.value if self.current.prev else "None"
            next_value = self.current.next.value if self.current.next else "None"
            self.prev_label.config(text="prev  -> " + previous_value)
            self.value_label.config(text="value -> " + self.current.value)
            self.next_label.config(text="next  -> " + next_value)

    def start_vehicle(self):
        plate = self.plate_entry.get().strip().upper()
        if plate == "":
            messagebox.showwarning("Falta la placa", "Escriba la placa o VIN del vehículo.")
            return
        if self.line.head is None:
            messagebox.showwarning("Línea vacía", "No hay estaciones en la línea de producción.")
            return
        self.plate = plate
        self.current = self.line.head
        self.log("Vehículo " + plate + " ingresa a la línea en: " + self.current.value)
        self.refresh()

    def move_forward(self):
        if self.current is None:
            messagebox.showinfo("Sin vehículo", "Primero ingrese un vehículo a la línea.")
            return
        if self.current.next is None:
            self.log("Vehículo " + self.plate + " aprobado. Sale de la línea terminado.")
            messagebox.showinfo("Producción terminada",
                                "El vehículo " + self.plate +
                                " completó todas las estaciones y sale de la planta.")
            self.current = None
            self.plate = ""
            self.refresh()
            return
        self.current = self.current.next
        self.log("Avanza a: " + self.current.value)
        self.refresh()

    def move_backward(self):
        if self.current is None:
            messagebox.showinfo("Sin vehículo", "Primero ingrese un vehículo a la línea.")
            return
        if self.current.prev is None:
            messagebox.showinfo("Inicio de línea",
                                "El vehículo ya está en la primera estación.")
            return
        rejected_at = self.current.value
        self.current = self.current.prev
        self.log("Rechazado en " + rejected_at + ". Reproceso en: " + self.current.value)
        self.refresh()

    def read_name(self):
        name = self.name_entry.get().strip()
        if name == "":
            messagebox.showwarning("Falta el nombre", "Escriba el nombre de la estación.")
            return None
        return name

    def read_index(self):
        text = self.index_entry.get().strip()
        if not text.isdigit():
            messagebox.showwarning("Posición inválida", "Escriba un número de posición válido.")
            return None
        return int(text)

    def add_to_end(self):
        name = self.read_name()
        if name is None:
            return
        self.line.append(name)
        self.log("append  -> '" + name + "' agregada al final (nueva cola).")
        self.name_entry.delete(0, "end")
        self.refresh()

    def add_to_start(self):
        name = self.read_name()
        if name is None:
            return
        self.line.prepend(name)
        self.log("prepend -> '" + name + "' agregada al inicio (nueva cabeza).")
        self.name_entry.delete(0, "end")
        self.refresh()

    def insert_at_index(self):
        name = self.read_name()
        if name is None:
            return
        index = self.read_index()
        if index is None:
            return
        self.line.insert(index, name)
        self.log("insert  -> '" + name + "' insertada en la posición " + str(index) + ".")
        self.name_entry.delete(0, "end")
        self.refresh()

    def remove_at_index(self):
        index = self.read_index()
        if index is None:
            return
        node = self.line.traverse_to_index(index)
        if node is None:
            messagebox.showwarning("Posición inválida",
                                   "No existe una estación en la posición " + str(index) + ".")
            return
        if node is self.current:
            self.current = node.next if node.next else node.prev
        self.line.remove(index)
        self.log("remove  -> estación '" + node.value + "' eliminada de la línea.")
        self.refresh()

    def show_reverse(self):
        values = self.line.print_list_reverse()
        self.log("Recorrido en reversa (solo posible con prev): " + " <- ".join(values))

    def reset_line(self):
        self.line = DoublyLinkedList()
        self.current = None
        self.plate = ""
        self.load_default_stations()
        self.log("Línea de producción reiniciada a su configuración original.")
        self.refresh()


if __name__ == "__main__":
    app = AssemblyLineApp()
    app.mainloop()
