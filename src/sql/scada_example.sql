alter table schema.table
	add city character varying,
	add cn_feeder character varying, 
	add cn_substat character varying, 
	add mail_add character varying, 
	add scada character varying,
	add serv_loc character varying, 
	add state character varying,
	add subname character varying,
	add phy_add character varying
	
update data.ms_east_recloser
	set city = null
update data.ms_east_recloser
	set cn_feeder = feeder
update data.ms_east_recloser
	set cn_substat = feeder
update data.ms_east_recloser
	set mail_add = null
update data.ms_east_recloser
	set scada = '1'
update data.ms_east_recloser
	set serv_loc = mapnumber
update data.ms_east_recloser
	set state = 'MS'
update data.ms_east_recloser
	set subname = 'x'
update data.ms_east_recloser
	set phy_add = null

update data.ms_east_recloser
set cn_substat = left(cn_substat, LENGTH(cn_substat) -2)
	
update data.ms_east_recloser
set cn_feeder = RIGHT(feeder, 1)


update data.ms_east_recloser
set cn_substat = concat('0', cn_substat)
where cn_substat = '1'
or cn_substat ='2'
or cn_substat ='3'
or cn_substat = '4'
or cn_substat ='5'
or cn_substat ='6'
or cn_substat ='7'
or cn_substat ='8'
or cn_substat ='9'

--update a column from another table using a left join
--in this example... set the subname field in the span data equal to the subname in the substation field based on cn_substat
update data.ms_east_recloser
	set subname = ms_east_meter.subname
	from data.ms_east_meter
	where ms_east_meter.cn_substat = ms_east_recloser.cn_substat
	
select feeder, cn_substat, cn_feeder, subname, count(*)
from data.ms_east_capacitor
group by feeder, cn_substat, cn_feeder, subname
order by feeder, cn_substat, cn_feeder, subname asc

select city, cn_substat, cn_feeder, mail_add, scada, serv_loc, state, subname, phy_add, count(*)
from data.ms_east_capacitor
group by city, cn_substat, cn_feeder, mail_add, scada, serv_loc, state, subname, phy_add

insert into data.ms_east_meter (city, cn_substat, cn_feeder, mail_add, scada, serv_loc, state, subname, phy_add, geom)
	select city, cn_substat, cn_feeder, mail_add, scada, serv_loc, state, subname, phy_add, geom
	from data.ms_east_capacitor
