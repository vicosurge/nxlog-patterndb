import sqlite3
import requests
from datetime import datetime

print("Attempting connection to sqlite database")
conn = sqlite3.connect('windows_events.db')
cursor = conn.cursor()

print("Loading table data")
results = cursor.execute("select windows_id from windows_events order by windows_id")

print("Building patterndb.xml file")
file = open("test.xml", "w")

pattern_id = 1
timestamp = datetime.now()
current_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
file.write("<patterndb>\n")
file.write("\t<created>%s</created>\n" % current_time)
file.write("\t<version>1</version>\n")
file.write("\t<group>\n")
file.write("\t\t<name>Windows Security Events</name>\n")
file.write("\t\t<id>1</id>\n")
# Start loop to create everything
print("Starting event loop")
for event in results:
    if str(event[0]) not in ["N/A", "-"]:
        file.write("\t\t<pattern>\n")
        file.write("\t\t\t<id>%s</id>\n" % pattern_id)
        file.write("\t\t\t<name>Windows Event - %s</name>\n" % event[0])
        website = "https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-%s" % event[0]
        find_web = requests.get(website)
        if find_web.status_code == 200:
            file.write("\t\t\t<description>%s</description>\n" % website)
        file.write("\t\t\t<matchfield>\n")
        file.write("\t\t\t\t<name>EventID</name>\n")
        file.write("\t\t\t\t<type>REGEXP</type>\n")
        file.write("\t\t\t\t<value>%s</value>\n" % event[0])
        file.write("\t\t\t</matchfield>\n")
        file.write("\t\t\t<exec>\n")
        file.write("\t\t\t\tdelete('Category');\n")
        file.write("\t\t\t\tdelete('Channel');\n")
        file.write("\t\t\t\tdelete('EventType');\n")
        file.write("\t\t\t\tdelete('EventType');\n")
        file.write("\t\t\t\tdelete('ExecutionProcessID');\n")
        file.write("\t\t\t\tdelete('ExecutionThreadID');\n")
        file.write("\t\t\t\tdelete('Keywords');\n")
        file.write("\t\t\t\tdelete('Message');\n")
        file.write("\t\t\t\tdelete('Opcode');\n")
        file.write("\t\t\t\tdelete('OpcodeValue');\n")
        file.write("\t\t\t\tdelete('ProviderGuid');\n")
        file.write("\t\t\t\tdelete('RecordNumber');\n")
        file.write("\t\t\t\tdelete('Severity');\n")
        file.write("\t\t\t\tdelete('SeverityValue');\n")
        file.write("\t\t\t\tdelete('SourceModuleName');\n")
        file.write("\t\t\t\tdelete('SourceModuleType');\n")
        file.write("\t\t\t\tdelete('SourceName');\n")
        file.write("\t\t\t\tdelete('TaskValue');\n")
        file.write("\t\t\t\tdelete('Version');\n")
        file.write("\t\t\t</exec>\n")
        file.write("\t\t</pattern>\n")
        pattern_id += 1
print("Finished event loop")
file.write("\t</group>\n")
file.write("</patterndb>\n")
print("Closing XML file")
file.close()
