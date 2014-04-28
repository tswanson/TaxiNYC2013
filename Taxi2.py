import csv,sys,os,time,math
#import arcpy
from datetime import datetime

from math import *

class XYCode:
    def __init__(self, row):
        self.XYcode = row[0]
        self.XYname = row[1]
        
def createXYLookup(dir):
    f = open(dir+'XYcode.csv', 'r')
    lookup = {}
    try:
        reader = csv.reader(f)
        for row in reader: 
            r = XYCode(row)
            lookup[r.XYcode] = "%s" % (r.XYname)
    except:
        print 'Error opening '+dir+'XYcode.csv', sys.exc_info()[0]
    
    return lookup

def distance(lon1, lat1, lon2, lat2):

    if(lon1 == 0 or lon2 == 0 or lat1 == 0 or lat2 == 0):
        return -1
    
    #haversine method
    #radius = 6371 # km
    radius = 3959 # miles
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    
    return d

def lineDirAngle(lon1, lat1, lon2, lat2):
#var y = Math.sin(dLon) * Math.cos(lat2);
#var x = Math.cos(lat1)*Math.sin(lat2) -
#        Math.sin(lat1)*Math.cos(lat2)*Math.cos(dLon);
#var brng = Math.atan2(y, x).toDeg();

    return atan2(lon2 - lon1, lat2 - lat1) * 180 / math.pi
    

    deltax = lon2 - lon1
    deltay = lat2 - lat1

    angle_rad = atan2(deltay,deltax)
    angle_deg = angle_rad*180.0/pi

    #print "The angle is %.5f radians (%.5f degrees)." % (angle_rad,angle_deg)
    return angle_deg

class taxiFare:
    def __init__(self, row):
        self.medallion = row[0]
        self.hack_license = row[1]
        self.vendor_id =  row[2]
        self.pickup_datetime = row[3]
        self.payment_type = row[4]
        self.fare_amount = row[5]
        self.surcharge = row[6]
        self.mta_tax = row[7]
        self.tip_amount = row[8]
        self.tolls_amount = row[9]
        self.total_amount = row[10]

class taxiData:
    def __init__(self, temp):
        row = temp.split(',')
        
        self.medallion = row[0]
        self.hack_license = row[1]
        self.vendor_id = row[2]
        self.rate_code = row[3]
        self.store_and_fwd_flag = row[4]
        self.pickup_datetime = row[5]
        self.dropoff_datetime = row[6]
        self.passenger_count = row[7]
        self.trip_time_in_secs = row[8]
        self.trip_distance = row[9]
        self.pickup_longitude = row[10]
        self.pickup_latitude = row[11]
        self.dropoff_longitude = row[12]
        tmp = row[13].split('\r\n')
        self.dropoff_latitude = tmp[0]

class taxiOut:
    def __init__(self):
        self.medallion = ''
        self.hack_license = ''
        self.vendor_id = ''
        self.rate_code = ''
        self.store_and_fwd_flag = ''
        self.pickup_datetime = ''
        self.dropoff_datetime = ''
        self.passenger_count = ''
        self.trip_time_in_secs = ''
        self.trip_distance = ''
        self.pickup_longitude = ''
        self.pickup_latitude = ''
        self.dropoff_longitude = ''
        self.dropoff_latitude = ''
        self.payment_type = ''
        self.fare_amount = ''
        self.surcharge = ''
        self.mta_tax = ''
        self.tip_amount = ''
        self.tolls_amount = ''
        self.total_amount = ''
        
header =  'epoch,hKey,rate_code,passenger_count,trip_time_in_secs,trip_distance,pickup_lon,pickup_lat,dropoff_lon,dropoff_lat,payment_type,fare_amount,tip_amount,tolls_amount,total_amount\n'
#header =  'pickup_dt,dropoff_dt,passenger_count,trip_time_in_secs,trip_distance,pickup_lon,pickup_lat,dropoff_lon,dropoff_lat,payment_type,fare_amount,surcharge,mta_tax,tip_amount,tolls_amount,total_amount,straight_dist,heading,pickup_month,pickup_day,pickup_hr,pickup_dow\n'

badCoord = 0

