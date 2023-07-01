import function_module as fm
import Database_queries as dbq
import json


if __name__ == '__main__':
    print(__name__)
    #fm.request_json_file('https://jsonplaceholder.typicode.com/users')
    fm.main()
    # dbq.database_creator('testoo')
    # dbq.create_tables('Testoo',dbq.Create_tables_queries)
    # dbq.DROP_tables('Testoo' , dbq.drop_tables_queries)
    #dbq.get_table_name_from_create_query(dbq.master_table_create_query)
    #dbq.get_column_from_create_query(create_query=dbq.Address_create_query)
    #dbq.get_column_from_create_query("Create table  my_t       (id int identity defalut (0) ,__name varchar default ('yes') )")
    #dbq.get_column_from_create_query(dbq.master_table_create_query)
    #dbq.build_insert_query_from_create_query("Create table myt (IDD int ) on ()")
