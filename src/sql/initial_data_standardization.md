# Initial Data Standardizatiion

This document details the sql statements needed to standardize electrical data to prepare it to be run through auto design. **Make sure that these changes not being made in your clients database in pgaws.** If you are standardizing within pgaws, check to make sure that you are in your cleints schema in the **standardize** database. You can also standardize within your own local server on pgAdmin.

---

### substation

##### Add the standard fields to the substation table and populate those fields
``` 
alter table schema.table
	add cn_substat character varying,
 	add subname character varying
``` 

``` 
update schema.table
	set cn_substat = 'x',
	subname = 'x'
``` 
---	
	
### electric_span

##### Add the standard fields to the electric_span table and populate those fields.
* Subtypes
	* 1 = oh primary, 2 = oh secondary, 3 = ug primary, 4 = ug secondary
 
``` 
alter table schema.table
	add cn_substat character varying,
	add cn_feeder character varying,
 	add subname character varying,
	add ring int,
	add ring_size int,
	add subtype int, 
	add length int
``` 

``` 
update schema.table
	set cn_substat = 'x',
	cn_feeder = 'x',
	subname = 'x',
	ring = 'x',
	subtype = 'x',
	length = 'x',
	ring_size = 'x'
``` 
---

### meter

##### Add the standard fields to the meter table and populate those fields.

Make sure to add scada to this table (caps, regs, devices, etc.). If you don't know what these are then reach out to another designer. Standardization is NOT complete without scada.

* **Necessary columns:**
	* cn_feeder
	* cn_substat
	* scada
	* subname

* Add the other columns if data is available.

``` 
alter table schema.table
	add city character varying,
	add cn_feeder character varying, 
	add cn_substat character varying, 
	add mail_add character varying, 
	add scada character varying,
	add serv_loc character varying, 
	add state character varying,
	add subname character varying,
	add phy_add character varying,
	add acct_num character varying,
	add zip character varying
```  

``` 
update schema.table
	set city = 'x',
	cn_feeder = 'x',
	cn_substat = 'x',
	mail_add = 'x',
	scada = 'x',
	serv_loc = 'x',
	state = 'x',
	subname = 'x',
	phy_add = 'x',
	acct_num = 'x',
	zip = 'x'
``` 

--- 

### structure

##### Add the standard fields to the structure table and populate those fields.

* Make sure to include ug transformers to this table.
* ugtrans should be equal to 0 or 1
	* 0 = pole and 1 = ugtrans

``` 
alter table schema.table
	add cn_feeder character varying,
	add cn_substat character varying,
	add structid character varying, 
	add subname character varying,
	add ugtrans integer
``` 

``` 
update schema.table
	set cn_feeder = 'x',
	cn_substat = 'x',
	structid = 'x',
	subname = 'x',
	ugtrans = 'x'
``` 	
	
--- 

### scada
SCADA devices (capacitors, regulators, reclosers, devices, etc.) will be standardized with the same columns as the meter table. 

* Set scada = 1 before you insert into the meter table.


##### Insert scada rows into meters

``` 
insert into coop.meter (city, cn_feeder, cn_substat, mail_add, scada, serv_loc, state, subname, phy_add, geom)
	select city, cn_feeder, cn_substat, mail_add, scada, serv_loc, state, subname, phy_add, geom
	from coop.scada
``` 

---

### ug_transformer
 Underground transformers will be standardized with the same columns as structure table. 
 
 * Set ugtrans = 1 before you insert into the structure table.

##### Insert ug transformer rows into structures 

``` 
insert into coop.structure (cn_feeder, cn_substat, subname, structid, ugtrans, geom)
	select cn_feeder, cn_substat, subname, structid, ugtrans, geom
	from coop.ugtransformer
``` 