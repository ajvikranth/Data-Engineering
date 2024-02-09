-- Query to highlight versatile anime producers with multiple-genre involvement, sorting by average popularity.

SELECT Producers.Producers, COUNT(DISTINCT Genres.gID) AS NumberOfGenres, AVG(descriptions.Popularity) AS AveragePopularity
FROM Producers
JOIN animeProducers ON Producers.pID = animeProducers.pID
JOIN descriptions ON animeProducers.malID = descriptions.malID
JOIN animeGenres ON descriptions.malID = animeGenres.malID
JOIN Genres ON animeGenres.gID = Genres.gID
GROUP BY Producers.Producers
HAVING NumberOfGenres > 1
ORDER BY AveragePopularity DESC;

-- Query to Find Active Studios with Most Anime: 

SELECT Studios.Studios, COUNT(animeStudios.malID) AS AnimeCount
FROM anime.Studios
JOIN anime.animeStudios ON Studios.sID = animeStudios.sID
GROUP BY Studios.Studios
ORDER BY AnimeCount DESC;

-- Retrieve Anime with Specific Genre (e.g., 'Action'):

SELECT d.*, g.Genres
FROM anime.descriptions d
JOIN anime.animeGenres ag ON d.malID = ag.malID
JOIN anime.Genres g ON ag.gID = g.gID
WHERE g.Genres = 'Action';


-- Find Anime Produced by a Specific Studio (e.g., 'Studio Ghibli'): 

SELECT d.*, s.Studios
FROM anime.descriptions d
JOIN anime.animeStudios ast ON d.malID = ast.malID
JOIN anime.Studios s ON ast.sID = s.sID
WHERE s.Studios = 'Studio Ghibli';

-- Query to Retrieve Anime with a Certain Producer:

SELECT d.*, p.Producers
FROM anime.descriptions d
JOIN anime.animeProducers ap ON d.malID = ap.malID
JOIN anime.Producers p ON ap.pID = p.pID
WHERE p.Producers = 'Madhouse';

-- Query to Find Anime Licensed by a Specific Company:

SELECT d.*, l.Licensors
FROM anime.descriptions d
JOIN anime.animeLicensors al ON d.malID = al.malID
JOIN anime.Licensors l ON al.lID = l.lID
WHERE l.Licensors = 'Funimation';

-- Query to Find Average Score for Each Genre:

SELECT g.Genres, AVG(d.Score) AS AverageScore
FROM anime.Genres g
JOIN anime.animeGenres ag ON g.gID = ag.gID
JOIN anime.descriptions d ON ag.malID = d.malID
GROUP BY g.Genres
ORDER BY AverageScore DESC;

-- Query to Find Studios with the Most Released Episodes:

SELECT s.Studios, SUM(d.Episodes) AS TotalEpisodes
FROM anime.Studios s
JOIN anime.animeStudios ast ON s.sID = ast.sID
JOIN anime.descriptions d ON ast.malID = d.malID
GROUP BY s.Studios
ORDER BY TotalEpisodes DESC

