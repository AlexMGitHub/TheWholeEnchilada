/*Solutions to Chapter 4 exercises.

###############################################################################
# chapter4_exercsies.sql
#
# Revision:     1.00
# Date:         7/29/2021
# Author:       Alex
#
# Purpose:      Solutions to chapter 4 exercises from "Murach's MySQL", 3rd
#               edition by Joel Murach.
#
###############################################################################
*/


/*Solution to exercise 4.1.

Write a SELECT statement that returns all columns from the Vendors table
inner-joined with all columns from the Invoices table. This should return 114
rows. Hint: You can use an asterisk(*) to select the columns from both tables.
*/
SELECT *
FROM vendors JOIN invoices
ON vendors.vendor_id = invoices.vendor_id;


/*Solution to exercise 4.2.

Write a SELECT statement that returns these four columns:

1. vendor_name
    The vendor_name column from the Vendors table

2. invoice_number
    The invoice number column from the Invoices table

3. invoice_date
    The invoice date column from the Invoices table

4. balance_due
    The invoice_total column minus the payment_total and credit_total columns
    from the Invoices table

Use these aliases for the tables: v for Vendors and i for Invoices.

Return one row for each invoice with a non-zero balance. This should return
11 rows.

Sort the result set by vendor_name in ascending order.
*/
SELECT vendor_name, invoice_number, invoice_date,
    invoice_total - payment_total - credit_total AS balance_due
FROM vendors v JOIN invoices i
ON v.vendor_id = i.vendor_id
WHERE invoice_total - payment_total - credit_total > 0
ORDER BY vendor_name;


/*Solution to exercise 4.3.

Write a SELECT statement that returns these three columns:

1. vendor_name
    The vendor_name column from the Vendors table

2. default_account
    The default_account_number column from the Vendors table

3. description
    The account_description column from the General_Ledger_Accounts table

Return one row for each vendor. This should return 122 rows.

Sort the result set by account_description and then by vendor_name.
*/
SELECT vendor_name, default_account_number AS default_account,
    account_description AS description
FROM vendors v JOIN general_ledger_accounts g
    ON v.default_account_number = g.account_number
ORDER BY account_description, vendor_name;


/*Solution to exercise 4.4.

Write a SELECT statement that returns these five columns:

1. vendor_name
    The vendor_name column from the Vendors table

2. invoice_date
    The invoice_date column from the Invoices table

3. invoice_number
    The invoice_number column from the Invoices table

4. li_sequence
    The invoice_sequence column from the Invoice_Line_Items table

5. li_amount
    The line_item_amount column from the Invoice_Line_Items table

Use aliases for the tables. This should return 118 rows.

Sort the final result set by vendor_name, invoice_date, invoice_number, and
invoice_sequence.
*/
SELECT vendor_name, invoice_date, invoice_number, invoice_sequence
    AS li_sequence, line_item_amount as li_amount
FROM vendors v JOIN invoices i
        ON v.vendor_id = i.vendor_id
    JOIN invoice_line_items li
        ON i.invoice_id = li.invoice_id
ORDER BY vendor_name, invoice_date, invoice_number, invoice_sequence;


/*Solution to exercise 4.5.

Write a SELECT statement that returns three columns:

1. vendor_id
    The vendor id column from the Vendors table

2. vendor_name
    The vendor name column from the Vendors table

3. contact_name
    A concatenation of the vendor_contact_first_name and
    vendor_contact_last_name columns with a space between

Return one row for each vendor whose contact has the same last name as
another vendor's contact. This should return 2 rows.

Hint: Use a self-join to check that the vendor_id columns aren't equal but the
vendor_contact_last_name columns are equal.

Sort the result set by vendor_contact_last_name.
*/
SELECT v1.vendor_id, v1.vendor_name,
    CONCAT(v1.vendor_contact_first_name, ', ', v1.vendor_contact_last_name) AS
    contact_name
FROM vendors v1 JOIN vendors v2
    ON v1.vendor_contact_last_name = v2.vendor_contact_last_name
    AND v1.vendor_id != v2.vendor_id
ORDER BY v2.vendor_contact_last_name;


/*Solution to exercise 4.6.

Write a SELECT statement that returns these three columns:

1. account_number
    The account number column from the General_Ledger_Accounts table

2. account_description
    The account_description column from the General_Ledger_Accounts table

3. invoice_id
    The invoice_id column from the Invoice_Line_Items table

Return one row for each account number that has never been used. This should
return 54 rows.  Hint: Use an outer join and only return rows where the
invoice_id column contains a null value.

Remove the invoice_id column from the SELECT clause.

Sort the final result set by the account_number column.
*/
SELECT g.account_number, account_description
FROM general_ledger_accounts g LEFT JOIN invoice_line_items i
    ON i.account_number = g.account_number
WHERE invoice_id IS NULL
ORDER BY g.account_number;


/*Solution to exercise 4.7.

Use the UNION operator to generate a result set consisting of two columns
from the Vendors table: vendor_name and vendor_state. If the vendor is in
California, the vendor_state value should be "CA".  Otherwise, the
vendor_state value should be "Outside CA." Sort the final result set by
vendor_name.
*/
    SELECT vendor_name, vendor_state
    FROM vendors
    WHERE vendor_state = 'CA'
UNION
    SELECT vendor_name, 'Outside CA' AS outside_ca_vendor_states
    FROM vendors
    WHERE vendor_state != 'CA'
ORDER BY vendor_name;