@echo off
REM Script para ejecutar respaldo biométrico automatizado
REM Creado automáticamente por el instalador

echo ========================================
echo EJECUTANDO RESPALDO BIOMETRICO AUTOMATIZADO
echo ========================================
echo Fecha: %date% %time%
echo ========================================

cd /d "C:\Users\bgacitua\Desktop\Repositorio_GitHub\Scripts de Python"
python "respaldo_biometrico_automatizado.py"

echo ========================================
echo RESPALDO COMPLETADO
echo ========================================
pause
