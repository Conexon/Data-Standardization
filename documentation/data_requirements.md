# Conexon Data Standardization Requirements

This document describes the requirements for the input spatial data. We keep these requirements to a minimum, as most cooperative’s already keep GIS data in similar formats. Conexon design and construction requires a minimum of five input spatial data sets in order to start our design process. Those five are (1) Substations, (2) Customers, (3) Spans, (4) Poles and (5) Underground Transformers. Data delivery can be either in an ESRI File Geodatabase or individual ESRI Shapefiles. 

Conexon requires two supplementary data sets for better network connectivity and construction efficiency. Those two are (6) SCADA devices and (7) Any Existing Fiber Data if applicable. Below are the requirements for these files. In ESRI speak, these would be individual Feature Classes. **All spatial data need to have the *same defined state plane projection in US feet.* If this is not what you use within your mapping system, please let Conexon know.** 

1. **Substation/Distrobution Sources** -
are point data showing the location of the electric substations. Substations need to be snapped to the span linear features (minor spatial gaps are acceptable, but these should be small < 1'). The name of this feature class can be called anything, but the Coop should tell Conexon explicitly which dataset represents Substations. Attribute data for Substations needs to contain at least the fields described below and can contain any other fields that already exist in the cooperative’s database. The Field Name column can be called any name, but there needs at least to be a field in the feature class performing this function. 
  
    **Substation layer must only include true substations as a point file.** Metering stations must be excluded from this layer.
    
    Number | Field Name | Example Values | Comment
    ------------ | ------------- | ------------- | -------------
    1 | Name | "Mike's Substation" | This field and its values is purely for naming convention
    2 | Substation | 1 or "Ark" | A substation number (preferred) or shortened name. This same field and associated value need to be on the Customers and Span data as a primary key relationship
    
    
    
2. **Consumers** -
aka meters, service locations, etc. - are the point data showing the locations of the electric customers in your network. Consumers need to be connected to the span linear features (e.g. intersecting with the electric line data). The name of this feature class can be called anything, but the cooperative should tell Conexon explicitly which dataset represents Consumers. Attribute data for Consumers needs to contain at least the fields described below and can contain any other fields that already exist in the Coops database. The Field Name column can be called any name, but there needs at least to be a field in the feature class performing this function.

    Number | Field Name | Example Values | Comment
    ------------ | ------------- | ------------- | -------------
    1 | Substation | 1 or "Ark" | A substation number (preferred) or shortened name. This same field and associated value need to be on the Customers and Span data as a primary key relationship
    2 | Feeder | 1 or “Feeder = 1”  | The Feeder field is populated to filter all of the meters in a particular feeder.  It has a primary key relationship with Spans and Substations. 
    3 | Service Map Location | | The service map location for the meter.  This is a unique field value. 
    4 | Account Number | | A unique identifier for consumer accounts that would allow any cooperative member to find their account. This is for member sign-ups post construction using Conexon Sign-Ups.
    
3. **Spans** -
are the linear data showing the locations of the electric spans for your network. The Spans data needs to be a **topologically connected network.** What this means is that each line needs to snap to and be connected to any line it is next to. If gaps in the linear network exist, then the data cannot be accepted to perform basic electric use cases and fiber design. The name of this feature class can be called anything, but the cooperative should tell Conexon explicitly which source dataset represents Spans. Attribute data for Spans needs to contain at least the fields below and can contain any other fields that already exist in the cooperative’s database. The Field Name column can be called any name, but there needs to be at least a field in the feature class performing this function. It is most helpful if this is one appended dataset, rather than distinct separated feature classes or shapefiles. Conexon has a method of helping with ensuring the data is topologically connected. 

    **Spans need to also have a column containing 3phase information.** This allows the Conexon Design team to create the fiber distribution ring; a path to each substation within the proposed fiber network that sends light to fiber huts.  
    
    Number | Field Name | Example Values | Comment
    ------------ | ------------- | ------------- | -------------
    1 | Substation | 1 or "Ark" | A substation number (preferred) or shortened name. This same field and associated value need to be on the Customers and Span data as a primary key relationship
    2 | Feeder | 1 or “Feeder = 1”  | The Feeder field is populated to filter all of the meters in a particular feeder.  It has a primary key relationship with Spans and Substations. 
    3 | Subtype | 1, 2, 3, 4 | The Subtype field filters values for Primary/Secondary/Aerial/Underground. Primary Aerial are coded as 1; Secondary Aerial are coded as 2; Primary Underground are coded as 3; Secondary Underground are coded as 4. 
    
4. **Poles** - 
are the point data showing the locations of the electric poles in your network (aka structure). Poles need to be connected to the span linear features (e.g. intersecting with the electric line data). The name of this feature class can be called anything, but the Coop should tell Conexon explicitly which dataset represents Poles represents. Poles do not need to have sub/feeder information but do need to have a unique structure ID that represents its location out in the field. 

5. **Underground transformers** – 
point data showing the locations of the transformer banks in your network. UG transformers need to be connected to the span linear features (e.g. intersecting with the electric line data). The name of this feature class can be called anything, but the Coop should tell Conexon explicitly which dataset represents UG Transformers. These do not need to have sub/feeder information but do need to have a unique structure ID that represents its location out in the field. 

6. **SCADA devices** - 
we often append point data like SCADA and other devices that you want as potential locations for smartgrid etc. Please let us know what other point data you want to appear in the ‘meters’ table. These should all include substation and feeder information. Conexon builds to one hundred percent of meters and therefore will want to include these devices within the Customers data. We also request **capacitors, reclosers and regulators** for potential fiber connectivity. 

7. **Any Existing Fiber Data** – 
if applicable, we would like to have any fiber optic cable lines (polylines) and any pedestals and/or vaults (points). This is useful in terms of wanting to incorporate this into your future fiber optic network, understand financial models with this existing implementation, etc. 

8. **Pole Assembly Units** – 
classification of the type of assemblies found on poles, including crossarms, transformers, guys, anchors, arrestors, fuses, etc. These are needed for Make-Ready engineering, specifically for poles with crossarms. Conexon requires number of assembly types by feeder provided by the client if using construction services. 


### Other information needed: 

   * Provide a primary contact for GIS data related questions 

   * All database extensions turned off (example: ArcFM or Futura extensions) 

   * Spreadsheet of Substations and their Feeders 
    
