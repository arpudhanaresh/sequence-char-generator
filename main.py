import string
import itertools
import time
import mysql.connector
import hashlib





cnx = mysql.connector.connect(
  host="arpudhacheck.online",
  database='apqurufmu_password_hash',
  user="apqurufmu_arpudha",
  password="arpudha@123")
cursor = cnx.cursor()

getquery = "SELECT plain_text FROM md5 order by id desc LIMIT 1"
cursor.execute(getquery)

# Fetch the result
result = cursor.fetchone()
last_inserted_value = result[0]

# Print the result
print("Last inserted value: ", last_inserted_value)



def generate_sequence(start):
    length = len(start)
    chars = string.digits + string.ascii_letters + string.punctuation.replace('"', '').replace('/', '').replace('\\', '').replace("'", '')
    start_index = sum(len(chars) ** i * chars.index(c) for i, c in enumerate(reversed(start)))
    for i in itertools.count(start_index):
        seq = ''
        for _ in range(length):
            seq = chars[i % len(chars)] + seq
            i //= len(chars)
        if seq >= start:
            yield seq
        #time.sleep(1) # Pause for 1 second before generating next sequence

start = last_inserted_value
for seq in generate_sequence(start):
    print(seq)
    md5_hash = hashlib.md5(seq.encode()).hexdigest()
    print(md5_hash)
    query = ("INSERT INTO md5 (plain_text, md5) VALUES ('{}','{}')".format(seq, md5_hash))
    print(query)
    cursor.execute(query)

# Commit the changes
    cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
