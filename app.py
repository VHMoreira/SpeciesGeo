import os
import googlemaps
from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
from SpeciesGeo.Map import Ocurrence, CoordinatesConversor
from SpeciesGeo.SpreadSheet import SpreadSheet

UPLOAD_FOLDER = 'static/uploads'
typeDocument = {'xls'}

runner = Flask(__name__)
runner.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


dataXls = {}
dataGeoCoords = {}

def order(ocurrence_list):
    for i in range(len(ocurrence_list)):
        for j in range(len(ocurrence_list)-1):
            if ocurrence_list[i].get_lat() < ocurrence_list[j].get_lat():
                aux = ocurrence_list[i]
                ocurrence_list[i] = ocurrence_list[j]
                ocurrence_list[j] = aux

    return ocurrence_list


def share(ordered_ocurrence):
    previous_lat = 0
    previous_lng = 0
    child_list = []
    parent_list = []
    for oc in ordered_ocurrence:
        if (oc.get_lat() == previous_lat) and (oc.get_lng() == previous_lng):
            child_list.append([oc.get_number(),oc.get_lat(),oc.get_lng(), oc.get_scienticName()])
        else:
            parent_list.append(child_list)
            child_list = []
            child_list.append([oc.get_number(),oc.get_lat(),oc.get_lng(), oc.get_scienticName()])
        previous_lat = oc.get_lat()
        previous_lng = oc.get_lng()
    parent_list.append(child_list)
    parent_list.pop(0)

    return parent_list

@runner.route('/',methods=['POST','GET'])
def selSheet():
    if os.path.isdir(UPLOAD_FOLDER) == False:
        os.mkdir(UPLOAD_FOLDER)
    return render_template('selSheet.html' , erro = 'false')

@runner.route('/lerTabela', methods=['POST','GET' ])
def selTabela():
    if request.method == ('POST' or 'GET'):
        xlsFile = ''
        filename = ''
        try:
            xlsFile = request.files['xlsFile']
            filename = secure_filename(xlsFile.filename)
        except:
            filename = dataXls['filename']
        sh = filename[len(filename) - 3:]
        if sh in typeDocument:
            if 'filename' not in dataXls:
                if (filename not in UPLOAD_FOLDER) and (filename.endswith('xls')):
                    xlsFile.save(os.path.join(runner.config['UPLOAD_FOLDER'], filename))
                    dataXls['filename'] = filename
                    dataXls['path'] = UPLOAD_FOLDER + '/' + filename
            else:
                dataXls['filename'] = filename
                dataXls['path'] = UPLOAD_FOLDER + '/' + filename
        else:
            return render_template('selSheet.html', erro = 'true')
        return render_template('selArea.html', xlsFile=dataXls['filename'], erro = 'false')


@runner.route('/selArea',methods=['POST','GET'])
def selArea():
    if request.method == ('POST' or 'GET'):
        try:
            north = request.form.getlist('norte')
            south = request.form.getlist('sul')
            east = request.form.getlist('leste')
            west = request.form.getlist('oeste')
            print(north, south, east, west)
        except:
            north = dataGeoCoords['north']
            south = dataGeoCoords['south']
            east = dataGeoCoords['east']
            west = dataGeoCoords['west']

        if (north == '') or (south == '') or (east == '') or (west == ''):
            return render_template('selArea.html', xlsFile = dataXls['filename'], erro = 'true')
        else:
            if (('north' or 'south' or 'east' or 'west' or 'zoom') not in dataGeoCoords) or (([dataGeoCoords['north'], dataGeoCoords['south'], dataGeoCoords['east'], dataGeoCoords['west']],
                    [north, south, east, west]) == False):
                dataGeoCoords['north'] = float(north[0])
                dataGeoCoords['south'] = float(south[0])
                dataGeoCoords['east'] = float(east[0])
                dataGeoCoords['west'] = float(west[0])

            if 'tab' not in dataXls:
                dataXls['tab'] = SpreadSheet()
            else:
                dataXls['tab'].reset()


            dataXls['header'] = dataXls['tab'].createHeader(dataXls['path'])

            dataXls['indexHeader'] = []
            for i in range(len(dataXls['header'])):
                dataXls['indexHeader'].append(i)

            return render_template('selLatLng.html', xlsFile=dataXls['filename'], header=dataXls['header'],
                                   values=dataXls['indexHeader'], max=len(dataXls['indexHeader']), n=dataGeoCoords['north'],
                                   s=dataGeoCoords['south'], e=dataGeoCoords['east'], w=dataGeoCoords['west'], erro = 'false')


