NYC Taxi 2013
=======

Data from Chris Whong - http://chriswhong.com/open-data/foil_nyc_taxi/

This project attempt to take raw NYC Taxi data and make it usable to analysis and mapping.
This data is roughly 50GB and 170mill records which creates a challenge.
There are two files for each month, one for fare data and the other trip


Taxi2.py
-----------
Python script combines the data, normalized fields, cleans up outliers.

taxi2.py uses XYcode.csv as input to link a zone(LGA or MN17) for easier analysis.  Zones are modified Neighborhood Tabulation Areas - http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml

taxi2.py keeps track of counts for unique values for most fields.

-epoch - Trip start time, seconds since 1/1/1970
-hackID - normalized id for hack
-rateCode - rate code - see 
-passengerCount
-tripTimeSec
-distance - actual miles driven
-pickupLongitude - 
-pickupLatitude
-dropoffLongitude
-dropoffLatitude
-paymentType
-fareAmount
-tipAmount - Credit card transactions only
-tollsAmount 
-totalAmount
-pickup - Zone code (LGA, MN17)
-dropoff - Zone code (LGA, MN17)
