/*Solutions to Chapter 6 exercises.

###############################################################################
# chapter6_exercsies.sql
#
# Revision:     1.00
# Date:         7/29/2021
# Author:       Alex
#
# Purpose:      Solutions to chapter 6 exercises from "Murach's MySQL", 3rd
#               edition by Joel Murach.
#
###############################################################################
*/


/*Solution to exercise 6.1.

Write a SELECT statement that returns one row for each vendor in the
Invoices table that contains these columns:

    The vendor_id column from the Invoices table
    The sum of the invoice_total columns in the Invoices table for that vendor

This should return 34 rows.
*/
SELECT vendor_id, SUM(invoice_total) AS vendor_invoice_total
FROM invoices
GROUP BY vendor_id;


/*Solution to exercise 6.2.

Write a SELECT statement that returns one row for each vendor that contains
these columns:

    The vendor_name column from the Vendors table
    The sum of the payment_total columns in the Invoices table for that vendor

Sort the result set in descending sequence by the payment total sum for each
vendor.
*/
SELECT vendor_name, SUM(payment_total) AS vendor_total_payments
FROM vendors v JOIN invoices i
    ON v.vendor_id = i.vendor_id
GROUP BY v.vendor_id
ORDER BY vendor_total_payments DESC;


/*Solution to exercise 6.3.

Write a SELECT statement that returns one row for each vendor that contains
three columns:

    The vendor name column from the Vendors table
    The count of the invoices in the Invoices table for each vendor
    The sum of the invoice_total columns in the Invoices table for each vendor

Sort the result set so the vendor with the most invoices appears first.
*/
SELECT vendor_name, COUNT(i.vendor_id) AS invoice_count,
    SUM(invoice_total) AS vendor_invoice_total
FROM vendors v JOIN invoices i
    ON v.vendor_id = i.vendor_id
GROUP BY v.vendor_id
ORDER BY COUNT(i.vendor_id) DESC;


/*Solution to exercise 6.4.

Write a SELECT statement that returns one row for each general ledger
account number that contains three columns:

    The account_description column from the General_Ledger_Accounts table

    The count of the items in the Invoice_Line_Items table that have the same
    account_number

    The sum of the line_item_amount columns in the Invoice_Line_Items table
    that have the same account_number

Return only those rows where the count of line items is greater than 1. This
should return 10 rows.

Group the result set by the account_description column.

Sort the result set in descending sequence by the sum of the line item amounts.
*/
SELECT account_description,
    COUNT(il.account_number) AS count_invoice_line_items,
    SUM(line_item_amount) AS sum_line_item_amount
FROM general_ledger_accounts g JOIN invoice_line_items il
    ON g.account_number = il.account_number
GROUP BY account_description
HAVING COUNT(il.account_number) > 1
ORDER BY SUM(line_item_amount) DESC;


/*Solution to exercise 6.5.

Modify the solution to exercise 4 so it returns only invoices dated in the
second quarter of 2018 (April 1, 2018 to June 30, 2018). This should still
return 10 rows but with some different line item counts for each vendor. Hint:
Join to the Invoices table to code a search condition based on invoice_date.
*/
SELECT account_description,
    COUNT(il.account_number) AS count_invoice_line_items,
    SUM(line_item_amount) AS sum_line_item_amount
FROM general_ledger_accounts g JOIN invoice_line_items il
        ON g.account_number = il.account_number
    JOIN invoices i
        ON il.invoice_id  = i.invoice_id
WHERE invoice_date BETWEEN '2018-04-01' AND '2018-06-30'
GROUP BY account_description
HAVING COUNT(il.account_number) > 1
ORDER BY SUM(line_item_amount) DESC;


/*Solution to exercise 6.6.

Write a SELECT statement that answers this question: What is the total
amount invoiced for each general ledger account number? Return these
columns:

    The account_number column from the Invoice_Line_Items table

    The sum of the line_item_amount columns from the Invoice_Line_Items
    table

Use the WITH ROLLUP operator to include a row that gives the grand total.
This should return 22 rows.
*/
SELECT account_number, SUM(line_item_amount)
FROM invoice_line_items
GROUP BY account_number WITH ROLLUP;


