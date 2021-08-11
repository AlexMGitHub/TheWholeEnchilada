/*Solutions to Chapter 3 exercises.

###############################################################################
# chapter3_exercsies.sql
#
# Revision:     1.00
# Date:         7/29/2021
# Author:       Alex
#
# Purpose:      Solutions to chapter 3 exercises from "Murach's MySQL", 3rd
#               edition by Joel Murach.
#
###############################################################################
*/


/*Solution to exercise 3.8.

Write a SELECT statement that returns three columns from the Vendors table:
vendor_name, vendor_contact_last_name, and vendor_contact_first_name.
Then, run this statement to make sure it works correctly.

Add an ORDER BY clause to this statement that sorts the result set by last
name and then first name, both in ascending sequence. Then, run this state-
ment again to make sure it works correctly. This is a good way to build and
test a statement, one clause at a time.
*/
SELECT vendor_name, vendor_contact_last_name, vendor_contact_first_name
FROM vendors
ORDER BY vendor_contact_last_name, vendor_contact_first_name;


/*Solution to exercise 3.9.

Write a SELECT statement that returns one column from the Vendors table named
full_name that joins the vendor_contact_last_name and vendor_contact_first_name
columns.

Format this column with the last name, a comma, a space, and the first name
like this:

    Doe, John

Sort the result set by last name and then first name in ascending sequence.

Return only the contacts whose last name begins with the letter A, B, C, or E.
This should retrieve 41 rows.
*/
SELECT CONCAT(vendor_contact_last_name, ', ', vendor_contact_first_name)
FROM vendors
WHERE vendor_contact_last_name REGEXP '^[ABCE]'
ORDER BY vendor_contact_last_name, vendor_contact_first_name;


/*Solution to exercise 3.10.

Write a SELECT statement that returns these column names and data from the
Invoices table:

1. Due Date
    The invoice due date column

2. Invoice Total
    The invoice total column

3. 10%
    10% of the value of invoice total

4.  Plus 10%
    The value of invoice_total plus 10%

Return only the rows with an invoice total that's greater than or equal to 500
and less than or equal to 1000. This should retrieve 12 rows.

Sort the result set in descending sequence by invoice_due_date.
*/
SELECT invoice_due_date AS 'Due Date', invoice_total AS 'Invoice Total',
    0.1*invoice_total AS '10%', 1.1*invoice_total AS 'Plus 10%'
FROM invoices
WHERE invoice_total >= 500 AND invoice_total <= 1000
ORDER BY invoice_due_date DESC;


/*Solution to exercise 3.11.

Write a SELECT statement that returns these columns from the Invoices table:

1. invoice_number
    The invoice_number column

2. invoice_total
    The invoice total column

3. payment_credit_total
    Sum of the payment_total and credit_total columns

4. balance_due
    The invoice total column minus the payment_total and credit_total columns

Return only invoices that have a balance due that's greater than $50.

Sort the result set by balance due in descending sequence.

Use the LIMIT clause so the result set contains only the rows with the 5
largest balances.
*/
SELECT invoice_number, invoice_total, payment_total + credit_total
    AS payment_credit_total,
    invoice_total - payment_total - credit_total AS balance_due
FROM invoices
WHERE invoice_total - payment_total - credit_total > 50
ORDER BY balance_due DESC
LIMIT 5;


/*Solution to exercise 3.12.

Write a SELECT statement that returns these columns from the Invoices table:

1. invoice_number
    The invoice_number column

2. invoice_date
    The invoice date column

3. balance_due
    The invoice_total column minus the payment_total and credit_total columns

4. payment_date
    The payment_date column

Return only the rows where the payment_date column contains a null value.
This should retrieve 11 rows.
*/
SELECT invoice_number, invoice_date,
    invoice_total - payment_total - credit_total as balance_due, payment_date
FROM invoices WHERE payment_date IS NULL;


/*Solution to exercise 3.13.

Write a SELECT statement without a FROM clause that uses the
CURRENT_DATE function to return the current date in its default format.

Use the DATE_FORMAT function to format the current date in this format:

    mm-dd-yyyy

This displays the month, day, and four-digit year of the current date.
Give this column an alias of current_date. To do that, you must enclose the
alias in quotes since that name is already used by the CURRENT_DATE
function.
*/
SELECT DATE_FORMAT(current_date,'%m-%d-%Y') AS 'current_date';


/*Solution to exercise 3.14.

Write a SELECT statement without a FROM clause that creates a row with
these columns:

1. starting_principal
    Starting principal of $50,000

2. interest
    6.5% of the principal

3. principal_plus_interest
    The principal plus the interest

To calculate the third column, add the expressions you used for the first two
columns.
*/
SELECT 50000 AS 'starting_principal', 0.065*50000 AS 'interest',
    50000 + 0.065*50000 AS 'principal_plus_interest';