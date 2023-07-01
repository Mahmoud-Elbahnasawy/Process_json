"""a = {'id': 10,
    'name': 'Clementina DuBuque',
    'username': 'Moriah.Stanton',
    'email': 'Rey.Padberg@karina.biz', 
    'address': {
        'street': 'Kattie Turnpike',
        'suite': 'Suite 198',
        'city': 'Lebsackbury',
        'zipcode': '31428-2261',
        'geo': {
            'lat': {
                'X_degree':{
                    'Written':'two_hundreds',
                      'Number':200} ,
                'X_rad':22
                   } ,
               
            'lng': '57.2232' }
               },
    'phone': '024-648-3804',
    'website': 'ambrose.net',
    'company': {
        'name': {
            'english':'Hoeger LLC' ,
            'Arabic':'هوجر',
            'French':'Heugare'},
        'catchPhrase': 'Centralized empowering task-force',
        'bs': 'target end-to-end models'
               }
    }



"""






from function_module import *
from Database_queries import *
# get the file 
j = request_json_file('https://jsonplaceholder.typicode.com/users')
#j = request_json_file('https://dummyjson.com/products/1')
# get an object and try to parse its schema
# this counter is used to determine how many items we would want to parsed our schema deplending on
counter = 1
table_withcolumns  = dict()
for i in json_passer(j):
    if counter <= 1 :
        tables_with_columns = process_json_object(i , 'Main_table')
        
        create_statements = table_create_statement_builder(tables_with_columns)
        print("-"*80)
        print('|',create_statements,'|')
        print("-"*80)

        values = json_values_extractor(i,'Main_table' )
        print("-"*80)

        print('\n\n',values)
        print("-"*80)


        counter += 1

# creat_statments_dict = table_create_statement_builder(table_withcolumns)
# table_withcolumns = process_json_object(i ,parent_table_name='hamoza')
# print(creat_statments_dict)







