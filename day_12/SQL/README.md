SQL

Execution Order
--------------
FROM + JOIN
WHERE
GROUP BY
HAVING
SELECT ( Windows function happen here )
ORDER BY
LIMIT


Writing Order
-------------
SELECT
FROM [ JOIN ON  CONDITION   / USING (COLUMNS, ..) ]
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT


Joins
[INNER] JOIN
LEFT [OUTER] JOIN
RIGHT [OUTER] JOIN
FULL [OUTER] JOIN
CARTESIAN / CROSS JOIN  ( Also done with a , seperator ) ( use where clause to make result equivalent to inner join, etc. )

- OUTER JOIN on-side with more focus or side of a super-set.


Pivoting:
PIVOT   ( only in modern SQL Engines )
CASE

SELECT
  customer,
  SUM(
      CASE WHEN type = 'type_1'
        THEN amount
      ELSE 0
      END
  ) AS sum_type_1,
  SUM(
      CASE WHEN type = 'type_2'
        THEN amount
      ELSE 0
      END
  ) AS sum_type_2,
  SUM(
      CASE WHEN type = 'type_3'
        THEN amount
      ELSE 0
      END
  ) AS sum_type_3
FROM transactions


Here's a quick overview of the most common SQL aggregate functions:

FUNCTION                PURPOSE                                                             EXAMPLE
--------------------------------------------------------------------------------------------------------------------------------
MIN                     Returns the smallest value in a column.                             SELECT MIN(column) FROM table_name
MAX                     Returns the largest value in a column                               SELECT MAX(column) FROM table_name
SUM                     Calculates the sum of all numeric values in a column                SELECT SUM(column) FROM table_name
AVG                     Returns the average value for a column                              SELECT AVG(column) FROM table_name
COUNT(column)           Counts the number of non-null values in a column                    SELECT COUNT(column) FROM table_name
COUNT(*)                Counts the total number of rows (including NULLs) in a column	    SELECT COUNT(*) FROM table_name

CTEs
----
Common table expressions (CTEs) allow you to structure and organize SQL queries. Knowing how to organize SQL queries is a necessity when you begin to move deeper into SQL, so if you want to become an SQL master, you need to know CTEs.

WITH statements

SQL CTE is a named temporary result set within a SELECT, INSERT, UPDATE, or DELETE statement

CTEs replace subqueries, views, and inline user-defined functions

SQL developers use CTEs to create hierarchical queries and to re-factor and organize SQL queries for better readability or performance.

WITH sumary_sales AS ( 
    SELECT
        sum(sales_num*sales_price) sum_sales_revenue,
        sales_item_id 
    FROM sales
    GROUP BY sales_item_id ORDER BY sum_sales_revenue
    ),
customers_sales AS (
    SELECT
        sales_customer_id,
        round(sum(sales_num*sales_price)/sum_sales_revenue,2)*100 sales_percent,
        sumary_sales.sales_item_id
    FROM sales
    JOIN sumary_sales ON sumary_sales.sales_item_Id = sales.sales_item_id
    GROUP BY sales_customer_id, sumary_sales.sales_item_id, sum_sales_revenue
    )

SELECT * FROM customers_sales


Matching by Null with Masking Nulls:
------------------------------------
COALESCE

SELECT
    title,
    g.genres
FROM
    movies m
    JOIN genres g
        ON (COALESCE(m.genres, 0.0) = COALESCE(G.ID, 0.0))


Union
-----
UNION
UNION ALL
UNION DISTINCT

set union
A ∪ B

Intersect
---------
INTERSECT

set intersect
A ∩ B

Except
------
EXCEPT 

A - B

A - ( A ∩ B )



Window Function
---------------
SELECT duration_seconds,
SUM(duration_seconds) OVER
    (
        ORDER BY start_time
    ) AS running_total
FROM tutorial.dc_bikeshare_q1_2012


SELECT start_terminal,
duration_seconds,
SUM(duration_seconds) OVER
    (
        PARTITION BY start_terminal
        ORDER BY start_time
    ) AS running_total
FROM tutorial.dc_bikeshare_q1_2012

query groups and orders the query by start_terminal
Within each value of start_terminal, it is ordered by start_time
running total sums across the current row and all previous rows of duration_seconds

ORDER BY clause would, except that it treats every partition as separate. It also creates the running total

