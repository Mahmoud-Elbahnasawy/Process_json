import requests
import json
import pandas as pd
from Database_queries import *
# 1
def request_json_file(url):
    """This function request an object from a URL
    INPUT : URL
    OUTPUT : json file
    
    """
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:

        # Parse the JSON data
        json_data = response.json()
        
        print(f"DEBUGGING MESSAGE : The type of the requested object is {type(json_data)}\n")

        # IF IT WAS ASKED TO WRITED THE JSON OBJECT TO DISK
        print(json_data)
        
        # IF THE API RETURNS A LIST OBJECT , GET ITS LENGTH
        if isinstance(json_data , list):
            print(f"DEBUGGING MESSAGE : the number of items in this list is {len(json_data)}")
            
        #pretty = json.dumps(json_data, indent=4)

    else :
        print('WE COULD NOT CALL THE API')
        json_data = None
    return json_data
# 2
def write_to_disk (object, file_path):
    """this function takes an object and writes it to a file (Overwrite) in the same directroy
    INPUT 
        object : (list , or str)
        (file_path) : string
    OUTPUT 
        NONE  
    """
    try :
        if isinstance(object , str):
            with open(file_path, 'wt') as outfile:
                        outfile.write(object)
        elif isinstance(object , list):
            with open(file_path, 'wt') as outfile:
                for i in object:
                    outfile.write(str(i))
    except Exception as e:
        print(e)

# 3 
def json_passer(json_file, passed_items_count = None):
    """THIS FUNCTION(GENERATOR) TAKES A JSON_FILE AND YIELDS OBJECT BY OBJECT
    INPUT
        JSON_FILE : (LIST)

    OUTPUT 
        NONE
    """
    if passed_items_count is None  and isinstance(json_file , list):
        passed_items_count = len(json_file)
    counter = 1
    if isinstance (json_file , list) :
        print(f"DEBUGGING MESSAGE : THE passed_items_count = {passed_items_count}")
        for i in json_file:
            if counter <= passed_items_count:
                yield i
                counter += 1
            else:
                break

    elif isinstance(json_file , dict):
        return json_file

# 4
def process_json_object(Josn_object  , parent_table_name = 'Main_table' , nested_level=0 , tables = dict() , linking_column = ''):
    """get tables with columns names for a passed json object
    INPUT 
        JSON_OBJECT : DICT
        parent_table_name
        TABLES : DICTIONARY CONTAING TABLE NAME AS A KEY AND COMMA SEPERATED COLUMN NAMES 
        NESTED_LEVEL : INT
        linking_column (string) : it is used a column liking difierent tables in a single json object  
    OUTPUT
        TABLES : DICTIONARY CONTAING TABLE NAME AS A KEY AND COMMA SEPERATED COLUMN NAMES  
    """
    print("DEBUGGING MESSAGE : ********************** THE FUNCTION ==> process_json_object <== WAS CALLED.\n")
    # THIS PART IS USED IN DEBUGGING MODE
    print("2.The passed argumet as json data is\n ")
    # pretty = json.dumps(Josn_object, indent=4)
    # print(pretty , '\n')
    print (f'3.The type of the passed argument is {type(Josn_object)}.\n')    
    # IF FOR SOME REASONE THE KEY COUNTER WAS NEEDED FOR ANY DEBUGGING PURPOSE
    
    #defing a variable that limits the number of items to parse schema based on to a single element
    key_counter = 1
    if nested_level == 0:
        linking_column = list(Josn_object.keys())[0]
    # ITERATING OVER THE ITEMS OF THE DICTIONARY
    for key , value in Josn_object.items() :
        if nested_level == 0:
            #print(f"6.key is : {key} **********  value is {value}" )
            # If the key does not exist add it
            if parent_table_name in tables.keys():
                print(f"DEBUGGING MESSAGE : THIS TABLE NAME DID NOT EXIST YET IN THE DICT, THE DICT IS {tables}")
                tables[parent_table_name] = tables[parent_table_name] + ","+ key
            if parent_table_name not in tables.keys():
                tables[parent_table_name] = key
            print(f"DEBUGGING MESSAGE : AFTER ADDING THIS KEY {key} THE DICTIONARY OF COLUMNS IS {tables}")
            # if the value was nested json object , JUMP INTO HERE 
            if isinstance(value, dict):
                nested_level += 1
                print(f'7.The key of the nested json object is {key} , this happens at nested level = {nested_level}')
                # WE WANT TO MAKE THE TABLE NAME HAS THE PARENT KEY IF THE JSON OBJECT WAS NESTED
                process_json_object(value   ,parent_table_name = key,nested_level = nested_level , linking_column=linking_column )
                # THIS AUGMENTING IS NOT GOING TO EXECUTE EXCEPT AT THE END OF A NESTED LEVEL
                nested_level -= 1
        elif nested_level > 0 :
            if parent_table_name not in tables.keys() and key_counter == 1:
                tables[parent_table_name] = linking_column
            print(f"6.key is : {key} **********  value is {value}" )
            # If the key does not exist add it
            if parent_table_name in tables.keys():
                print(f"DEBUGGING MESSAGE : THIS TABLE NAME DID NOT EXIST YET IN THE DICT, THE DICT IS {tables}")
                tables[parent_table_name] = tables[parent_table_name] + ","+ key
            if parent_table_name not in tables.keys():
                tables[parent_table_name] = key
            # tables[parent_table_name] = tables[parent_table_name] + ","+ key
            print(f"DEBUGGING MESSAGE : AFTER ADDING THIS KEY {key} THE DICTIONARY OF COLUMNS IS {tables}")
            if isinstance(value, dict):
            
                nested_level += 1
                print(f'7.The key of the nested json object is {key} , this happens at nested level = {nested_level}')
                # WE WANT TO MAKE THE TABLE NAME HAS THE PARENT KEY IF THE JSON OBJECT WAS NESTED
                process_json_object(value   , parent_table_name = key, nested_level = nested_level , linking_column=linking_column)
        key_counter += 1
        print(f"At the end of this key, key counter is {key_counter} ")
    print(f"We had up to  {nested_level} nested levels")
    # REMOVING THE FIRST COMMA IN THE VALUE
    print ( f"lookups are {tables}")
    return tables
