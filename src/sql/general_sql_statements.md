# General SQL Statements for Standardization

Let’s keep this document as a reference for SQL statements that are handy for us to use. Please add to it if you have a more efficient statement or have a different statement that helped you accomplish a task. 

---

You want to…

### Look at records:

``` 
  Select * from schema.table
``` 

* Let’s you see all records within the table

* Acts as a wildcard


``` 
  Select column, column, …, 
    from schema.table
```  
      
* Let’s you see records for specific columns 


``` 
Select column, column, …, count(*) 
  from schema.table
  Group by column, column, …
  Order by column, column, … 
```  
  
* Let’s you see how many records are aggregated by the columns you have chosen by number of those records


```  
Select * from schema.table limit 10 
```  
  
* Let’s you see the first ten rows, you can set any limit you want. 

--- 

### Change Records:

``` 
Update schema.table
    set column = another_column,
    set column = <‘string’>,
    set column = <an integer> string,
    set column = another column’s values,
    set column = a numeric value
``` 
* Let’s you change records to be a specific

``` 
Insert into schema.table1 (column, column, …, ..., geom) 
select column, column, …, ..., geom from schema.table2
``` 

* Get records from one table  to another table using specific columns that exist in both, must include geom.

``` 
Update schema.table1
  set column = table2.column, column = table2.column
  from schema.table2
  where ST_Dwithin(table1.geom, table2.geom,<distance>)
```  
   
* Allows you to update columns from one table to another depending on spatial relationship

---

### Change the table:

``` 
Alter table schema.table
  add column varchar, 
  add column int,
  add column double precision,
``` 

* Allows you to add new columns to your table, you must state the data type and precision if needed.
  
```
Alter table schema.table rename to <new table name>
``` 

* Allows you to rename the table

```
Drop table if exists schema.table 
```

* Allows you to drop a table


``` 
Create table schema.table 
  (
    column varchar, 
    column int,
    column double precision,
  )
``` 

* Allows you to create a table with specified columns.


```     
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
    ST_Intersects(someabbreviation.geom,someotherabbreviation.geom)
``` 

* Allows you to create a new table where there is a spatial relationship between the two tables.   

--- 