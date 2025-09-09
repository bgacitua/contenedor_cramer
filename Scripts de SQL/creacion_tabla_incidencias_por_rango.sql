-- 1. Selecciona la base de datos
USE rrhh_app;

-- 2. Elimina la tabla si ya existe para evitar errores
DROP TABLE IF EXISTS incidencias;

-- 3. Crea la tabla 'incidencias' a partir de una consulta SELECT
CREATE TABLE incidencias AS
SELECT
    t1.employee_id,
    t2.full_name,
    t1.mes,
    t1.quincena,
    t1.tipo_incidencia,
    t1.fecha_incidencia,
    t1.start_date_absences,
    t1.end_date_absences,
    t1.type_code_absences,
    t1.start_date_licences,
    t1.end_date_licences,
    t1.type_code_licences,
    t1.start_date_permissions,
    t1.end_date_permissions,
    t1.type_code_permissions
FROM (
    -- SELECT 1: Consolidación para registros posteriores a 2020-01-01
    SELECT
        employee_id,
        CASE
            WHEN start_date >= '2024-12-07' AND start_date <= '2025-01-06' THEN 'Enero'
            WHEN start_date >= '2025-01-07' AND start_date <= '2025-02-05' THEN 'Febrero'
            WHEN start_date >= '2025-02-06' AND start_date <= '2025-03-06' THEN 'Marzo'
            WHEN start_date >= '2025-03-07' AND start_date <= '2025-04-06' THEN 'Abril'
            WHEN start_date >= '2025-04-07' AND start_date <= '2025-05-06' THEN 'Mayo'
            WHEN start_date >= '2025-05-07' AND start_date <= '2025-06-05' THEN 'Junio'
            WHEN start_date >= '2025-06-06' AND start_date <= '2025-07-05' THEN 'Julio'
            WHEN start_date >= '2025-07-06' AND start_date <= '2025-08-05' THEN 'Agosto'
            WHEN start_date >= '2025-08-06' AND start_date <= '2025-09-04' THEN 'Septiembre'
            WHEN start_date >= '2025-09-05' AND start_date <= '2025-10-04' THEN 'Octubre'
            WHEN start_date >= '2025-10-05' AND start_date <= '2025-11-03' THEN 'Noviembre'
            WHEN start_date >= '2025-11-04' AND start_date <= '2025-12-03' THEN 'Diciembre'
            WHEN start_date >= '2025-12-04' AND start_date <= '2026-01-03' THEN 'Enero'
            ELSE 'Año anterior'
        END AS mes,
        CASE
            WHEN start_date >= '2024-12-07' AND start_date <= '2024-12-22' THEN '1 Quincena'
            WHEN start_date >= '2024-12-23' AND start_date <= '2025-01-06' THEN '2 Quincena'
            WHEN start_date >= '2025-01-07' AND start_date <= '2025-01-21' THEN '1 Quincena'
            WHEN start_date >= '2025-01-22' AND start_date <= '2025-02-05' THEN '2 Quincena'
            WHEN start_date >= '2025-02-06' AND start_date <= '2025-02-20' THEN '1 Quincena'
            WHEN start_date >= '2025-02-21' AND start_date <= '2025-03-06' THEN '2 Quincena'
            WHEN start_date >= '2025-03-07' AND start_date <= '2025-03-21' THEN '1 Quincena'
            WHEN start_date >= '2025-03-22' AND start_date <= '2025-04-06' THEN '2 Quincena'
            WHEN start_date >= '2025-04-07' AND start_date <= '2025-04-21' THEN '1 Quincena'
            WHEN start_date >= '2025-04-22' AND start_date <= '2025-05-06' THEN '2 Quincena'
            WHEN start_date >= '2025-05-07' AND start_date <= '2025-05-21' THEN '1 Quincena'
            WHEN start_date >= '2025-05-22' AND start_date <= '2025-06-05' THEN '2 Quincena'
            WHEN start_date >= '2025-06-06' AND start_date <= '2025-06-20' THEN '1 Quincena'
            WHEN start_date >= '2025-06-21' AND start_date <= '2025-07-05' THEN '2 Quincena'
            WHEN start_date >= '2025-07-06' AND start_date <= '2025-07-20' THEN '1 Quincena'
            WHEN start_date >= '2025-07-21' AND start_date <= '2025-08-05' THEN '2 Quincena'
            WHEN start_date >= '2025-08-06' AND start_date <= '2025-08-20' THEN '1 Quincena'
            WHEN start_date >= '2025-08-21' AND start_date <= '2025-09-04' THEN '2 Quincena'
            WHEN start_date >= '2025-09-05' AND start_date <= '2025-09-19' THEN '1 Quincena'
            WHEN start_date >= '2025-09-20' AND start_date <= '2025-10-04' THEN '2 Quincena'
            WHEN start_date >= '2025-10-05' AND start_date <= '2025-10-19' THEN '1 Quincena'
            WHEN start_date >= '2025-10-20' AND start_date <= '2025-11-03' THEN '2 Quincena'
            WHEN start_date >= '2025-11-04' AND start_date <= '2025-11-18' THEN '1 Quincena'
            WHEN start_date >= '2025-11-19' AND start_date <= '2025-12-03' THEN '2 Quincena'
            WHEN start_date >= '2025-12-04' AND start_date <= '2025-12-18' THEN '1 Quincena'
            WHEN start_date >= '2025-12-19' AND start_date <= '2026-01-03' THEN '2 Quincena'
            ELSE 'Año anterior'
        END AS quincena,
        'absences' AS tipo_incidencia,
        start_date AS fecha_incidencia,
        start_date AS start_date_absences,
        end_date AS end_date_absences,
        absence_type_code AS type_code_absences,
        NULL AS start_date_licences,
        NULL AS end_date_licences,
        NULL AS type_code_licences,
        NULL AS start_date_permissions,
        NULL AS end_date_permissions,
        NULL AS type_code_permissions
    FROM absences
    WHERE start_date >= '2020-01-01'
    
    UNION ALL
    
    SELECT
        employee_id,
        CASE
            WHEN start_date >= '2024-12-07' AND start_date <= '2025-01-06' THEN 'Enero'
            WHEN start_date >= '2025-01-07' AND start_date <= '2025-02-05' THEN 'Febrero'
            WHEN start_date >= '2025-02-06' AND start_date <= '2025-03-06' THEN 'Marzo'
            WHEN start_date >= '2025-03-07' AND start_date <= '2025-04-06' THEN 'Abril'
            WHEN start_date >= '2025-04-07' AND start_date <= '2025-05-06' THEN 'Mayo'
            WHEN start_date >= '2025-05-07' AND start_date <= '2025-06-05' THEN 'Junio'
            WHEN start_date >= '2025-06-06' AND start_date <= '2025-07-05' THEN 'Julio'
            WHEN start_date >= '2025-07-06' AND start_date <= '2025-08-05' THEN 'Agosto'
            WHEN start_date >= '2025-08-06' AND start_date <= '2025-09-04' THEN 'Septiembre'
            WHEN start_date >= '2025-09-05' AND start_date <= '2025-10-04' THEN 'Octubre'
            WHEN start_date >= '2025-10-05' AND start_date <= '2025-11-03' THEN 'Noviembre'
            WHEN start_date >= '2025-11-04' AND start_date <= '2025-12-03' THEN 'Diciembre'
            WHEN start_date >= '2025-12-04' AND start_date <= '2026-01-03' THEN 'Enero'
            ELSE 'Año anterior'
        END AS mes,
        CASE
            WHEN start_date >= '2024-12-07' AND start_date <= '2024-12-22' THEN '1 Quincena'
            WHEN start_date >= '2024-12-23' AND start_date <= '2025-01-06' THEN '2 Quincena'
            WHEN start_date >= '2025-01-07' AND start_date <= '2025-01-21' THEN '1 Quincena'
            WHEN start_date >= '2025-01-22' AND start_date <= '2025-02-05' THEN '2 Quincena'
            WHEN start_date >= '2025-02-06' AND start_date <= '2025-02-20' THEN '1 Quincena'
            WHEN start_date >= '2025-02-21' AND start_date <= '2025-03-06' THEN '2 Quincena'
            WHEN start_date >= '2025-03-07' AND start_date <= '2025-03-21' THEN '1 Quincena'
            WHEN start_date >= '2025-03-22' AND start_date <= '2025-04-06' THEN '2 Quincena'
            WHEN start_date >= '2025-04-07' AND start_date <= '2025-04-21' THEN '1 Quincena'
            WHEN start_date >= '2025-04-22' AND start_date <= '2025-05-06' THEN '2 Quincena'
            WHEN start_date >= '2025-05-07' AND start_date <= '2025-05-21' THEN '1 Quincena'
            WHEN start_date >= '2025-05-22' AND start_date <= '2025-06-05' THEN '2 Quincena'
            WHEN start_date >= '2025-06-06' AND start_date <= '2025-06-20' THEN '1 Quincena'
            WHEN start_date >= '2025-06-21' AND start_date <= '2025-07-05' THEN '2 Quincena'
            WHEN start_date >= '2025-07-06' AND start_date <= '2025-07-20' THEN '1 Quincena'
            WHEN start_date >= '2025-07-21' AND start_date <= '2025-08-05' THEN '2 Quincena'
            WHEN start_date >= '2025-08-06' AND start_date <= '2025-08-20' THEN '1 Quincena'
            WHEN start_date >= '2025-08-21' AND start_date <= '2025-09-04' THEN '2 Quincena'
            WHEN start_date >= '2025-09-05' AND start_date <= '2025-09-19' THEN '1 Quincena'
            WHEN start_date >= '2025-09-20' AND start_date <= '2025-10-04' THEN '2 Quincena'
            WHEN start_date >= '2025-10-05' AND start_date <= '2025-10-19' THEN '1 Quincena'
            WHEN start_date >= '2025-10-20' AND start_date <= '2025-11-03' THEN '2 Quincena'
            WHEN start_date >= '2025-11-04' AND start_date <= '2025-11-18' THEN '1 Quincena'
            WHEN start_date >= '2025-11-19' AND start_date <= '2025-12-03' THEN '2 Quincena'
            WHEN start_date >= '2025-12-04' AND start_date <= '2025-12-18' THEN '1 Quincena'
            WHEN start_date >= '2025-12-19' AND start_date <= '2026-01-03' THEN '2 Quincena'
            ELSE 'Año anterior'
        END AS quincena,
        'licences' AS tipo_incidencia,
        start_date AS fecha_incidencia,
        NULL AS start_date_absences,
        NULL AS end_date_absences,
        NULL AS type_code_absences,
        start_date AS start_date_licences,
        end_date AS end_date_licences,
        licence_type_code AS type_code_licences,
        NULL AS start_date_permissions,
        NULL AS end_date_permissions,
        NULL AS type_code_permissions
    FROM licences
    WHERE start_date >= '2020-01-01'

    UNION ALL
    
    SELECT
        employee_id,
        CASE
            WHEN start_date >= '2024-12-07' AND start_date <= '2025-01-06' THEN 'Enero'
            WHEN start_date >= '2025-01-07' AND start_date <= '2025-02-05' THEN 'Febrero'
            WHEN start_date >= '2025-02-06' AND start_date <= '2025-03-06' THEN 'Marzo'
            WHEN start_date >= '2025-03-07' AND start_date <= '2025-04-06' THEN 'Abril'
            WHEN start_date >= '2025-04-07' AND start_date <= '2025-05-06' THEN 'Mayo'
            WHEN start_date >= '2025-05-07' AND start_date <= '2025-06-05' THEN 'Junio'
            WHEN start_date >= '2025-06-06' AND start_date <= '2025-07-05' THEN 'Julio'
            WHEN start_date >= '2025-07-06' AND start_date <= '2025-08-05' THEN 'Agosto'
            WHEN start_date >= '2025-08-06' AND start_date <= '2025-09-04' THEN 'Septiembre'
            WHEN start_date >= '2025-09-05' AND start_date <= '2025-10-04' THEN 'Octubre'
            WHEN start_date >= '2025-10-05' AND start_date <= '2025-11-03' THEN 'Noviembre'
            WHEN start_date >= '2025-11-04' AND start_date <= '2025-12-03' THEN 'Diciembre'
            WHEN start_date >= '2025-12-04' AND start_date <= '2026-01-03' THEN 'Enero'
            ELSE 'Año anterior'
        END AS mes,
        CASE
            WHEN start_date >= '2024-12-07' AND start_date <= '2024-12-22' THEN '1 Quincena'
            WHEN start_date >= '2024-12-23' AND start_date <= '2025-01-06' THEN '2 Quincena'
            WHEN start_date >= '2025-01-07' AND start_date <= '2025-01-21' THEN '1 Quincena'
            WHEN start_date >= '2025-01-22' AND start_date <= '2025-02-05' THEN '2 Quincena'
            WHEN start_date >= '2025-02-06' AND start_date <= '2025-02-20' THEN '1 Quincena'
            WHEN start_date >= '2025-02-21' AND start_date <= '2025-03-06' THEN '2 Quincena'
            WHEN start_date >= '2025-03-07' AND start_date <= '2025-03-21' THEN '1 Quincena'
            WHEN start_date >= '2025-03-22' AND start_date <= '2025-04-06' THEN '2 Quincena'
            WHEN start_date >= '2025-04-07' AND start_date <= '2025-04-21' THEN '1 Quincena'
            WHEN start_date >= '2025-04-22' AND start_date <= '2025-05-06' THEN '2 Quincena'
            WHEN start_date >= '2025-05-07' AND start_date <= '2025-05-21' THEN '1 Quincena'
            WHEN start_date >= '2025-05-22' AND start_date <= '2025-06-05' THEN '2 Quincena'
            WHEN start_date >= '2025-06-06' AND start_date <= '2025-06-20' THEN '1 Quincena'
            WHEN start_date >= '2025-06-21' AND start_date <= '2025-07-05' THEN '2 Quincena'
            WHEN start_date >= '2025-07-06' AND start_date <= '2025-07-20' THEN '1 Quincena'
            WHEN start_date >= '2025-07-21' AND start_date <= '2025-08-05' THEN '2 Quincena'
            WHEN start_date >= '2025-08-06' AND start_date <= '2025-08-20' THEN '1 Quincena'
            WHEN start_date >= '2025-08-21' AND start_date <= '2025-09-04' THEN '2 Quincena'
            WHEN start_date >= '2025-09-05' AND start_date <= '2025-09-19' THEN '1 Quincena'
            WHEN start_date >= '2025-09-20' AND start_date <= '2025-10-04' THEN '2 Quincena'
            WHEN start_date >= '2025-10-05' AND start_date <= '2025-10-19' THEN '1 Quincena'
            WHEN start_date >= '2025-10-20' AND start_date <= '2025-11-03' THEN '2 Quincena'
            WHEN start_date >= '2025-11-04' AND start_date <= '2025-11-18' THEN '1 Quincena'
            WHEN start_date >= '2025-11-19' AND start_date <= '2025-12-03' THEN '2 Quincena'
            WHEN start_date >= '2025-12-04' AND start_date <= '2025-12-18' THEN '1 Quincena'
            WHEN start_date >= '2025-12-19' AND start_date <= '2026-01-03' THEN '2 Quincena'
            ELSE 'Año anterior'
        END AS quincena,
        'permissions' AS tipo_incidencia,
        start_date AS fecha_incidencia,
        NULL AS start_date_absences,
        NULL AS end_date_absences,
        NULL AS type_code_absences,
        NULL AS start_date_licences,
        NULL AS end_date_licences,
        NULL AS type_code_licences,
        start_date AS start_date_permissions,
        end_date AS end_date_permissions,
        permission_type_code AS type_code_permissions
    FROM permissions
    WHERE start_date >= '2020-01-01'

    UNION ALL
    
    -- SELECT 2: Consolidación para registros anteriores a 2020-01-01
    SELECT
        id as employee_id, -- Usamos el 'id' del movimiento como 'employee_id' en esta parte
        CASE
            WHEN start_date >= '2024-12-07' AND start_date <= '2025-01-06' THEN 'Enero'
            WHEN start_date >= '2025-01-07' AND start_date <= '2025-02-05' THEN 'Febrero'
            WHEN start_date >= '2025-02-06' AND start_date <= '2025-03-06' THEN 'Marzo'
            WHEN start_date >= '2025-03-07' AND start_date <= '2025-04-06' THEN 'Abril'
            WHEN start_date >= '2025-04-07' AND start_date <= '2025-05-06' THEN 'Mayo'
            WHEN start_date >= '2025-05-07' AND start_date <= '2025-06-05' THEN 'Junio'
            WHEN start_date >= '2025-06-06' AND start_date <= '2025-07-05' THEN 'Julio'
            WHEN start_date >= '2025-07-06' AND start_date <= '2025-08-05' THEN 'Agosto'
            WHEN start_date >= '2025-08-06' AND start_date <= '2025-09-04' THEN 'Septiembre'
            WHEN start_date >= '2025-09-05' AND start_date <= '2025-10-04' THEN 'Octubre'
            WHEN start_date >= '2025-10-05' AND start_date <= '2025-11-03' THEN 'Noviembre'
            WHEN start_date >= '2025-11-04' AND start_date <= '2025-12-03' THEN 'Diciembre'
            WHEN start_date >= '2025-12-04' AND start_date <= '2026-01-03' THEN 'Enero'
            ELSE 'Año anterior'
        END AS mes,
        CASE
            WHEN start_date >= '2024-12-07' AND start_date <= '2024-12-22' THEN '1 Quincena'
            WHEN start_date >= '2024-12-23' AND start_date <= '2025-01-06' THEN '2 Quincena'
            WHEN start_date >= '2025-01-07' AND start_date <= '2025-01-21' THEN '1 Quincena'
            WHEN start_date >= '2025-01-22' AND start_date <= '2025-02-05' THEN '2 Quincena'
            WHEN start_date >= '2025-02-06' AND start_date <= '2025-02-20' THEN '1 Quincena'
            WHEN start_date >= '2025-02-21' AND start_date <= '2025-03-06' THEN '2 Quincena'
            WHEN start_date >= '2025-03-07' AND start_date <= '2025-03-21' THEN '1 Quincena'
            WHEN start_date >= '2025-03-22' AND start_date <= '2025-04-06' THEN '2 Quincena'
            WHEN start_date >= '2025-04-07' AND start_date <= '2025-04-21' THEN '1 Quincena'
            WHEN start_date >= '2025-04-22' AND start_date <= '2025-05-06' THEN '2 Quincena'
            WHEN start_date >= '2025-05-07' AND start_date <= '2025-05-21' THEN '1 Quincena'
            WHEN start_date >= '2025-05-22' AND start_date <= '2025-06-05' THEN '2 Quincena'
            WHEN start_date >= '2025-06-06' AND start_date <= '2025-06-20' THEN '1 Quincena'
            WHEN start_date >= '2025-06-21' AND start_date <= '2025-07-05' THEN '2 Quincena'
            WHEN start_date >= '2025-07-06' AND start_date <= '2025-07-20' THEN '1 Quincena'
            WHEN start_date >= '2025-07-21' AND start_date <= '2025-08-05' THEN '2 Quincena'
            WHEN start_date >= '2025-08-06' AND start_date <= '2025-08-20' THEN '1 Quincena'
            WHEN start_date >= '2025-08-21' AND start_date <= '2025-09-04' THEN '2 Quincena'
            WHEN start_date >= '2025-09-05' AND start_date <= '2025-09-19' THEN '1 Quincena'
            WHEN start_date >= '2025-09-20' AND start_date <= '2025-10-04' THEN '2 Quincena'
            WHEN start_date >= '2025-10-05' AND start_date <= '2025-10-19' THEN '1 Quincena'
            WHEN start_date >= '2025-10-20' AND start_date <= '2025-11-03' THEN '2 Quincena'
            WHEN start_date >= '2025-11-04' AND start_date <= '2025-11-18' THEN '1 Quincena'
            WHEN start_date >= '2025-11-19' AND start_date <= '2025-12-03' THEN '2 Quincena'
            WHEN start_date >= '2025-12-04' AND start_date <= '2025-12-18' THEN '1 Quincena'
            WHEN start_date >= '2025-12-19' AND start_date <= '2026-01-03' THEN '2 Quincena'
            ELSE 'Año anterior'
        END AS quincena,
        'absences' AS tipo_incidencia,
        start_date AS fecha_incidencia,
        start_date AS start_date_absences,
        end_date AS end_date_absences,
        absence_type_code AS type_code_absences,
        NULL AS start_date_licences,
        NULL AS end_date_licences,
        NULL AS type_code_licences,
        NULL AS start_date_permissions,
        NULL AS end_date_permissions,
        NULL AS type_code_permissions
    FROM absences
    WHERE start_date < '2020-01-01'
    
    UNION ALL
    
    SELECT
        id as employee_id, -- Usamos el 'id' del movimiento como 'employee_id' en esta parte
        CASE
            WHEN start_date >= '2024-12-07' AND start_date <= '2025-01-06' THEN 'Enero'
            WHEN start_date >= '2025-01-07' AND start_date <= '2025-02-05' THEN 'Febrero'
            WHEN start_date >= '2025-02-06' AND start_date <= '2025-03-06' THEN 'Marzo'
            WHEN start_date >= '2025-03-07' AND start_date <= '2025-04-06' THEN 'Abril'
            WHEN start_date >= '2025-04-07' AND start_date <= '2025-05-06' THEN 'Mayo'
            WHEN start_date >= '2025-05-07' AND start_date <= '2025-06-05' THEN 'Junio'
            WHEN start_date >= '2025-06-06' AND start_date <= '2025-07-05' THEN 'Julio'
            WHEN start_date >= '2025-07-06' AND start_date <= '2025-08-05' THEN 'Agosto'
            WHEN start_date >= '2025-08-06' AND start_date <= '2025-09-04' THEN 'Septiembre'
            WHEN start_date >= '2025-09-05' AND start_date <= '2025-10-04' THEN 'Octubre'
            WHEN start_date >= '2025-10-05' AND start_date <= '2025-11-03' THEN 'Noviembre'
            WHEN start_date >= '2025-11-04' AND start_date <= '2025-12-03' THEN 'Diciembre'
            WHEN start_date >= '2025-12-04' AND start_date <= '2026-01-03' THEN 'Enero'
            ELSE 'Año anterior'
        END AS quincena,
        'licences' AS tipo_incidencia,
        start_date AS fecha_incidencia,
        NULL AS start_date_absences,
        NULL AS end_date_absences,
        NULL AS type_code_absences,
        start_date AS start_date_licences,
        end_date AS end_date_licences,
        licence_type_code AS type_code_licences,
        NULL AS start_date_permissions,
        NULL AS end_date_permissions,
        NULL AS type_code_permissions
    FROM licences
    WHERE start_date < '2020-01-01'
    
    UNION ALL
    
    SELECT
        id as employee_id, -- Usamos el 'id' del movimiento como 'employee_id' en esta parte
        CASE
            WHEN start_date >= '2024-12-07' AND start_date <= '2025-01-06' THEN 'Enero'
            WHEN start_date >= '2025-01-07' AND start_date <= '2025-02-05' THEN 'Febrero'
            WHEN start_date >= '2025-02-06' AND start_date <= '2025-03-06' THEN 'Marzo'
            WHEN start_date >= '2025-03-07' AND start_date <= '2025-04-06' THEN 'Abril'
            WHEN start_date >= '2025-04-07' AND start_date <= '2025-05-06' THEN 'Mayo'
            WHEN start_date >= '2025-05-07' AND start_date <= '2025-06-05' THEN 'Junio'
            WHEN start_date >= '2025-06-06' AND start_date <= '2025-07-05' THEN 'Julio'
            WHEN start_date >= '2025-07-06' AND start_date <= '2025-08-05' THEN 'Agosto'
            WHEN start_date >= '2025-08-06' AND start_date <= '2025-09-04' THEN 'Septiembre'
            WHEN start_date >= '2025-09-05' AND start_date <= '2025-10-04' THEN 'Octubre'
            WHEN start_date >= '2025-10-05' AND start_date <= '2025-11-03' THEN 'Noviembre'
            WHEN start_date >= '2025-11-04' AND start_date <= '2025-12-03' THEN 'Diciembre'
            WHEN start_date >= '2025-12-04' AND start_date <= '2026-01-03' THEN 'Enero'
            ELSE 'Año anterior'
        END AS quincena,
        'permissions' AS tipo_incidencia,
        start_date AS fecha_incidencia,
        NULL AS start_date_absences,
        NULL AS end_date_absences,
        NULL AS type_code_absences,
        NULL AS start_date_licences,
        NULL AS end_date_licences,
        NULL AS type_code_licences,
        start_date AS start_date_permissions,
        end_date AS end_date_permissions,
        permission_type_code AS type_code_permissions
    FROM permissions
    WHERE start_date < '2020-01-01'
) AS t1
JOIN employees AS t2
    ON (t1.fecha_incidencia >= '2020-01-01' AND t1.employee_id = t2.person_id)
    OR (t1.fecha_incidencia < '2020-01-01' AND t1.employee_id = t2.id);