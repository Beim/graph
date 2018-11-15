from py2neo.ogm import GraphObject, Property, Label, RelatedTo
from models.PropertyModels import Name, Text, Year, Url, Gender
from models.GeneralModels import Language, Place

class Movie(GraphObject):
    rid = Property()
    name = Property()
    language = Property()
    place = Property()
    description = Property()
    doubanId = Property()
    dataFrom = Property()
    year = Property()
    originalName = Property()

    hasName = RelatedTo('Name')
    useLanguage = RelatedTo('Language')
    inPlace = RelatedTo('Place')
    hasDesctiption = RelatedTo('Text')
    dataFromUrl = RelatedTo('Url')
    inYear = RelatedTo('Year')

    hasActor = RelatedTo('Actor')
    hasDirector = RelatedTo('Director')
    hasGenre = RelatedTo('Genre')
    hasResource = RelatedTo('Resource')

class Genre(GraphObject):
    rid = Property()
    name = Property()

    hasName = RelatedTo('Name')

class Actor(GraphObject):
    rid = Property()
    name = Property()
    doubanId = Property()
    gender = Property()
    foreignName = Property()
    bornPlace = Property()
    dataFrom = Property()

    hasName = RelatedTo('Name')
    isGender = RelatedTo('Gender')
    bornIn = RelatedTo('Place')
    dataFromUrl = RelatedTo('Url')

class Director(GraphObject):
    rid = Property()
    name = Property()
    doubanId = Property()
    gender = Property()
    foreignName = Property()
    bornPlace = Property()
    dataFrom = Property()

    hasName = RelatedTo('Name')
    isGender = RelatedTo('Gender')
    bornIn = RelatedTo('Place')
    dataFromUrl = RelatedTo('Url')

class Resource(GraphObject):
    rid = Property()
    url = Property()
    platform = Property()
    price = Property()
    dataFrom = Property()
    movieId = Property()
