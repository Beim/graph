from py2neo.ogm import GraphObject, Property, Label, RelatedTo

class Name(GraphObject):
    val = Property()

class Url(GraphObject):
    val = Property()

class Text(GraphObject):
    val = Property()

class Year(GraphObject):
    val = Property()

class Gender(GraphObject):
    val = Property()