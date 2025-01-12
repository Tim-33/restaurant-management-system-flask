SELECT mjesec, SUM(iznos) AS iznos
FROM zaposlenik_placa
WHERE disabled = false
GROUP BY mjesec
ORDER BY mjesec DESC;