#5
def json_values_extractor(Josn_object , parent_table_name ,   nested_level= 0 , extracted_values = dict() , the_value_of_first_key = '') :
    print("DEBUGGING MESSAGE : ********************** THE FUNCTION WAS CALLED.\n")
    # this value is going to be used if the nested level is more than one , it is used as a foreing key to the lookups
    # this value is not going to be assigined except if the nested level = 1
    if nested_level == 0:
        the_value_of_first_key = list(Josn_object.values())[0]
        print(f"the value of first key is {the_value_of_first_key}\n")
    # THIS PART IS USED IN DEBUGGING MODE
    print("2.The passed argumet as json data is\n ")
    pretty = json.dumps(Josn_object, indent=4)
    print(pretty , '\n')
    print (f'3.The type of the passed argument is {type(Josn_object)}.\n')    
    
    # IF FOR SOME REASONE THE KEY COUNTER WAS NEEDED FOR ANY DEBUGGING PURPOSE
    key_counter = 1

    # ITERATING OVER THE ITEMS OF THE DICTIONARY
    for key , value in Josn_object.items() :
        if nested_level == 0:
            print(f"6.key is : {key} **********  value is {value}" )
            # If the key does not exist add it
            if parent_table_name in extracted_values.keys() and not isinstance(value , dict):
                print(f"DEBUGGING MESSAGE : THIS TABLE NAME DID NOT EXIST YET IN THE DICT, THE DICT IS {extracted_values}")
                extracted_values[parent_table_name] = str(extracted_values[parent_table_name]) + ","+ str(value)

            if parent_table_name not in extracted_values.keys():
                extracted_values[parent_table_name] = str(value)
            print(f"DEBUGGING MESSAGE : AFTER ADDING THIS KEY {key} THE DICTIONARY OF COLUMNS IS {extracted_values}")
            # if the value was nested json object , JUMP INTO HERE 
            if isinstance(value, dict):
                nested_level += 1
                extracted_values[parent_table_name] = str(extracted_values[parent_table_name]) + "," + str(the_value_of_first_key)
                print(f'7.The key of the nested json object is {key} , this happens at nested level = {nested_level}')
                # WE WANT TO MAKE THE TABLE NAME HAS THE PARENT KEY IF THE JSON OBJECT WAS NESTED
                
                json_values_extractor(value   ,parent_table_name = key , nested_level = nested_level , extracted_values = extracted_values ,the_value_of_first_key=the_value_of_first_key )
                # THIS AUGMENTING IS NOT GOING TO EXECUTE EXCEPT AT THE END OF A NESTED LEVEL
                nested_level -= 1

        elif nested_level > 0 :
            # IF IT IS A NETSED OBJECT WE WANT TO LINKE THIS NESTED LEVEL WITH THE ZERO NETSTED LEVEL OBJECT BY THE VALUE OF THE FIRST KEY
            if parent_table_name not in extracted_values.keys() and (key_counter == 1 ):
                extracted_values[parent_table_name] = the_value_of_first_key
            print(f"6.key is : {key} **********  value is {value}" )
            # If the key does not exist add it
            if parent_table_name in extracted_values.keys() and not isinstance(value , dict):
                print(f"DEBUGGING MESSAGE : THIS TABLE NAME DID NOT EXIST YET IN THE DICT, THE DICT IS {extracted_values}")
                extracted_values[parent_table_name] = str(extracted_values[parent_table_name]) + ","+ str(value)

            if parent_table_name not in extracted_values.keys():
                extracted_values[parent_table_name] = str(value)
            # tables[parent_table_name] = tables[parent_table_name] + ","+ key
            print(f"DEBUGGING MESSAGE : AFTER ADDING THIS KEY {key} THE DICTIONARY OF COLUMNS IS {extracted_values}")
            
            if isinstance(value, dict) :
                extracted_values[parent_table_name] = str(extracted_values[parent_table_name]) + "," + str(the_value_of_first_key)
                nested_level += 1

                print(f'7.The key of the nested json object is {key} , this happens at nested level = {nested_level}')
                # WE WANT TO MAKE THE TABLE NAME HAS THE PARENT KEY IF THE JSON OBJECT WAS NESTED
                
                json_values_extractor(value   , parent_table_name = key, nested_level = nested_level , extracted_values=extracted_values , the_value_of_first_key=the_value_of_first_key)

        key_counter += 1
        print(f"At the end of this key, key counter is {key_counter} ")
    print(f"We had up to  {nested_level} nested levels")
    # REMOVING THE FIRST COMMA IN THE VALUE
      
    #print ( f"dict values is  are {extracted_values}")
        


    return extracted_values
    
