import os
import sys
import time
CorePath = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0,CorePath+"/Comms/")
print(CorePath)
from receive import ReceiveData 
import threading

rec = ReceiveData()
i = True
while i:
    print("Receiving")
    rec.receive_data()
    print("Received")