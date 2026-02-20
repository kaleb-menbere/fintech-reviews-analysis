# PostgreSQL Connection Parameters
# These credentials must match the user/password you set up for your PostgreSQL server.
DB_CONFIG = {
    # The host is 'localhost' if PostgreSQL is running on your machine.
    "host": "localhost",
    
    # The database name we created in pgAdmin.
    "database": "bank_reviews",
    
    # !!! MANDATORY: Replace with your actual PostgreSQL username (often 'postgres' by default) !!!
    "user": "postgres",       

    # !!! MANDATORY: Replace with your actual PostgreSQL password !!!
    "password": "2424", 
    
    # Default PostgreSQL port. Do not change unless you customized it. can also be edited
    "port": "5432"
}

