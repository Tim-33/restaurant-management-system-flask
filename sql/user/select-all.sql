SELECT 
    u.User AS 'User',
    p.Table_name AS 'Table',
    p.Privilege_type AS 'Privilege'
FROM mysql.user u JOIN information_schema.table_privileges p
ON concat('''',u.User,'''@''',u.host,'''') = p.GRANTEE
WHERE p.Table_schema = 'sustav_za_upravljanje_restoranom'
ORDER BY u.User, u.Host;