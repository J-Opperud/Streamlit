import streamlit as st
import math

# --------------------------------------------------
# Page Setup
# --------------------------------------------------

st.set_page_config(
    page_title="Pumps & Hydraulics Explorer",
    page_icon="💧",
    layout="wide"
    )

st.title("💧 Pumps & Hydraulics Explorer")

st.write(
    "Explore how flow rate, pipe size, elevation, and pipe material "
    "affect pump performance and total system head."
    )

# --------------------------------------------------
# System Setup
# --------------------------------------------------

st.header(" Hydraulic System Setup")

pump_name = st.text_input(
    "Pump / System Name",
    "Main Water Pump"
    )

pump_type = st.selectbox(
    "Pump Type",
    ["Centrifugal", "Gear", "Piston", "Vane"]
    )

flow_rate = st.slider(
    "Flow Rate (GPM)",
    min_value=5,
    max_value=500,
    value=50,
    step=5
    )

pipe_size = st.selectbox(
    "Pipe Inside Diameter (inches)",
    [1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0],
    index=3
    )

pipe_length = st.number_input(
    "Pipe Length (ft)",
    min_value=1.0,
    max_value=5000.0,
    value=200.0,
    step=25.0
    )

pipe_material = st.radio(
    "Pipe Material",
    ["PVC", "Steel", "Cast Iron"]
    )

# Hazen-Williams roughness coefficient
if pipe_material == "PVC":
    C = 150
elif pipe_material == "Steel":
    C = 120
else:
    C = 100

# --------------------------------------------------
# Elevation / Lift
# --------------------------------------------------

st.header(" Lift & Head")

static_head = st.number_input(
    "Static Head / Elevation (ft)",
    min_value=0.0,
    max_value=1000.0,
    value=50.0,
    step=5.0
)

dynamic_head = st.number_input(
    "Dynamic Head (ft)",
    min_value=0.0,
    max_value=1000.0,
    value=20.0,
    step=5.0
)

# --------------------------------------------------
# Pipe Friction Calculation
# --------------------------------------------------

# Hazen-Williams equation
#
# hf = 4.52 * L * Q^1.85 / (C^1.85 * d^4.87)
#
# hf = friction head loss in feet
# L  = pipe length in feet
# Q  = flow rate in GPM
# C  = Hazen-Williams coefficient
# d  = pipe diameter in inches

friction_head = (
    4.52
    * pipe_length
    * (flow_rate ** 1.85)
    / (
        (C ** 1.85)
        * (pipe_size ** 4.87)
    )
)

# --------------------------------------------------
# Total Dynamic Head
# --------------------------------------------------

total_head = (
    static_head
    + dynamic_head
    + friction_head
    )

# 1 ft of water head ≈ 0.433 PSI
total_pressure = total_head * 0.433

friction_pressure = friction_head * 0.433

# --------------------------------------------------
# Hydraulic Power
# --------------------------------------------------

# Water horsepower
water_hp = (flow_rate * total_pressure) / 1714

# --------------------------------------------------
# Results
# --------------------------------------------------

st.header(" Pump System Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Friction Loss",
        f"{friction_head:.1f} ft"
        )

with col2:
    st.metric(
        "Total Head",
        f"{total_head:.1f} ft"
        )

with col3:
    st.metric(
        "System Pressure",
        f"{total_pressure:.1f} PSI"
        )

with col4:
    st.metric(
        "Water Horsepower",
        f"{water_hp:.1f} HP"
        )

# --------------------------------------------------
# System Status
# --------------------------------------------------

st.subheader(" System Status")

if friction_head < 5:
    st.success(
        "Low pipe friction loss. The pipe size is producing "
        "relatively little resistance."
        )

elif friction_head < 20:
    st.info(
        "Moderate pipe friction loss. The system has noticeable "
        "resistance from the piping."
        )

else:
    st.warning(
        "High pipe friction loss. Increasing pipe size or reducing "
        "flow may significantly reduce the required pump head."
        )

# --------------------------------------------------
# Head Breakdown
# --------------------------------------------------

st.subheader(" Head Breakdown")

st.write(f"**Static Head:** {static_head:.1f} ft")
st.write(f"**Dynamic Head:** {dynamic_head:.1f} ft")
st.write(f"**Pipe Friction:** {friction_head:.1f} ft")
st.write(f"**Total Dynamic Head:** {total_head:.1f} ft")

# Progress bar showing friction's contribution
friction_percentage = min(
    friction_head / total_head,
    1.0
    )

st.write("Percentage of total head caused by pipe friction:")

st.progress(friction_percentage)

# --------------------------------------------------
# Pump Information
# --------------------------------------------------

st.header(" Pump Information")

if pump_type == "Centrifugal":
    st.write(
        "Centrifugal pumps use a rotating impeller to increase "
        "fluid velocity and pressure. They are commonly used "
        "for water and other continuous-flow applications."
        )

elif pump_type == "Gear":
    st.write(
        "Gear pumps use rotating gears to move fluid. They are "
        "commonly used in hydraulic systems where a consistent "
        "flow is required."
        )

elif pump_type == "Piston":
    st.write(
        "Piston pumps use reciprocating pistons and can produce "
        "high pressures. They are common in high-pressure "
        "hydraulic applications."
        )

else:
    st.write(
        "Vane pumps use sliding vanes inside a rotating rotor. "
        "They are commonly used in industrial hydraulic systems."
        )

# --------------------------------------------------
# Optional Safety / Operating Information
# --------------------------------------------------

st.header(" System Analysis")

high_flow = st.checkbox(
    "Show high-flow analysis"
    )

if high_flow:

    if flow_rate >= 200:
        st.warning(
            f"The selected flow rate of {flow_rate} GPM is high. "
            "Pipe friction can become a significant part of the "
            "pump's required head."
            )
    else:
        st.success(
            f"The selected flow rate of {flow_rate} GPM is below "
            "the high-flow threshold used by this demonstration."
            )

# --------------------------------------------------
# Summary
# --------------------------------------------------

st.header(" System Summary")

st.write(
    f"""
    **System:** {pump_name}

    **Pump:** {pump_type}

    **Flow:** {flow_rate} GPM

    **Pipe:** {pipe_size:.2f} inch {pipe_material}

    **Pipe Length:** {pipe_length:.0f} ft

    **Static Head:** {static_head:.1f} ft

    **Dynamic Head:** {dynamic_head:.1f} ft

    **Friction Loss:** {friction_head:.1f} ft

    **Total Dynamic Head:** {total_head:.1f} ft

    **Equivalent Pressure:** {total_pressure:.1f} PSI
    """
    )      


