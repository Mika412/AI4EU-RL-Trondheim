import string

additional_template = string.Template("""<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">
${document_list}
</additional>
""")

poly_template = string.Template('''<poly id="${id}" color="${color}" fill="1" layer="${layer}" shape="${shape}"/>''')

color = "255,0,0,100"
id_prefix = "poly_"
layer = "128.00"


def generatePoly(save_location, width, height, poly_width, poly_height):
    polys = []
    counter = 0
    xCount = int(width / poly_width)
    yCount = int(height / poly_height)
    for x in range(xCount):
        for y in range(yCount):
            btmLeftX = x * poly_width
            btmLeftY = y * poly_height

            btmRightX = (x + 1) * poly_width
            btmRightY = y * poly_height

            topRightX = (x + 1) * poly_width
            topRightY = (y + 1) * poly_height

            topLeftX = x * poly_width
            topLeftY = (y + 1) * poly_height

            shape = str(btmLeftX) + "," + str(btmLeftY) + " " + str(btmRightX) + "," + str(btmRightY) + " " + str(
                topRightX) + "," + str(topRightY) + " " + str(topLeftX) + "," + str(topLeftY)
            polyNode = poly_template.substitute(id=id_prefix + str(counter), color=color, layer=layer, shape=shape)
            polys.append(polyNode)
            counter += 1

    result = additional_template.substitute(document_list='\n'.join(polys))

    file1 = open(save_location, "w")
    file1.write(result)
    file1.close()