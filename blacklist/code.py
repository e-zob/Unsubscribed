import pandas as pd
import sqlite3

df = pd.read_csv('data.csv')

def add_person(df, first_name, last_name):
    df = df.append({'first_name': first_name, 'last_name': last_name}, ignore_index=True)
    
def remove_person(df, first_name, last_name):
    filt = (df['first_name'] ==  first_name) & (df['last_name'] == last_name)   
    df.drop(index = df[filt].index, inplace=True)

def check_person(df, first_name, last_name):
    if df.empty:
        print('person not blacklisted')
    else:
        print('person blacklisted')

email = "z"
conn = sqlite3.connect("data.db")
cur = conn.cursor()
#cur.execute("DROP TABLE names")
# cur.execute("CREATE TABLE names (first_name text,last_name text, email text PRIMARY KEY)")
# cur.execute("DELETE FROM names WHERE email=?", (email,))
# cur.execute("INSERT OR IGNORE INTO names (first_name, last_name, email) VALUES ('elle','zob','ez@ez')")

# conn.commit()
# conn.close()

with conn:
    cur.execute("SELECT * FROM names")
    print(cur.fetchall())

  

  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  

    