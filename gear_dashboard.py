import streamlit as st
import pandas as pd
from itertools import product

# -------------------------
# Solver
# -------------------------

def find_best_change_gears(target, gears, top_n=20):

    #target = K / Z
    results = []

    for A, B, C, D in product(gears, repeat=4):

        # avoid divide by zero
        if B == 0 or D == 0:
            continue

        ratio = (A / B) * (C / D)
        error = abs(ratio - target)

        results.append({
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "Ratio": ratio, #round(ratio, 6),
            "Error": error #round(error, 6)
        })

    results.sort(key=lambda x: x["Error"])

    return pd.DataFrame(results[:top_n])


# -------------------------
# Dashboard
# -------------------------

mode = st.radio(
    "Select Input Method",
    [
        "Machine Constant + Teeth",
        "Direct Ratio"
    ]
)

st.title("Gear Hobbing Change Calculator")


### OPTION 1

if mode == "Machine Constant + Teeth":

    K = st.number_input("Machine Constant", value=40.0)

    Z = st.number_input("Number of Teeth", value=63)

    ratio = K/Z
    st.success(f"Target Ratio = {ratio:.6f}")

else:

    ratio = st.number_input(
        "Enter Target Ratio",
        value=0.634920
    )

    st.success(f"Target Ratio = {ratio:.6f}")





st.subheader("Inputs")

gear_text = st.text_input(
    "Available Gears",
    "24,26,28,30,32,34,36,38,40,42,44,46"
)

top_n = st.slider("Top Results", 5, 50, 20)

# convert gear list
gears = [int(x.strip()) for x in gear_text.split(",")]

# target ratio
target_ratio = ratio

#st.metric("Target Ratio", round(target_ratio, 6))

# calculate
if st.button("Find Best Gear Trains"):

    df = find_best_change_gears(target_ratio, gears, top_n)

    st.subheader("Best Solutions")

    st.dataframe(df, use_container_width=True)