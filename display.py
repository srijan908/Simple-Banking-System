import sqlite3

conn = sqlite3.connect('card.s3db')
conn.commit()

get_con = conn.cursor()  # cursor to manage the db
conn.commit()

# displaying all contents of the database
temp_cur = conn.execute('''SELECT * FROM card''')
for row in temp_cur:
    print('ID           =', row[0])
    print('Card num     =', row[1])
    print('Card pin     =', row[2])
    print('Card balance =', row[3])
    print()
