from math import sin, cos, sqrt, atan2, radians
import decimal
import geopy
import geopy.distance
		
def DistanceClaculate(lat1,lon1,lat2,lon2):



	pt1 = geopy.Point(lat1, lon1)
	pt2 = geopy.Point(lat2, lon2)
	# distance.distance() is the  VincentyDistance by default.
	dist = geopy.distance.distance(pt1, pt2).km
	return round(dist,2)
def DistanceClaculate2():
		
	R = 6373.0

	# lat1 = radians(23.812678)
	# lon1 = radians(90.403876)
	# lat2 = radians(23.778908)
	# lon2 = radians(90.398211)
	lat1 = radians(23.810332)
	lon1 = radians(90.4125181)
	lat2 = radians(23.7417656252)
	lon2 = radians(90.4087260576)

	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	distance = R * c

	print "Result", distance
	# print "Should be", 278.546
	#print "Result", distance46
	return distance
# DistanceClaculate2()











# Result 437.002911868

