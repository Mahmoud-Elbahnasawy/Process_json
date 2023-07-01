import pandas as pd
import json
import function_module as fm
fm.request_json_file('https://jsonplaceholder.typicode.com/users')

f = pd.read_json('json_data.json')
print(f.head(10))


