import sqlite3
import os
import csv
import re

def populateTables(gtfs_dir):

    # Stop Data
    print('Importing stop data...')
    with open(os.path.join(gtfs_dir, 'stops.txt')) as localfile:
        reader = csv.reader(localfile,delimiter=',',quotechar='"')
        reader.next()
        for row in reader:
            stopTable(row)

    # Time Data
    print('Importing time data...')
    with open(os.path.join(gtfs_dir, 'stop_times.txt')) as localfile:
        reader = csv.reader(localfile,delimiter=',',quotechar='"')
        reader.next()
        for row in reader:
            timeTable(row)

    # Trip Data
    print('Importing trip data...')
    with open(os.path.join(gtfs_dir, 'trips.txt')) as localfile:
        reader = csv.reader(localfile,delimiter=',',quotechar='"')
        reader.next()
        for row in reader:
            tripTable(row)

    # Route Data
    print('Importing route data...')
    with open(os.path.join(gtfs_dir, 'routes.txt')) as localfile:
        reader = csv.reader(localfile,delimiter=',',quotechar='"')
        reader.next()
        for row in reader:
            routeTable(row)



def createTables():

    # Create Stop table
    s  = 'CREATE TABLE Stop ('
    s += 'stop_id   text,'
    s += 'stop_code text,'
    s += 'stop_name text,'
    # s += 'stop_desc text,'
    s += 'stop_lat  text,'
    s += 'stop_lon  text' 
    s += ')'
    c.execute(s)

    # Create Time table
    s  = 'CREATE TABLE Time ('
    s += 'trip_id        text,' 
    s += 'arrival_time   text,' 
    s += 'departure_time text,'
    s += 'stop_id        text,'
    s += 'stop_sequence  text,'
    #s += 'arrival_time_seconds text,'
    s += 'departure_time_seconds  text'
    s += ')'
    c.execute(s)

    # Create Trip table
    s  = 'CREATE TABLE Trip ('
    s += 'route_id      text,'
    s += 'service_id    text,'
    s += 'trip_id       text,'
    s += 'trip_headsign text,'
    s += 'direction_id  text,'
    s += 'block_id      text,'
    s += 'shape_id      text'
    s += ')'
    c.execute(s)

    # Create Route table
    s  = 'CREATE TABLE Route ('
    s += 'route_id         text,'
    s += 'route_short_name text,'
    s += 'route_long_name  text,'
    s += 'route_desc       text,'
    s += 'route_type       text'
    s += ')'
    c.execute(s)

def stopTable(csv_line):
    '''
    # Create Stop table
    s  = 'CREATE TABLE Stop ('
    s += 'stop_id   text,'
    s += 'stop_code text,'
    s += 'stop_name text,'
    s += 'stop_desc text,'
    s += 'stop_lat  text,'
    s += 'stop_lon  text' 
    s += ')'
    c.execute(s)
    '''
    # Stop data.
    s  = 'INSERT INTO Stop VALUES('
    s += '"' + csv_line[0] + '"' + ','
    s += '"' + csv_line[1] + '"' + ','
    s += '"' + csv_line[2] + '"' + ','
    #s += '"' + csv_line[3] + '"' + ','
    s += '"' + csv_line[4] + '"' + ','
    s += '"' + csv_line[5] + '"' 
    s += ')'
    c.execute(s)

def timeTable(csv_line):
    '''
    # Create Time table
    s  = 'CREATE TABLE Time ('
    s += 'trip_id        text,' 
    s += 'arrival_time   text,' 
    s += 'departure_time text,'
    s += 'stop_id        text,'
    s += 'stop_sequence  text,'
    #s += 'arrival_time_seconds text,'
    s += 'departure_time_seconds  text'
    s += ')'
    c.execute(s)
    '''
    s  = 'INSERT INTO Time VALUES('
    s += '"' + csv_line[0] + '"' + ','
    s += '"' + csv_line[1] + '"' +','
    s += '"' + csv_line[2] + '"' + ','
    s += '"' + csv_line[3] + '"' + ','
    s += '"' + csv_line[4] + '"' +','
    #s += '"' + str(processTime(csv_line[1])) + '"' + ','
    s += '"' + str(processTime(csv_line[2])) + '"'
    s += ')'
    c.execute(s)

def tripTable(csv_line):
    '''
    # Create Trip table
    s  = 'CREATE TABLE Trip ('
    s += 'route_id      text,'
    s += 'service_id    text,'
    s += 'trip_id       text,'
    s += 'trip_headsign text,'
    s += 'direction_id  text,'
    s += 'block_id      text,'
    s += 'shape_id      text'
    s += ')'
    c.execute(s)
    '''
    s  = 'INSERT INTO Trip VALUES('
    s += '"' + csv_line[0] + '"' + ','
    s += '"' + csv_line[1] + '"' + ','
    s += '"' + csv_line[2] + '"' + ','
    s += '"' + csv_line[3] + '"' + ','
    s += '"' + csv_line[4] + '"' + ','
    s += '"' + csv_line[5] + '"' + ','
    s += '"' + csv_line[6] + '"'
    s += ')'
    c.execute(s)

def routeTable(csv_line):
    '''
    # Create Route table
    s  = 'CREATE TABLE Route ('
    s += 'route_id         text,'
    s += 'route_short_name text,'
    s += 'route_long_name  text,'
    s += 'route_desc       text,'
    s += 'route_type       text'
    s += ')'
    c.execute(s)
    '''
    s  = 'INSERT INTO Route VALUES('
    s += '"' + csv_line[0] + '"' + ','
    s += '"' + csv_line[1] + '"' + ','
    s += '"' + csv_line[2] + '"' + ','
    s += '"' + csv_line[3] + '"' + ','
    s += '"' + csv_line[4] + '"'
    s += ')'
    c.execute(s)



def processTime(timeString):
            
    m = re.search("([0-9]*):([0-9]*):([0-9]*)", timeString)
    hours = float(m.group(1))
    minutes = float(m.group(2))
    seconds = float(m.group(3))

    return int(3600 * hours + 60 * minutes + seconds)


# Main.
if __name__ == "__main__":
    print 'Creating database...'
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    print 'Creating tables...'
    createTables()
    populateTables('SEQ_GTFS')

    print 'Closing...'
    conn.commit()
    conn.close()
