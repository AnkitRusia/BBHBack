from pymongo import MongoClient
import sys
from datetime import datetime
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

This is admin pannel. Please use it carefully. In case of emergency please contact to +91 9827168348. 

''')

choices_p = '''
Select the desired option: 

1. Change password.
2. Time left for website to expire.
3. Exit

'''


s = input("password: ")
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
        sys.exit()
    ip = int(input("Choice: "))
    

