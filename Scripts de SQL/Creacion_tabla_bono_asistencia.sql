SELECT 
`full_name`, 
`rut`,  
`active_since`, 
`status`, 
`name_role`
FROM employees
WHERE name_role IN (
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
'Peoneta')
AND status = 'activo'
order by active_since DESC;