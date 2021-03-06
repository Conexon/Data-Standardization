--1. did you add scada (regs, caps, devices, etc.) to the meter table?
--   did you add ug transformers to the structure table?
--   if you answered "no" to these questions, then go back and add them
--   if you are unsure if the coop has these, then reach out to another designer



--2. check that the standardized columns exist in each table
--if a column does not exist in the table you will receive an error (ex: "ERROR: column 'cn_substat' does not exist")

--substation
select cn_substat, subname
  from schema.substation

--meter
select city, cn_feeder, cn_substat, mail_add, scada, serv_loc, state, subname, phy_add, acct_num, zip
  from schema.meter

--electric_span
select cn_feeder, cn_substat, length, ring, ring_size, subtype, subname
  from schema.electric_span
  
--structure
select cn_feeder, cn_substat, structid, subname, ugtrans
  from schema.structure
  


--3. check that the data type of all required fields are correct 
--select the table, select SQL on the browser, check that data types match https://github.com/Conexon/data-processing/wiki/Data-Validation-Fields



--4. check fields that CANNOT have null values
--if null values exist in any of these fields, you must fix the data and check again

--substation
select * from schema.substation
  where cn_substat is null
  or subname is null
  
--meter
select * from table.meter
  where cn_substat is null 
  or cn_feeder is null
  or subname is null
  or scada is null

--electric_span
select * from schema.electric_span 
  where cn_feeder is null
  or cn_substat is null
  or length is null
  or ring is null
  or ring_size is null
  or subtype is null
  
--structure
select * from schema.structure 
  where cn_feeder is null
  or cn_substat is null
  or structid is null
  
  
 
--5. check fields that can only have specific domain values
--if values other than those allowed are in the data, you must fix the data and check again

--meter
select scada, count(*)
  from schema.meter
  where not scada = '0'
  and not scada = '1'
  group by scada  
  
--electric_span
select ring, count(*)
  from schema.electric_span
  where not ring = 0
  and not ring = 1
  group by ring
  
select ring_size, count(*)
  from schema.electric_span
  where not ring_size = 0
  and not ring_size = 96
  and not ring_size = 144
  group by ring_size
  
select subtype, count(*)
  from schema.electric_span
  where not subtype = 1
  and not subtype = 2
  and not subtype = 3
  and not subtype = 4
  and not subtype = 5
  group by subtype

--6. check for invalid geometries
--if duplicate values or incorrect spatial proximity (e.g. not within data envelope) exist in any layer.

select cn_substat, cn_feeder, st_x(geom), st_y(geom)
    from schema.table
    where st_x(geom) < 1
    order by st_x(geom)
    
select gid, cn_substat, cn_feeder, st_length(geom), st_geometrytype(geom), st_isvalid(geom)
    from schema.electric_span
    where st_isvalid(geom) is Null
    order by st_length(geom) desc
    
select st_length(geom),cn_substat, cn_feeder, count(*)
    from schema.electric_span
    group by st_length(geom), cn_substat, cn_feeder
    having count(*) > 0
    order by count(*) desc
