import streamlit as st
import pandas as pd
import openpyxl
from openpyxl.styles import Font
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="QuickBooks Budget Builder", layout="wide")

# YMCA Blue ribbon header - matching website proportions
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;600;700&display=swap');
    
    .ymca-header {
        background: #43A5E6;
        padding: 0.6rem 2rem;
        margin: -1rem -1rem 1.5rem -1rem;
        border-radius: 0;
    }
    .ymca-title {
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin: 0;
        font-family: 'Montserrat', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        text-transform: uppercase;
    }
    .main-title {
        color: #2c3e50;
        font-size: 2rem;
        font-weight: 700;
        margin: 1.5rem 0 0.5rem 0;
        font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    </style>
    <div class="ymca-header">
        <div class="ymca-title">Skagit Valley Family YMCA</div>
    </div>
    <div class="main-title">QuickBooks Budget File Generator</div>
""", unsafe_allow_html=True)

# File uploaders
col1, col2 = st.columns(2)
with col1:
    intersections_file = st.file_uploader("Upload Intersections File", type=['csv'])
with col2:
    hierarchies_file = st.file_uploader("Upload Hierarchies File", type=['csv'])

if intersections_file and hierarchies_file:
    
    # Load data
    with st.spinner("Loading data..."):
        intersections = pd.read_csv(intersections_file)
        hierarchies = pd.read_csv(hierarchies_file)
    
    st.success(f"✓ Loaded {len(intersections):,} intersection records and {len(hierarchies):,} hierarchy records")
    
    # Configuration inputs
    st.subheader("Configuration")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        company_name = st.text_input("Company Name", value="Skagit Valley Family YMCA")
    with col2:
        budget_name = st.text_input("Budget Name", value="Budget_FY26_P&L")
    with col3:
        fiscal_year = st.text_input("Fiscal Period", value="FY 2026 (Jan 2026 - Dec 2026)")
    
    # Filter year selection
    available_years = sorted(intersections['_Year'].unique())
    selected_year = st.selectbox("Select Year for Export", available_years, index=len(available_years)-1)
    
    # Custom styling for elegant indigo button - Apple aesthetic
    st.markdown("""
        <style>
        .stButton > button[kind="primary"] {
            background-color: #4B5FAA;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 400;
            letter-spacing: 0.3px;
            transition: all 0.2s ease;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #3D4E8F;
            color: white;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(75, 95, 170, 0.3);
        }
        /* Clean Apple-style inputs */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #E5E5E5;
        }
        .stSelectbox > div > div > div {
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("▸ Generate QuickBooks Budget File", type="primary"):
        
        with st.spinner("Building Excel file..."):
            
            # Filter data
            df = intersections[
                (intersections['_Year'] == selected_year) & 
                (intersections['_Scenario'] == 'Plan')
            ].copy()
            
            st.info(f"▸ Processing {len(df):,} records for year {selected_year}")
            
            # Get hierarchies
            account_hier = hierarchies[hierarchies['_dim'] == 'Account'].copy()
            dept_hier = hierarchies[hierarchies['_dim'] == 'Department'].copy()
            
            # Build account lookup with descriptions
            account_lookup = {}
            for _, row in account_hier.iterrows():
                code = row['_member_name']
                alias = row['_member_alias'] if pd.notna(row['_member_alias']) else code
                account_lookup[code] = {
                    'name': code,
                    'alias': alias,
                    'parent': row['_parent_name'] if pd.notna(row['_parent_name']) else None
                }
            
            # Function to build full account hierarchy path
            def get_account_level(account_code, lookup):
                level = 0
                current = str(account_code)
                while current and current in lookup and lookup[current]['parent']:
                    level += 1
                    current = lookup[current]['parent']
                    if level > 10:  # Safety check
                        break
                return level
            
            # Function to format account name with indentation
            def format_account_name(account_code, lookup):
                account_str = str(account_code)
                if account_str not in lookup:
                    return account_str
                
                level = get_account_level(account_str, lookup)
                indent = "   " * level
                
                # Get the account name/alias
                name = lookup[account_str]['alias']
                
                # If account code is numeric and not already in the name, prepend it
                # Check if the name already starts with the code
                if account_str.isdigit() and not name.startswith(account_str):
                    formatted_name = f"{account_str} {name}"
                else:
                    formatted_name = name
                
                return f"{indent}{formatted_name}"
            
            # Pivot data by department and account
            df['Period_Name'] = df['_Period'].map({
                1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
            })
            
            # Create workbook
            wb = openpyxl.Workbook()
            wb.remove(wb.active)  # Remove default sheet
            
            # Add Guidelines sheet
            guidelines = wb.create_sheet("Guidelines", 0)
            guidelines['A1'] = 'Company name'
            guidelines['B1'] = company_name
            guidelines['A2'] = 'Budget name'
            guidelines['B2'] = budget_name
            guidelines['A3'] = 'Budget type'
            guidelines['B3'] = 'Profit and loss'
            guidelines['A4'] = 'Vena Scenario'
            guidelines['B4'] = 'Plan'
            guidelines['A5'] = 'Year'
            guidelines['B5'] = selected_year
            guidelines['A6'] = 'Period'
            guidelines['B6'] = f'1 - 12 (Jan {selected_year} - Dec {selected_year})'
            guidelines['A7'] = 'Subdivided by'
            guidelines['B7'] = 'Sub-Departments'
            
            # Get unique departments
            departments = sorted(df['_Department'].unique())
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, dept in enumerate(departments):
                status_text.text(f"Creating sheet for {dept}...")
                
                # Filter data for this department
                dept_data = df[df['_Department'] == dept].copy()
                
                # Pivot to wide format
                pivot = dept_data.pivot_table(
                    index='_Account',
                    columns='Period_Name',
                    values='_value',
                    aggfunc='sum',
                    fill_value=0
                )
                
                # Ensure all months are present
                month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                for month in month_order:
                    if month not in pivot.columns:
                        pivot[month] = 0
                
                pivot = pivot[month_order]
                
                # Calculate budget total
                pivot['Budget totals'] = pivot.sum(axis=1)
                
                # Reorder columns
                pivot = pivot[['Budget totals'] + month_order]
                
                # Create sheet
                ws = wb.create_sheet(dept)
                
                # Row 1: Department name
                ws['A1'] = dept
                ws['A1'].font = Font(bold=True)
                
                # Row 2: Headers
                ws['A2'] = 'Accounts'
                ws['B2'] = 'Budget totals'
                for i, month in enumerate(month_order):
                    ws.cell(row=2, column=3+i, value=f'{month} {selected_year}')
                
                # Add account data
                current_row = 3
                
                for account in pivot.index:
                    account_name = format_account_name(account, account_lookup)
                    ws.cell(row=current_row, column=1, value=account_name)
                    
                    # Add values
                    for col_idx, col_name in enumerate(['Budget totals'] + month_order):
                        value = pivot.loc[account, col_name]
                        if value != 0:
                            ws.cell(row=current_row, column=2+col_idx, value=value)
                    
                    current_row += 1
                
                progress_bar.progress((idx + 1) / len(departments))
            
            status_text.text("✓ Complete!")
            
            # Save to BytesIO
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            
            progress_bar.progress(1.0)
            status_text.text("✓ Complete!")
            
            # Download button
            st.success(f"▸ Generated QuickBooks budget file with {len(departments)} department tabs!")
            
            st.download_button(
                label="↓ Download QuickBooks Budget File",
                data=output.getvalue(),
                file_name=f"QB_Budget_{budget_name}_{selected_year}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
else:
    st.info("↑ Please upload both CSV files to get started")
