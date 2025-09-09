SELECT DISTINCT
    ci.*, 
    e.full_name,
    e.name_role,
    e.rut,
    CASE
        WHEN ci.start_date >= '2024-12-07' AND ci.start_date <= '2025-01-06' THEN 'Enero'
        WHEN ci.start_date >= '2025-01-07' AND ci.start_date <= '2025-02-05' THEN 'Febrero'
        WHEN ci.start_date >= '2025-02-06' AND ci.start_date <= '2025-03-06' THEN 'Marzo'
        WHEN ci.start_date >= '2025-03-07' AND ci.start_date <= '2025-04-06' THEN 'Abril'
        WHEN ci.start_date >= '2025-04-07' AND ci.start_date <= '2025-05-06' THEN 'Mayo'
        WHEN ci.start_date >= '2025-05-07' AND ci.start_date <= '2025-06-05' THEN 'Junio'
        WHEN ci.start_date >= '2025-06-06' AND ci.start_date <= '2025-07-05' THEN 'Julio'
        WHEN ci.start_date >= '2025-07-06' AND ci.start_date <= '2025-08-05' THEN 'Agosto'
        WHEN ci.start_date >= '2025-08-06' AND ci.start_date <= '2025-09-04' THEN 'Septiembre'
        WHEN ci.start_date >= '2025-09-05' AND ci.start_date <= '2025-10-04' THEN 'Octubre'
        WHEN ci.start_date >= '2025-10-05' AND ci.start_date <= '2025-11-03' THEN 'Noviembre'
        WHEN ci.start_date >= '2025-11-04' AND ci.start_date <= '2025-12-03' THEN 'Diciembre'
        WHEN ci.start_date >= '2025-12-04' AND ci.start_date <= '2026-01-03' THEN 'Enero'
        ELSE 'Año anterior'
    END AS mes,
    CASE
        WHEN ci.start_date >= '2024-12-07' AND ci.start_date <= '2024-12-22' THEN '1 Quincena'
        WHEN ci.start_date >= '2024-12-23' AND ci.start_date <= '2025-01-06' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-01-07' AND ci.start_date <= '2025-01-21' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-01-22' AND ci.start_date <= '2025-02-05' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-02-06' AND ci.start_date <= '2025-02-20' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-02-21' AND ci.start_date <= '2025-03-06' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-03-07' AND ci.start_date <= '2025-03-21' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-03-22' AND ci.start_date <= '2025-04-06' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-04-07' AND ci.start_date <= '2025-04-21' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-04-22' AND ci.start_date <= '2025-05-06' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-05-07' AND ci.start_date <= '2025-05-21' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-05-22' AND ci.start_date <= '2025-06-05' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-06-06' AND ci.start_date <= '2025-06-20' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-06-21' AND ci.start_date <= '2025-07-05' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-07-06' AND ci.start_date <= '2025-07-20' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-07-21' AND ci.start_date <= '2025-08-05' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-08-06' AND ci.start_date <= '2025-08-20' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-08-21' AND ci.start_date <= '2025-09-04' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-09-05' AND ci.start_date <= '2025-09-19' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-09-20' AND ci.start_date <= '2025-10-04' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-10-05' AND ci.start_date <= '2025-10-19' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-10-20' AND ci.start_date <= '2025-11-03' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-11-04' AND ci.start_date <= '2025-11-18' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-11-19' AND ci.start_date <= '2025-12-03' THEN '2 Quincena'
        WHEN ci.start_date >= '2025-12-04' AND ci.start_date <= '2025-12-18' THEN '1 Quincena'
        WHEN ci.start_date >= '2025-12-19' AND ci.start_date <= '2026-01-03' THEN '2 Quincena'
        ELSE 'Año anterior'
    END AS quincena
FROM 
    consolidado_incidencias ci
INNER JOIN 
    employees e ON ci.employee_id = e.id
WHERE ci.start_date > '2025-08-05' and ci.start_date < '2025-09-04'
AND e.name_role IN (
'Asistente De Servicios Generales', 
'Analista de Control De Calidad', 
'Analista De Microbiología', 
'Asistente De Laboratorio', 
'Coordinadora Muestras', 
'Inspector De Proceso', 
'Administrativo Bodega Despacho', 
'Ayudante De Bodega', 
'Asistente De Bodega', 
'Chofer Administrativo Transporte', 
'Chofer', 
'Coordinador de Planta', 
'Encargado De Bodega Inflamables', 
'Encargado De Bodega Materias Primas', 
'Operario', 
'Operario Almacenamiento y Gestión de Residuos', 
'Peoneta');