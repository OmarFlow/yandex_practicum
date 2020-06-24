SELECT actor.name FROM actors as actor 
JOIN movie_actors as movactor
	ON movactor.actor_id = actor.id
JOIN movies as movie
	ON movie.id = movactor.movie_id
WHERE movie.director LIKE '%Lerdam%'


SELECT writer.name FROM movies as movie
INNER JOIN writers as writer
    ON writer.id = movie.writer
WHERE writer.name != 'N/A'
	GROUP BY movie.writer
	ORDER BY COUNT(movie.writer) DESC


SELECT COUNT(movactor.actor_id), actor.name FROM movie_actors as movactor
JOIN actors as actor
    ON actor.id = movactor.actor_id
WHERE actor.name != 'N/A'
	GROUP BY movactor.actor_id
	ORDER BY COUNT(movactor.actor_id) DESC