#6
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


        # DEFINING A NEW DICT TO HOLD THE SAME VALUES AS THE PASSED DICTIONARY BUT HAS ITS KEYS AS UPPER CASE
        upper_values_dict = dict()
        for i in values_dict.keys():
            upper_values_dict[i.upper()] = values_dict[i]
        # defing a list to hold the values     
        values = list((upper_values_dict[table_name].split(",")))
        return values
    except Exception as e:
        print(e)
        print("Failed to get table name from insert statement")

# def json_values_extractor_2(josn_object,target_nested_level,actual_nested_level = 1 , values_list = [] ):
#     print("************ the function is called ya bashareya")
#     #actual_nested_level = 1
#     print(f"the actual nested levels at the top of the function is {actual_nested_level} , target nested level is {target_nested_level}\n")
    
#     print(f"the passed object is{josn_object}\nthe type of the passed object is {type(josn_object)}\n")
#     #nested_value = josn_object.values()[1]
#     if isinstance(josn_object , dict): 
#         # this value is going to be used if the nested level is more than one , it is used as a foreing key to the lookups
#         # this value is not going to be assigined except if the nested level = 1
#         if actual_nested_level == 1:
#             the_value_of_first_key = list(josn_object.values())[0]
#             print(f"the value of first key is {the_value_of_first_key}\n")
#         # aading the id as it will be used as a foreign key