without ORDER BY, each value will simply be a sum of all the duration_seconds values in its respective start_terminal


SELECT start_terminal,
duration_seconds,
SUM(duration_seconds) OVER
    (
        PARTITION BY start_terminal
    ) AS start_terminal_total
FROM tutorial.dc_bikeshare_q1_2012


can't use window functions and standard aggregations in the same query
More specifically, can't include window functions in a GROUP BY clause


SELECT start_terminal,
duration_seconds,
SUM(duration_seconds) OVER (PARTITION BY start_terminal) AS running_total,
COUNT(duration_seconds) OVER (PARTITION BY start_terminal) AS running_count,
AVG(duration_seconds) OVER (PARTITION BY start_terminal) AS running_avg
FROM tutorial.dc_bikeshare_q1_2012


SELECT start_terminal,
duration_seconds,
SUM(duration_seconds) OVER (PARTITION BY start_terminal ORDER BY start_time) AS running_total,
COUNT(duration_seconds) OVER (PARTITION BY start_terminal ORDER BY start_time) AS running_count,
AVG(duration_seconds) OVER (PARTITION BY start_terminal ORDER BY start_time) AS running_avg
FROM tutorial.dc_bikeshare_q1_2012


- partition makes groups, aggregate values to start over end of group
- order by makes running aggregates



ROW_NUMBER()
1

RANK() would give the identical rows a rank of 2, then skip ranks 3 and 4, so the next result would be 5
DENSE_RANK() would still give all the identical rows a rank of 2, but the following row would be 3—no ranks would be skipped.


NTILE
-----
quartile(bucket no.s)


SELECT start_terminal,
       duration_seconds,
       NTILE(4) OVER
         (PARTITION BY start_terminal ORDER BY duration_seconds)
          AS quartile,
       NTILE(5) OVER
         (PARTITION BY start_terminal ORDER BY duration_seconds)
         AS quintile,
       NTILE(100) OVER
         (PARTITION BY start_terminal ORDER BY duration_seconds)
         AS percentile
  FROM tutorial.dc_bikeshare_q1_2012


LAG and LEAD
------------

SELECT start_terminal,
duration_seconds,
LAG(duration_seconds, 1) OVER (PARTITION BY start_terminal ORDER BY duration_seconds) AS lag,
LEAD(duration_seconds, 1) OVER (PARTITION BY start_terminal ORDER BY duration_seconds) AS lead
FROM tutorial.dc_bikeshare_q1_2012


SELECT start_terminal,
duration_seconds,
duration_seconds - LAG(duration_seconds, 1) OVER (PARTITION BY start_terminal ORDER BY duration_seconds) AS difference
FROM tutorial.dc_bikeshare_q1_2012



SELECT o.id,
o.occurred_at,
o.gloss_qty,
MAX(gloss_qty) OVER(ORDER BY o.occurred_at  
            ROWS BETWEEN 5 PRECEDING AND 1 PRECEDING
        ) as max_order
FROM demo.orders o


select *,
avg(Price) OVER(ORDER BY Date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    )
as moving_average
from stock_price;


select *,
avg(Price) OVER(ORDER BY Date 
    ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
) as 2day_moving_average,
avg(Price) OVER(ORDER BY Date
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
) as 30day_moving_average
from stock_price;




ORDER BY [order_var] ROWS BETWEEN window_start AND window_end
ORDER BY [order_var] VALUES BETWEEN window_start AND window_end

