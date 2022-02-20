"""Preencher os parametros de cota de topo e fundo das caixas de esgoto"""
# Load the Python Standard and DesignScript Libraries
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript import Geometry as geom
clr.AddReference("RevitNodes")
import Revit
from Revit import Elements
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

def ciclo(x):
    return range(len(x))

caixas = []
ct = []
cb = []

feet = 3.281
arr = 2

doc = __revit__.ActiveUIDocument.Document

collector = FilteredElementCollector(doc)
filtro = ElementCategoryFilter(BuiltInCategory.OST_PlumbingFixtures)
elements = collector.WherePasses(filtro).WhereElementIsNotElementType().ToElements()

for element in elements:
    element_type = doc.GetElement(element.GetTypeId())
    element_typename = element_type.FamilyName
    if "Caixa" in element_typename:
        caixa = element
        caixa_altura = round(element_type.LookupParameter("Altura Caixa").AsDouble()/feet , arr)
        caixa_lvl = doc.GetElement(caixa.LookupParameter("Level").AsElementId())
        caixa_lvl_ele = round(caixa_lvl.LookupParameter("Elevation").AsDouble()/feet , arr)
        caixa_ele_fromlvl = round(caixa.LookupParameter("Elevation from Level").AsDouble()/feet , arr)
        cota_topo = round(caixa_lvl_ele + caixa_ele_fromlvl , arr)
        cota_bot = round(cota_topo - caixa_altura , arr)
        caixas.append(caixa)
        ct.append(format(cota_topo , ".2f"))
        cb.append(format(cota_bot, ".2f"))

t = Transaction(doc, "Cotar Caixas")
t.Start()

for i in ciclo(caixas):
    cotatopo = caixas[i].LookupParameter("Cota de Topo da Caixa").Set(ct[i])
    cotabot = caixas[i].LookupParameter("Cota de Fundo da Caixa").Set(cb[i])

t.Commit()

