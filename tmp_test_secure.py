import os
os.environ['JWT_SECRET_KEY'] = 'testkey'
import json
import sys
sys.path.append(r"c:/Users/ABHINAV KUMAR/Desktop/CalliopeIDE")
from server.utils.secure_execution import secure_execute
result = secure_execute('print("Hello Docker")')
print(json.dumps(result))