hack = {}
hack_c = {}
hackId = 0
medallion = {}
medallion_c = {}
medallionId = 0
vendor_id = {}
vendor_c = {}
vendor_idId = 0
rate_code = {}
rate_code_c = {}
store_and_fwd_flag = {}
store_and_fwd_flag_c = {}
passenger_count = {}
passenger_count_c = {}
trip_time_in_secs = {}
trip_time_in_secs_c = {}
trip_distance = {}
trip_distance_c = {}
payment_type = {}
payment_type_c = {}
payment = ''
fare_amount = {}
fare_amount_c = {}
surcharge = {}
surcharge_c = {}
mta_tax = {}
mta_tax_c = {}
tip_amount = {}
tip_amount_c = {}
tolls_amount = {}
tolls_amount_c = {}
total_amount = {}
total_amount_c = {}
pc = 0
rc = 0
triptime = 0
surchargeInt = 0
mtaInt = 0
tripDistInt = 0
fareInt = 0
tipInt = 0
totalInt = 0
tollsInt = 0
dropoffzone = ''
pickupzone = ''

XY = ''
XY_c = {}

start = time.time()
dir = os.path.dirname(os.path.realpath(__file__))+"\\"
j = 0

xylookup = createXYLookup(dir)


for num in range(1,13):

    numstr = '%i' % (num)
    
    ofile  = open(dir+'out'+numstr+'.csv', 'a')
    #if(num == 1):
    #    ofile.writelines(header)
    
    try:
        

        f_fare = open(dir+'trip_fare_'+numstr+'.csv', 'rb')
        f_data = open(dir+'trip_data_'+numstr+'.csv', 'rb') 
        
        i = 0
        reader_fare = csv.reader(f_fare)
        
        
        for row in reader_fare:
            
            fare = taxiFare(row)
            
            temp = f_data.readline()
            data= taxiData(temp)
            if(fare.medallion <> data.medallion):
                print 'bad medallion on line %i' % (i)
                
                
            if(fare.hack_license <> data.hack_license):
                print 'bad hack License on line %i' % (i)
                
               
            if(fare.pickup_datetime <> data.pickup_datetime):
                print 'bad datetime on line %i' % (i)
                   
            if(fare.medallion == 'medallion' or data.medallion == 'medallion'):
                continue

            if not data.medallion in medallion_c:
                medallion_c[data.medallion] = 1
            else:
                medallion_c[data.medallion] += 1

            if not data.hack_license in hack_c:
                hack_c[data.hack_license] = 1
            else:
                hack_c[data.hack_license] += 1

            if not data.vendor_id in vendor_c:
                vendor_c[data.vendor_id] = 1
            else:
                vendor_c[data.vendor_id] += 1

            if not data.rate_code in rate_code_c:
                rate_code_c[data.rate_code] = 1
            else:
                rate_code_c[data.rate_code] += 1

            if not data.store_and_fwd_flag in store_and_fwd_flag_c:
                store_and_fwd_flag_c[data.store_and_fwd_flag] = 1
            else:
                store_and_fwd_flag_c[data.store_and_fwd_flag] += 1

            if not data.passenger_count in passenger_count_c:
                passenger_count_c[data.passenger_count] = 1
            else:
                passenger_count_c[data.passenger_count] += 1

            if not data.trip_time_in_secs in trip_time_in_secs_c:
                trip_time_in_secs_c[data.trip_time_in_secs] = 1
            else:
                trip_time_in_secs_c[data.trip_time_in_secs] += 1

            if not data.trip_distance in trip_distance_c:
                trip_distance_c[data.trip_distance] = 1
            else:
                trip_distance_c[data.trip_distance] += 1

            if not fare.payment_type in payment_type_c:
                payment_type_c[fare.payment_type] = 1
            else:
                payment_type_c[fare.payment_type] += 1

            if not fare.fare_amount in fare_amount_c:
                fare_amount_c[fare.fare_amount] = 1
            else:
                fare_amount_c[fare.fare_amount] += 1

            if not fare.surcharge in surcharge_c:
                surcharge_c[fare.surcharge] = 1
            else:
                surcharge_c[fare.surcharge] += 1

            if not fare.mta_tax in mta_tax_c:
                mta_tax_c[fare.mta_tax] = 1
            else:
                mta_tax_c[fare.mta_tax] += 1

            if not fare.tip_amount in tip_amount_c:
                tip_amount_c[fare.tip_amount] = 1
            else:
                tip_amount_c[fare.tip_amount] += 1

            if not fare.total_amount in total_amount_c:
                total_amount_c[fare.total_amount] = 1
            else:
                total_amount_c[fare.total_amount] += 1

            if not fare.tolls_amount in tolls_amount_c:
                tolls_amount_c[fare.tolls_amount] = 1
            else:
                tolls_amount_c[fare.tolls_amount] += 1
                

            mKey = medallion.get(data.medallion, 'N')
            if(mKey == 'N'):
                medallion[data.medallion] = medallionId
                medallionId = medallionId +1
                mKey = medallion.get(data.medallion, 'N')

            hKey = hack.get(data.hack_license, 'N')
            if(hKey == 'N'):
                hack[data.hack_license] = hackId
                hackId = hackId +1
                hKey = hack.get(data.hack_license, 'N')

            vKey = vendor_id.get(data.vendor_id, 'N')
            if(vKey == 'N'):
                vendor_id[data.vendor_id] = vendor_idId
                vendor_idId = vendor_idId +1
                vKey = vendor_id.get(data.vendor_id, 'N')
            
            try:
                pc = int(data.passenger_count )
                
            except:
                pc = 0
                data.passenger_count = '0'
            if(pc>6):
                data.passenger_count = '6'
                

            try:
                pc = int(data.rate_code )
                
            except:
                pc = 0
                data.rate_code = '0'
            if(pc>6):
                data.rate_code = '6'


            try:
                triptime = int(data.trip_time_in_secs )
                
            except:
                triptime = 0
                data.trip_time_in_secs = '0'
            #4hrs
            if(triptime>14400 or triptime < 0):
                data.trip_time_in_secs = '0'
                triptime = 0

            try:
                tripDistInt = float(data.trip_distance )
                
            except:
                tripDistInt = 0.0
                data.trip_distance= '0'
            if(tripDistInt>70.0 or tripDistInt < 0):
                tripDistInt = 0
                data.trip_distance = '0'
                

            try:
                surchargeInt = float(fare.surcharge )
                
            except:
                surchargeInt = 0.0
                fare.surcharge = '0'
            if(surchargeInt>1 or surchargeInt < 0):
                surchargeInt = 0
                fare.surcharge = '0'

            try:
                mtaInt = float(fare.mta_tax )
                
            except:
                mtaInt = 0.0
                fare.mta_tax = '0'
            if(mtaInt>1 or mtaInt < 0):
                mtaInt = 0
                fare.mta_tax = '0'

            try:
                mtaInt = float(fare.mta_tax )
                
            except:
                mtaInt = 0.0
                fare.mta_tax = '0'
            if(mtaInt>1 or mtaInt < 0):
                mtaInt = 0
                fare.mta_tax = '0'

            try:
                tipInt = float(fare.tip_amount )
                
            except:
                tipInt = -1
                fare.tip_amount = '-1'
            if(tipInt>200 or tipInt < 0):
                tipInt = -1
                fare.tip_amount = '-1'
                
            try:
                fareInt = float(fare.fare_amount )
                
            except:
                fareInt = -1
                fare.fare_amount = '-1'
            if(fareInt>300 or fareInt < 0):
                fareInt = -1
                fare.fare_amount = '-1'

            try:
                totalInt = float(fare.total_amount )
                
            except:
                totalInt = -1
                fare.total_amount = '-1'
            if(totalInt>400 or totalInt < 0):
                totalInt = -1
                fare.total_amount = '-1'

            try:
                tollsInt = float(fare.tolls_amount )
                
            except:
                tollsInt = -1
                fare.tolls_amount = '-1'
            if(tollsInt>40 or tollsInt < 0):
                tollsInt = -1
                fare.tolls_amount = '-1'
                
            try:
                lon1 = float(data.pickup_longitude)
                lon2 = float(data.dropoff_longitude)
                lat1 = float(data.pickup_latitude)
                lat2 = float(data.dropoff_latitude)
            except:
                lon1 = 0
                lon2 = 0
                lat1 = 0
                lat2 = 0

      
                
            if(lon1 <-76.0 or lon1> -70.0 or lon2 <-76.0 or lon2> -70.0 or lat1<38.0 or lat1>42.0 or lat2<38.0 or lat2>42.0 ):
                lon1 = 0
                lon2 = 0
                lat1 = 0
                lat2 = 0
                data.pickup_longitude = '0'
                data.dropoff_longitude = '0'
                data.pickup_latitude = '0'
                data.dropoff_latitude = '0'
                badCoord +=1
                
            if(len(data.pickup_longitude) > 8):
                data.pickup_longitude = data.pickup_longitude[:8]
            if(len(data.dropoff_longitude) > 8):
                data.dropoff_longitude = data.dropoff_longitude[:8]

            if(len(data.pickup_latitude) > 7):
                data.pickup_latitude = data.pickup_latitude[:7]
            if(len(data.dropoff_latitude) >7):
                data.dropoff_latitude = data.dropoff_latitude[:7]
                             
 
                
            if(fare.payment_type == 'CSH'):
                payment = '0' 
            elif(fare.payment_type == 'DIS'):
                payment = '1'
            elif(fare.payment_type == 'NOC'):
                payment = '2'
            elif(fare.payment_type == 'CRD'):
                payment = '3'
            elif(fare.payment_type == 'UNK'):
                payment = '4'
            else:
                payment = '5'
            
            #print  '%s,%s,%s,%s' % (data.pickup_longitude,data.pickup_latitude,data.dropoff_longitude,data.dropoff_latitude)   
            dist = distance(lon1,lat1,lon2,lat2)
            if(dist >0):
                heading = lineDirAngle(lon1, lat1, lon2, lat2)
            else:
                heading = -1

            #dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
            #2013-01-01 15:11:48
            pattern = '%Y-%m-%d %H:%M:%S'
            dt_pickup =  datetime.strptime(data.pickup_datetime,pattern)
            pickup_yr = dt_pickup.year
            pickup_month = dt_pickup.month
            pickup_day= dt_pickup.day
            pickup_hr = dt_pickup.hour
            pickup_dow = dt_pickup.strftime("%w")
            pickup_weekday = dt_pickup.strftime("%A")
            date_time = data.pickup_datetime
           
            epoch = int(time.mktime(time.strptime(date_time, pattern)))

            XY = '%s%s' % (str((lon1*-1)*1000000)[:6],str((lat1)*1000000)[:6])
            
            #XY = '%s|%s' % (data.pickup_longitude,data.pickup_latitude)
            if not XY in XY_c :
                XY_c [XY] = 1
            else:
                XY_c [XY] += 1

            try:
                pickupzone = xylookup[XY]
            except:
                pickupzone = ''
                

            XY = '%s%s' % (str((lon2*-1)*1000000)[:6],str((lat2)*1000000)[:6])
            
            #XY = '%s|%s' % (data.pickup_longitude,data.pickup_latitude)
            if not XY in XY_c :
                XY_c [XY] = 1
            else:
                XY_c [XY] += 1

            try:
                dropoffzone = xylookup[XY]
            except:
                dropoffzone = ''
                
            #dt_dropoff =  datetime
            #    .strptime(data.dropoff_datetime,"%Y-%m-%d %H:%M:%S")
            #dropoff_yr = dt_dropoff.year
            #dropoff_month = dt_dropoff.month
            #dropoff_day= dt_dropoff.day
            #dropoff_hr = dt_dropoff.hour
            #dropoff_dow = dt_dropoff.strftime("%w")
            #dropoff_weekday = dt_dropoff.strftime("%A")
            
            #pickup = '%s,%s,%s,%s' % (pickup_month,pickup_day,pickup_hr,pickup_dow)
            #dropoff  = '%s,%s,%s,%s,%s,%s' % (dropoff_yr,dropoff_month,dropoff_day,dropoff_hr,dropoff_dow,dropoff_weekday)


            ret = '%i,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (epoch,hKey,data.rate_code,data.passenger_count,data.trip_time_in_secs,data.trip_distance,data.pickup_longitude,data.pickup_latitude,data.dropoff_longitude,data.dropoff_latitude,payment,fare.fare_amount,fare.tip_amount,fare.tolls_amount,fare.total_amount,pickupzone,dropoffzone)
            #,%.1f,%.0f
            if(lat2 <> 0 and tripDistInt <> 0 and triptime <>0 and tipInt <> -1 and fareInt <> -1 and totalInt <> -1 and tollsInt <> -1 and pickupzone <> '' and dropoffzone <> ''):
                ofile.writelines(ret)
            
            j = j+1
            i = i+1
            
            if(j%1000000 == 0):
               
                print j
                print time.time() - start, "seconds."
                   
                start = time.time()

        
        
        print str(i)+' records processed'
        f_fare.close()      # closing
        f_data.close()
        
            
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

