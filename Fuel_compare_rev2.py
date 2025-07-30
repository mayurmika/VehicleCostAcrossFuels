# [Full Updated Streamlit App]

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Vehicle Ownership Cost Comparison", layout="centered")
st.title("Vehicle Cost of Ownership Projection across Fuels Rev 2")
st.subheader("Developed by Mayur")

# Year selection toggle
duration = st.toggle("Switch to 15-year projection", value=False)
years = 15 if duration else 10

# Fuel types
fuel_types = ['Petrol', 'CNG', 'Diesel', 'Electric']

# Inputs grouped in expanders
with st.expander("Vehicle Inputs"):
    # Vehicle 1
    v1_fuel = st.selectbox("Vehicle 1 Fuel Type", fuel_types, key="v1_fuel")
    v1_cost = st.number_input("Vehicle 1 Base Cost (₹)", min_value=0, key="v1_cost")
    v1_kmpl = st.number_input(
        "Vehicle 1 Efficiency (KMPL for Petrol / CNG / Diesel: KM/kWh : Distance / Battery size, example : 450km / 45kWh = 10) " if v1_fuel != 'Electric' else "Vehicle 1 Efficiency (KM per kWh)",
        min_value=1.0, key="v1_kmpl"
    )

    # Vehicle 2
    v2_fuel = st.selectbox("Vehicle 2 Fuel Type", fuel_types, key="v2_fuel")
    v2_cost = st.number_input("Vehicle 2 Base Cost (₹)", min_value=0, key="v2_cost")
    v2_kmpl = st.number_input(
        "Vehicle 2 Efficiency (KMPL for Petrol / CNG / Diesel: KM/kWh : Distance / Battery size, example : 450km / 45kWh = 10)" if v2_fuel != 'Electric' else "Vehicle 2 Efficiency (KM per kWh)",
        min_value=1.0, key="v2_kmpl"
    )

    # Optional Vehicle 3
    add_vehicle3 = st.checkbox("Add Vehicle 3")
    if add_vehicle3:
        v3_fuel = st.selectbox("Vehicle 3 Fuel Type", fuel_types, key="v3_fuel")
        v3_cost = st.number_input("Vehicle 3 Base Cost (₹)", min_value=0, key="v3_cost")
        v3_kmpl = st.number_input(
            "Vehicle 3 Efficiency (KMPL for Petrol / CNG / Diesel: KM/kWh : Distance / Battery size, example : 450km / 45kWh = 10)" if v3_fuel != 'Electric' else "Vehicle 3 Efficiency (KM per kWh)",
            min_value=1.0, key="v3_kmpl"
        )

with st.expander("Fuel & Usage Inputs"):
    distance_per_year = st.number_input("Driving Distance per Year (KM)", min_value=0, value=10000)

    fuel_cost_petrol = st.number_input("Fuel Cost - Petrol (₹/L)", min_value=1.0, value=110.0)
    fuel_cost_cng = st.number_input("Fuel Cost - CNG (₹/Kg)", min_value=1.0, value=85.0)
    fuel_cost_diesel = st.number_input("Fuel Cost - Diesel (₹/L)", min_value=1.0, value=100.0)
    fuel_cost_electric = st.number_input("Electricity Cost - per unit (₹/kWh)", min_value=1.0, value=8.0)

    fuel_cost_map = {
        'Petrol': fuel_cost_petrol,
        'CNG': fuel_cost_cng,
        'Diesel': fuel_cost_diesel,
        'Electric': fuel_cost_electric
    }

# Function to calculate year-wise ownership cost, fuel usage, and fuel cost
def calculate_vehicle_data(base_cost, kmpl, fuel_type):
    fuel_cost = fuel_cost_map.get(fuel_type, 100)
    cost_list = []
    fuel_used_list = []
    fuel_cost_list = []
    total_cost = base_cost
    for year in range(years + 1):
        if year == 0:
            cost_list.append(total_cost)
            fuel_used_list.append(0)
            fuel_cost_list.append(0)
        else:
            yearly_fuel = distance_per_year / kmpl
            yearly_fuel_cost = yearly_fuel * fuel_cost
            cumulative_fuel = fuel_used_list[-1] + yearly_fuel
            cumulative_cost = fuel_cost_list[-1] + yearly_fuel_cost
            fuel_used_list.append(cumulative_fuel)
            fuel_cost_list.append(cumulative_cost)
            total_cost += yearly_fuel_cost
            cost_list.append(total_cost)
    return cost_list, fuel_used_list, fuel_cost_list

# Compute values for each vehicle
v1_costs, v1_fuel_used, v1_fuel_costs = calculate_vehicle_data(v1_cost, v1_kmpl, v1_fuel)
v2_costs, v2_fuel_used, v2_fuel_costs = calculate_vehicle_data(v2_cost, v2_kmpl, v2_fuel)
if add_vehicle3:
    v3_costs, v3_fuel_used, v3_fuel_costs = calculate_vehicle_data(v3_cost, v3_kmpl, v3_fuel)

# Year labels
year_labels = list(range(0, years + 1))

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(year_labels, [c / 100000 for c in v1_costs], label=f"Vehicle 1 - {v1_fuel}")
ax.plot(year_labels, [c / 100000 for c in v2_costs], label=f"Vehicle 2 - {v2_fuel}")
if add_vehicle3:
    ax.plot(year_labels, [c / 100000 for c in v3_costs], label=f"Vehicle 3 - {v3_fuel}")

