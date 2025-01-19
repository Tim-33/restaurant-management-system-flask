SELECT j.naziv AS naziv_jelovnika, COUNT(js.stavka_id) AS broj_stavki
FROM jelovnik j
LEFT JOIN jelovnik_stavka js ON j.id = js.jelovnik_id
GROUP BY j.id
ORDER BY broj_stavki DESC;