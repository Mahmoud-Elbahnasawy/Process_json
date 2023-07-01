from function_module import *
a = {'id': 10,
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
#a = {'name':'Mahmoud' , 'languages':{'arabic':8 , 'english':6} , 'age':25}


def map_keys_to_their_levels_ (json_object , nested_level = 1 , key_nested_level_dict = dict() , function_counter = 0 , Loop_counter = 0 , parent_key = ''):
    function_counter += 1
    print("****************The function is called************************")
    try :
        # first check if the passed object is a json object
        if isinstance(json_object, dict):
            
            print(f"the passed object is {json_object} , \nand nested_level {nested_level} ,\n the dict {key_nested_level_dict}\n\n")
            # iterating through the json keys and values 
            for key , value in json_object.items():
                # if the the key has no netsed json objects then write the keys with the nested value to key_nested_level_dict
                if not isinstance(value, dict) :
                    print(f"11..We iterate through {value} , the loop counter is {Loop_counter} , function_counter is {function_counter}\n ")
                    # check if the keys exists or not so that not to overwrite an existing key
                    
                    if "["+key+"]" not in key_nested_level_dict.keys():
                        if parent_key == '':
                            print("1")
                            key_nested_level_dict["["+key+"]"] = nested_level 
                        else :

                            print("2")

                            key = "["+parent_key+"]" + '.'+ "["+key + "]"
                            if key not in key_nested_level_dict.keys():
                            # we can't add +"[]" here 
                                key_nested_level_dict[key] = nested_level

                    # if the key already existed before the add a dot to its name 
                    else :
                        print("3")
                        key = "["+ key +"]"+ "."
                        key_nested_level_dict[key] = nested_level
                    ###print(f"key is {key} -- values {value}\n")
                    print(f"11..the final dict is {key_nested_level_dict}")
                # if the value is a nested json object then we have to call the function agian
                elif isinstance(value , dict) :
                    print(f"22..We iterate through {value} , the loop counter is {Loop_counter} , function_counter is {function_counter}\n")
                    # check if the keys exists or not so that not to overwrite an existing key
                    if "["+key+"]" not in key_nested_level_dict.keys():
                        if parent_key == '':
                            print("4")
                            key_nested_level_dict["["+key+"]"] = nested_level
                        else :
                            print("5")
                            key = "["+parent_key+"]"+"."+ "["+key + "]"
                            key_nested_level_dict[key] = nested_level
                    # if the key already existed before the add a dot to its name 
                    else :
                        print("6")
                        if parent_key == '':
                            key_nested_level_dict["["+key+"]"] = nested_level
                        else :
                            print("7")
                            key = parent_key+"."+ "["+ key + "]"
                            key_nested_level_dict[key] = nested_level
                        # print(f"HELP!!!!!!! : this key is existed {key}")
                        # key = key + "."
                        # key_nested_level_dict[key] = nested_level                    
                    print(f"22..the dict is {key_nested_level_dict}")
                    # increment the nested key by one 
                    nested_level += 1
                    # call the function agian to process the nested json object
                    map_keys_to_their_levels_(value , nested_level , function_counter=function_counter , Loop_counter=Loop_counter,parent_key = key)
                    # decrement the nested level by one as here we already got out of a nested level
                    nested_level -= 1
                print(f"I am out of the loop , nested level is {nested_level} , the loop counter is {Loop_counter} , function_counter is {function_counter}\n")
                Loop_counter += 1
            print(f"I am __OUTER__ of the loop , nested level is {nested_level} , , the loop counter is {Loop_counter} , function_counter is {function_counter}\n")        
                
                        
    
    except  Exception as e:
        print(e)
    
    return key_nested_level_dict






def map_keys_to_their_levels__(json_object, nested_level=1, key_nested_level_dict=dict(), function_counter=0, Loop_counter=0, parent_keys=None):
    function_counter += 1
    print("****************The function is called************************")
    try:
        # first check if the passed object is a json object
        if isinstance(json_object, dict):
            print(f"the passed object is {json_object},\nand nested_level {nested_level},\nthe dict {key_nested_level_dict}\n\n")
            # iterating through the json keys and values
            for key, value in json_object.items():
                # define the full key for this key-value pair
                if parent_keys is None:
                    full_key = key
                else:
                    full_key = '.'.join(parent_keys + [key])

                # if the the key has no nested json objects then write the keys with the nested value to key_nested_level_dict
                if not isinstance(value, dict):
                    print(f"11..We iterate through {value}, the loop counter is {Loop_counter}, function_counter is {function_counter}\n")
                    # check if the keys exists or not so that not to overwrite an existing key
                    if full_key not in key_nested_level_dict.keys():
                        print("1")
                        key_nested_level_dict[full_key] = nested_level
                    # if the key already existed before then add a dot to its name
                    else:
                        print("3")
                        key_nested_level_dict[full_key + "."] = nested_level
                    print(f"11..the final dict is {key_nested_level_dict}")
                # if the value is a nested json object then we have to call the function again
                elif isinstance(value, dict):
                    print(f"22..We iterate through {value}, the loop counter is {Loop_counter}, function_counter is {function_counter}\n")
                    # check if the keys exists or not so that not to overwrite an existing key
                    if full_key not in key_nested_level_dict.keys():
                        print("4")
                        key_nested_level_dict[full_key] = nested_level
                    # if the key already existed before then add a dot to its name
                    else:
                        print("6")
                        key_nested_level_dict[full_key + "."] = nested_level
                    print(f"22..the dict is {key_nested_level_dict}")
                    # increment the nested key by one
                    nested_level += 1
                    # call the function again to process the nested json object
                    map_keys_to_their_levels__(value, nested_level, key_nested_level_dict=key_nested_level_dict, function_counter=function_counter, Loop_counter=Loop_counter, parent_keys=[*parent_keys, key] if parent_keys else [key])
                    # decrement the nested level by one as here we already got out of a nested level
                    nested_level -= 1
                print(f"I am out of the loop, nested level is {nested_level}, the loop counter is {Loop_counter}, function_counter is {function_counter}\n")
                Loop_counter += 1
            print(f"I am __OUTER__ of the loop, nested level is {nested_level}, the loop counter is {Loop_counter}, function_counter is {function_counter}\n")

    except Exception as e:
        print(e)

    return key_nested_level_dict

def keys_namer(keys_dict , main_big_dict):
    """This function takes a dict and returns a dict 
    sample input {'one.two.three':1}
    sample output {'['one']['two']['three'] : 1'}
    """
    l = []
    new_dict = dict()
    for i , v in keys_dict.items():
        #del keys_dict[i]
        print
        l.append(i.replace(".",'"."'))
        
    print(l)
    for i in l :
        print(main_big_dict[i])

        
o = {'id': 1, 'name': 1, 'username': 1, 'email': 1, 'address': 1, 'address.street': 2, 'address.suite': 2, 'address.city': 2, 'address.zipcode': 2, 'address.geo': 2, 'address.geo.lat': 3, 'address.geo.lat.X_degree': 4, 'address.geo.lat.X_degree.Written': 5, 'address.geo.lat.X_degree.Number': 5, 'address.geo.lat.X_rad': 4, 'address.geo.lng': 3, 'phone': 1, 'website': 1, 'company': 1, 'company.name': 2, 'company.name.english': 3, 'company.name.Arabic': 3, 'company.name.French': 3, 'company.catchPhrase': 2, 'company.bs': 2}
#keys_namer(o , a)

w = build_insert_query_from_create_query('CREATE TABLE geo ( id  VARCHAR(8000) ,lat  VARCHAR(8000) ,lng  VARCHAR(8000) )  ')
print(w)

#create_tables("CREATE TABLE company ( id  VARCHAR(8000) ,name  VARCHAR(8000) ,catchPhrase  VARCHAR(8000) ,bs  VARCHAR(8000) )")
def values_extractor (insert_Statement , values_dict):
    """THIS FUNCTION TAKES AN INSERT STATMENT TO EXTRACT THE TABLE NAME FROM , AND 
    TAKES THE VALUES DICTIONARY TO SELECT THE VALUES CORRESPONDING TO A CERTAIN TABLE_NAME
    INPUT :
        INSERT_STATEMENT(STR) : THE INSERT STATEMENT USED TO EXTRACT TABLE NAME FROM
        VALUES_DICT (DICT) : A DICTIONARY CONTAINIG THE VALUES OF EACH TABLE
    OUTPUT :
    NONE """
    try :
        # REMOVING THE EXTRA SPACES
        insert_Statement = insert_Statement.replace(" ","")
        # SQL IS CASE SENSITIVE UNLIKE PYTHON , SO I WANT TO UNIFY EACH STATEMENT TO BE ALWAYS UPPER CASE
        insert_Statement = insert_Statement.upper()
        # REMOVING ALL THE STRING BEFORE INSERT INTO KEYWORD
        insert_Statement = insert_Statement.split("INSERTINTO")[1]
        # SLICING THE INSERT STATEMENT TO THE FIRST LEFT PARENTHESIS 
        table_name = insert_Statement[:insert_Statement.index("(")]


        # DEFINING A NEW DICT TO HOL THE THE SAME VALUES AS THE PASSED DICTIONARY BUT HAS ITS KEYS AS UPPER CASE
        upper_values_dict = dict()
        for i in values_dict.keys():
            upper_values_dict[i.upper()] = values_dict[i]
            
        print(f"7.{upper_values_dict.keys()}")
        values = list((upper_values_dict[table_name].split(",")))
        print(type(values))
        print(values)
    except Exception as e:
        print(e)
        print("Failed to get table name from insert statement")


values_extractor(insert_Statement="INSERT INTO GEO (ID,LAT,LNG) values (?,?,?)",values_dict = {'main_table': '1,Leanne Graham,Bret,Sincere@april.biz,1,1-770-736-8031 x56442,hildegard.org,1', 'address': '1,Kulas Light,Apt. 556,Gwenborough,92998-3874,1', 'geo': '1,-37.3159,81.1496', 'company': '1,Romaguera-Crona'})