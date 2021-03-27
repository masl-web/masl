login = {
    'user'     : 'jaewook',	
    'password' : 'password',	
    'host'     : 'localhost',	
    'port'     : 3306,			
    'database' : 'mydb'		
    
}

SQLALCHEMY_DATABASE_URI= f"mysql+mysqlconnector://{login['user']}:{login['password']}@{login['host']}:{login['port']}/{login['database']}?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False