f_medallion_c  = open(dir+'medallion_c.csv', 'a')        
for item in medallion_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_medallion_c.writelines(templine)
f_medallion_c.close()

f_medallion  = open(dir+'medallion.csv', 'a')        
for item in medallion.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_medallion.writelines(templine)
f_medallion.close()

f_hack_c  = open(dir+'hack_c.csv', 'a')        
for item in hack_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_hack_c.writelines(templine)
f_hack_c.close()

f_hack  = open(dir+'hack.csv', 'a')        
for item in hack.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_hack.writelines(templine)
f_hack.close()

f_vendor_c  = open(dir+'vendor_c.csv', 'a')        
for item in vendor_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_vendor_c.writelines(templine)
f_vendor_c.close()

f_vendor  = open(dir+'vendor.csv', 'a')        
for item in vendor_id.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_vendor.writelines(templine)
f_vendor.close()

f_rate_code_c  = open(dir+'rate_code_c.csv', 'a')        
for item in rate_code_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_rate_code_c.writelines(templine)
f_rate_code_c.close()

f_store_and_fwd_flag_c  = open(dir+'store_and_fwd_flag_c.csv', 'a')        
for item in store_and_fwd_flag_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_store_and_fwd_flag_c.writelines(templine)
f_store_and_fwd_flag_c.close()