ax.set_title("Total Cost of Ownership Over Time (excluding Maintenance)")
ax.set_xlabel("Year")
ax.set_ylabel("Cost in Lakhs")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Table
with st.expander("Show Yearly Summary Table"):
    st.subheader("Yearly Summary Table")
    table_data = {
        "Year": year_labels,
        "Total KM Driven": [distance_per_year * y for y in year_labels],
        "Vehicle 1 - Fuel Used": v1_fuel_used,
        "Vehicle 1 - Fuel Cost (₹)": v1_fuel_costs,
        "Vehicle 2 - Fuel Used": v2_fuel_used,
        "Vehicle 2 - Fuel Cost (₹)": v2_fuel_costs,
    }

    if add_vehicle3:
        table_data["Vehicle 3 - Fuel Used"] = v3_fuel_used
        table_data["Vehicle 3 - Fuel Cost (₹)"] = v3_fuel_costs

    df = pd.DataFrame(table_data)
    st.dataframe(df.style.format({
        "Vehicle 1 - Fuel Used": "{:.1f}",
        "Vehicle 1 - Fuel Cost (₹)": "₹{:,.0f}",
        "Vehicle 2 - Fuel Used": "{:.1f}",
        "Vehicle 2 - Fuel Cost (₹)": "₹{:,.0f}",
        "Vehicle 3 - Fuel Used": "{:.1f}",
        "Vehicle 3 - Fuel Cost (₹)": "₹{:,.0f}",
        "Total KM Driven": "{:,.0f}"
    }), use_container_width=True)

# Per KM Fuel Cost Summary
#st.subheader("Per KM Running Cost by Fuel Type")
#per_km_costs = {
#    "Petrol": fuel_cost_petrol / v1_kmpl if v1_fuel == 'Petrol' else fuel_cost_petrol / v2_kmpl,
#    "CNG": fuel_cost_cng / v1_kmpl if v1_fuel == 'CNG' else fuel_cost_cng / v2_kmpl,
#    "Diesel": fuel_cost_diesel / v1_kmpl if v1_fuel == 'Diesel' else fuel_cost_diesel / v2_kmpl,
#    "Electric": fuel_cost_electric / v1_kmpl if v1_fuel == 'Electric' else fuel_cost_electric / v2_kmpl,
#}
#per_km_df = pd.DataFrame.from_dict(per_km_costs, orient='index', columns=["₹ per KM"])
#st.dataframe(per_km_df.style.format("₹{:.2f}"))


# Per KM Running Cost Summary
st.subheader("Per KM Running Cost by Fuel Type")

per_km_rows = []

# Vehicle 1
if v1_kmpl > 0:
    v1_per_km = fuel_cost_map[v1_fuel] / v1_kmpl
    unit = "kWh" if v1_fuel == "Electric" else "Litre/Kg"
    per_km_rows.append({
        "Vehicle": "Vehicle 1",
        "Fuel Type": v1_fuel,
        "Mileage": f"{v1_kmpl} km/{'kWh' if v1_fuel == 'Electric' else 'L'}",
        "Fuel Cost (₹/unit)": fuel_cost_map[v1_fuel],
        "Running Cost (₹/km)": round(v1_per_km, 2)
    })

# Vehicle 2
if v2_kmpl > 0:
    v2_per_km = fuel_cost_map[v2_fuel] / v2_kmpl
    per_km_rows.append({
        "Vehicle": "Vehicle 2",
        "Fuel Type": v2_fuel,
        "Mileage": f"{v2_kmpl} km/{'kWh' if v2_fuel == 'Electric' else 'L'}",
        "Fuel Cost (₹/unit)": fuel_cost_map[v2_fuel],
        "Running Cost (₹/km)": round(v2_per_km, 2)
    })

# Vehicle 3 (if used)
if add_vehicle3 and v3_kmpl > 0:
    v3_per_km = fuel_cost_map[v3_fuel] / v3_kmpl
    per_km_rows.append({
        "Vehicle": "Vehicle 3",
        "Fuel Type": v3_fuel,
        "Mileage": f"{v3_kmpl} km/{'kWh' if v3_fuel == 'Electric' else 'L'}",
        "Fuel Cost (₹/unit)": fuel_cost_map[v3_fuel],
        "Running Cost (₹/km)": round(v3_per_km, 2)
    })

per_km_df = pd.DataFrame(per_km_rows)
st.dataframe(per_km_df, use_container_width=True)

# Recommendation
st.subheader("Recommendation")
price_difference = v2_cost - v1_cost
fuel_saving_in_3_years = sum(v1_fuel_costs[1:4]) - sum(v2_fuel_costs[1:4])

if fuel_saving_in_3_years >= price_difference:
    st.markdown(
        f"✅ If the price difference between Vehicle 2 and Vehicle 1 (₹{price_difference:,.0f}) "
        f"is recovered through fuel savings in 3 years (₹{fuel_saving_in_3_years:,.0f}), then **go for Vehicle 2**."
    )
else:
    st.markdown(
        f"⚠️ Since the fuel saving in 3 years (₹{fuel_saving_in_3_years:,.0f}) is **less** than the price difference "
        f"(₹{price_difference:,.0f}), it's better to **go with Vehicle 1**."
    )
