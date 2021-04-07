import xml.etree.ElementTree as ET

try:
    tree = ET.parse("items.xml")
    root = tree.getroot()
    # print(str(root))

    for elem in root:
        subelem = elem.findall("datum")
        print(subelem[0].text)

except FileNotFoundError:
    data = ET.Element("data")
    item = ET.SubElement(data,"items")
    log1 = ET.SubElement(item,"datum")
    log2 = ET.SubElement(item,"datum")
    log1.set("name","name")
    log2.set("name","progress")
    log1.text = "KievCangs"
    log2.text = "0"

    toET = ET.ElementTree()
    toET._setroot(data)
    toET.write("items.xml")
    # pass
except ET.ParseError:
    data = ET.Element("data")
    item = ET.SubElement(data,"items")
    log1 = ET.SubElement(item,"datum")
    log2 = ET.SubElement(item,"datum")
    log1.set("name","name")
    log2.set("name","progress")
    log1.text = "KievCangs"
    log2.text = "0"

    toET = ET.ElementTree()
    toET._setroot(data)
    toET.write("items.xml")


print("end of run")