#         #if actual_nested_level == target_nested_level:
#         #print("actual_nested_level = target_nested_level")
#         for key , value in josn_object.items():
#             if not isinstance(value , dict) and (actual_nested_level == target_nested_level):
#                 print(f"key :{key} $$ value {value } ..\n"  )
#                 values_list.append(value)
#             elif not isinstance(value , dict) and (actual_nested_level < target_nested_level):
#                 # please not THAT WE CAN'T RECURSIVELY CALL THE FUNCTION HERE AS THE VALUE IS NOT A DICT
#                 print(f"The nested level is less that the target nested level\n")
#                 actual_nested_level += 1
#                 print(f"before call the function :: value is {value} ,, target_nested_lvel is {target_nested_level} , actual nested lvel is {actual_nested_level}\n")

                
#             elif isinstance(value , dict) and (actual_nested_level == target_nested_level ):
#                 values_list.append(the_value_of_first_key) 
#                 actual_nested_level += 1
#                 json_values_extractor_2(value , target_nested_level=target_nested_level , actual_nested_level=actual_nested_level, values_list = values_list)     
#                 actual_nested_level-=1      
#             elif isinstance(value , dict) and (actual_nested_level < target_nested_level):
#                 print("The nested level is incremented by +1")
#                 actual_nested_level += 1
#                 print(f"before recursion the value of the nested value is '{actual_nested_level}'..")
#                 json_values_extractor_2(value , target_nested_level=target_nested_level , actual_nested_level=actual_nested_level, values_list = values_list)   
#                 actual_nested_level -= 1
#     print( values_list) 



def get_max_nested_level(Josn_object , nested_level=1 , levels = set()) :
    """Returns the maximumn nested level of a json object"""
    # we define a default value for the nested level to be 1 and define an empty set for levels
    # adding the current nested level for the set
    levels.add(nested_level)

    print(f"DEBUGGING MESSAGE : the passed object is {Josn_object} and nested level is {nested_level} and the levels are {levels}\n\n")
    # ITERATING THROUGH THE KEYS OF THE JSON OBJECT
    for key , value in Josn_object.items() :
        # IF THE VALUE OF THE KEY IS OF DICT TYPE THEN ICREASE THE ACTUAL NESTED LEVEL BY ONE
        if isinstance(value, dict):
            nested_level += 1
            print(f'DEBUGGING MESSAGE : The key of the nested json object is {key} , this happens at nested level = {nested_level}')
            # CALLING THE FUNCTION AGIAN TO INSPECT MORE NESTED LEVELS
            get_max_nested_level(value , nested_level)
    return max(levels)


def map_keys_to_their_levels (json_object , nested_level = 1 , key_nested_level_dict = dict() , function_counter = 0 , Loop_counter = 0):
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
                    
                    if key not in key_nested_level_dict.keys():
                        key_nested_level_dict[key] = nested_level
                    # if the key already existed before the add a dot to its name 
                    else :
                        key = key + "."
                        key_nested_level_dict[key] = nested_level
                    ###print(f"key is {key} -- values {value}\n")
                    print(f"11..the final dict is {key_nested_level_dict}")
                # if the value is a nested json object then we have to call the function agian
                elif isinstance(value , dict) :
                    print(f"22..We iterate through {value} , the loop counter is {Loop_counter} , function_counter is {function_counter}\n")
                    # check if the keys exists or not so that not to overwrite an existing key
                    if key not in key_nested_level_dict.keys():
                        key_nested_level_dict[key] = nested_level
                    # if the key already existed before the add a dot to its name 
                    else :
                        key = key + "."
                        key_nested_level_dict[key] = nested_level                    
                    print(f"22..the dict is {key_nested_level_dict}")
                    # increment the nested key by one 
                    nested_level += 1
                    # call the function agian to process the nested json object
                    map_keys_to_their_levels(value , nested_level , function_counter=function_counter , Loop_counter=Loop_counter)
                    # decrement the nested level by one as here we already got out of a nested level
                    nested_level -= 1
                print(f"I am out of the loop , nested level is {nested_level} , the loop counter is {Loop_counter} , function_counter is {function_counter}\n")
                Loop_counter += 1
            print(f"I am __OUTER__ of the loop , nested level is {nested_level} , , the loop counter is {Loop_counter} , function_counter is {function_counter}\n")        
                
                        
    
    except  Exception as e:
        print(e)
    
    return key_nested_level_dict