@runner.route('/plotar', methods=['POST','GET' ])
def plotar():
    dataXls['tab'].reset_Values()
    if request.method == 'POST':
        conv = CoordinatesConversor()
        try:
            latitudeColumnIndex = int(request.form['latitude'])
            longitudeColumnIndex = int(request.form['longitude'])
            genusColumnIndex = int(request.form['genus'])
            speciesColumnIndex = int(request.form['species'])
        except:
            return render_template('selLatLng.html', xlsFile=dataXls['filename'], header=dataXls['header'],
                                   values=dataXls['indexHeader'], max=len(dataXls['indexHeader']),
                                   n=dataGeoCoords['north'],
                                   s=dataGeoCoords['south'], e=dataGeoCoords['east'], w=dataGeoCoords['west'], erro = 'true')

        dataXls['genusColumn'] = int(genusColumnIndex)
        dataXls['speciesColumn'] = int(speciesColumnIndex)
        dataXls['latitudeColumn'] = int(latitudeColumnIndex)
        dataXls['longitudeColumn'] = int(longitudeColumnIndex)

        gmaps = googlemaps.Client(key="YOU_API_KEY")

        #dataXls['tab'].lerTabela(latitudeColumnIndex, longitudeColumnIndex)
        columns = dataXls['tab'].read(latitudeColumnIndex, longitudeColumnIndex, genusColumnIndex, speciesColumnIndex)

        if dataXls['tab'].get_latitudeValues(0) == True or dataXls['tab'].get_longitudeValues(0) == True:
            return render_template('selLatLng.html',
                                   xlsFile=dataXls['filename'],
                                   header=dataXls['header'],
                                   values=dataXls['indexHeader'],
                                   max=len(dataXls['indexHeader']),
                                   n=dataGeoCoords['north'],
                                   s=dataGeoCoords['south'],
                                   e=dataGeoCoords['east'],
                                   w=dataGeoCoords['west'],
                                   erro = 'true')
        else:
            longitudeColumn = conv.degreesToFloatLongitude(columns[2])
            latitudeColumn = conv.degreesToFloatLatitude(columns[1])
            tombosColumn = columns[0]
            scientficNamesColumn = columns[3]

            ocurrence_list = []

            for i in range(len(tombosColumn)):
                oc = Ocurrence(tombosColumn[i], latitudeColumn[i], longitudeColumn[i], scientficNamesColumn[i])
                ocurrence_list.append(oc)

            oredened_ocurrence = order(ocurrence_list)

            markers = share(oredened_ocurrence)
            for marker in markers:

                address = gmaps.reverse_geocode((marker[0][1], marker[0][2]))
                city = address[0]['address_components'][0]['short_name']
                state = address[0]['address_components'][1]['long_name']
                country = address[0]['address_components'][2]['long_name']
                for ocurrence in marker:
                    ocurrence.append(city)
                    ocurrence.append(state)
                    ocurrence.append(country)


        return render_template('resultPage.html', ocurrenceMarkers=markers, n=dataGeoCoords['north'], s=dataGeoCoords['south'],
                           e=dataGeoCoords['east'], w=dataGeoCoords['west'], xlsFile=dataXls['filename'])

runner.run(debug=True, port=5005)