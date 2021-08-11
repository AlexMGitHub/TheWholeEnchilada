/*Solutions to Chapter 9 exercises.

###############################################################################
# chapter9_exercsies.sql
#
# Revision:     1.00
# Date:         7/31/2021
# Author:       Alex
#
# Purpose:      Solutions to chapter 9 exercises from "Murach's MySQL", 3rd
#               edition by Joel Murach.
#
###############################################################################
*/


/*Solution to exercise 9.1.

Write a SELECT statement that returns these columns from the Invoices table:

    The invoice_total column

    A column that uses the ROUND function to return the invoice_total
    column with 1 decimal digit

    A column that uses the ROUND function to return the invoice_total
    column with no decimal digits

    A column that uses the TRUNCATE function to return the invoice_total
    column with no decimal digits
*/
SELECT invoice_total, ROUND(invoice_total, 1), ROUND(invoice_total),
    TRUNCATE(invoice_total, 0)
from invoices;


/*Solution to exercise 9.2.

Write a SELECT statement that returns these columns from the Date_Sample
table in the EX database:

    The start_date column

    A column that uses the DATE_FORMAT function to return the start_date
    column with its month name abbreviated and its month, day, and two-digit
    year separated by slashes

    A column that uses the DATE_FORMAT function to return the start_date
    column with its month and day returned as integers with no leading zeros, a
    two-digit year, and all date parts separated by slashes

    A column that uses the DATE_FORMAT function to return the start_date
    column with only the hours and minutes on a 12-hour clock with an am/pm
    indicator
*/
USE ex;
SELECT start_date, DATE_FORMAT(start_date, '%b %m/%d/%y'),
    DATE_FORMAT(start_date, '%c/%e/%y'),
    DATE_FORMAT(start_date, '%Y-%m-%d %l:%i %p')
FROM date_sample;
USE ap;


/*Solution to exercise 9.3.

Write a SELECT statement that returns these columns from the Vendors table:

    The vendor_name column

    The vendor_name column in all capital letters

    The vendor_phone column

    A column that displays the last four digits of each phone number

When you get that working right, add the columns that follow to the result set.
This is more difficult because these columns require the use of functions
within functions.

    The vendor_phone column with the parts of the number separated by dots,
    as in 555.555.5555

    A column that displays the second word in each vendor name if there is one
    and blanks if there isn't
*/
SELECT vendor_name, UPPER(vendor_name), vendor_phone, RIGHT(vendor_phone, 4),
    REPLACE(REPLACE(RIGHT(vendor_phone, 13), ') ', '.'), '-', '.')
        AS dot_number,
    CASE
        WHEN REGEXP_LIKE(vendor_name, '^\\S+\\s(\\S.+)\\s\\S+.+$')
            THEN REGEXP_REPLACE(vendor_name, '^\\S+\\s(\\S+)\\s\\S+.+$', '$1')
        WHEN REGEXP_LIKE(vendor_name, '^\\S+\\s(\\S+)$')
            THEN REGEXP_REPLACE(vendor_name, '\\S+\\s(\\S+)$', '$1')
        ELSE ''
    END AS second_word
FROM vendors;


/*Solution to exercise 9.4.

Write a SELECT statement that returns these columns from the Invoices table:

    The invoice_number column

    The invoice_date column

    The invoice_date column plus 30 days

    The payment_date column

    A column named days_to_pay that shows the number of days between the
    invoice date and the payment date

    The number of the invoice date's month

    The four-digit year of the invoice date

When you have this working, add a WHERE clause that retrieves just the
invoices for the month of May based on the invoice date, not the number of
the invoice month.
*/
SELECT invoice_number, invoice_date,
    DATE_ADD(invoice_date, INTERVAL 30 DAY) AS due_date,
    payment_date, DATEDIFF(payment_date, invoice_date) AS days_to_pay,
    DATE_FORMAT(invoice_date, '%c') AS invoice_numeric_month,
    DATE_FORMAT(invoice_date, '%Y') AS invoice_year
FROM invoices
WHERE MONTH(invoice_date) = 5;


/*Solution to exercise 9.5.

Write a SELECT statement that returns these columns from the String_Sample
table of the EX database:

    The emp_name column

    A column that displays each employee's first name

    A column that displays each employee's last name

Use regular expression functions to get the first and last name. If a name
contains three parts, everything after the first part should be considered part
of the last name. Be sure to provide for last names with hypens and
apostrophes.

Hint: To include an apostrophe in a pattern, you can code a \ in front of it or
you can enclose the pattern in double quotes.
*/
USE ex;
SELECT emp_name,
    REGEXP_REPLACE(emp_name, '^(\\S+)\\s\\S+.+$', '$1') AS first_name,
    REGEXP_REPLACE(emp_name, '^(\\S+)\\s(\\S+.+)$', '$2') AS last_name
FROM string_sample;
USE ap;


/*Solution to exercise 9.6.

Write a SELECT statement that returns these columns from the Invoice table
of the AP database:

    The invoice_number column

    The balance due for each invoice with a balance due greater than zero

    A column that uses the RANK() function to rank the balance due in
    descending sequence
*/
SELECT invoice_number,
    (invoice_total - payment_total - credit_total) AS balance_due,
    RANK() OVER (ORDER BY (invoice_total - payment_total - credit_total) DESC)
        AS 'rank'
FROM invoices
WHERE (invoice_total - payment_total - credit_total) > 0;