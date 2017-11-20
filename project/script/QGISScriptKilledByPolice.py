###############################
# Download shapefile and data
###############################
import urllib 
urllib.urlretrieve('https://iu.box.com/shared/static/dyd79nfosj25kdqo4hk0me1tmhrbn275.zip', 'counties.zip')

###############################
# Unzip counties file
###############################
from qgis.utils import iface
import zipfile
zip_ref = zipfile.ZipFile('counties.zip', 'r')
zip_ref.extractall('counties')
zip_ref.close()

########################################
# Open the shapefile from inside QGIS python plugin
########################################
wb=QgsVectorLayer('counties/tl_2017_us_county.shp','counties','ogr')
QgsMapLayerRegistry.instance().addMapLayer(wb)

########################################
# Delete everything except contiguous 48 states
########################################
features = wb.getFeatures()
deletelist=['02', '15', '60', '66', '69', '72', '78']
ids = [ f.id() for f in features if f.attribute('STATEFP') in deletelist]
with edit( wb ):
    wb.deleteFeatures( ids )


########################################
# Color counties by killed per county population into 5 categories
########################################
myRangeList = []
from PyQt4 import QtGui
myColor = QtGui.QColor('#1ca232')
mySymbol1 = QgsSymbolV2.defaultSymbol(wb.geometryType())
mySymbol1.setColor(myColor)
mySymbol1.setAlpha(1)
myRange1 = QgsRendererRangeV2(0, 0, mySymbol1, '0 Killed')
myRangeList.append(myRange1)

myColor = QtGui.QColor('#91ffa5')
mySymbol2 = QgsSymbolV2.defaultSymbol(wb.geometryType())
mySymbol2.setColor(myColor)
mySymbol2.setAlpha(1)
myRange2 = QgsRendererRangeV2(0.0001, 2, mySymbol2, '0-2 Killed')
myRangeList.append(myRange2)

myColor = QtGui.QColor('#fbd261')
mySymbol3 = QgsSymbolV2.defaultSymbol(wb.geometryType())
mySymbol3.setColor(myColor)
mySymbol3.setAlpha(1)
myRange3 = QgsRendererRangeV2(2.0001, 5, mySymbol3, '2-5 Killed')
myRangeList.append(myRange3)

myColor = QtGui.QColor('#fa6f44')
mySymbol4 = QgsSymbolV2.defaultSymbol(wb.geometryType())
mySymbol4.setColor(myColor)
mySymbol4.setAlpha(1)
myRange4 = QgsRendererRangeV2(5.0001, 10, mySymbol4, '5-10 Killed')
myRangeList.append(myRange4)


myColor = QtGui.QColor('#ff0400')
mySymbol5 = QgsSymbolV2.defaultSymbol(wb.geometryType())
mySymbol5.setColor(myColor)
mySymbol5.setAlpha(1)
myRange5 = QgsRendererRangeV2(10.0001, 61, mySymbol5, '10-60 Killed')
myRangeList.append(myRange5)

myRenderer = QgsGraduatedSymbolRendererV2('', myRangeList)
myRenderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
myRenderer.setClassAttribute('KillPop')
wb.setRendererV2(myRenderer)

########################################
# Zoom to full size
########################################
vLayer = iface.activeLayer()
canvas = iface.mapCanvas()
extent = vLayer.extent()
canvas.setExtent(extent)
