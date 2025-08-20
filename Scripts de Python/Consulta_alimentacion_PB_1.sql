-- Consulta simplificada para Power BI
-- Versión sin CTEs complejos - Compatible con Power BI
-- Muestra registros de las últimas 3 semanas

SELECT 
    -- Información del trabajador
    u.[FIRSTNAME],
    u.[LASTNAME],
    u.[EMPLOYEEID],
    
    -- Fecha convertida a Santiago
    CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE) AS [FECHA_SANTIAGO],
    
    -- Dispositivo utilizado
    ISNULL(bd.[NAME_], 'Sin dispositivo') AS [DISPOSITIVO],
    
    -- Información de la marca
    m.[FUNCTIONKEYTEXT] AS [TIPO_MARCA],
    CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS TIME) AS [HORA_MARCA],
    
    -- Información completa de fecha/hora
    m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS [FECHA_HORA_COMPLETA],
    
    -- Información adicional
    m.[ACCESS] AS [ACCESO],
    m.[TOKEN],
    m.[DURATION] AS [DURACION],
    
    -- Campos calculados útiles para Power BI
    CASE 
        WHEN m.[FUNCTIONKEYTEXT] = 'IN' THEN 1 
        ELSE 0 
    END AS [ES_ENTRADA],
    
    CASE 
        WHEN m.[FUNCTIONKEYTEXT] = 'OUT' THEN 1 
        ELSE 0 
    END AS [ES_SALIDA],
    
    CASE 
        WHEN m.[FUNCTIONKEYTEXT] = 'No Key' THEN 1 
        ELSE 0 
    END AS [ES_NO_KEY],
    
    -- Día de la semana
    DATENAME(WEEKDAY, CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE)) AS [DIA_SEMANA],
    
    -- Fecha de consulta para referencia
    CAST(GETDATE() AS DATE) AS [FECHA_CONSULTA]
    
FROM [MorphoManager].[dbo].[AccessLog] AS m
INNER JOIN [MorphoManager].[dbo].[User_] AS u 
    ON m.[USERID] = u.[ID]
LEFT JOIN [MorphoManager].[dbo].[BiometricDevice] AS bd 
    ON m.[MORPHOACCESSID] = bd.[ID]

WHERE 
    -- Filtro de las últimas 3 semanas
    CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE) 
        >= DATEADD(WEEK, -3, CAST(GETDATE() AS DATE))
    AND CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE) 
        <= CAST(GETDATE() AS DATE)
    -- Filtrar solo empleados válidos
    AND u.[EMPLOYEEID] IS NOT NULL 
    AND u.[EMPLOYEEID] != '';