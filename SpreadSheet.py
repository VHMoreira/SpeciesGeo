''' Essa classe lê a tabela xls que o usuario vai inserir. '''

import xlrd

class SpreadSheet:
    def __init__(self):
        self.__file = ''
        self.__xls = ''
        self.__sheet = ''

        self.__latitudeValues = []
        self.__longitudeValues = []
        self.__idValues = []
        self.__header = []
        self.__scientificNameValues = []

        self.__latColumn = int
        self.__lngColumn = int
        self.__genusColumn = int
        self.__epithetColumn = int

    def createHeader(self, file):

        self.__file = file

        self.__xls = xlrd.open_workbook(self.__file)
        self.__sheet = self.__xls.sheet_by_index(0)

        for column in range(self.__sheet.ncols):
            cellValue = self.__sheet.cell(0,column).value
            self.__header.append(cellValue)

        return self.__header

    def read(self, lat=int, lng=int, genus=int, epithet=int):
        self.__latColumn = lat
        self.__lngColumn = lng
        self.__genusColumn = genus
        self.__epithetColumn = epithet
        listGenus = []
        listEpithet = []

        for row in range(1, self.__sheet.nrows):
            latitude = self.__sheet.cell(row, self.__latColumn).value
            self.__latitudeValues.append(latitude)

        for row in range(1, self.__sheet.nrows):
            longitude = self.__sheet.cell(row, self.__lngColumn).value
            self.__longitudeValues.append(longitude)

        for row in range(1, self.__sheet.nrows):
            id = self.__sheet.cell(row, 0).value
            self.__idValues.append(id)

        for row in range(1, self.__sheet.nrows):
            genus = self.__sheet.cell(row, self.__genusColumn).value
            listGenus.append(genus)

        for row in range(1, self.__sheet.nrows):
            epithet = self.__sheet.cell(row, self.__epithetColumn).value
            listEpithet.append(epithet)

        for item in range(0, len(listGenus)):
            self.__scientificNameValues.append(listGenus[item] + ' ' + listEpithet[item])

        return [self.__idValues, self.__latitudeValues,self.__longitudeValues,self.__scientificNameValues]

    def reset(self):
        self.__file = ''
        self.__xls = ''
        self.__sheet = ''
        self.__latitudeValues = []
        self.__longitudeValues = []
        self.__header = []
        self.__latColumn = int
        self.__lngColumn = int
        self.__idValues = []
        self.__scientificNameValues = []
        self.__genusColumn = int
        self.__epithetColumn = int

    def reset_Values(self):
        self.__idValues = []
        self.__scientificNameValues = []
        self.__latitudeValues = []
        self.__longitudeValues = []
        self.__genusColumn = int
        self.__epithetColumn = int
        self.__latColumn = int
        self.__lngColumn = int


    def get_latitudeValues(self, index):
        return self.__latitudeValues[index]

    def get_longitudeValues(self, index):
        return self.__longitudeValues[index]