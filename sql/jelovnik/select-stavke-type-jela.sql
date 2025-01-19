SELECT st.naziv AS naziv_stavke, st.cijena AS cijena, j.naziv AS naziv_jelovnika
FROM stavka st
JOIN jelovnik_stavka js ON st.id = js.stavka_id
JOIN jelovnik j ON js.jelovnik_id = j.id
WHERE j.jelovnik_tip = 'jela'
ORDER BY st.cijena DESC;
