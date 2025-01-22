import sqlite3
import re

file = open("windows_events.txt")

conn = sqlite3.connect("windows_events.db")
cursor = conn.cursor()
print("Connected to database")
sql = "create table if not exists windows_events (windows_id string, legacy_id string, criticality string, summary string)"
cursor.execute(sql)
print("Pushing records into database")
for item in file:
	item = item.replace("\n","")
	cleanup = re.findall(r"<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>",item)
	try:
		sqlite_command = "insert into windows_events (windows_id, legacy_id, criticality, summary) values ('%s','%s','%s','%s')" % (cleanup[0][0], cleanup[0][1], cleanup[0][2], cleanup[0][3])
		cursor.execute(sqlite_command)
		conn.commit()
	except Exception as e:
		pass

cursor.close()
print("Finished pushing data into database")
file.close()
