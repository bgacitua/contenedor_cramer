-- Crea la tabla 'consolidado_incidencias' si no existe.
DROP table consolidado_incidencias;
CREATE TABLE IF NOT EXISTS consolidado_incidencias AS
SELECT 
    id, 
    start_date, 
    end_date, 
    days_count, 
    workday_stage, 
    application_date, 
    application_end_date, 
    employee_id, 
    status, 
    created_at, 
    'permissions' AS tabla_origen 
FROM permissions
UNION ALL
SELECT 
    id, 
    start_date, 
    end_date, 
    days_count, 
    workday_stage, 
    application_date, 
    application_end_date, 
    employee_id, 
    status, 
    created_at, 
    'absences' AS tabla_origen 
FROM absences
UNION ALL
SELECT 
    id, 
    start_date, 
    end_date, 
    days_count, 
    workday_stage, 
    application_date, 
    application_end_date, 
    employee_id, 
    status, 
    created_at, 
    'licences' AS tabla_origen 
FROM licences;