--substation
--add the standard fields to the substation table and populate those fields

alter table schema.table
	add cn_substat character varying,
 	add subname character varying
 
update schema.table
	set cn_substat = 'x',
	subname = 'x'
	
	
	
	
--electric_span
--add the standard fields to the electric_span table and populate those fields
--1 = oh primary, 2 = oh secondary, 3 = ug primary, 4 = ug secondary

alter table schema.table
	add cn_substat character varying,
	add cn_feeder character varying,
 	add subname character varying,
	add ring int,
	add ring_size int,
	add subtype int, 
	add length int
	
update schema.table
	set cn_substat = 'x',
	cn_feeder = 'x',
	subname = 'x',
	ring = 'x',
	subtype = 'x',
	length = 'x',
	ring_size = 'x'
	
	


--meter
--add the standard fields to the meter table and populate those fields
--make sure to add scada to this table (caps, regs, devices, etc.). if you don't know what these are then reach out to another designer. standardization is NOT complete without scada.

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
	
	
		
	
--structure
--add the standard fields to the structure table and populate those fields
--make sure to include ug transformers to this table
--ugtrans should be equal to 0 or 1
--0 = pole and 1 = ugtrans

alter table schema.table
	add cn_feeder character varying,
	add cn_substat character varying,
	add structid character varying, 
	add subname character varying,
	add ugtrans integer
	
update schema.table
	set cn_feeder = 'x',
	cn_substat = 'x',
	structid = 'x',
	subname = 'x',
	ugtrans = 'x'
	
	
	
	
--insert scada rows into meters
insert into coop.meter (city, cn_feeder, cn_substat, mail_add, scada, serv_loc, state, subname, phy_add, geom)
	select city, cn_feeder, cn_substat, mail_add, scada, serv_loc, state, subname, phy_add, geom
	from coop.scada
	
--insert ug transformer rows into structures 
insert into coop.structure (cn_feeder, cn_substat, subname, structid, ugtrans, geom)
	select cn_feeder, cn_substat, subname, structid, ugtrans, geom
	from coop.ugtransformer