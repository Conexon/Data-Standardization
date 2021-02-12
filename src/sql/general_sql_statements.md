# General SQL Statements for Standardization

Let’s keep this document as a reference for SQL statements that are handy for us to use. Please add to it if you have a more efficient statement or have a different statement that helped you accomplish a task. 

---

You want to…

### Look at records:


##### Look at all records

* Acts as a wildcard

``` 
  Select * from schema.table
``` 
---

##### Look at specific columns

  ``` 
   Select column, column, …, 
     from schema.table
  ```  

--- 

##### Aggregate and count by chosen columns

* Similar to Summary Statistics in ArcMap
* Great tool for QCing tables after standardization is complete

``` 
Select column, column, …, count(*) 
  from schema.table
  Group by column, column, …
  Order by column, column, … 
```  
  
---

##### View a specific number of rows from the table

* You can set any limit 

```  
Select * from schema.table limit 10 
```  
  

--- 

### Change Records:

##### Populate column values
``` 
Update schema.table
    set column = another_column,
    set column = <‘string’>,
    set column = <an integer> string,
    set column = another column’s values,
    set column = a numeric value
``` 
---

##### Append records from one table into another

* Must include geom data

``` 
Insert into schema.table1 (column, column, …, ..., geom) 
select column, column, …, ..., geom from schema.table2
``` 

---

##### Update one table based on another, depending on spatial relationship

* If missing susbstation or feeder info in the structure layer, this statement allows you to pull data from the closest electrical spans 

* Sets columns equal to the columns of the closest feature within the specified distance 

``` 
Update schema.table1
  set column = table2.column, column = table2.column
  from schema.table2
  where ST_Dwithin(table1.geom, table2.geom,<distance>)
```  

---

### Change the table:

##### Add new columns to cable

* Must state data type and precision if needed

``` 
Alter table schema.table
  add column varchar, 
  add column int,
  add column double precision,
``` 

---
  
##### Rename Table
```
Alter table schema.table rename to <new table name>
``` 

---

##### Delete/Drop a table

```
Drop table if exists schema.table 
```

---

##### Create table with specified columns

``` 
Create table schema.table 
  (
    column varchar, 
    column int,
    column double precision,
  )
``` 

---

##### Create a new table with a spatial relationship with another table

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
 
--- 