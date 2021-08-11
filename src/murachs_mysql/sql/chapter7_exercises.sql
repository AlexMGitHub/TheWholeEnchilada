/*Solutions to Chapter 7 exercises.

###############################################################################
# chapter7_exercsies.sql
#
# Revision:     1.00
# Date:         7/30/2021
# Author:       Alex
#
# Purpose:      Solutions to chapter 7 exercises from "Murach's MySQL", 3rd
#               edition by Joel Murach.
#
###############################################################################
*/


/*Solution to exercise 7.1.

Write a SELECT statement that returns the same result set as this SELECT
statement, but don't use a join. Instead, use a subquery in a WHERE clause
that uses the IN keyword.

SELECT DISTINCT vendor_name
FROM vendors JOIN invoices
    ON vendors.vendor_id = invoices.vendor_id
ORDER BY vendor_name
*/
SELECT DISTINCT vendor_name
FROM vendors
WHERE vendors.vendor_id IN
    (SELECT vendor_id
    FROM invoices)
ORDER BY vendor_name;


/*Solution to exercise 7.2.

Write a SELECT statement that answers this question: Which invoices have
a payment total that's greater than the average payment total for all invoices
with a payment total greater than O?

Return the invoice_number and invoice_total columns for each invoice. This
should return 20 rows.

Sort the results by the invoice_total column in descending order.
*/
SELECT invoice_number, invoice_total
FROM invoices
WHERE payment_total > 0 AND payment_total >
    (SELECT AVG(payment_total)
    FROM invoices
    WHERE payment_total > 0)
ORDER BY invoice_total DESC;


/*Solution to exercise 7.3.

Write a SELECT statement that returns two columns from the
General_Ledger_Accounts table: account_number and account_description.

Return one row for each account number that has never been assigned to any
line item in the Invoice_Line_Items table. To do that, use a subquery intro-
duced with the NOT EXISTS operator. This should return 54 rows.

Sort the results by the account_number column.
*/
SELECT account_number, account_description
FROM general_ledger_accounts g
WHERE NOT EXISTS
    (SELECT *
    FROM invoice_line_items il
    WHERE il.account_number = g.account_number)
ORDER BY g.account_number;


/*Solution to exercise 7.4.

Write a SELECT statement that returns four columns: vendor_name, invoice_id,
invoice_sequence, and line_item_amount.

Return a row for each line item of each invoice that has more than one line
item in the Invoice_Line_Items table. Hint: Use a subquery that tests for
invoice_sequence > 1. This should return 6 rows.

Sort the results by the vendor_name, invoice_id, and invoice_sequence
columns.
*/
SELECT vendor_name, i.invoice_id, invoice_sequence, line_item_amount
FROM invoices i JOIN invoice_line_items il
        ON i.invoice_id = il.invoice_id
    JOIN vendors v
        ON v.vendor_id = i.vendor_id
WHERE i.invoice_id IN
    (SELECT DISTINCT invoice_id
    FROM invoice_line_items
    WHERE invoice_sequence > 1)
ORDER BY vendor_name, i.invoice_id, invoice_sequence;


/*Solution to exercise 7.5.

Write a SELECT statement that returns two columns: vendor_id and the
largest unpaid invoice for each vendor. To do this, you can group the result
set by the vendor_id column. This should return 7 rows.

Write a second SELECT statement that uses the first SELECT statement in its
FROM clause. The main query should return a single value that represents the
sum of the largest unpaid invoices for each vendor.
*/
SELECT SUM(unpaid_invoice) AS sum_largest_unpaid_invoices
FROM
    (SELECT vendor_id, MAX(invoice_total - payment_total - credit_total)
        AS unpaid_invoice
    FROM invoices
    GROUP BY vendor_id
    HAVING unpaid_invoice > 0) AS temp;


/*Solution to exercise 7.6.

Write a SELECT statement that returns the name, city, and state of each
vendor that's located in a unique city and state. In other words, don't include
vendors that have a city and state in common with another vendor. This
should return 38 rows.

Sort the results by the vendor_state and vendor_city columns.
*/
SELECT vendor_name, vendor_city, vendor_state
FROM vendors
WHERE CONCAT(vendor_city, ', ', vendor_state) IN
    (
    SELECT vendor_location
    FROM
        (
        SELECT CONCAT(vendor_city, ', ', vendor_state) AS vendor_location,
            COUNT(CONCAT(vendor_city, ', ', vendor_state)) AS city_count
        FROM vendors
        GROUP BY vendor_location
        HAVING city_count = 1
        ) AS temp
    )
ORDER BY vendor_state, vendor_city;


/*Solution to exercise 7.7.

Use a correlated subquery to return one row per vendor, representing the
vendor's oldest invoice (the one with the earliest date). Each row should
include these four columns: vendor_name, invoice_number, invoice_date, and
invoice_total. This should return 34 rows.

Sort the results by the vendor_name column.
*/
SELECT vendor_name, invoice_number, invoice_date, invoice_total
FROM invoices i JOIN vendors v
    ON i.vendor_id = v.vendor_id
WHERE invoice_date =
    (
    SELECT MIN(invoice_date)
    FROM invoices
    WHERE vendor_id = i.vendor_id
    )
ORDER BY vendor_name;


/*Solution to exercise 7.8.

Rewrite exercise 7 so it gets the same result but uses an inline view instead
of a correlated subquery.
*/
SELECT vendor_name, invoice_number, invoice_date, invoice_total
FROM
    (
    SELECT vendor_name, invoice_number, invoice_date, invoice_total,
        min_invoice_date
    FROM invoices i JOIN vendors v
            ON i.vendor_id = v.vendor_id
        JOIN
            (
                SELECT vendor_id, MIN(invoice_date) AS min_invoice_date
                FROM invoices
                GROUP BY vendor_id
            ) AS temp
            ON i.vendor_id = temp.vendor_id
    WHERE invoice_date = min_invoice_date
    ) as temp2
ORDER BY vendor_name;


/*Solution to exercise 7.9.

Rewrite exercise 5 so it uses a common table expression (CTE) instead of an
inline view.
*/
WITH largest_unpaid_invoices AS
(
    SELECT vendor_id, MAX(invoice_total - payment_total - credit_total)
        AS unpaid_invoice
    FROM invoices
    GROUP BY vendor_id
    HAVING unpaid_invoice > 0
)
SELECT SUM(largest_unpaid_invoices.unpaid_invoice) AS
    sum_largest_unpaid_invoices
FROM largest_unpaid_invoices;