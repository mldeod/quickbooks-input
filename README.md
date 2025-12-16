# QuickBooks Budget File Generator

A Streamlit application that converts Vena budget data exports into QuickBooks-compatible Excel files for Skagit Valley Family YMCA.

## Features

- **Vena Integration**: Imports budget data from Vena intersections and hierarchies
- **Multi-Department Support**: Generates separate tabs for each department
- **Account Hierarchy**: Maintains proper account hierarchy with indentation
- **QuickBooks Compatible**: Creates Excel files ready for QuickBooks import
- **Clean UI**: Minimalist design with YMCA branding

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/quickbooks-input.git
cd quickbooks-input
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Upload your two CSV files:
   - **Intersections file**: Contains budget data from Vena
   - **Hierarchies file**: Contains account and department hierarchies

3. Configure settings:
   - Company name
   - Budget name
   - Fiscal period
   - Year

4. Click "Generate QuickBooks Budget File"

5. Download the generated Excel file

## Input File Format

### Intersections CSV
Required columns:
- `_Account`: Account code
- `_Department`: Department name
- `_Year`: Fiscal year
- `_Period`: Period (1-12)
- `_Scenario`: Budget scenario (e.g., "Plan")
- `_value`: Budget amount

### Hierarchies CSV
Required columns:
- `_dim`: Dimension type ("Account" or "Department")
- `_member_name`: Member code
- `_member_alias`: Display name
- `_parent_name`: Parent member code

## Output Format

The generated Excel file includes:
- **Guidelines sheet**: Metadata about the budget
- **Department sheets**: One tab per department with:
  - Row 1: Department name
  - Row 2: Column headers (Accounts, Budget totals, Jan-Dec)
  - Rows 3+: Account hierarchy with monthly values

## Technology Stack

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation
- **OpenPyXL**: Excel file generation
- **Python 3.8+**

## Author

Built for Skagit Valley Family YMCA by Vena Analytics Accelerator

## License

Proprietary - All rights reserved
