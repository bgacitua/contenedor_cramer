-- Versión optimizada con rango de fechas dinámico
-- Muestra automáticamente las últimas 3 semanas desde la fecha actual
DECLARE @fecha_fin DATE = CAST(GETDATE() AS DATE);  -- Fecha actual
DECLARE @fecha_inicio DATE = DATEADD(WEEK, -3, @fecha_fin);  -- 3 semanas atrás

-- Mostrar el rango de fechas que se está consultando
PRINT 'Consultando registros desde: ' + CAST(@fecha_inicio AS VARCHAR(10)) + ' hasta: ' + CAST(@fecha_fin AS VARCHAR(10));
PRINT 'Total de días a consultar: ' + CAST(DATEDIFF(DAY, @fecha_inicio, @fecha_fin) + 1 AS VARCHAR(10));

WITH fechas_rango AS (
    -- Generar secuencia de fechas entre inicio y fin
    SELECT @fecha_inicio AS [FECHA_SANTIAGO]
    UNION ALL
    SELECT DATEADD(DAY, 1, [FECHA_SANTIAGO])
    FROM fechas_rango
    WHERE DATEADD(DAY, 1, [FECHA_SANTIAGO]) <= @fecha_fin
),
todos_trabajadores AS (
    -- Obtener todos los trabajadores activos
    SELECT DISTINCT 
        u.[ID] AS [USER_ID],
        u.[FIRSTNAME],
        u.[LASTNAME],
        u.[EMPLOYEEID]
    FROM [MorphoManager].[dbo].[User_] AS u
    WHERE u.[EMPLOYEEID] IS NOT NULL 
      AND u.[EMPLOYEEID] != ''  -- Filtrar empleados válidos
),
combinaciones_trabajador_fecha AS (
    -- Crear matriz completa trabajador x fecha
    SELECT 
        t.[USER_ID],
        t.[FIRSTNAME],
        t.[LASTNAME], 
        t.[EMPLOYEEID],
        f.[FECHA_SANTIAGO]
    FROM todos_trabajadores t
    CROSS JOIN fechas_rango f
)
SELECT 
    -- Información del trabajador
    ctf.[FIRSTNAME],
    ctf.[LASTNAME],
    -- Dispositivos utilizados (concatenados si son múltiples)
    COALESCE(STRING_AGG(bd.[NAME_], ', '), 'Sin dispositivo') AS [DISPOSITIVOS_USADOS],
    ctf.[EMPLOYEEID],
    ctf.[FECHA_SANTIAGO],
    
    -- Conteo de registros por tipo (0 si no hay marcas)
    COALESCE(SUM(CASE WHEN m.[FUNCTIONKEYTEXT] = 'IN' THEN 1 ELSE 0 END), 0) AS [KEY_IN],
    COALESCE(SUM(CASE WHEN m.[FUNCTIONKEYTEXT] = 'OUT' THEN 1 ELSE 0 END), 0) AS [KEY_OUT],
    COALESCE(SUM(CASE WHEN m.[FUNCTIONKEYTEXT] = 'No Key' THEN 1 ELSE 0 END), 0) AS [NO_KEY],
    
    -- Estado de asistencia
    CASE 
        WHEN COUNT(m.[ID]) = 0 THEN 'Ausente'
        WHEN COUNT(m.[ID]) >= 1 THEN 'Asiste'
    END AS [ESTADO_ASISTENCIA],
    
    -- Información adicional
    COALESCE(COUNT(DISTINCT bd.[NAME_]), 0) AS [CANTIDAD_DISPOSITIVOS],
    COALESCE(COUNT(m.[ID]), 0) AS [TOTAL_REGISTROS],
    
    -- Información de horarios (opcional)
    COALESCE(MIN(CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS TIME)), CAST('00:00:00' AS TIME)) AS [PRIMERA_MARCA],
    COALESCE(MAX(CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS TIME)), CAST('00:00:00' AS TIME)) AS [ULTIMA_MARCA]
    
FROM combinaciones_trabajador_fecha ctf
LEFT JOIN [MorphoManager].[dbo].[AccessLog] AS m 
    ON ctf.[USER_ID] = m.[USERID]
    AND ctf.[FECHA_SANTIAGO] = CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE)
    AND CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE) BETWEEN @fecha_inicio AND @fecha_fin
LEFT JOIN [MorphoManager].[dbo].[BiometricDevice] AS bd 
    ON m.[MORPHOACCESSID] = bd.[ID]
    
GROUP BY 
    ctf.[FIRSTNAME],
    ctf.[LASTNAME],
    ctf.[EMPLOYEEID],
    ctf.[FECHA_SANTIAGO],
    ctf.[USER_ID]
    
ORDER BY 
    ctf.[FECHA_SANTIAGO] DESC, ctf.[LASTNAME], ctf.[FIRSTNAME]
OPTION (MAXRECURSION 366);  -- Permite hasta 366 días en la recursión