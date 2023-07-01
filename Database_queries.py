import pyodbc
import re

# Connect to SQL Server using Windows Authentication


# Create a new database called "mydatabase"
def database_creator( database_name):
    try:
        conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-V1JN67L;'
                      'Database=master;'
                      'Trusted_Connection=yes;',autocommit=True)
        cursor = conn.cursor()
        #cursor.execute('BEGIN TRANSACTION')
        cursor.execute(f"""
                       IF NOT EXISTS (SELECT * FROM SYS.DATABASES WHERE name = '{database_name}')
                        BEGIN
                            CREATE DATABASE {database_name} 
                        END 
                       """)
        #cursor.execute('COMMIT TRANSACTION')
        # Close the connection
        conn.close()
    except Exception as e:
        print(e)

master_table_create_query = """IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'MASTER_DATA')
BEGIN
CREATE TABLE MASTER_DATA 
(ID int, name VARCHAR(50) ,username VARCHAR(50) , email VARCHAR(80),
 ADDRESS_ID INT , phone CHAR(12), WEBSITE VARCHAR(50), COMPANY_ID INT)
END"""
Address_create_query = """IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Address')
BEGIN
CREATE TABLE ADDRESS 
(ID INT, STreet VARCHAR(80) ,SUITE VARCHAR(80) , CITY VARCHAR(80),
 ZIP_CODE VARCHAR , GEO_ID INT)
END"""
GEO_create_query = """IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'GEO')
BEGIN
CREATE TABLE GEO 
(ID INT, LONG VARCHAR(80) ,LAT VARCHAR(80) ,ADDRESS_ID INT)
END"""
drop_MASTER_TABLE_query = """
IF EXISTS 
(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'MASTER_DATA')
BEGIN
DROP TABLE [MASTER_DATA]
END
"""
drop_ADDRESS_query = """IF EXISTS 
(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ADDRESS')
BEGIN
DROP TABLE ADDRESS
END
"""
drop_GEO_query = """IF EXISTS 
(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'GEO')
BEGIN
DROP TABLE GEO
END
"""
# # # # Insert_MASTER_TABLE = """INSERT INTO MASTER_TABLE 
# # # # (
# # # # user_id,first_name,last_name,gender,level
# # # # ) 
# # # # VALUES (%s,%s,%s,%s,%s)
# # # # ON CONFLICT(user_id) DO UPDATE SET level = EXCLUDED.level
# # # # """
Create_tables_queries = [master_table_create_query ,Address_create_query , GEO_create_query]
drop_tables_queries = [drop_MASTER_TABLE_query ,drop_ADDRESS_query , drop_GEO_query]

#5
def table_create_statement_builder(dict_of_tables_with_Columns):
    creat_statements = dict() 
    for i , v in dict_of_tables_with_Columns.items():
        key = i
        creat_statement = f"IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{i}') BEGIN CREATE TABLE {i} ( "
        for i in v.split(","):
            print(f"DEBUGGING MESSAGE : I IS {i}")
            creat_statement += f"{i}" + "  VARCHAR(8000) ,"

        # removing the last comma
        print(f'1.DEBUGGING MESSAGE : the create statment is {creat_statement} , the index of the last commma is {creat_statement.rindex(",")}')
        creat_statement =  creat_statement[:creat_statement.rindex(",")]
        print(f"2.DEBUGGING MESSAGE : the create statment is {creat_statement}")
        creat_statement += ") END"
        if key not in creat_statements.keys():
            creat_statements[key] = creat_statement
    return creat_statements


def create_tables(target_databases,Create_tables_queries):
    for i in Create_tables_queries :
        try:
            print(f"THE PASSED CREATE QUERY IS {i}")
            conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                              'Server=DESKTOP-V1JN67L;'
                              f'Database={target_databases};'
                              'Trusted_Connection=yes;',autocommit=True)
            cursor = conn.cursor()
            #cursor.execute('BEGIN TRANSACTION')
