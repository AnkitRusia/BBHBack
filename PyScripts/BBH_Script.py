from pymongo import MongoClient
import sys
from datetime import datetime
import pyqrcode
import png
from pyqrcode import QRCode
import os
# from dateutil.relativedelta import relativedelta

client = MongoClient("mongodb+srv://bhilaibiryanihouseweb:BhilaiBiryaniHouse2022@cluster0.48fot.mongodb.net/items?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
db = client.BBH
user_collection = db["userCollection"]
expire_collection = db["expireCollection"]

user_name = "admin"
print('''

**********************************************
|   * * *           * * *        *       *   | 
|   *     *         *     *      *       *   | 
|   *     *         *     *      *       *   | 
|   * * *           * * *        * * * * *   | 
|   *     *         *     *      *       *   | 
|   *     *         *     *      *       *   | 
|   * * *           * * *        *       *   | 
**********************************************

This is admin panel. Please use it carefully. In case of emergency please contact to +91 9827168348. 

''')

choices_p = '''
Select the desired option: 

1. Change password.
2. Validity left.
3. Generate QR
4. Exit

'''


s = input("Shop Name: ")
if not (s == "BBH" or s == 'bbh' or s == 'Bbh'):
    sys.exit()

print(choices_p)
ip = int(input("Choice: "))
while True:
    if ip == 1:
        passwd = input("[+] IMPORTANT [+]\nThis will change the current password\nEnter new password: ")
        ud = {"user": "admin", "passwd": passwd, "_id": 1}
        try:
            user_collection.find_one_and_update({"_id": 1}, {"$set": ud})
            print("Updated")
        except :
            print("Failed")
    elif ip == 2:
        expire_date = expire_collection.find_one({"_id":1})['endDate']
        now = datetime.now()
        print(str(expire_date - now))
    elif ip == 3:
        # String which represents the QR code
        table_number = input("Enter Table number: ")
        s = f"https://www.bhilaibiryanihouse.store/Customer/{table_number}"

        # Generate QR code
        url = pyqrcode.create(s)
        
        # Create and save the png file naming "Table_no_{}.png"
        name = f'Table_no_{table_number}.png'
        url.png(name, scale = 6)
        print(f"Image saved in {os.getcwd()} with name {name}.")
    elif ip == 4:
        sys.exit()
    ip = int(input("Choice: "))
    

