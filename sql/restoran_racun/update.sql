UPDATE restoran_racun
SET restoran_id = %s,
    valuta = %s
WHERE id = %s AND disabled = false;