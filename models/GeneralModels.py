from py2neo.ogm import GraphObject, Property, Label, RelatedTo
from models.PropertyModels import Name
from py2neo.data import Node

class Place(GraphObject):
    name = RelatedTo('Name')

class Language(GraphObject):
    name = RelatedTo('Name')