#            cursor.execute(f"""USE {target_databases};
#                           """)
            cursor.execute(i)
            conn.close()
            print(f"TABLE WAS CREATED SUCCESSFULLY : {get_table_name_from_create_query(i)}")
        except Exception as e:
            print(f"COULD NOT CREATE TABLE ")
            print(e)
            conn.rollback()


def DROP_tables(target_databases,Create_tables_queries):
    for i in Create_tables_queries :
        try:
            conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                              'Server=DESKTOP-V1JN67L;'
                              f'Database={target_databases};'
                              'Trusted_Connection=yes;',autocommit=True)
            cursor = conn.cursor()
            #cursor.execute('BEGIN TRANSACTION')
#            cursor.execute(f"""USE {target_databases};
#                           """)
            cursor.execute(i)
            conn.close()
        except Exception as e:
            print(e)
            conn.rollback()




def get_table_name_from_create_query (create_query):
    #FIRST TRIMMING WHITE SPACES FROM THE LEFT OF THE PASSED CREATE QUERY , 
    create_query = create_query.lstrip()
    # capitalize the query as sql is Case insensitive while python is Case sensitive
    create_query = create_query.upper()
    #remove all new line character from the sting as sql has no meaning for new lines while python has a meaning for a new line charcter
    create_query = create_query.replace("\n" , "")
    #removing all spaces as a space in sql has no meaning but has a meaning python ( creata     table is the same as create table )
    create_query = create_query.replace(" ","")
    # splitting at the createtable key word  
    table_name_With_columns = create_query.split("CREATETABLE")[1]
    #print(table_name_With_columns)
    #get the index of the first "("
    index_of_left_brace = table_name_With_columns.index("(")
    table_name =table_name_With_columns[:index_of_left_brace]
    print(table_name)
    return table_name

def turn_successive_multiple_space_to_one(create_query):
    """IN SQL WE MIGHT WRITE THE CREATE QUETY LIKE THIS 
    CREATA TABLEE        (COL1 INT , COL2 CHAR)
    OR LIKE THIS 
    CREATA TABLEE (COL1 INT , COL2 CHAR)
    SO TO SEARCH FOR COLUMN NAME IN A CREATE QUERY WHILE YOU DON'T KNOW HOW MANY 
    SPACE ARE EXISTED YOU MIGHT NEED TO TURN MULTIPLE SUCCESSIVE SPACE INTO ONE SPACE
    """
    #FIRST TRIMMING WHITE SPACES FROM THE LEFT OF THE PASSED CREATE QUERY , 
    create_query = create_query.lstrip()
    # capitalize the query as sql is Case insensitive while python is Case sensitive
    create_query = create_query.upper()
    #remove all new line character from the sting as sql has no meaning for new lines while python has a meaning for a new line charcter
    create_query = create_query.replace("\n" , "")
    # this line of code is to help me when i specifically has to take the name of the column out of a create query
    # i added this line of code as 
    # the passed query to the function get_column_from_create_query may be like this 
    # create tablee (id int ,name varchar)
    # or like this 
    # create tablee ( id int , name varchar)
    # and to get the column name i already split the parentheses () at "," and take the name from index one to the index of the first while space 
    # at the first case the name of colums will be ["id","ame"]
    # and at the second case the name would be [" id","name"] 
    create_query = create_query.replace(",",", ")
    # and the same issue for if the user typed the query like this create table (id int ) or like this ( id int)
    create_query = create_query.replace("(","( ")

    # IF THERE IS MORE THAN ONE SUCCESSIVE SPACE TURN THEN TO BE ONE SPACE 
    create_tables_one_space = re.sub(r'\s+', ' ', create_query)

    return create_tables_one_space



def get_max_key_of_unclosed_parenthesis_in_dict(dict):
    # define the minimum number (negative infinity)
    
    max_key = float('-inf')
    for i in dict.keys():
        if len(dict[i]) == 1: 
            try:
              i = int(i)
              if isinstance(i , int):
                  if i > max_key:
                      max_key = i
            except Exception as e:
                print(e)
    return max_key


