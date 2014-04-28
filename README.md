NYC Taxi 2013
=======

Data from Chris Whong - http://chriswhong.com/open-data/foil_nyc_taxi/

This project attempt to take raw NYC Taxi data and make it usable to analysis and mapping.
This data is roughly 50GB and 170mill records which creates a challenge.
There are two files for each month, one for fare data and the other trip


Taxi2.py
-----------
Python script combines the data, normalized fields, cleans up outliers.

taxi2.py keeps track of counts for unique values for most fields.

   fare_amount_c.csv  
   hack_c.csv  
   medallion_c.csv  
   mta_tax_c.csv  
   passenger_count_c.csv  
   payment_type_c.csv  
   rate_code_c.csv  
   store_and_fwd_flag_c.csv  
   surcharge_c.csv  
   tip_amount_c.csv  
   tolls_amount_c.csv  
   total_amount_c.csv  
   trip_distance_c.csv  
   trip_time_in_secs_c.csv  
   vendor_c.csv 
   
Output Fields
-----------
   epoch - Trip start time, seconds since 1/1/1970  
   hackID - normalized id for hack  
   rateCode - rate code - see   
   passengerCount  
   tripTimeSec  
   distance - actual miles driven  
   pickupLongitude - 4 decimal places only  
   pickupLatitude - 4 decimal places only  
   dropoffLongitude - 4 decimal places only  
   dropoffLatitude - 4 decimal places only  
   paymentType - see payment_type_c.csv  
   fareAmount
   tipAmount - Credit card transactions only  
   tollsAmount   
   totalAmount - fareAmount+MTAcharge+Surchare+tolls+tip  
   pickup - Zone code (LGA, MN17)  
   dropoff - Zone code (LGA, MN17)  

Zone Codes
-------------

taxi2.py uses XYcode.csv as input to link a zone(LGA or MN17) for easier analysis.  Zones are modified Neighborhood        Tabulation Areas - http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml  
   Added default areas for NJ, EWR, Upstate NY, CT, LI  

Totals by Pickup and Dropoff Zones - pickupAndDropoffZone.csv

Totals by Pickup Zone - PickupByZone.csv

Totals by Dropoff Zone - dropoffByZone.csv

Shape file of Zones - Taxi2013Zones.zip

Example Map of Zones - http://www.arcgis.com/home/item.html?id=ab7a2fbf8d614603b2feb1c2b9289a95

