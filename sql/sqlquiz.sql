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


SELECT COUNT(ma.actor_id), a.name FROM movie_actors as ma
  JOIN actors as a
    ON a.id = ma.actor_id
    WHERE a.name != 'N/A'
GROUP BY ma.actor_id
ORDER BY COUNT(ma.actor_id) DESC