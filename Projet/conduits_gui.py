import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import sv_ttk

try:
    from conduits_fonctions import *
except:
    pass


class FluidFlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fluid Flow Grid")

        # Parameters
        self.params_frame = ttk.LabelFrame(root, text="Global Parameters", padding=10)
        self.params_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.length_var = tk.DoubleVar()
        self.diameter_var = tk.DoubleVar()
        self.roughness_var = tk.DoubleVar()
        self.density_var = tk.DoubleVar()
        self.viscosity_var = tk.DoubleVar()

        self.length = 25
        self.diameter = 0.2
        self.roughness = 0.00026
        self.density = 1000
        self.viscosity = 0.00089

        self.create_param_fields()

        # Grid creation
        self.grid_frame = ttk.LabelFrame(root, text="Grid Setup", padding=10)
        self.grid_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.grid_canvas = tk.Canvas(self.grid_frame, width=600, height=400, bg="black")
        self.grid_canvas.pack()

        self.grid_size = 50  # Size of each grid cell in pixels
        self.points = {}
        self.selected_point = None
        self.graph = nx.DiGraph()
        self.draw_grid()

        self.grid_canvas.bind("<Button-1>", self.add_or_select_point)
        self.grid_canvas.bind("<Button-3>", self.erase_point)

        # Buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        self.compute_button = ttk.Button(self.button_frame, text="Start Computation", command=self.compute_flow)
        self.compute_button.pack(anchor='center', padx=5)

        self.reset_button = ttk.Button(self.button_frame, text="Reset Grid", command=self.reset_grid)
        self.reset_button.pack(anchor='center', padx=5)

        # Plot Visualization
        self.plot_frame = ttk.LabelFrame(root, text="Visualization", padding=10)
        self.plot_frame.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=10, pady=10)

        plt.style.use('dark_background')

        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.axis('off')
        self.canvas_plot = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas_plot.get_tk_widget().pack()

        sv_ttk.set_theme("dark")

    def create_param_fields(self):
        fields = [
            ("Length (m):", self.length_var, self.length),
            ("Diameter (m):", self.diameter_var, self.diameter),
            ("Roughness (m):", self.roughness_var, self.roughness),
            ("Density (kg/m³):", self.density_var, self.density),
            ("Dynamic Viscosity (Pa·s):", self.viscosity_var, self.viscosity),
        ]
        for i, (label, var, txt) in enumerate(fields):
            var.set(txt)
            ttk.Label(self.params_frame, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            ttk.Entry(self.params_frame, textvariable=var).grid(row=i, column=1, padx=5, pady=5)

    def draw_grid(self):
        """Draws a Cartesian grid on the canvas."""
        for x in range(0, 600, self.grid_size):
            self.grid_canvas.create_line(x, 0, x, 400, fill="#64676b")
        for y in range(0, 400, self.grid_size):
            self.grid_canvas.create_line(0, y, 600, y, fill="#64676b")

    def snap_to_grid(self, x, y):
        """Snaps a given point to the nearest grid intersection."""
        grid_x = round(x / self.grid_size) * self.grid_size
        grid_y = round(y / self.grid_size) * self.grid_size
        return grid_x, grid_y

    def add_or_select_point(self, event):
        x, y = self.snap_to_grid(event.x, event.y)
        point_id = (x, y)

        if point_id in self.points:
            self.select_point(point_id)
        else:
            self.add_point(x, y, point_id)

    def add_point(self, x, y, point_id):
        """Adds a new point to the canvas and graph."""
        self.grid_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#3b92f5")

        self.points[point_id] = {
            "pression": tk.DoubleVar(),
            "debit": tk.DoubleVar(),
            "active": tk.StringVar(value="pression")  # Default to pressure
        }
        self.graph.add_node(point_id, pos=(x, 400-y))

        self.connect_cardinal_neighbors(point_id)

    def select_point(self, point_id):
        """Displays editing fields for the selected point."""
        self.deselect_point()
        self.selected_point = point_id
        x, y = point_id

        point_data = self.points[point_id]
        active = point_data["active"]

        # Create radio buttons to toggle pressure/flow
        self.pressure_radio = ttk.Radiobutton(
            self.grid_canvas, text="Pressure", variable=active, value="pression", command=self.update_input_fields
        )
        self.flow_radio = ttk.Radiobutton(
            self.grid_canvas, text="Flow", variable=active, value="debit", command=self.update_input_fields
        )

        # Create input fields for pressure/flow
        self.pressure_entry = ttk.Entry(self.grid_canvas, textvariable=point_data["pression"], width=6, state="normal")
        self.flow_entry = ttk.Entry(self.grid_canvas, textvariable=point_data["debit"], width=6, state="disabled")

        # Place components on the canvas
        self.radio_window = self.grid_canvas.create_window(x - 40, y - 20, window=self.pressure_radio)
        self.radio_window2 = self.grid_canvas.create_window(x + 40, y - 20, window=self.flow_radio)
        self.pressure_window = self.grid_canvas.create_window(x - 30, y + 20, window=self.pressure_entry)
        self.flow_window = self.grid_canvas.create_window(x + 30, y + 20, window=self.flow_entry)

    def update_input_fields(self):
        """Enable the appropriate input field based on the selected parameter."""
        if self.selected_point:
            active = self.points[self.selected_point]["active"].get()
            if active == "pression":
                self.pressure_entry.config(state="normal")
                self.flow_entry.config(state="disabled")
            else:
                self.pressure_entry.config(state="disabled")
                self.flow_entry.config(state="normal")

    def deselect_point(self):
        """Hides the editing fields for the previously selected point."""
        if self.selected_point:
            self.grid_canvas.delete(self.pressure_window)
            self.grid_canvas.delete(self.flow_window)
            self.grid_canvas.delete(self.radio_window)
            self.grid_canvas.delete(self.radio_window2)
            self.selected_point = None

    def erase_point(self, event):
        x, y = self.snap_to_grid(event.x, event.y)
        point_id = (x, y)

        if point_id not in self.points:
            return

        self.deselect_point()
        self.graph.remove_node(point_id)
        del self.points[point_id]

        self.redraw_canvas()

    def redraw_canvas(self):
        """Clears the canvas and redraws all elements."""
        self.grid_canvas.delete("all")
        self.draw_grid()
        for node in self.graph.nodes:
            nx, ny = node
            self.grid_canvas.create_oval(nx - 5, ny - 5, nx + 5, ny + 5, fill="#3b92f5")
        for edge in self.graph.edges:
            x1, y1 = edge[0]
            x2, y2 = edge[1]
            self.grid_canvas.create_line(x1, y1, x2, y2, fill="#3b92f5", tags="connection", width=3)

    def reset_grid(self):
        """Clears the entire grid, resets all points, and redraws the canvas."""
        # Clear data structures
        self.points.clear()
        self.graph.clear()

        # Clear canvas and redraw grid
        self.grid_canvas.delete("all")
        self.draw_grid()

        # Clear any selected point data
        self.deselect_point()

    def connect_cardinal_neighbors(self, point_id):
        """Connects the current point to valid neighbors and updates their connections."""
        x, y = point_id

        # Remove any existing connections for this point
        if point_id in self.graph:
            self.graph.remove_node(point_id)

        self.graph.add_node(point_id, pos=(x, 400 - y))  # Ensure the point exists in the graph

        # Check in all four cardinal directions
        for dx, dy in [(0, -self.grid_size), (0, self.grid_size), (-self.grid_size, 0), (self.grid_size, 0)]:
            neighbor = self.find_neighbor_in_direction(x, y, dx, dy)
            if neighbor:
                # Connect this point to the found neighbor
                self.graph.add_edge(point_id, neighbor)
                # self.graph.add_edge(neighbor, point_id)  # Ensure bidirectional connection
                self.draw_line_between_points(point_id, neighbor)

    def find_neighbor_in_direction(self, x, y, dx, dy):
        """Finds the nearest neighbor in the given direction, if any."""
        while True:
            x += dx
            y += dy
            if (x, y) in self.points:
                return (x, y)
            if not (0 <= x < self.grid_canvas.winfo_width() and 0 <= y < self.grid_canvas.winfo_height()):
                break  # Stop if we go out of canvas bounds
        return None

    def draw_line_between_points(self, point1, point2):
        """Draws a line connecting two points on the canvas."""
        x1, y1 = point1
        x2, y2 = point2
        self.grid_canvas.create_line(x1, y1, x2, y2, fill="#3b92f5", tags="connection", width=3)

    def export_grid_data(self):
        """Exports the grid as a dictionary containing points, neighbors, distances, and values."""
        point_index = {point: i for i, point in enumerate(self.points)}  # Map points to indices
        grid_data = {}

        for point, index in point_index.items():
            x, y = point
            neighbors = []

            for neighbor in self.graph.neighbors(point):
                neighbor_index = point_index[neighbor]
                neighbors.append(neighbor_index)

            # Export only the selected parameter
            active = self.points[point]["active"].get()
            value = self.points[point][active].get()

            grid_data[index] = {
                active: value,
                "voisins": neighbors
            }

        return grid_data

    def compute_flow(self):
        try:
            length = self.length_var.get()
            diameter = self.diameter_var.get()
            roughness = self.roughness_var.get()
            density = self.density_var.get()
            viscosity = self.viscosity_var.get()
            if not all([length, diameter, roughness, density, viscosity]):
                raise ValueError("All global parameters must be set.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        prm = parametres()
        prm.L = length
        prm.D = diameter
        prm.e = roughness
        prm.rho = density
        prm.mu = viscosity

        network = self.export_grid_data()

        noeuds, conduits = calculation_sim(network, prm)
        sortie_console(noeuds, conduits)

        self.ax.clear()
        self.ax.margins(0.1)
        self.ax.axis('off')

        pos = nx.get_node_attributes(self.graph, "pos")

        nx.draw_networkx_nodes(self.graph, pos, node_color="tab:blue")
        nx.draw_networkx_edges(
            self.graph,
            pos,
            arrowstyle="-",
            arrowsize=10,
            edge_color="lightblue",
            width=2
        )

        labels = {}
        nodes = np.array(self.graph.nodes())
        for node in noeuds:
            pression = noeuds[node]["pression"]
            debit = noeuds[node]["debit"]
            labels[tuple(nodes[node])] = f"{pression:.2f} mmH2O \n {debit:.2f} m³/s"

        nx.draw_networkx_labels(self.graph, pos, labels, ax=self.ax, font_size=12, font_color="whitesmoke")

        edges = self.graph.edges()
        labels_edge = {}
        for edge in conduits:
            debit = conduits[edge]["debit"]
            n1, n2 = list(edges)[edge]

            labels_edge[(n1, n2)] = f"{debit:.2f} m³/s"

        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels_edge, font_size=10,  font_color="black")

        plt.savefig("sim_output",dpi=300)
        self.canvas_plot.draw()


class parametres():
    L = 25  # Longueur des conduits (m)
    D = 0.2  # Diametre (m)
    e = 0.00026  # Rugosite (m)
    rho = 1000  # Masse volumique (kg/m3)
    mu = 0.00089  # Viscosite dynamique (pa/s)
    n = 1.8099


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = FluidFlowApp(root)
    root.mainloop()