where window_start and windown_end take on one of the following values:
-----------------------------------------------------------------------
UNBOUNDED PRECEDING                         (i.e. all rows before the current row)
[VALUE] PRECEDING                           (where [VALUE] = # of rows behind the current row to consider)
CURRENT ROW
[VALUE] FOLLOWING                           (where [VALUE] = # of rows ahead of the current row to consider)
UNBOUNDED FOLLOWING                         (i.e. all rows after the current row)







Window Alias
------------

SELECT start_terminal,
duration_seconds,
NTILE(4) OVER (PARTITION BY start_terminal ORDER BY duration_seconds) AS quartile,
NTILE(5) OVER (PARTITION BY start_terminal ORDER BY duration_seconds) AS quintile,
NTILE(100) OVER (PARTITION BY start_terminal ORDER BY duration_seconds) AS percentile
FROM tutorial.dc_bikeshare_q1_2012

As

SELECT start_terminal,
duration_seconds,
NTILE(4) OVER ntile_window AS quartile,
NTILE(5) OVER ntile_window AS quintile,
NTILE(100) OVER ntile_window AS percentile
FROM tutorial.dc_bikeshare_q1_2012
WINDOW ntile_window AS (PARTITION BY start_terminal ORDER BY duration_seconds)



The WINDOW clause, if included, should always come after the WHERE clause



SubQuery vs CTEs
----------------

CTE == subquery used in FROM clause

CTEs not useful in where clause

- CTE useful in FROM clause
- subqueries useful in WHERE and SELECT clause (correlated subqueries)


CTEs Must Be Named
CTEs can be recursive
CTEs are reusable
CTEs can be more readable


Filtering with a subquery
Subqueries can act like columns
correlated subqueries are worst use cases, run for each row


EXISTS
------
EXISTS is an unary operator. It has only one operand, which is a subquery (correlated or not)




select *,
case when 
	LAG(trip_count, 10) OVER (PARTITION BY driver_id  ORDER BY year) AS lag,
then 1 else 0
from trip_fact




select *,
LAG(trip_count, 1, 0) OVER (PARTITION BY driver_id  ORDER BY year) AS previous_count,
then 1 else 0
from trip_fact


select *,
LEAD(trip_count, 1, 0) OVER (PARTITION BY driver_id  ORDER BY year DESC) AS previous_count,
then 1 else 0
from trip_fact

lag\lead(column_name [, no. of back\forth [, default value] ] )


-------------------------------------------------------------------------

Examples
--------


select distinct city from station where not REGEXP_LIKE(city, "^[aeiou].*[aeiou]$", 'i');

select distinct city from station where not REGEXP_LIKE(city, "(^[aeiou]|[aeiou]$)", 'i');


select distinct city from station where not REGEXP_LIKE(city, "^[aeiou]", 'i') or not REGEXP_LIKE(city, "[aeiou]$", 'i');

select distinct city from station where not REGEXP_LIKE(city, "^[aeiou]", 'i') and not REGEXP_LIKE(city, "[aeiou]$", 'i');


SELECT CEIL(AVG(Salary)-AVG(REPLACE(Salary,'0',''))) FROM EMPLOYEES;


select format(round(sum(LAT_N), 2), '0.00') lat, format(round(sum(LONG_W), 2), '0.00') lon from station;


select OrderDate, TotalSales,
    percentile_cont(.5)  within group (order by TotalSales) over() MedianSales
from (
    select OrderDate, sum(FinalOrderPrice) TotalSales
    from CustomerOrderSummary
    group by OrderDate
) d


select c.company_code, c.founder,
    count(distinct l.lead_manager_code ),
    count(distinct s.senior_manager_code ),
    count(distinct m.manager_code ),
    count(distinct e.employee_code )
from Company c, Lead_Manager l, Senior_Manager s, Manager m, Employee e
where c.company_code = l.company_code and
        l.lead_manager_code = s.lead_manager_code and
        s.senior_manager_code = m.senior_manager_code and
        m.manager_code = e.manager_code
group by c.company_code, c.founder
order by c.company_code
;



Select S.Name
From ( Students S join Friends F Using(ID)
       join Packages P1 on S.ID=P1.ID
       join Packages P2 on F.Friend_ID=P2.ID
    )
Where P2.Salary > P1.Salary
Order By P2.Salary;


select con.contest_id,
        con.hacker_id, 
        con.name, 
        sum(total_submissions), 
        sum(total_accepted_submissions), 
        sum(total_views), sum(total_unique_views)
from contests con 
    join colleges col on con.contest_id = col.contest_id 
    join challenges cha on  col.college_id = cha.college_id 
    left join (
        select challenge_id, sum(total_views) as total_views, sum(total_unique_views) as total_unique_views
            from view_stats group by challenge_id
    ) vs on cha.challenge_id = vs.challenge_id 
    left join (
        select challenge_id, sum(total_submissions) as total_submissions, sum(total_accepted_submissions) as total_accepted_submissions
            from submission_stats group by challenge_id
    ) ss on cha.challenge_id = ss.challenge_id
group by con.contest_id, con.hacker_id, con.name
having sum(total_submissions)!=0 or 
    sum(total_accepted_submissions)!=0 or
    sum(total_views)!=0 or
    sum(total_unique_views)!=0
order by contest_id;
