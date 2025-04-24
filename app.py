import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Polar Chart Generator", layout="centered")

st.title("🌪️ Polar Chart Generator from Excel")
st.markdown("""
Upload an Excel file (`.xlsx`) with **three required columns**:

- **Wind direction** (in degrees)
- **PM10** (pollution level)
- **Wind speed** (in m/s)

### 📄 Sample Format:
| Wind direction | PM10   | Wind speed |
|----------------|--------|------------|
| 274.45333      | 148.19 | 0          |
| 0              | 228.44 | 0.3        |
| 21.88          | 3062.16| 0          |
""")

uploaded_file = st.file_uploader("📤 Upload Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Check for required columns
        required_cols = {'Wind direction', 'PM10', 'Wind speed'}
        if not required_cols.issubset(df.columns):
            st.error(f"❌ Your file must include the following columns: {', '.join(required_cols)}")
        else:
            st.success("✅ File loaded successfully! Generating polar chart...")

            # Convert wind direction to radians
            df['Wind direction (radians)'] = np.deg2rad(df['Wind direction'])

            # Plotting
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, polar=True)

            sc = ax.scatter(
                df['Wind direction (radians)'],
                df['PM10'],
                c=df['Wind speed'],
                cmap='viridis',
                s=50 + df['Wind speed'] * 200,
                alpha=0.75,
                edgecolors='black'
            )

            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            ax.set_title("Polar Chart of PM10 vs Wind Direction and Speed", fontsize=14)
            ax.set_rlabel_position(135)

            cbar = plt.colorbar(sc, ax=ax, orientation='vertical', label='Wind Speed (m/s)')
            st.pyplot(fig)

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
