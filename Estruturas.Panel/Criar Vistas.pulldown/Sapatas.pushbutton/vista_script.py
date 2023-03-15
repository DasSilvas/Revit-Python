# -*- coding: utf-8 -*-
"""WIP vistas"""
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

import os.path
import sys

# get the absolute path to the grandparent directory
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# add the grandparent directory to the system path
sys.path.insert(0, grandparent_dir)

from classes import Sapata, Funk
from classes import RvtApiCategory as cat
from classes import RvtApi as rvt
from classes import RvtClasses as cls

doc = __revit__.ActiveUIDocument.Document

elements = rvt.get_elements_bycategory(doc, cat.FUNDACAO)

#ViewFamTypes = FilteredElementCollector(doc).OfClass(ViewFamilyType).WhereElementIsElementType().ToElements()
ViewFamTypes = rvt.get_element_byclass(doc, cls.VIEW_TYPE, element_type=True)

def get_section(vistas):
    for view in vistas:
        if view.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString() == "Building Section":
            return view

vista = get_section(ViewFamTypes).Id

sapatas = [Sapata(doc, element) for element in elements if element.LookupParameter("Criar_vistas").AsInteger() == 1]

OFFSET = Funk.internal_units(0.15, "m")

t = Transaction(doc, "vistas")
t.Start()

for sapata in sapatas:

        vistas = sapata.criar_vistas(vista, OFFSET)

t.Commit()

