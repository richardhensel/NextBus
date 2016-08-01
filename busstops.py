import urllib2
import csv
import os
import heapq
import pickle
from math import sqrt

from google.transit import gtfs_realtime_pb2
import urllib
import datetime
import time

# Import data storage classes
from busdata import Stop, Time, Trip, Route


class Schedule():
    def __init__(self, savedir = None):
        gtfs_dir = 'SEQ_GTFS'
        self.import_static_gtfs(gtfs_dir)


    def import_static_gtfs(self, gtfs_dir):
        """ Import relevant GTFS data """

        # Stop Data
        print('Importing stop data...')
        self.stop = []
        with open(os.path.join(gtfs_dir, 'stops.txt')) as localfile:
            reader = csv.reader(localfile,delimiter=',',quotechar='"')
            reader.next()
            for row in reader:
                self.stop.append(Stop(row))

        # Time Data
        print('Importing time data...')
        self.time = []
        with open(os.path.join(gtfs_dir, 'stop_times.txt')) as localfile:
            reader = csv.reader(localfile,delimiter=',',quotechar='"')
            reader.next()
            for row in reader:
                self.time.append(Time(row, day_number=0))

        # Trip Data
        print('Importing trip data...')
        self.trip = []
        with open(os.path.join(gtfs_dir, 'trips.txt')) as localfile:
            reader = csv.reader(localfile,delimiter=',',quotechar='"')
            reader.next()
            for row in reader:
                self.trip.append(Trip(row))

        # Route Data
        print('Importing route data...')
        self.route = []
        with open(os.path.join(gtfs_dir, 'routes.txt')) as localfile:
            reader = csv.reader(localfile,delimiter=',',quotechar='"')
            reader.next()
            for row in reader:
                self.route.append(Route(row))

    def get_times_by_stop(self, stop, n_times, dt_offset = 120):
        """ Return the next n arrivals at the given stop """

        
        current_time = self._seconds_since_midnight()

        next_times = []
        for time in self.time:
            if time.stop_id == stop.stop_id and time.departure_time_seconds + dt_offset > current_time\
                and 'FUL' in time.trip_id:
                next_times.append(time)


        return heapq.nsmallest(n_times, next_times, key = lambda t: t.departure_time_seconds)

    def get_trip(self, time):
        """ Return the trip (containing route_id and direction_id) for a given stop time """

        for trip in self.trip:
            if trip.trip_id == time.trip_id:
                # trip_id should be the primary key in the trip database
                return trip

    def get_route(self, trip):
        """ Return the route (containing short and long route names) for a given trip """

        for route in self.route:
            if route.route_id == trip.route_id:
                # route_id should be the primary key in the route database
                return route


    def nearest(self,u_lat,u_lon, n_stops = 1):
        """ Return index of nearest bus stop to specified coordinates """

        dist = lambda stop: sqrt((float(u_lat)-float(stop.stop_lat))**2 +  (float(u_lon)-float(stop.stop_lon))**2)
        # return min(self.stop, key=dist)
        return heapq.nsmallest(n_stops, self.stop, key=dist)

    def _seconds_since_midnight(self):
        now = time.time()
        return int(now - self._seconds_at_midnight())
    
    def _seconds_at_midnight(self):
        today = datetime.date.today()
        unix_time= today.strftime("%s") #Second as a decimal number [00,61] (or Unix Timestamp)
        return int(unix_time)

    def sign_test(self,u_lat,u_lon, n_stops=2, n_times=3):
        """ Print a test sign to the command line """

        stops = self.nearest(u_lat, u_lon, n_stops)

        seconds_since_midnight = self._seconds_since_midnight()

        # print the sign
        for stop in stops:
            print('\n')
            times = self.get_times_by_stop(stop, n_times)
            print('Stop: {0}'.format(stop.stop_name))
            print('Current time: {0}'.format(strftime('%H:%M')))

            dist_to_stop = sqrt((float(u_lat)-float(stop.stop_lat))**2 +  (float(u_lon)-float(stop.stop_lon))**2)*111.120
            print('Distance to stop: {0:.1f} km'.format(dist_to_stop))

            line_string_format = '{0} {1} {2}'
            print(line_string_format.format('Route','Destination','Departs'))

            for time in times:
                trip  = self.get_trip(time)
                route = self.get_route(trip)
                mins_to_dep = int((time.departure_time_seconds - seconds_since_midnight)//60)
                min_suffix = ' min' if abs(mins_to_dep) == 1 else ' mins'

                print(line_string_format.format(route.route_short_name, route.route_long_name, str(mins_to_dep)+min_suffix))
                # print(line_string_format.format(route.route_short_name, time.trip_id, time.departure_time))

    def output(self, u_lat, u_lon, n_stops = 1, n_times = 3):

        #get latest live feed
        updatedFeed = self.update_info()
       
        stops = self.nearest(u_lat, u_lon, n_stops)

        seconds_since_midnight = self._seconds_since_midnight()

        stoplist = []
        for stop in stops:
            times = self.get_times_by_stop(stop, n_times)
            print times
            lines = []

            dist_to_stop = sqrt((float(u_lat)-float(stop.stop_lat))**2 +  (float(u_lon)-float(stop.stop_lon))**2)*111.120

            # Check if times is empty
            if not times:
               for i in range(0, n_times):
                   lines.append(
                       ("   ", "         No Service         ", "     ")
                       )
            else:

                for time in times:
                    trip  = self.get_trip(time)
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
                   # print "stop_id", i.stop_id
                   # print "stop_sequence", i.stop_sequence
                   # print "arrival time", i.arrival.time - secondsAtMidnight
                   # print "departure time", i.departure.time - secondsAtMidnight
                    outputArray.append([i.stop_id, i.stop_sequence, i.arrival.time - secondsAtMidnight, i.departure.time - secondsAtMidnight])
        return outputArray


def save(schedule, filename):
    with open(filename, 'w') as f:
        pickle.dump(schedule,f)

def load(filename):
    with open(filename, 'r') as f:
        return pickle.load(f)

def seconds_since_midnight():
    now = time.time()
    return int(now - seconds_at_midnight())

def seconds_at_midnight():
    today = datetime.date.today()
    unix_time= today.strftime("%s") #Second as a decimal number [00,61] (or Unix Timestamp)
    return int(unix_time)


if __name__ == '__main__':
    sched_savefile = 'schedule.save'
    mode = 1    # 0 = load, 1 = new/save, 2 = don't initialise

    latlon = u'-27.4990795,153.0146127'

    if mode == 0:
        print('Loading imported data from {0}...'.format(sched_savefile))
        schedule = load(sched_savefile)
    elif mode == 1:
        schedule = Schedule()
        # print('Saving imported data to {0}. This may take a while...'.format(sched_savefile))
        # save(schedule, sched_savefile)
        print('Searching nearest connections...')
        # schedule.sign_test(-27.504001, 152.990025, 10)
        # schedule.sign_test(-27.4990795,153.0146127,5)
        print(schedule.sign_test(*latlon.split(','),n_stops=20,n_times=5))

    print(seconds_since_midnight(), 3600*9)
    