def get_column_from_create_query(create_query):
    column_names = ""
    create_query = turn_successive_multiple_space_to_one(create_query)
    print(create_query)
    target_query = create_query.split("CREATE TABLE")[1]

    #get the index of the first open parenthesis
    start_target_parenthesis_index = target_query.index("(")
    # this is made as there may be multiple spaces after the create table key word and the multiple spaces after the table name
    target_query = target_query[start_target_parenthesis_index :]
    print(target_query)
    number_of_opened_parentheses = 0
    number_of_closed_parentheses  = 0
    dict_of_parentheses_indeices = dict()
    index = 0
    for i in target_query :
        if i == "(" :
            index_of_current_left_parenthesis = index
            number_of_opened_parentheses += 1
            print(f"(opend : {number_of_opened_parentheses} , closed : {number_of_closed_parentheses}")
            dict_of_parentheses_indeices[number_of_opened_parentheses] = [index_of_current_left_parenthesis]

        elif i == ")" :
            # the closing happens from left to righ 
            # get the max index of a unclosed parenthesis to close it 
            max_index_of_unclosed_parenthesis = get_max_key_of_unclosed_parenthesis_in_dict(dict_of_parentheses_indeices)
            index_of_current_right_parenthesis = index
            number_of_closed_parentheses += 1
            print(f")opend : {number_of_opened_parentheses} , closed : {number_of_closed_parentheses}")
            dict_of_parentheses_indeices[max_index_of_unclosed_parenthesis].append(index_of_current_right_parenthesis) 

        index += 1    
    
    
    #get the max 
    #print(target_query.split(","))
    #column_name = [col_name for col_name in target_query.split(",")[1:(target_query.split(",")).index(" ")]]
    
    print(dict_of_parentheses_indeices)
    #print(column_name)
    for i in target_query.split(","):
        index_of_the_first_space = i.lstrip().index(" ")
        #print(index_of_the_first_space)
        print(i)
        if index_of_the_first_space == 1:
            index_of_the_first_space = i.find(" ") + 1
        
        column_names = column_names + (i.replace("(","").lstrip()[:index_of_the_first_space+1]).rstrip() +","
        #remove the last ","
        
        #index_of_the_last_comma = column_names.rindex(",")
        #print(index_of_the_last_comma)
        
    column_names = "("+column_names[:(len(column_names)-1)]+")"
    return column_names
    
def build_insert_query_from_create_query(create_query):
    table_name = get_table_name_from_create_query(create_query)
    column_name = get_column_from_create_query(create_query)
    Number_of_columns = column_name.count(',') + 1
    variables = "("
    for i in range(Number_of_columns):
        variables += r"?" + ","
    variables = variables[:len(variables)-1]
    variables = variables + ")"
    print(f"DEBUGGING MESSAGE : THE TABLE NAME FROM build_insert_query_from_create_query FUNCTION IS {table_name}")
    print(f"DEBUGGING MESSAGE : THE COLUMNS FROM build_insert_query_from_create_query FUNCTION IS {column_name}")
    print(f"DEBUGGING MESSAGE : VARIABLE FROM build_insert_query_from_create_query FUNCTION IS {column_name}")
    q = f"INSERT INTO {table_name} {column_name} values {variables}"
    print(f"THE INSERT STATEMENT IS {q}")
    return q


   

# def inserter(target_databases,json_object , create_query):
#     conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
#                       'Server=DESKTOP-V1JN67L;'
#                       f'Database={target_databases};'
#                       'Trusted_Connection=yes;',autocommit=True)
#     insert_query = build_insert_query_from_create_query(create_query)
#     values = [value for value in json_object.values() if not isinstance(json_object.values() ,dict )]
#     for key , value in json_object.items():
#         cur =conn.cursor()
#         cur.execute(i)
# cursor.execute("Insert Into Ticket_Info (<columnname>) values (?)", (json.dumps(record),))