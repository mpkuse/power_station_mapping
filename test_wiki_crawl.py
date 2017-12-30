""" Downloads a wiki page and lists its tables

        Created  : 30th Dec, 2017
        Author   : Manohar Kuse <mpkuse@connect.ust.hk>
"""

import all_utils as uf
import code
from bs4 import BeautifulSoup

URL = 'https://en.wikipedia.org/wiki/List_of_major_power_stations_in_Guangdong'
URL = 'https://en.wikipedia.org/wiki/List_of_major_power_stations_in_Gansu'

html_response = uf.url_download( URL )

soup = BeautifulSoup( html_response, 'lxml' )
all_tables = soup.findAll( "table", class_='wikitable' )


print '%d tables found' % len(all_tables)

for table_i, table in enumerate(all_tables):
    print '---'
    print 'Processing table#%d' % table_i
    all_th = table.findAll( 'th' )
    n_cols = len(all_th)
    print 'Found %d colums' %( n_cols )

    # Loop on <th>
    # for th_i, th in enumerate(all_th):
        # print '    %2d.' %(th_i)+th.text


    __name_col_id, __geocord_col_id = uf.smart_get( all_th )

    print '__name_col_id    : ', __name_col_id
    print '__geocord_col_id : ', __geocord_col_id

    DATA = {}
    DATA['Name'] = []
    DATA['GeoCord'] = []





    all_tr = table.findAll( 'tr' )
    print 'Found %d rows' %len(all_tr)

    # Loop on <tr>
    ok=0
    no_ok=-1 #1st row will not contain td as they will have th
    for tr in all_tr:
        all_td = tr.findAll( 'td' )
        this_row_n_col = len(all_td)
        if this_row_n_col != n_cols:
            no_ok += 1
            continue
        ok+=1
        # print 'row contains %d cols' %(len(all_td))
        __name = all_td[__name_col_id].text
        __latlong =  uf.geocord_str_to_latlong( all_td[__geocord_col_id].text )
        # code.interact( local=locals() )
        DATA['Name'].append( __name )
        DATA['GeoCord'].append( __latlong )


    print '%d rows ok, %d rows not ok' %(ok, no_ok)


    q = uf.DATA_2_geojson( DATA, '%d.geojson' %(table_i) )


    code.interact( local=locals() )
