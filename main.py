import xml.etree.ElementTree as gfg
from datetime import datetime

now = datetime.now(tz=None)

# Reference for this function can be found here:
# https://norwied.wordpress.com/2013/08/27/307/
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

root = gfg.Element("patterndb")
main_list = ["created","version","group"]
for item in main_list:
    tree_value = gfg.Element(item)
    if item == "version":
        tree_value.text = "1"
    elif item == "created":
        tree_value.text = now.strftime("%Y-%b-%d %H:%M:%S")
    root.append(tree_value)
#version = gfg.Element("version")
#version.text = "1"
#root.append(gfg.Element("version"))

indent(root)
tree = gfg.ElementTree(root)

tree.write("patterndb.xml", xml_declaration=True, encoding='utf-8', method="xml")