#imports and setup

#required imports
import pandas as pd
import requests
import json
import plotly.graph_objects as go
import socket
import ipaddress


#set up dataframe
file_path = input('Enter the filename of your wireshark capture: ')
file_path = str(file_path)
shark = pd.read_csv(file_path)
shark = shark.drop(columns = ['No.', 'Time', 'Protocol', 'Length', 'Info'])


#get users IP
hostname = socket.gethostname()
myIP = socket.gethostbyname(hostname)


#function for validating IP address
def getIP():
    global myIP
    myIP = input('Enter your IP address: ')
    try:
        ip = ipaddress.ip_address(myIP)
        return True
    except ValueError:
        return False

#check if input is a valid IP address; if not quit program
def validateIP():
    global myIP
    while getIP() == False:
        print('Invalid IP address.')
    
validateIP()

#request user for their lat and long
global myLat, myLong
myLat = float(input('Enter your current latitude: '))
while myLat > 90 and myLat < -90:
    myLat = float(input('Invalid latitude. Re-enter your latitude: '))
myLong = float(input('Enter your current longitude: '))
while myLong > 180 and myLong < -180:
    myLong = float(input('Invalid longitude. Re-enter your current longitude: '))
    
    
#dictionary to store all IP to lat/long pairings
global ipDictionary
ipDictionary = {}


#locate source function
def locateSources():
    index = 0
    while index < len(shark):
        ip_address = shark.loc[index].at['Source']
        if ip_address not in ipDictionary:

            #send request for geolocation and turn it into a dictionary
            request_url = 'https://geolocation-db.com/jsonp/' + ip_address
            response = requests.get(request_url)
            result = response.content.decode()
            result = result.split("(")[1].strip(")")
            result = json.loads(result)

            #add to IP dictionary
            if result['city'] == 'Not found' or result['city'] == 'None':
                if ip_address == myIP:
                    ipDictionary.update({ip_address : [myLat, myLong]})
                else:
                    ipDictionary.update({ip_address : ['---']})
            else:
                ipDictionary.update({ip_address : [float(result['latitude']), float(result['longitude'])]})
        index = index + 1


#locate destination function
def locateDest():
    index = 0
    while index < len(shark):
        ip_address = shark.loc[index].at['Destination']
        if ip_address not in ipDictionary:

            #send request for geolocation and turn it into a dictionary
            request_url = 'https://geolocation-db.com/jsonp/' + ip_address
            response = requests.get(request_url)
            result = response.content.decode()
            result = result.split("(")[1].strip(")")
            result = json.loads(result)

            #add to IP dictionary
            if result['city'] == 'Not found' or result['city'] == 'None':
                if ip_address == myIP:
                    ipDictionary.update({ip_address : [myLat, myLong]})
                else:
                    ipDictionary.update({ip_address : ['---']})
            else:
                ipDictionary.update({ip_address : [float(result['latitude']), float(result['longitude'])]})
        index = index + 1


#initiate locate functions
print('Information being process...')
locateSources()
locateDest()


#check if users IP address was found in capture
while myIP not in ipDictionary:
    print('The IP address you entered was not found in the capture.')
    validateIP()
    ipDictionary = {}
    print('Information being processed...')
    locateSources()
    locateDest()


#display map
print('Creating map...')
connections = []
index = 0
while index < len(shark):
    source = shark.loc[index].at['Source']
    dest = shark.loc[index].at['Destination']
    connection = [source, dest]
    if ipDictionary[source][0] != '---' and ipDictionary[dest][0] != '---' and connection not in connections:
        connections.append(connection)
        connectionMap = go.Figure(go.Scattermapbox(
            mode = "markers+lines",
            lat = [ipDictionary[source][0], ipDictionary[dest][0]],
            lon = [ipDictionary[source][1], ipDictionary[dest][1]],
            marker = {'size': 10},
            name = 'S: ' + source + '   D: ' + dest))
        while index < len(shark):
            source = shark.loc[index].at['Source']
            dest = shark.loc[index].at['Destination']
            connection = [source, dest]
            if ipDictionary[source][0] != '---' and ipDictionary[dest][0] != '---' and connection not in connections:
                connections.append(connection)
                connectionMap.add_trace(go.Scattermapbox(
                    mode = "markers+lines",
                    lat = [ipDictionary[source][0], ipDictionary[dest][0]],
                    lon = [ipDictionary[source][1], ipDictionary[dest][1]],
                    marker = {'size': 10},
                    name = 'S: ' + source + '   D: ' + dest))
            index = index + 1
    index = index + 1


#update map layout    
connectionMap.update_layout(
    title = 'Public IP Connections',
    autosize = True,
    mapbox = {
        'center': {'lon':10, 'lat': 10},
        'style': 'stamen-terrain',
        'center': {'lon': -20, 'lat':-20},
        'zoom': 1})


#show map
connectionMap.show()

