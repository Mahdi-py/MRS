from Flask_MRS import db
from Flask_MRS.models import *
import random
from Flask_MRS.utils import UpdateMRSRating
#user1 = Movie(id='k23421',MRSRating=8.9)
#db.session.add(user1)
#user1 = Movie(id='Inception',MRSRating=8.9)
#db.session.add(user1)
#user1 = Movie(id='Marvel',MRSRating=8.9)
#db.session.add(user1)
#db.session.commit()


#user1 = User(username='Mahdi',email='m@gmail',password='123')
#db.session.add(user1)
#user1 = User(username='Qassem',email='Q@gmail',password='123')
#db.session.add(user1)
#user1 = User(username='Khalid',email='K@gmail',password='123')
#db.session.add(user1)
#db.session.commit()

#m =Movie.query.all()
#print(m)
#m = User.query.all()
#print(m)

#users = User.query.all()
#for user in users:
#    rating = Ratings(user_id=user.id,movie_id='Inception', rating=random.randint(0,10))
#    db.session.add(rating)
#    print(rating)
#db.session.commit()
#print(UpdateMRSRating('Inception'))
#db.create_all()
#UpdateMRSRating('Inception')
#rating = Ratings(user_id=user.id,movie_id='Inception', rating=random.randint(0,10))
#rating = m.ratings[0]
#print(rating.movie_id)
#print(rating.rating)
#print(rating.user_id)
## THe same for users you can access it by the user
#r= Ratings.query.first()
#print(r.user)

#print(Ratings.query.filter_by(movie_id='i', user_id=user.id).first())
#if not Movie.query.filter_by(id='k23421').first():
#    print('fuck yeah')
#db.session.commit()


list = List.query.get(1)
movie = Movie.query.get('Inception')
list.movies.append(movie)
db.session.commit()
for movie in list.movies:
    print(movie.id)












