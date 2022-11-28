SELECT title FROM movies, stars, people, ratings
WHERE stars.movie_id = movies.id
AND ratings.movie_id = movies.id
AND stars.person_id = people.id
AND people.name = "Chadwick Boseman"
ORDER BY ratings.rating DESC
LIMIT 5;