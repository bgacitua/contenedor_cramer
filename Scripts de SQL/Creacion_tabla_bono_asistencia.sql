SELECT
    e.full_name,
    e.rut,
    e.active_since,
    e.status,
    e.name_role,
    e.cost_center,
    a.first_level_name AS area_name
FROM
    rrhh_app.employees AS e
INNER JOIN
    rrhh_app.areas AS a ON e.area_id = a.id
WHERE
    e.name_role IN (
        'Analista de Calidad y Procesos',
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
        'Peoneta'
    )
    AND e.status = 'activo'
ORDER BY
    e.active_since DESC;