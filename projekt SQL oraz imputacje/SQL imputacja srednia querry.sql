SELECT * FROM dane2

ALTER TABLE dane2
DROP COLUMN [nasogastric tube], [nasogastric reflux PH], [nasogastric reflux], [rectal examination - feces],
              [abdomen], [abdominocentesis appearance], [abdomcentesis total protein];

---- wyrzucenie kolumn z bardzo wieloma brakami
---- SQL zastąpił braki jako 0, w niektórych zmiennych utrudni/uniemożliwi to imputacje. Dla lepszego wglądu w imputacje proszę o wgląd w wysłany link do notebooka google collab w pythonie

SELECT AVG([rectal temperature]) as 'Średnia'
FROM dane2
WHERE [rectal temperature] > 0

--- imputacja średnią kolumny [rectal temperature]

UPDATE dane2
SET [rectal temperature] = (SELECT AVG([rectal temperature]) as 'Średnia'
FROM dane2
WHERE [rectal temperature] > 0)
WHERE [rectal temperature] = 0

--- imputacja średnią kolumny [pulse]

UPDATE dane2
SET [pulse] = (SELECT AVG([pulse]) as 'Średnia'
FROM dane2
WHERE [pulse] > 0)
WHERE [pulse] = 0

--- imputacja średnią kolumny [respiratory rate]

UPDATE dane2
SET [respiratory rate] = (SELECT AVG([respiratory rate]) as 'Średnia'
FROM dane2
WHERE [respiratory rate] > 0)
WHERE [respiratory rate] = 0


