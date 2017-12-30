import urllib2
import hashlib
import code
import os

def _debug( msg ):
    print '[DEBUG]', msg

def _printer( msg ):
    print '[INFO ]', msg

def _error( msg ):
    print '[ERROR]', msg


def url_download( url, use_cache=True ):
    if url is None:
        _debug( 'URL is None, Skipping...' )
        return None


    m = hashlib.md5( url.encode() )
    fname = './cache/'+m.hexdigest()

    if os.path.isfile( fname ) and use_cache:
        _debug( 'Cache hit' )
        with open( fname, 'r' ) as handle:
            return handle.read()

    _debug( 'cache miss')
    _debug( 'download :'+ url )

    try:
        _debug( 'Attempt downloading :'+url)
        html_response = urllib2.urlopen( url ).read()


        with open(fname, "w") as handle:
            handle.write( html_response )
            _debug( 'written to : '+ fname )


        return html_response
    except urllib2.HTTPError, e:
        #self._printer( 'ERROR : '+str(e.code)+':'+e.reason )
        _error( 'ERROR : '+str(e) )
        return None
    except urllib2.URLError, e:
        #self._printer( 'ERROR : '+str(e.code)+':'+e.reason )
        _error( 'ERROR : '+str(e) )
        return None



def smart_get( all_th ):
    """ Given the table header, select col corresponding to plant-name and plant-geocord """

    for th_i, th in enumerate(all_th):
        print '    %2d.' %(th_i)+th.text

    __name_col_id = raw_input( 'col# corresponding to `Name of the plant`? ' )
    __geocord_col_id = raw_input( 'col# corresponding to `GeoCord of the plant`? ' )

    return int(__name_col_id), int(__geocord_col_id)


def geocord_str_to_latlong( _str ):
    try:
        _str = _str.encode( 'ascii', errors='ignore' )
        _debug( 'geocord_str_to_latlong.input : '+_str)
        _str = _str.split( '/')
        _str = _str[1].strip().split( ' ' )

        latitude = _str[0]
        longitude = _str[1]

        latitude_f = float(latitude[0:-1])
        latitude_dirn = latitude[-1]
        longitude_f = float(longitude[0:-1])
        longitude_dirn = longitude[-1]


        # North: +
        # South: -
        # East : +
        # West : -
        if latitude_dirn == 'S':
            latitude_f = -latitude_f
        if longitude_dirn == 'W':
            longitude_f = -longitude_f

        _to_return = [ latitude_f, longitude_f]
        _debug( 'geocord_str_to_latlong.output: '+str(_to_return))
        return _to_return

    except:
        _error( 'geocord_str_to_latlong: Fail to decode, return 0,0 ')
        return [0., 0.]


def DATA_2_geojson( DATA, output_fname ):
    """ DATA is a dict(). Each key is an array of values. It is a parsed representation of table """


    # for r in range( len(DATA['Name']) ):
    #     this_name = DATA['Name'][r]
    #     this_geocord = DATA['GeoCord'][r] #2-array
    #
    #     print '%f,%f,%s' %(this_geocord[0], this_geocord[1], this_name)
    #     continue


    # Adopted from : https://github.com/conmolloy/Geojson-Script

    #reads it in again this time to count the rows in the file
    tot_row_count = len(DATA['Name']) + 1
    # with open(userFile,"r") as l:
        # reader = csv.reader(l,delimiter = ",")
        # data = list(reader)
        # tot_row_count = len(data)

    #opening text of the geojson
    test = "{ \n\t\"type\": \"FeatureCollection\",\n\t\"features\": [\n\t"
    cords_list = []



    row_count = 0

    #iterates through all the rows of the file
    # for row in csv_f:
    for r in range( len(DATA['Name']) ):
        this_name = DATA['Name'][r]
        this_geocord = DATA['GeoCord'][r] #2-array


        #increments what row currently on
        row_count = row_count + 1
        #the latitude data is stored on column 4 (5-1 = 4 =column F)
        latitude = this_geocord[0]# row[5]
        longitude = this_geocord[1] #row[6]
        store_name = this_name #row[1]
        address = "N/A" #row[2]
        town = "N/A" #row[3]
        no_of_machine = "N/A" #row[4]
        machine_type = "N/A" #row[0]
        #etc etc serial_number stored on 6 (5-1 = 6 = column H)
        serial_number = "N/A" #row[7]
        macine_no_str = ""

        #if no of machine = 1 do nothing
        if no_of_machine == "1":
            macine_no_str = ""
        #if it is 2 put a 2 on the marker styling
        if no_of_machine == "2":
            macine_no_str = "\"marker-symbol\": \"2\",\n\t\t\t"
        #if it is 3 put a 3 on the marker styling
        if no_of_machine == "3":
            macine_no_str = "\"marker-symbol\": \"3\",\n\t\t\t"
        #if the machine type is a vending machine colour it blue
        if machine_type == "Vending":
            macine_no_str = macine_no_str +"\"marker-color\": \"#5ab4ac\",\n\t\t\t"
        #else colour it orange
        else:
            macine_no_str = macine_no_str + "\"marker-color\": \"#d8b365\",\n\t\t\t"

        #if the row is not the last rown continue as normal
        if (row_count < tot_row_count - 1 ):
            cords_list.append("\t\t{\n\t\t\"type\": \"Feature\",\n\t\t\"geometry\": {\n\t\t\t\"type\": \"Point\",\n\t\t\t\"coordinates\": [\n\t\t\t"+str(longitude)+",\n\t\t\t"+str(latitude)+"\n\t\t\t]\n\t\t},\n\t\t\"properties\": {\n\t\t\t\"store-name\": \""+str(store_name)+"\",\n\t\t\t\"marker-size\": \"small\",\n\t\t\t"+macine_no_str+"\"address\": \""+str(address)+"\",\n\t\t\t\"machineType\": \""+str(machine_type)+"\",\n\t\t\t\"serialNo\": \""+ str(serial_number)+"\",\n\t\t\t\"city\": \""+str(town)+"\"\n\t\t}\n\t\t},\n")
        #if the row is the last row dont put a comma at the end
        else:
            cords_list.append("\t\t{\n\t\t\"type\": \"Feature\",\n\t\t\"geometry\": {\n\t\t\t\"type\": \"Point\",\n\t\t\t\"coordinates\": [\n\t\t\t"+str(longitude)+",\n\t\t\t"+str(latitude)+"\n\t\t\t]\n\t\t},\n\t\t\"properties\": {\n\t\t\t\"store-name\": \""+str(store_name)+"\",\n\t\t\t\"marker-size\": \"small\",\n\t\t\t"+macine_no_str+"\"address\": \""+str(address)+"\",\n\t\t\t\"machineType\": \""+str(machine_type)+"\",\n\t\t\t\"serialNo\": \""+ str(serial_number)+"\",\n\t\t\t\"city\": \""+str(town)+"\"\n\t\t}\n\t\t}\n")


    #output geojson
    #deletes any geojson file first before recreating

    # try:
        # os.remove("geojson.geojson")
    # except OSError:
        # pass
    with open(output_fname, "w") as outputFile:
        outputFile.write(test)
        for line in cords_list:
            outputFile.write(line)
        outputFile.write("\t]\n}")
