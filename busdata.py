import re

class Stop():

    def __init__(self, csv_line):
        self.importData(csv_line)

    def importData(self, csv_line):

        self.stop_id   = csv_line[0]
        self.stop_code = csv_line[1]
        self.stop_name = csv_line[2]
        self.stop_desc = csv_line[3]
        self.stop_lat  = csv_line[4]
        self.stop_lon  = csv_line[5]
       # self.zone_id   = csv_line[6]
# stopUrl
       # self.location_type  = csv_line[8]
       # self.parent_station = csv_line[9]
       # self.platform_code  = csv_line[10]



class Time():

    # day number: integer between 0 to 6 beginning from Monday. 
    def __init__(self, csv_line, day_number):
        #if "FUL" in csv_line[0]:
        self.importData(csv_line)

    def importData(self, csv_line):

        self.trip_id        = csv_line[0]
        self.arrival_time   = csv_line[1]
        self.departure_time = csv_line[2]
        self.stop_id        = csv_line[3]
        self.stop_sequence  = csv_line[4]
        #self.pickup_type    = csv_line[5]
        #self.drop_off_type  = csv_line[6]

        self.arrival_time_seconds = self.processTime(csv_line[1])
        self.departure_time_seconds = self.processTime(csv_line[2])

    def processTime(self, timeString):
                
        m = re.search("([0-9]*):([0-9]*):([0-9]*)", timeString)
        hours = float(m.group(1))
        minutes = float(m.group(2))
        seconds = float(m.group(3))

        return int(3600 * hours + 60 * minutes + seconds)

class Trip():

    def __init__(self, csv_line):
        self.importData(csv_line)

    def importData(self, csv_line):

        self.route_id   = csv_line[0]
        self.service_id = csv_line[1]
        self.trip_id = csv_line[2]
        self.trip_headsign = csv_line[3]
        self.direction_id  = csv_line[4]
        self.block_id  = csv_line[5]
        self.shape_id   = csv_line[6]

class Route():

    def __init__(self, csv_line):
        self.importData(csv_line)

    def importData(self, csv_line):

        self.route_id   = csv_line[0]
        self.route_short_name = csv_line[1]
        self.route_long_name = csv_line[2]
        self.route_desc = csv_line[3]
        self.route_type  = csv_line[4]
#       self.route_url  = csv_line[5]
        self.route_color   = csv_line[6]
        self.route_text_color   = csv_line[7]
