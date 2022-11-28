SELECT title, rating FROM movies, stars, people, ratings
WHERE stars.movie_id = movies.id
AND title = "Get on Up"
AND ratings.movie_id = movies.id
AND stars.person_id = people.id
AND people.name = "Chadwick Boseman"
ORDER BY ratings.rating DESC
LIMIT 10;