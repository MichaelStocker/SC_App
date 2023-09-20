import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString, Node
file = "Shops\RetailProductPrices.xml"
doc = parse(file)
print (doc.nodeName)
print (doc.firstChild.tagName)

nodes = doc.getElementsByTagName('Node')
testDict = {}
i = 0
for node in nodes:
    node_id = node.getAttribute('ID')
    node_name = node.getAttribute('Name')
    node_price = node.getAttribute('BasePrice')
    node_file = node.getAttribute('FileName')
    if node_file.Contains('Data\Libs\Foundry\Records\Entities\SCItem\Ships\')
        i+=1
        print (node_name + ' : ' + node_price + ' ID#: ' + node_id)
        testDict[float(node_price)] = node_name
print ('Count : ' + str(i))


#tree = ET.parse(file)
#root = tree.getroot()
#print ("Tree Data")
#i = 0
#for elem in root:
    #for sub1 in elem:
        #i+=1
        #print (i)