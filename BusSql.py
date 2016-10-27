import heapq
import datetime
import time
import sqlite3
from math import sqrt, atan2, degrees

from google.transit import gtfs_realtime_pb2
import urllib
import datetime
import time


class Stop():
    def __init__(self, stop_id, name, lat, lon, dist, dire):
        self.stop_id = stop_id
        self.stop_name = name
        self.stop_lat = lat
        self.stop_lon = lon
        self.stop_dist = dist
        self.stop_dir = dire

class Time():
    def __init__(self, trip_id, departure_time):
        self.trip_id = trip_id
        self.departure_time_seconds = departure_time

class Trip():
    def __init__(self, route_id):
        self.route_id = route_id

class Route():
    def __init__(self, short_name, long_name):
        self.route_short_name = short_name
        self.route_long_name = long_name


class Schedule():
    def __init__(self, staticDir):
        self.conn = sqlite3.connect(staticDir)
        self.curs = self.conn.cursor()

    def get_times_by_stop(self, stop, n_times, dt_offset = 120):
        """ Return the next n arrivals at the given stop """
        
        current_time = self._seconds_since_midnight()

        # Get the next n times which are arriving at a given stop
        s = 'SELECT trip_id, departure_time_seconds FROM Time WHERE stop_id == "' + str(stop.stop_id) + '"'
        s += ' AND departure_time_seconds > "' +str(current_time-dt_offset)+ '"'
        s += ' AND trip_id LIKE "%FUL%"' 
        
        self.curs.execute(s)
        rows = self.curs.fetchall()

        times = []
        for row in rows:
            times.append(Time(row[0], int(row[1])))

        return heapq.nsmallest(n_times, times, key = lambda t: t.departure_time_seconds)

    def get_trip(self, time):
        """ Return the trip (containing route_id and direction_id) for a given stop time """

        # Get the next n times which are arriving at a given stop
        s = 'SELECT route_id FROM Trip WHERE trip_id == "' + str(time.trip_id) + '"'
        self.curs.execute(s)
        rows = self.curs.fetchall()
        ## There may be multiple route ids for each trip
        #for row in rows:
        trip = Trip(rows[0][0])

        return trip

    def get_route(self, trip):
        """ Return the route (containing short and long route names) for a given trip """

        s = 'SELECT route_short_name, route_long_name FROM Route WHERE route_id == "' + str(trip.route_id) + '"'
        self.curs.execute(s)
        rows = self.curs.fetchone()
        route = Route(str(rows[0]), str(rows[1]))

        return route

# return empty stops but make it clear there is nothin there succinctly.

    def nearest_with_trips(self,u_lat,u_lon, n_stops = 1):
        """ Return index of nearest bus stop to specified coordinates """

        s = 'SELECT stop_id, stop_name, stop_lat, stop_lon FROM Stop' 
        self.curs.execute(s)
        rows = self.curs.fetchall()

        stops = []
        for row in rows:
            dist, dirn = self.get_loc(u_lat, u_lon, float(row[2]), float(row[3]))
            stops.append(Stop(row[0], str(row[1]), float(row[2]), float(row[3]), dist, dirn))

        dist = lambda stop: stop.stop_dist
        return heapq.nsmallest(n_stops, stops, key = dist)

    def get_loc(self, lat1, lon1, lat2, lon2):
        """ Return distance and direction from user to stop (Euclidian approximation) """

        R = 6371 # Approx radius of Earth (km)

        dist = sqrt((float(lat1)-float(lat2))**2 + (float(lon1)-float(lon2))**2)*R

        bearing = atan2((lon2 - lon1),(lat2 - lat1))

        dirn = {
            "N":    0,
            "NNE":  22.5,
            "NE":   45,
            "ENE":  67.5,
            "E":    90,
            "ESE":  112.5,
            "SE":   135,
            "SSE":  157.5,
            "S":    180,
            "SSW":  202.5,
            "SW":   225,
            "WSW":  247.5,
            "W":    270,
            "WNW":  292.5,
            "NW":   315,
            "NNW":  337.5
        }

        for key in dirn:
            if abs(degrees(bearing)-dirn[key]) <= 11.25:
                return dist, key
        else:
            # value must have fallen between 348.75 and 0
            return dist, "N"


    def _seconds_since_midnight(self):
        now = time.time()
        return int(now - self._seconds_at_midnight())
    
    def _seconds_at_midnight(self):
        today = datetime.date.today()
        unix_time= today.strftime("%s") #Second as a decimal number [00,61] (or Unix Timestamp)
        return int(unix_time)

    def output(self, u_lat, u_lon, n_stops = 1, n_times = 3):

        #get latest live feed
        ### updatedFeed = self.update_info()
       
        close_stops = self.nearest_with_trips(u_lat, u_lon, n_stops)

        seconds_since_midnight = self._seconds_since_midnight()

        stoplist = []
        for stop in close_stops:
            times = self.get_times_by_stop(stop, n_times)
            lines = []

            # Check if times is empty
            if not times:
               for i in range(0, n_times):
                   lines.append(
                       ("   ", "         No Service         ", "     ")
                       )
            else:

                for time in times:
                    trip = self.get_trip(time)
                    route = self.get_route(trip)

                    #Update the time entry from live feed
                    #### latest_time = self.update_time(updatedFeed, time)
                    latest_time = time
    
                    mins_to_dep = int((latest_time.departure_time_seconds - seconds_since_midnight)//60)
                    min_suffix = ' min' if abs(mins_to_dep) == 1 else ' mins'
    
                    lines.append(
                        (route.route_short_name, route.route_long_name, str(mins_to_dep)+min_suffix)
                        )
                
            stoplist.append({
                'stop':  stop.stop_name,
                'lines': lines,
                'dist':  '{0:.1f} km'.format(stop.stop_dist),
                'dirn': stop.stop_dir
                })
        return stoplist

    def update_time(self, updatedFeed, time):
        for updatedLine in updatedFeed:
                if updatedLine[1] == time.stop_sequence:
                    time.arrival_time_seconds = updatedLine[2]
                    time.departure_time_seconds = updatedLine[3]
        return time 

    
    def update_info(self):
        secondsAtMidnight = seconds_at_midnight()
        feed = gtfs_realtime_pb2.FeedMessage()
        response = urllib.urlopen('https://gtfsrt.api.translink.com.au/Feed/SEQ')
        feed.ParseFromString(response.read())
        arrayRow = 0
        outputArray = []
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                stopTimeUpdate = entity.trip_update.stop_time_update

            if len(stopTimeUpdate) > 0:
                for i in stopTimeUpdate:
                    outputArray.append([i.stop_id, i.stop_sequence, i.arrival.time - secondsAtMidnight, i.departure.time - secondsAtMidnight])
        return outputArray



if __name__ == '__main__':

    schedule = Schedule('StaticGtfs.db')
    print schedule.output(-27.4836803,152.9950037, 1,3)

    
