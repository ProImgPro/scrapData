import pymongo


myClient = pymongo.MongoClient('mongodb://localhost:27017/')
education = myClient['vnexpress']
news = education['news']
href = education['href']
userRegister = education['user_register']
Token = education['token']

