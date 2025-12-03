# Tax Management Module

This module provides Aadhaar-based tax management functionality for the Gram Panchayat System.

## Features

1. **Citizen Tax Bills Display**
   - Citizens can view their pending tax bills based on their Aadhaar number
   - Color-coded status indicators (Green = Paid, Orange = Pending, Red = Overdue)
   - Detailed breakdown of each tax type with amounts, penalties, and due dates

2. **Excel Upload System**
   - Admins and Clerks can upload Excel files containing tax data for all citizens
   - Automatic processing and updating of citizen tax records
   - Support for Property Tax, Water Tax, Garbage Tax, and Health Tax

3. **Access Control**
   - Citizens: View only their own tax information
   - Clerks: Upload and edit tax records
   - Admins: Full access including delete capabilities

## Database Structure

The module uses the `CitizenTaxData` model with the following structure:

- **Primary Key**: Aadhaar Number (12-digit unique identifier)
- **Tax Categories**: Property, Water, Garbage, and Health Taxes
- **Fields per Tax**: Amount, Due Date, Penalty, Status
- **Status Values**: paid, pending, overdue

## Excel Upload Format

The Excel file must contain the following columns:
- Aadhaar Number (Required)
- Property Tax Amount
- Property Due Date
- Property Penalty
- Property Status
- Water Tax Amount
- Water Due Date
- Water Penalty
- Water Status
- Garbage Tax Amount
- Garbage Due Date
- Garbage Penalty
- Garbage Status
- Health Tax Amount
- Health Due Date
- Health Penalty
- Health Status

## URLs

### Citizen
- `/tax/citizen/bills/` - View personal tax bills

### Admin
- `/tax/admin/excel-upload/` - Upload tax data Excel file

### Clerk
- `/tax/clerk/excel-upload/` - Upload tax data Excel file

## Implementation Details

1. **Authentication**: Uses Aadhaar number as the unique identifier
2. **Data Filtering**: All citizen views are filtered by Aadhaar number
3. **Excel Processing**: Automatically creates new records or updates existing ones
4. **Status Management**: Real-time status updates with color coding

## Sample Data

Sample data templates are available in the `sample_data` directory:

1. `tax_data_template.csv` - Contains sample tax data that can be used as a template for Excel uploads

The template includes all required columns for the four tax categories (Property, Water, Garbage, Health) with sample values demonstrating the expected format.