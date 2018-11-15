from utils.neo4jUtil import NeoUtil
from models.PropertyModels import Name, Url, Year, Text, Gender
from models.MovieModels import Movie, Actor, Genre, Director
from models.GeneralModels import Language, Place


def expand_genre(neoUtil):
    graph = neoUtil.graph
    genres = Genre.match(graph).where()
    idx = 0
    for genre in genres:
        idx += 1
        print('%s' % str(idx / 45))
        genre_name = genre.name
        if genre_name != None:
            cur = graph.run('match (n:Name) where n.val={gn} return n;', gn=genre_name)
            if cur.forward() == 0:
                genre_name_obj = Name()
                genre_name_obj.val = genre_name
                graph.push(genre_name_obj)
            else:
                genre_name_obj = Name.wrap(cur.current['n'])
            genre.hasName.add(genre_name_obj)
        graph.push(genre)

def expand_actor(neoUtil):
    graph = neoUtil.graph
    actors = Actor.match(graph).where()
    idx = 0
    for actor in actors:
        idx += 1
        print('%s' % str(idx / 26683))
        actor_name = actor.name
        actor_foreign_name = actor.foreignName
        actor_gender = actor.gender
        actor_bornPlace = actor.bornPlace
        actor_dataFrom = actor.dataFrom

        if actor_name != None:
            cur = graph.run('match (n:Name) where n.val={name} return n;', name=actor_name)
            if cur.forward() == 0:
                actor_name_obj = Name()
                actor_name_obj.val = actor_name
                graph.push(actor_name_obj)
            else:
                actor_name_obj = Name.wrap(cur.current['n'])
            actor.hasName.add(actor_name_obj)

        if actor_foreign_name != None and actor_foreign_name != actor_name:
            cur = graph.run('match (n:Name) where n.val={name} return n;', name=actor_foreign_name)
            if cur.forward() == 0:
                actor_foreign_name_obj = Name()
                actor_foreign_name_obj.val = actor_foreign_name
                graph.push(actor_foreign_name_obj)
            else:
                actor_foreign_name_obj = Name.wrap(cur.current['n'])
            actor.hasName.add(actor_foreign_name_obj)
        
        if actor_gender != None:
            cur = graph.run('match (n:Gender) where n.val={name} return n;', name=actor_gender)
            if cur.forward() == 0:
                actor_gender_obj = Gender()
                actor_gender_obj.val = actor_gender
                graph.push(actor_gender_obj)
            else:
                actor_gender_obj = Gender.wrap(cur.current['n'])
            actor.isGender.add(actor_gender_obj)

        
        if actor_bornPlace != None:
            cur = graph.run('match (n:Name) where n.val={name} return n;', name=actor_bornPlace)
            if cur.forward() == 0:
                place_name_obj = Name()
                place_name_obj.val = actor_bornPlace
                graph.push(place_name_obj)
                place_obj = Place()
                place_obj.name.add(place_name_obj)
                graph.push(place_obj)
                actor.bornIn.add(place_obj)
            else:
                place_name_obj = Name.wrap(cur.current['n'])
                cur = graph.run('match (p:Place)-[:NAME]->(n:Name) where n.val="%s" return p' % actor_bornPlace)
                if cur.forward() == 1:
                    place_obj = Place.wrap(cur.current['p'])
                    actor.bornIn.add(place_obj)
                else:
                    place_obj = Place()
                    place_obj.name.add(place_name_obj)
                    graph.push(place_obj)
                    actor.bornIn.add(place_obj)
        
        if actor_dataFrom != None:
            if len(list(actor.dataFromUrl)) == 0:
                url_obj = Url()
                url_obj.val = actor_dataFrom
                graph.push(url_obj)
                actor.dataFromUrl.add(url_obj)

        graph.push(actor)

                
def expand_director(neoUtil):
    graph = neoUtil.graph
    directors = Director.match(graph).where()
    idx = 0
    for director in directors:
        idx += 1
        print('%s' % str(idx / 10299))
        director_name = director.name
        director_foreign_name = director.foreignName
        director_gender = director.gender
        director_bornPlace = director.bornPlace
        director_dataFrom = director.dataFrom

        if director_name != None:
            cur = graph.run('match (n:Name) where n.val={name} return n;', name=director_name)
            if cur.forward() == 0:
                director_name_obj = Name()
                director_name_obj.val = director_name
                graph.push(director_name_obj)
            else:
                director_name_obj = Name.wrap(cur.current['n'])
            director.hasName.add(director_name_obj)

        if director_foreign_name != None and director_foreign_name != director_name:
            cur = graph.run('match (n:Name) where n.val={name} return n;', name=director_foreign_name)
            if cur.forward() == 0:
                director_foreign_name_obj = Name()
                director_foreign_name_obj.val = director_foreign_name
                graph.push(director_foreign_name_obj)
            else:
                director_foreign_name_obj = Name.wrap(cur.current['n'])
            director.hasName.add(director_foreign_name_obj)

        if director_gender != None:
            cur = graph.run('match (n:Gender) where n.val={name} return n;', name=director_gender)
            if cur.forward() == 0:
                director_gender_obj = Gender()
                director_gender_obj.val = director_gender
                graph.push(director_gender_obj)
            else:
                director_gender_obj = Gender.wrap(cur.current['n'])
            director.isGender.add(director_gender_obj)

        if director_bornPlace != None:
            cur = graph.run('match (n:Name) where n.val={name} return n;', name=director_bornPlace)
            if cur.forward() == 0:
                place_name_obj = Name()
                place_name_obj.val = director_bornPlace
                graph.push(place_name_obj)
                place_obj = Place()
                place_obj.name.add(place_name_obj)
                graph.push(place_obj)
                director.bornIn.add(place_obj)
            else:
                place_name_obj = Name.wrap(cur.current['n'])
                cur = graph.run('match (p:Place)-[:NAME]->(n:Name) where n.val="%s" return p' % director_bornPlace)
                if cur.forward() == 1:
                    place_obj = Place.wrap(cur.current['p'])
                    director.bornIn.add(place_obj)
                else:
                    place_obj = Place()
                    place_obj.name.add(place_name_obj)
                    graph.push(place_obj)
                    director.bornIn.add(place_obj)

        if director_dataFrom != None:
            if len(list(director.dataFromUrl)) == 0:
                url_obj = Url()
                url_obj.val = director_dataFrom
                graph.push(url_obj)
                director.dataFromUrl.add(url_obj)

        graph.push(director)
    