/*Solution to exercise 6.7.

Write a SELECT statement that answers this question: Which vendors are
being paid from more than one account? Return these columns:

    The vendor_name column from the Vendors table

    The count of distinct general ledger accounts that apply to that vendor's
    invoices

This should return 2 rows.
*/
SELECT vendor_name, COUNT(DISTINCT il.account_number) AS count_account_numbers
FROM vendors v JOIN invoices i
        ON v.vendor_id = i.vendor_id
    JOIN invoice_line_items il
        ON il.invoice_id = i.invoice_id
GROUP BY v.vendor_id
HAVING count_account_numbers > 1;


/*Solution to exercise 6.8.

Write a SELECT statement that answers this question: What are the last
payment date and total amount due for each vendor with each terms id?
Return these columns:

    The terms_id column from the Invoices table

    The vendor_id column from the Invoices table

    The last payment date for each combination of terms_id and vendor_id in the
    Invoices table

    The sum of the balance due (invoice_total - payment_total - credit_total)
    for each combination of terms_id and vendor_id in the Invoices table

Use the WITH ROLLUP operator to include rows that give a summary for
each terms_id as well as a row that gives the grand total. This should return
40 rows.

Use the IF and GROUPING functions to replace the null values in the terms_id
and vendor_id columns with literal values if they're for summary rows.
*/
SELECT IF(GROUPING(terms_id) = 1, 'Grand Total', terms_id) AS 'Term ID',
    IF(GROUPING(vendor_id) = 1,
        CONCAT('Term ', terms_id, ' total'), vendor_id) AS 'Vendor ID',
    MAX(payment_date) AS last_payment_date,
    SUM(invoice_total - payment_total - credit_total) AS balance_due
FROM invoices
GROUP BY terms_id, vendor_id WITH ROLLUP;


/*Solution to exercise 6.9.

Write a SELECT statement that uses aggregate window functions to calculate
the total due for all vendors and the total due for each vendor. Return these
columns:

    The vendor_id from the Invoices table

    The balance due (invoice_total - payment_total - credit_total) for each
    invoice in the Invoices table with a balance due greater than 0

    The total balance due for all vendors in the Invoices table

    The total balance due for each vendor in the Invoices table

Modify the column that contains the balance due for each vendor so it
contains a cumulative total by balance due. This should return 11 rows.
*/
SELECT vendor_id,
    (invoice_total - payment_total - credit_total) AS balance_due,
    SUM(invoice_total - payment_total - credit_total) OVER()
        AS total_balance_all_vendors,
    SUM(invoice_total - payment_total - credit_total)
        OVER(PARTITION BY vendor_id
            ORDER BY (invoice_total - payment_total - credit_total)
        )
        AS total_balance_of_vendor
FROM invoices
WHERE (invoice_total - payment_total - credit_total) > 0;


/*Solution to exercise 6.10.

Modify the solution to exercise 9 so it includes a column that calculates the
average balance due for each vendor in the Invoices table. This column should
contain a cumulative average by balance due.

Modify the SELECT statement so it uses a named window for the last two
aggregate window functions.
*/
SELECT vendor_id,
    (invoice_total - payment_total - credit_total) AS balance_due,
    SUM(invoice_total - payment_total - credit_total) OVER()
        AS total_balance_all_vendors,
    SUM(invoice_total - payment_total - credit_total)
        OVER(vendor_window
            ORDER BY (invoice_total - payment_total - credit_total)
        )
        AS total_balance_of_vendor,
    ROUND(AVG(invoice_total - payment_total - credit_total)
        OVER(vendor_window
            ORDER BY (invoice_total - payment_total - credit_total)
            ), 2)
        AS cumu_average_vendor_balance_due
FROM invoices
WHERE (invoice_total - payment_total - credit_total) > 0
WINDOW vendor_window AS (PARTITION BY vendor_id);


/*Solution to exercise 6.11.

Write a SELECT statement that uses an aggregate window function to calcu-
late a moving average of the sum of invoice totals. Return these columns:

    The month of the invoice date from the Invoices table

    The sum of the invoice totals from the Invoices table

    The moving average of the invoice totals sorted by invoice month

The result set should be grouped by invoice month and the frame for the
moving average should include the current row plus three rows before the
current row.
*/
SELECT MONTH(invoice_date) AS month, SUM(invoice_total) AS total_invoices,
    ROUND(AVG(SUM(invoice_total)) OVER(ORDER BY MONTH(invoice_date)
        RANGE BETWEEN 3 PRECEDING AND 0 FOLLOWING), 2) AS moving_avg
FROM invoices
GROUP BY MONTH(invoice_date);