from Flask_MRS import db
from Flask_MRS.models import *

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

user = User.query.get(1)
m = Movie.query.get('Inception')
rating = m.ratings[0]
print(rating.movie_id)
print(rating.rating)
print(rating.user_id)
# THe same for users you can access it by the user
r= Ratings.query.first()
print(r.user)

db.session.commit()