def expand_movie(neoUtil):
    graph = neoUtil.graph
    matcher = neoUtil.matcher
    movies = Movie.match(graph).where()
    idx = 0
    for movie in movies:
        idx += 1
        if idx % 100 == 0:
            print('%s' % str(idx / 33131))

        movie_name = movie.name
        movie_language = movie.language
        movie_place = movie.place
        movie_description = movie.description
        movie_dataFrom = movie.dataFrom
        movie_year = movie.year
        movie_originalName = movie.originalName


        if movie_name != None:
            cur = graph.run('match (n:Name) where n.val={name} return n;', name=movie_name)
            if cur.forward() == 0:
                name_obj = Name()
                name_obj.val = movie_name
                graph.push(name_obj)
            else:
                name_obj = Name.wrap(cur.current['n'])
            movie.hasName.add(name_obj)

        if movie_language != None:
            cur = graph.run('match (n:Name) where n.val={name} return n;', name=movie_language)
            if cur.forward() == 0:
                language_name_obj = Name()
                language_name_obj.val = movie_language
                graph.push(language_name_obj)
                language_obj = Language()
                language_obj.name.add(language_name_obj)
                graph.push(language_obj)
                movie.useLanguage.add(language_obj)
            else:
                language_name_obj = Name.wrap(cur.current['n'])
                cur = graph.run('match (l:Language)-[:NAME]->(n:Name) where n.val="%s" return l' % movie_language)
                if cur.forward() == 1:
                    language_obj = Language.wrap(cur.current['l'])
                    movie.useLanguage.add(language_obj)
                else:
                    language_obj = Language()
                    language_obj.name.add(language_name_obj)
                    graph.push(language_obj)
                    movie.useLanguage.add(language_obj)

        if movie_place != None:
            cur = graph.run('match (n:Name) where n.val={name} return n;', name=movie_place)
            if cur.forward() == 0:
                place_name_obj = Name()
                place_name_obj.val = movie_place
                graph.push(place_name_obj)
                place_obj = Place()
                place_obj.name.add(place_name_obj)
                graph.push(place_obj)
                movie.inPlace.add(place_obj)
            else:
                place_name_obj = Name.wrap(cur.current['n'])
                cur = graph.run('match (p:Place)-[:NAME]->(n:Name) where n.val="%s" return p' % movie_place)
                if cur.forward() == 1:
                    place_obj = Place.wrap(cur.current['p'])
                    movie.inPlace.add(place_obj)
                else:
                    place_obj = Place()
                    place_obj.name.add(place_name_obj)
                    graph.push(place_obj)
                    movie.inPlace.add(place_obj)

        if movie_description != None:
            if len(list(movie.hasDesctiption)) == 0:
                desctiption_name_obj = Text()
                desctiption_name_obj.val = movie_description
                graph.push(desctiption_name_obj)
                movie.hasDesctiption.add(desctiption_name_obj)

        if movie_dataFrom != None:
            if len(list(movie.dataFromUrl)) == 0:
                url_obj = Url()
                url_obj.val = movie_dataFrom
                graph.push(url_obj)
                movie.dataFromUrl.add(url_obj)

        if movie_year != None:
            year_obj = Year.match(graph).where('_.val=%s' % movie_year).first()
            if year_obj == None:
                year_obj = Year()
                year_obj.val = movie_year
                graph.push(year_obj)
            movie.inYear.add(year_obj)

        if movie_originalName != None and movie_originalName != movie_name:
            cur = graph.run('match (n:Name) where n.val={name} return n;', name=movie_originalName)
            if cur.forward() == 0:
                original_name_obj = Name()
                original_name_obj.val = movie_originalName
                graph.push(original_name_obj)
            else:
                original_name_obj = Name.wrap(cur.current['n'])
            movie.hasName.add(original_name_obj)

        graph.push(movie)




if __name__ == '__main__':
    neoUtil = NeoUtil()
    # expand_movie(neoUtil)
    # expand_genre(neoUtil)
    # expand_actor(neoUtil)
    # expand_director(neoUtil)
