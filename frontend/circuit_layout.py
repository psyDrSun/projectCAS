# --- Grid System ---
# The foundational unit for all positions and sizes.
GRID_SIZE = 8 # A smaller grid size allows for more detailed layouts.

# --- Visual Theme (Turing Complete Inspired) ---
THEME = {
    "background": "#1a1a1a", # Very dark grey, almost black
    "component_bg": "#2c3e50", # Dark slate blue
    "component_border": "#34495e", # Slightly lighter slate blue
    "component_border_active": "#f1c40f", # Bright yellow for active components
    "component_label": "#ecf0f1", # Light grey, almost white
    "font": "Consolas",
    "font_size": 9,
    
    "wire_idle": "#4a6572", # Desaturated dark blue/grey for inactive wires
    
    # A palette of vibrant, neon-like colors for active buses
    "wire_colors": {
        "DEFAULT": "#3498db", # Bright blue for default active bus
        "ADDR_BUS": "#e74c3c", # Neon Red
        "DATA_BUS": "#2ecc71", # Neon Green
        "PC_MAR_BUS": "#9b59b6", # Neon Purple
        "MDR_IR_BUS": "#f39c12", # Neon Orange
        "MDR_ACC_BUS": "#1abc9c", # Turquoise
        "PC_ALU_BUS": "#e67e22", # Carrot Orange
    }
}

# --- Component Layout Definition ---
# All coordinates and dimensions are in GRID units.
# (0,0) is the top-left corner of the canvas.
# Format: "NAME": {"grid_pos": (x, y), "grid_size": (width, height), "label": "Display Text"}
COMPONENTS = {
    # Left Side (Memory and Control)
    "RAM":      {"grid_pos": (4, 4), "grid_size": (18, 50), "label": "RAM"},
    "MAR":      {"grid_pos": (26, 4), "grid_size": (10, 6), "label": "MAR"},
    "PC":       {"grid_pos": (26, 14), "grid_size": (10, 6), "label": "PC"},
    
    # Middle (Data Path and Decode)
    "MDR":      {"grid_pos": (40, 4), "grid_size": (10, 6), "label": "MDR"},
    "IR":       {"grid_pos": (40, 14), "grid_size": (10, 6), "label": "IR"},
    "CU":       {"grid_pos": (26, 24), "grid_size": (24, 12), "label": "Control Unit"},
    
    # Right Side (Execution)
    "ALU":      {"grid_pos": (54, 4), "grid_size": (12, 16), "label": "ALU"},
    "ACC":      {"grid_pos": (54, 24), "grid_size": (12, 6), "label": "ACC"},
    "FLAG":     {"grid_pos": (54, 34), "grid_size": (12, 6), "label": "FLAG"},
}

# --- Wire/Bus Layout Definition ---
# A wire is a list of grid-coordinate points that will be connected sequentially.
# The key (e.g., "ADDR_BUS") MUST match the bus names yielded by the backend CPU generator.
WIRES = {
    # Address bus from MAR to RAM
    "ADDR_BUS": [
        (36, 7), # Start at MAR's right edge
        (38, 7),
        (38, 2),
        (2, 2),
        (2, 7), # End near RAM's left edge
        (4, 7)
    ],
    # Data bus connecting RAM, MDR, ALU, ACC
    "DATA_BUS": [
        (2, 20), # From RAM
        (4, 20),
        (38, 20), # Main horizontal bus line
        (38, 7), # Branch up to MDR
        (40, 7),
        (38, 20), # Back to main line
        (52, 20), # Branch up to ALU
        (52, 12),
        (54, 12),
        (52, 20), # Back to main line
        (52, 27), # Branch down to ACC
        (54, 27),
    ],
    # Internal CPU buses
    "PC_MAR_BUS": [
        (36, 17), # From PC
        (38, 17),
        (38, 17),
        (38, 7), # To MAR
        (36, 7)
    ],
    "MDR_IR_BUS": [
        (45, 10), # From MDR
        (45, 12),
        (45, 17), # To IR
        (40, 17)
    ],
}