import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Vehicle Ownership Cost Comparison", layout="centered")
st.title("Vehicle Cost of Ownership Projection across Fuels")
st.subheader("Developed by Mayur")

# Year selection toggle
duration = st.toggle("Switch to 15-year projection", value=False)
years = 15 if duration else 10

# Fuel types
fuel_types = ['Petrol', 'CNG', 'Diesel', 'Electric']

# Vehicle 1 inputs
with st.expander("Vehicle Inputs"):
    # Vehicle 1
    v1_fuel = st.selectbox("Vehicle 1 Fuel Type", fuel_types, key="v1_fuel")
    v1_cost = st.number_input("Vehicle 1 Base Cost (₹)", min_value=0, key="v1_cost")
    v1_kmpl = st.number_input("Vehicle 1 Mileage (KMPL)", min_value=1.0, key="v1_kmpl")

    # Vehicle 2
    v2_fuel = st.selectbox("Vehicle 2 Fuel Type", fuel_types, key="v2_fuel")
    v2_cost = st.number_input("Vehicle 2 Base Cost (₹)", min_value=0, key="v2_cost")
    v2_kmpl = st.number_input("Vehicle 2 Mileage (KMPL)", min_value=1.0, key="v2_kmpl")

    # Optional Vehicle 3
    add_vehicle3 = st.checkbox("Add Vehicle 3")
    if add_vehicle3:
        v3_fuel = st.selectbox("Vehicle 3 Fuel Type", fuel_types, key="v3_fuel")
        v3_cost = st.number_input("Vehicle 3 Base Cost (₹)", min_value=0, key="v3_cost")
        v3_kmpl = st.number_input("Vehicle 3 Mileage (KMPL)", min_value=1.0, key="v3_kmpl")

# Common Inputs
with st.expander("Fuel & Usage Inputs"):
    distance_per_year = st.number_input("Driving Distance per Year (KM)", min_value=0, value=10000)

    fuel_cost_petrol = st.number_input("Fuel Cost - Petrol (₹/L)", min_value=1.0, value=110.0)
    fuel_cost_cng = st.number_input("Fuel Cost - CNG (₹/Kg)", min_value=1.0, value=85.0)
    fuel_cost_diesel = st.number_input("Fuel Cost - Diesel (₹/L)", min_value=1.0, value=100.0)
    fuel_cost_electric = st.number_input("Electricity Cost - per unit (₹/kWh)", min_value=1.0, value=4.0)

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

# Plotting cost chart
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

# Tabular Summary
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


st.subheader("Verdict")
st.subheader("Identify the Graph Cross-over at the year mark")
st.subheader("Recommendation")

price_difference = v2_cost - v1_cost
fuel_saving_in_3_years = sum(v1_fuel_costs[1:4]) - sum(v2_fuel_costs[1:4])

if fuel_saving_in_3_years >= price_difference:
    recommendation = "✅ Since the extra cost of Vehicle 2 can be recovered within 3 years due to lower fuel expenses, go for **Vehicle 2**."
else:
    recommendation = "⚠️ The extra cost of Vehicle 2 cannot be recovered within 3 years, so go for **Vehicle 1**."

st.markdown(recommendation)