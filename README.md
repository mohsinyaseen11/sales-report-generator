# Sales Report Generator

A simple desktop application (built with Tkinter) that takes a sales CSV file, cleans the data, and generates a polished PDF sales report — complete with summary stats and charts.

## Features

- Simple GUI to select a CSV file (no command line needed)
- Automatic data cleaning:
  - Removes invalid dates, empty products/categories
  - Converts quantity and price to numeric, drops invalid/zero values
  - Fills missing city values with "Unknown City"
  - Removes duplicate rows
  - Standardizes text formatting (product names, city, category)
- Calculates key metrics:
  - Total sales, total transactions, average order value, total quantity sold
  - Top 5 best-selling and bottom 5 least-selling products
  - Category-wise and city-wise sales breakdown
  - Best performing category and top performing city
  - Daily and monthly sales trends
- Generates a PDF report with:
  - Summary statistics
  - Top 5 / Worst 5 product tables
  - Bar chart of top products
  - Line chart of daily sales trend
  - Pie chart of category distribution
- Exports a cleaned version of the CSV alongside the report

## Requirements

- Python 3.8+
- See `requirements.txt` for Python packages

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/sales-report-generator.git
cd sales-report-generator
pip install -r requirements.txt
```

## Usage

```bash
python sales_report_generator.py
```

1. Click **"Select CSV File"**
2. Choose your sales CSV file
3. Wait for the success message
4. Find the generated `sales_report_<timestamp>.pdf` and `cleaned_data_<timestamp>.csv` in the project folder

## Expected CSV Columns

Your input CSV should contain at least the following columns:

| Column   | Description                  |
|----------|-------------------------------|
| Date     | Transaction date              |
| Product  | Product name                  |
| Category | Product category              |
| Quantity | Units sold                    |
| Price    | Price per unit                |
| City     | City of sale       |

## License

This project is open source and available under the [MIT License](LICENSE).
