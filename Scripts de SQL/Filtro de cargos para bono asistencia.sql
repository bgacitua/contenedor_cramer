SELECT i.*, e.full_name, e.name_role
FROM incidencias i
LEFT JOIN employees e ON i.employee_id = e.person_id
WHERE e.status = 'Activo' AND e.name_role IN ('Asistente De Servicios Generales', 
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