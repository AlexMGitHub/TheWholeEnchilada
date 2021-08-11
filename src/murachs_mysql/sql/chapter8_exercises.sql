/*Solutions to Chapter 8 exercises.

###############################################################################
# chapter8_exercsies.sql
#
# Revision:     1.00
# Date:         7/31/2021
# Author:       Alex
#
# Purpose:      Solutions to chapter 8 exercises from "Murach's MySQL", 3rd
#               edition by Joel Murach.
#
###############################################################################
*/


/*Solution to exercise 8.1.

Write a SELECT statement that returns these columns from the Invoices
table:

    The invoice_total column

    A column that uses the FORMAT function to return the invoice total
    column with 1 digit to the right of the decimal point

    A column that uses the CONVERT function to return the invoice total
    column as an integer

    A column that uses the CAST function to return the invoice total column
    as an integer
*/
SELECT invoice_total, FORMAT(invoice_total, 1), CONVERT(invoice_total, SIGNED),
    CAST(invoice_total AS SIGNED)
FROM invoices;


/*Solution to exercise 8.2.

Write a SELECT statement that returns these columns from the Invoices
table:

    The invoice_date column

    A column that uses the CAST function to return the invoice_date column
    with its full date and time

    A column that uses the CAST function to return the invoice_date column
    with just the year and the month
*/
SELECT invoice_date, CAST(invoice_date AS DATETIME),
    CAST(invoice_date AS CHAR(7))
FROM invoices;