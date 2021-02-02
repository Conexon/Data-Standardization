SQL statements for standardization
-----------------------------------

Let’s keep this document as a reference for SQL statements that are handy for us to use. Please add to it if you have a more efficient statement or have a different statement that helped you accomplish a task. 

You want to…

Look at records:
----------------
  - Select * from schema.table  - let’s you see all records within the table; * acts as a wildcard
  - Select column, column, …, 
      from schema.table - let’s you see records for specific columns 
  - Select column, column, …, count(*) 
      from schema.table
      Group by column, column, …
      Order by column, column, … - let’s you see how many records are aggregated by the columns you have chosen by number of those records
  - Select * from schema.table limit 10 - let’s you see the first ten rows, you can set any limit you want. 

Change Records:
---------------
  - Update schema.table
      Set column = another_column, column = <‘string’>, column = <an integer> - let’s you change records to be a specific string, another column’s values, a numeric value, etc.
  - Insert into schema.table1 (column, column, …, ..., geom) select column, column, …, ..., geom from schema.table2 - get records from one table  to another table using specific columns that exist in both, must include geom.
  - Update schema.table1
    	set column = table2.column, 
	   column = table2.column
	   from schema.table2
    where ST_Dwithin(table1.geom, table2.geom,<distance>) - allows you to update columns from one table to another depending on spatial relationship

Change the table:
-----------------
  - Alter table schema.table
    add column varchar, 
    add column int,
    add column double precision,


…,
…. - allows you to add new columns to your table, you must state the data type and precision if needed.
Alter table schema.table rename to <new table name> - allows you to rename the table
Drop table schema.table - drops a table
Create table schema.table (
add column varchar, 
add column int,
add column double precision,
) - creates a table
create table schema.table as
select 
  someabbreviation.gid, 
  someabbreviation.column, 
  someabbreviation.column
  someabbreviation.column
  someabbreviation.geom
from 
 schema.table1 as someabbreviation left join
  schema.table2 as someotherabbreviation on
  ST_Intersects(someabbreviation.geom,someotherabbreviation.geom) - this allows you to create a new table where there is a spatial relationship between the two tables. 