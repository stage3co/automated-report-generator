import pymongo
import mysql.connector as sql
import pandas as pd

# Creating a Sql connection object
conn = sql.connect(host='10.240.0.20', user='root', password='root123')
cursor = conn.cursor()
cursor.execute("SHOW DATABASES")
data = cursor.fetchall()
for i in data:
    print(i[0])

# Creating a MongoDB connection client
client = pymongo.MongoClient("10.240.0.8", maxPoolSize=50)


# Creating a dataframe of the orderLines catalogue
db_user_info = client["stage3reportingdb"]
collection_userInfo = db_user_info["orderlineCollection"]
orderLines = pd.DataFrame(list(collection_userInfo.find()))


# Creating a dataframe of the looks catalogue
db_user_info = client["catalog"]
collection_userInfo = db_user_info["Look"]
catalogue = pd.DataFrame(list(collection_userInfo.find()))
