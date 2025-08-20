-- Consulta agregada simplificada para Power BI
-- Versión sin CTEs complejos - Compatible con Power BI
-- Muestra matriz completa trabajador x fecha con estados de asistencia
-- Últimas 3 semanas automáticamente

SELECT 
    -- Información del trabajador
    u.[FIRSTNAME],
    u.[LASTNAME],
    u.[EMPLOYEEID],
    
    -- Fecha convertida a Santiago
    CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE) AS [FECHA_SANTIAGO],
    
    -- Información de la marca agregada
    ISNULL(STRING_AGG(bd.[NAME_], ', '), 'Sin dispositivo') AS [DISPOSITIVOS_USADOS],
    
    -- Conteo de registros por tipo
    SUM(CASE WHEN m.[FUNCTIONKEYTEXT] = 'IN' THEN 1 ELSE 0 END) AS [KEY_IN],
    SUM(CASE WHEN m.[FUNCTIONKEYTEXT] = 'OUT' THEN 1 ELSE 0 END) AS [KEY_OUT],
    SUM(CASE WHEN m.[FUNCTIONKEYTEXT] = 'No Key' THEN 1 ELSE 0 END) AS [NO_KEY],
    
    -- Estado de asistencia
    CASE 
        WHEN COUNT(m.[ID]) = 0 THEN 'Ausente'
        ELSE 'Asiste'
    END AS [ESTADO_ASISTENCIA],
    
    -- Información adicional
    COUNT(DISTINCT bd.[NAME_]) AS [CANTIDAD_DISPOSITIVOS],
    COUNT(m.[ID]) AS [TOTAL_REGISTROS],
    
    -- Información de horarios
    MIN(CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS TIME)) AS [PRIMERA_MARCA],
    MAX(CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS TIME)) AS [ULTIMA_MARCA],
    
    -- Campos adicionales útiles para Power BI
    DATENAME(WEEKDAY, CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE)) AS [DIA_SEMANA],
    
    -- Campos para filtros y análisis
    YEAR(CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE)) AS [AÑO],
    MONTH(CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE)) AS [MES],
    DATEPART(WEEK, CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE)) AS [SEMANA],
    
    -- Tipo de día
    CASE 
        WHEN DATENAME(WEEKDAY, CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE)) IN ('Saturday', 'Sunday') 
        THEN 'Fin de Semana'
        ELSE 'Día Laboral'
    END AS [TIPO_DIA],
    
    -- Fecha de consulta para referencia
    CAST(GETDATE() AS DATE) AS [FECHA_CONSULTA]
    
FROM [MorphoManager].[dbo].[User_] AS u
LEFT JOIN [MorphoManager].[dbo].[AccessLog] AS m 
    ON u.[ID] = m.[USERID]
    AND CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE) 
        BETWEEN DATEADD(WEEK, -3, CAST(GETDATE() AS DATE)) AND CAST(GETDATE() AS DATE)
LEFT JOIN [MorphoManager].[dbo].[BiometricDevice] AS bd 
    ON m.[MORPHOACCESSID] = bd.[ID]

WHERE 
    -- Filtrar solo empleados válidos
    u.[EMPLOYEEID] IS NOT NULL 
    AND u.[EMPLOYEEID] != ''

GROUP BY 
    u.[FIRSTNAME],
    u.[LASTNAME],
    u.[EMPLOYEEID],
    CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE),
    DATENAME(WEEKDAY, CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE)),
    YEAR(CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE)),
    MONTH(CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE)),
    DATEPART(WEEK, CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE));