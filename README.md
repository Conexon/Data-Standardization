## Data-Standardization

This is the data standardization repository. The purpose of this is to continue the process of standardizing coop data for Conexon clients. More documents live here:
https://teams.microsoft.com/_#/files/TRAINING?threadId=19%3A879c5e18fe5943ada580c8c0c284dc39%40thread.skype&ctx=channel&context=Standardization%2520and%2520Staking%2520Grids&rootfolder=%252Fsites%252FConexonDesignTeam%252FShared%2520Documents%252FTRAINING%252FStandardization%2520and%2520Staking%2520Grids

# Below are explanations of the client data that we request for designing and constructing fiber optic networks. Those who standardize client data need to know what they are looking for:

Conexon design and construction requires a minimum of five input spatial data sets in order to start our design process. Those five are (1) Substations, (2) Customers, (3) Spans, (4) Poles and (5) Underground Transformers. Data delivery can be either in an ESRI File Geodatabase or individual ESRI Shapefiles. 
Conexon requires two supplementary data sets for better network connectivity and construction efficiency. Those two are (6) SCADA devices and (7) Any Existing Fiber Data if applicable.
Below are the requirements for these files. In ESRI speak, these would be individual Feature Classes. All spatial data need to have the same defined state plane projection in US feet. 

1.	Substations/Distribution Sources - are point data showing the location of the electric substations. Substations need to be snapped to the span linear features (minor spatial gaps are acceptable, but these should be small < 1'). The name of this feature class can be called anything, but the Coop should tell Conexon explicitly which dataset represents Substations. Attribute data for Substations needs to contain at least the fields described below and can contain any other fields that already exist in the cooperative’s database. The Field Name column can be called any name, but there needs at least to be a field in the feature class performing this function. 
Substation layer must only include true substations as a point file. Metering stations must be excluded from this layer.

2.	Consumers - aka meters, service locations, etc. - are the point data showing the locations of the electric customers in your network. Consumers need to be connected to the span linear features (e.g. intersecting with the electric line data). The name of this feature class can be called anything, but the cooperative should tell Conexon explicitly which dataset represents Consumers. Attribute data for Consumers needs to contain at least the fields described below and can contain any other fields that already exist in the Coops database. The Field Name column can be called any name, but there needs at least to be a field in the feature class performing this function. 

Client Data Standardization Notes located at link below:
https://docs.google.com/spreadsheets/d/1LaqQctBjgub1Yu6_oHfL_KEdhICQ5l48Y1oa_NPfb0U/edit?usp=sharing

All documentation related to data standardization is located [**here**](https://github.com/Conexon/Data-Standardization/tree/master/documentation)
