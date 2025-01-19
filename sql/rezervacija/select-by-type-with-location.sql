SELECT s.restoran_id, s.lokacija, COUNT(r.id) AS broj_rezervacija
FROM rezervacija r
JOIN stol s ON r.stol_id = s.id
GROUP BY s.restoran_id, s.lokacija
ORDER BY s.restoran_id, s.lokacija;
