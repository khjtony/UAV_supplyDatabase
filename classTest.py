__author__ = 'khjto'

import mysql.connector as mysql

conn = mysql.connect(host='localhost', user='khjtony', password='112358')
cur = conn.cursor()
cur.execute("USE supply_database")
query = "INSERT INTO supply_database.supply_item (datasheets,product_photos,product_training_modules,catalog_drawings,featured_product,pcn_design_specification,none,category,family,series,connector_type,contact_type,number_of_positions,number_of_positions_loaded,pitch,number_of_rows,row_spacing,mounting_type,termination,fastening_type,features,contact_finish,contact_finish_thickness,color,online_catalog,mating_products,other_names) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
values = ('http://portal.fciconnect.com/Comergent//fci/drawing/20021321.pdf', 'http://media.digikey.com/photos/FCI%20Photos/20021321-00008c4lf.jpg', 'http://www.digikey.com/en/ptm/f/fci/minitek127-connector-system', 'http://media.digikey.com/pdf/Catalog%20Drawings/Connectors/20021321_2.jpg', 'http://dkc1.digikey.com/us/en/ph/mkt/mezzselect.html', 'http://media.digikey.com/pdf/PCNs/FCI/PCN-12_117-R.1_Design_Change.pdf', '1', '/product-search/en/connectors-interconnects', '/product-search/en/connectors-interconnects/rectangular-connectors-headers-receptacles-female-sockets/1442548', '/product-search/en?FV=ffec5a67', 'receptacle', 'female_socket', '8', 'all', '0.050"_(1.27mm)', '2', '0.050"_(1.27mm)', 'surface_mount', 'solder', '-', '-', 'gold', '10µin_(0.25µm)', 'black', '/catalog/en/partgroup/minitek-127-series/11246?mpart=20021321-00008C4LF&vendor=609&WT.z_ref_page_type=PS&WT.z_ref_page_sub_type=PD&WT.z_ref_page_id=PD&WT.z_ref_page_event=DC_Link_Table', '/product-detail/en/20021121-00008C4LF/609-3694-2-ND/2209054', 'none')
cur.execute(query, values)


cur.close()
conn.close()