def main():
    print("1.We are starting the main program.")

    # create database if not exists
    database_creator('development')
    print("2.THE DATABASE WAS CREATED SUCCESSFULLY.")
    # request the file from the api
    #file = request_json_file('https://jsonplaceholder.typicode.com/users')
    file = [{
'id': 1,
'name': 'Leanne Graham',
'username': 'Bret',
'email': 'Sincere@april.biz',
'address':
    {
        'street': 'Kulas Light',
        'suite': 'Apt. 556',
        'city': 'Gwenborough',
        'zipcode': '92998-3874',
        'geo':
        {
            'lat': '-37.3159',
            'lng': '81.1496'
        }
    },
'phone': '1-770-736-8031 x56442',
'website': 'hildegard.org',
'company': 
    {
    'name': 'Romaguera-Crona',
    'catchPhrase': 'Multi-layered client-server neural-net',
    'bs': 'harness real-time e-markets'
    }
    }
 , 
 
 {'id': 2, 'name': 'Ervin Howell', 'username': 'Antonette', 'email': 'Shanna@melissa.tv', 'address': {'street': 'Victor Plains', 'suite': 'Suite 879', 'city': 'Wisokyburgh', 'zipcode': '90566-7771', 'geo': {'lat': '-43.9509', 'lng': '-34.4618'}}, 'phone': '010-692-6593 x09125', 'website': 'anastasia.net', 'company': {'name': 'Deckow-Crist', 'catchPhrase': 'Proactive didactic contingency', 'bs': 'synergize scalable supply-chains'}}, {'id': 3, 'name': 'Clementine Bauch', 'username': 'Samantha', 'email': 'Nathan@yesenia.net', 'address': {'street': 'Douglas Extension', 'suite': 'Suite 847', 'city': 'McKenziehaven', 'zipcode': '59590-4157', 'geo': {'lat': '-68.6102', 'lng': '-47.0653'}}, 'phone': '1-463-123-4447', 'website': 'ramiro.info', 'company': {'name': 'Romaguera-Jacobson', 'catchPhrase': 'Face to face bifurcated interface', 'bs': 'e-enable strategic applications'}}, {'id': 4, 'name': 'Patricia Lebsack', 'username': 'Karianne', 'email': 'Julianne.OConner@kory.org', 'address': {'street': 'Hoeger Mall', 'suite': 'Apt. 692', 'city': 'South Elvis', 'zipcode': '53919-4257', 'geo': {'lat': '29.4572', 'lng': '-164.2990'}}, 'phone': '493-170-9623 x156', 'website': 'kale.biz', 'company': {'name': 'Robel-Corkery', 'catchPhrase': 'Multi-tiered zero tolerance productivity', 'bs': 'transition cutting-edge web services'}}, {'id': 5, 'name': 'Chelsey Dietrich', 'username': 'Kamren', 'email': 'Lucio_Hettinger@annie.ca', 'address': {'street': 'Skiles Walks', 'suite': 'Suite 351', 'city': 'Roscoeview', 'zipcode': '33263', 'geo': {'lat': '-31.8129', 'lng': '62.5342'}}, 'phone': '(254)954-1289', 'website': 'demarco.info', 'company': {'name': 'Keebler LLC', 'catchPhrase': 'User-centric fault-tolerant solution', 'bs': 'revolutionize end-to-end systems'}}, {'id': 6, 'name': 'Mrs. Dennis Schulist', 'username': 'Leopoldo_Corkery', 'email': 'Karley_Dach@jasper.info', 'address': {'street': 'Norberto Crossing', 'suite': 'Apt. 950', 'city': 'South Christy', 'zipcode': '23505-1337', 'geo': {'lat': '-71.4197', 'lng': '71.7478'}}, 'phone': '1-477-935-8478 x6430', 'website': 'ola.org', 'company': {'name': 'Considine-Lockman', 'catchPhrase': 'Synchronised bottom-line interface', 'bs': 'e-enable innovative applications'}}, {'id': 7, 'name': 'Kurtis Weissnat', 'username': 'Elwyn.Skiles', 'email': 'Telly.Hoeger@billy.biz', 'address': {'street': 'Rex Trail', 
'suite': 'Suite 280',
'city': 'Howemouth',
'zipcode': '58804-1099',
'geo': {'lat': '24.8918', 'lng': '21.8984'}},
'phone': '210.067.6132',
'website': 'elvis.io',
'company': {'name': 'Johns Group', 'catchPhrase': 'Configurable multimedia task-force',
'bs': 'generate enterprise e-tailers'}}, {'id': 8, 'name': 'Nicholas Runolfsdottir V', 'username': 'Maxime_Nienow', 'email': 'Sherwood@rosamond.me', 'address': {'street': 'Ellsworth Summit', 'suite': 'Suite 729', 'city': 'Aliyaview', 'zipcode': '45169', 'geo': {'lat': '-14.3990', 'lng': '-120.7677'}}, 'phone': '586.493.6943 x140', 'website': 'jacynthe.com', 'company': {'name': 'Abernathy Group', 'catchPhrase': 'Implemented secondary concept', 'bs': 'e-enable extensible e-tailers'}}, {'id': 9, 'name': 'Glenna Reichert', 'username': 'Delphine', 'email': 'Chaim_McDermott@dana.io', 'address': {'street': 'Dayna Park', 'suite': 'Suite 449', 'city': 'Bartholomebury', 'zipcode': '76495-3109', 'geo': {'lat': '24.6463', 'lng': '-168.8889'}}, 'phone': '(775)976-6794 x41206', 'website': 'conrad.com', 'company': {'name': 'Yost and Sons', 'catchPhrase': 'Switchable contextually-based project', 'bs': 'aggregate real-time technologies'}}, {'id': 10, 'name': 'Clementina DuBuque', 'username': 'Moriah.Stanton', 'email': 'Rey.Padberg@karina.biz', 'address': {'street': 'Kattie Turnpike', 'suite': 'Suite 198', 'city': 'Lebsackbury', 'zipcode': '31428-2261', 'geo': {'lat': '-38.2386', 'lng': '57.2232'}}, 'phone': '024-648-3804', 'website': 'ambrose.net', 'company': {'name': 'Hoeger LLC', 'catchPhrase': 'Centralized empowering task-force', 'bs': 'target end-to-end models'}}]
    print("3.THE JSON OBJECT WAS DOWNLOADED SUCCESSFULLY.")
    
    # THIS COUNTER IS ONLY USED TO PARSE THE SCHEMA BASED ON A SINGLE JSON OBJECT
    # counter = 1
    for i in json_passer(file , passed_items_count = 1 ):
        # getting the schema of the json object
        # if counter <= 1 :
        tables_with_columns = process_json_object( i , 'Main_table')
            
    
        # Generate the create statements based on the dictionary got from process_json_object function 
        create_statements = table_create_statement_builder(tables_with_columns)
        print("^^"*20 , create_statements)
        # GENERATE INSERT STATEMENTS
        insert_statements = []
        for table ,create_statement in create_statements.items():
            print('##'*20,create_statement)
            w = build_insert_query_from_create_query(create_query = create_statement)
            insert_statements.append(w)

            
            #counter += 1
    create_tables('development' , Create_tables_queries = list(create_statements.values()))
    print("4.THE TABLES WERE CREATED SUCCESSFULLY.")

    #START INSERTING THE DATA
    print("5.STARTING INSERTING DATA.")
    list_of_values = []
    counter = 1

    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-V1JN67L;'
                      'Database=development;'
                      'Trusted_Connection=yes;',autocommit=True)
    print("We could connect to database successfully")

    for i in json_passer(file):
        # if counter <= 2:
        extracted_values  = json_values_extractor(i , 'main_table', extracted_values=dict())
        # main_table_values  = (list(extracted_values.values())[0])
        # Address_table_values = (list(extracted_values.values())[1])
        # geo_table_Values = (list(extracted_values.values())[2])
        # company_table_values  = (list(extracted_values.values()))[3]
        cur = conn.cursor()
        # print(main_table_values.split(",") )
        # print(insert_statements[0])
        for insert_statement in insert_statements:
            cur.execute(insert_statement ,values_extractor(insert_statement , extracted_values) )


        
    # here i will try pandas only with the main_table 
    df = pd.read_json('json_data.json')

    
    for index, row in df.iterrows():
        cur.execute(insert_statements[0], row.id , row.name, row.username, row.email , row.id , row.phone , row.website , row.id )

    conn.close()    
    # USING PANDAS 
    #main_table_insert_query = build_insert_query_from_create_query(table_create_statement_builder(process_json_object(i)))
    #print("\/"*20 , main_table_insert_query)
    


    print('\n\n')