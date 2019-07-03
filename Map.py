class Ocurrence:
    def __init__(self, number, lat, lng, scientificName):
        self.__number = number
        self.__scientificName = scientificName
        self.__lat = lat
        self.__lng = lng
        self.__city = ''
        self.__state = ''
        self.__country = ''

    def get_number(self):
        return self.__number

    def get_lat(self):
        return self.__lat

    def get_lng(self):
        return self.__lng

    def get_city(self):
        return self.__city

    def get_country(self):
        return self.__country

    def get_state(self):
        return self.__state

    def get_scienticName(self):
        return self.__scientificName

    def set_state(self, state):
        self.__state = state

    def set_city(self, city):
        self.__city = city

    def set_country(self, country):
        self.__country = country


class Bounds:
    def __init__(self, north, south, east, west):
        self.__north = north
        self.__south = south
        self.__east = east
        self.__west = west

    def getNorth(self):
        return self.__north

    def getSouth(self):
        return self.__south

    def getEast(self):
        return self.__east

    def getWest(self):
        return self.__west

    def getCenter(self):
        return 0

    def setNorth(self, north):
        self.__north = north

    def setSouth(self, south):
        self.__south = south

    def setEast(self, east):
        self.__east = east

    def setWest(self, west):
        self.__west = west

class CoordinatesConversor:

    def __init__(self):
        self.__longitudeValues = []
        self.__latitudeValues = []

    def degreesToFloatLongitude(self, longitude):
        for i in range(0, len(longitude)):
            lon = str(longitude[i]).split()
            degreeLon = lon[0].split()
            degreeLon = float(degreeLon[0])

            minutesLon, secondsLon = lon[1].split('.')
            minutesLon = float(minutesLon)
            secondsLon = float(secondsLon)

            direcao = lon[2]

            long = degreeLon + ((minutesLon / 60) + (secondsLon / 3600))

            if direcao == 'W' or direcao == 'w':
                long = long * -1



            self.__longitudeValues.append(long)


        return self.__longitudeValues

    def degreesToFloatLatitude(self, latitude):
        for i in range(0, len(latitude)):
            lat = str(latitude[i]).split()
            degreeLat = lat[0].split()
            degreeLat = float(degreeLat[0])

            minutesLat, secondsLat = lat[1].split('.')
            minutesLat = float(minutesLat)
            secondsLat = float(secondsLat)

            direcao = lat[2]

            lati = degreeLat + ((minutesLat / 60) + (secondsLat / 3600))

            if direcao == 'S' or direcao == 's':
                lati = lati * -1

            self.__latitudeValues.append(lati)

        return self.__latitudeValues