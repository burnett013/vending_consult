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

    # Export Section
    st.sidebar.markdown("---")
    st.sidebar.header("Export Data")
    
    # Download Option
    df = load_data()
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            "Download CSV",
            csv,
            "vending_data.csv",
            "text/csv",
            key='sidebar-download-csv'
        )
    
    # Email Option
    st.sidebar.subheader("Email Report")
    recipient_email = st.sidebar.text_input("Recipient Email", value="andyburnett013@gmail.com")
    
    if st.sidebar.button("Send CSV via Email"):
        df = load_data()
        if not df.empty:
            # Check for secrets
            if "email" in st.secrets:
                sender_email = st.secrets["email"]["sender_email"]
                sender_password = st.secrets["email"]["sender_password"]
                
                try:
                    import smtplib
                    from email.mime.text import MIMEText
                    from email.mime.multipart import MIMEMultipart
                    from email.mime.application import MIMEApplication

                    msg = MIMEMultipart()
                    msg['Subject'] = f"Vending Machine Report - {datetime.now().strftime('%Y-%m-%d')}"
                    msg['From'] = sender_email
                    msg['To'] = recipient_email

                    body = "Please find attached the latest vending machine refill report."
                    msg.attach(MIMEText(body, 'plain'))

                    # Attach CSV
                    csv_data = df.to_csv(index=False)
                    part = MIMEApplication(csv_data, Name="vending_data.csv")
                    part['Content-Disposition'] = 'attachment; filename="vending_data.csv"'
                    msg.attach(part)

                    # Send email
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
                    
                    st.sidebar.success(f"Email sent successfully to {recipient_email}!")
                except Exception as e:
                    st.sidebar.error(f"Failed to send email: {str(e)}")
            else:
                st.sidebar.error("Email configuration missing!")
                with st.sidebar.expander("How to fix this?"):
                    st.markdown("""
                    1. Go to your app dashboard on Streamlit Cloud.
                    2. Click **Settings** -> **Secrets**.
                    3. Paste this configuration:
                    ```toml
                    [email]
                    sender_email = "your_email@gmail.com"
                    sender_password = "your_app_password"
                    ```
                    **Note:** Use an App Password for Gmail.
                    """)
        else:
            st.sidebar.warning("No data to send.")

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
