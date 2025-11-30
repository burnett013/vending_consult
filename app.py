import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Vending Machine Tracker",
    page_icon="🥤",
    layout="wide"
)

# Constants
DATA_FILE = "vending_data.csv"

def load_data():
    """Load data from CSV file."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Date", "Location", "Product", "SKU", 
            "Starting Quantity", "Ending Quantity"
        ])

def save_data(df):
    """Save data to CSV file."""
    df.to_csv(DATA_FILE, index=False)

def main():
    st.title("🥤 Vending Machine Tracker")
    st.markdown("Track your vending machine refills and inventory.")

    # Sidebar for data entry
    st.sidebar.header("Add New Entry")
    
    with st.sidebar.form("entry_form"):
        date = st.date_input("Date", datetime.now())
        location = st.selectbox(
            "Location",
            ["FCA Snack Machine", "CFC Micro Market", "CFL Micro Market"]
        )
        product = st.text_input("Product Name")
        sku = st.text_input("SKU")
        start_qty = st.number_input("Starting Quantity", min_value=0, step=1)
        end_qty = st.number_input("Ending Quantity", min_value=0, step=1)
        
        submitted = st.form_submit_button("Add Entry")
        
        if submitted:
            if location and product and sku:
                new_data = {
                    "Date": date,
                    "Location": location,
                    "Product": product,
                    "SKU": sku,
                    "Starting Quantity": start_qty,
                    "Ending Quantity": end_qty
                }
                
                df = load_data()
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                save_data(df)
                st.sidebar.success("Entry added successfully!")
            else:
                st.sidebar.error("Please fill in all required fields (Location, Product, SKU).")

    # Reset Data Button
    st.sidebar.markdown("---")
    if st.sidebar.button("Reset All Data", type="primary"):
        # Create empty dataframe with headers
        df = pd.DataFrame(columns=[
            "Date", "Location", "Product", "SKU", 
            "Starting Quantity", "Ending Quantity"
        ])
        save_data(df)
        st.sidebar.success("All data has been reset!")
        st.rerun()

    # Main area for data display
    st.header("Refill History")
    
    df = load_data()
    
    if not df.empty:
        # Sort by date descending
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date", ascending=False)
            # Format date for display
            df["Date"] = df["Date"].dt.strftime('%Y-%m-%d')
        
        st.dataframe(df, use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Data as CSV",
            csv,
            "vending_data.csv",
            "text/csv",
            key='download-csv'
        )
    else:
        st.info("No data available. Add entries using the sidebar.")

if __name__ == "__main__":
    main()
