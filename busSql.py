import heapq
import datetime
import time



class Stop():
    def __init__(self, stop_id, name, lat, lon, dire):
        self.stop_id = stop_id
        self.stop_name = name
        self.stop_lat = lat
        self.stop_lon = lon
        delf.stop_dir = dire

class Time():
    def __init__(self, trip_id, departure_time):
        self.trip_id = trip_id
        self.departure_time_seconds = departure_time

class Trip():
    def __init__(self, route_id):
        self.route_id = route_id

class Route():
    def __init_(self, short_name, long_name):
        self.route_short_name = short_name
        self.route_long_name = long_name




class Schedule():
    def __init__(self, savedir = None):
        gtfs_dir = 'SEQ_GTFS'
        self.import_static_gtfs(gtfs_dir)


    def import_static_gtfs(self, gtfs_dir):
        self.conn = sqlite3.connect('staticGtfs.db')
        self.curs = self.conn.cursor()
        

        """ Import relevant GTFS data """

    def get_times_by_stop(self, stop, n_times, dt_offset = 120):
        """ Return the next n arrivals at the given stop """
        
        current_time = self._seconds_since_midnight()

        # Get the next n times which are arriving at a given stop
        s = 'SELECT trip_id, departure_time_seconds FROM Time WHERE stop_id ==' + str(stop_stop_id) 
        s += ' AND departure_time_seconds > ' +str(current_time-dt_offset)
        s += ' AND trip_id LIKE "%FUL%"' 
        
        self.curs.execute(s)
        rows = self.curs.fetchall()

        times = []
        for row in rows:
            times.append(Time(row[0], row[1]))

        time = lambda trip_info: trip_info[1]
        return heapq.nsmallest(n_times, trip_info, key = time )

    def get_trip(self, time):
        """ Return the trip (containing route_id and direction_id) for a given stop time """

        # Get the next n times which are arriving at a given stop
        s = 'SELECT route_id FROM Trip WHERE stop_id ==' + str(time.trip_id) 
        self.curs.execute(s)
        rows = self.curs.fetchall()

        trips = []
        for row in rows:
            trips.append(Trip(row[0]))

        return trips

    def get_route(self, trip):
        """ Return the route (containing short and long route names) for a given trip """

        s = 'SELECT route_short_name, route_long_name FROM Trip WHERE stop_id ==' + str(trip.route_id) 
        self.curs.execute(s)
        rows = self.curs.fetchone()

        return Route(rows[0], rows[1])

# return empty stops but make it clear there is nothin there succinctly.

    def nearest_with_trips(self,u_lat,u_lon, n_stops = 1):
        """ Return index of nearest bus stop to specified coordinates """

        s = 'SELECT stop_id, stop_name, stop_lat, stop_lon,  FROM Trip WHERE stop_id ==' + str(time_trip_id) 
        self.curs.execute(s)
        rows = self.curs.fetchall()

        stops = []
        for row in rows:
            stops.append(Stop(row[0], row[1], row[2], row[3], get_dist(u_lat, u_lon, row[2], row[3]), 0)

        return heapq.nsmallest(n_stops, stops, key=lambda stops: stops.dist)

    def get_dist(lat1, lon1, lat2, lon2):
        return sqrt((float(lat1)-float(lat2))**2 +  (float(lon1)-float(lon2))**2)

    def _seconds_since_midnight(self):
        now = time.time()
        return int(now - self._seconds_at_midnight())
    
    def _seconds_at_midnight(self):
        today = datetime.date.today()
        unix_time= today.strftime("%s") #Second as a decimal number [00,61] (or Unix Timestamp)
        return int(unix_time)

    def output(self, u_lat, u_lon, n_stops = 1, n_times = 3):

        #get latest live feed
        updatedFeed = self.update_info()
       
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
                    trip = self.get_route_id(trip_id_time[0])
                    route = self.get_route(trip)

                    #Update the time entry from live feed
                    latest_time = self.update_time(updatedFeed, time)
    
                    mins_to_dep = int((latest_time.departure_time_seconds - seconds_since_midnight)//60)
                    min_suffix = ' min' if abs(mins_to_dep) == 1 else ' mins'
    
                    lines.append(
                        (route.route_short_name, route.route_long_name, str(mins_to_dep)+min_suffix)
                        )
                
            stoplist.append({
                'stop':  stop.stop_name,
                'lines': lines,
                'dist':  '{0:.1f} km'.format(dist_to_stop),
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

    latlon = u'-27.4990795,153.0146127'

    schedule = Schedule()

    