f_passenger_count_c  = open(dir+'passenger_count_c.csv', 'a')        
for item in passenger_count_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_passenger_count_c.writelines(templine)
f_passenger_count_c.close()

f_trip_time_in_secs_c  = open(dir+'trip_time_in_secs_c.csv', 'a')        
for item in trip_time_in_secs_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_trip_time_in_secs_c.writelines(templine)
f_trip_time_in_secs_c.close()

f_trip_distance_c  = open(dir+'trip_distance_c.csv', 'a')        
for item in trip_distance_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_trip_distance_c.writelines(templine)
f_trip_distance_c.close()

f_payment_type_c  = open(dir+'payment_type_c.csv', 'a')        
for item in payment_type_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_payment_type_c.writelines(templine)
f_payment_type_c.close()

f_fare_amount_c  = open(dir+'fare_amount_c.csv', 'a')        
for item in fare_amount_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_fare_amount_c.writelines(templine)
f_fare_amount_c.close()

f_surcharge_c  = open(dir+'surcharge_c.csv', 'a')        
for item in surcharge_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_surcharge_c.writelines(templine)
f_surcharge_c.close()

f_mta_tax_c  = open(dir+'mta_tax_c.csv', 'a')        
for item in mta_tax_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_mta_tax_c.writelines(templine)
f_mta_tax_c.close()

f_tip_amount_c  = open(dir+'tip_amount_c.csv', 'a')        
for item in tip_amount_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_tip_amount_c.writelines(templine)
f_tip_amount_c.close()

f_tolls_amount_c  = open(dir+'tolls_amount_c.csv', 'a')        
for item in tolls_amount_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_tolls_amount_c.writelines(templine)
f_tolls_amount_c.close()

f_total_amount_c  = open(dir+'total_amount_c.csv', 'a')        
for item in total_amount_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_total_amount_c.writelines(templine)
f_total_amount_c.close()

f_XY_c  = open(dir+'total_XY_c.csv', 'a')        
for item in XY_c.iteritems():
    templine = '%s,%i\n' % (item[0],item[1])
    f_XY_c.writelines(templine)
f_XY_c.close()

print str(j)+' records processed'
print str(badCoord)+ ' bad or no coordinates'
ofile.close()