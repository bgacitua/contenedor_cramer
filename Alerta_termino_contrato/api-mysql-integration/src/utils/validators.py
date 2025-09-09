def validate_data(data):
    """
    Valida los datos extraídos antes de ser procesados o enviados a la base de datos.

    Args:
        data (dict): Datos a validar.

    Returns:
        bool: True si los datos son válidos, False en caso contrario.
    """
    if not isinstance(data, dict):
        print("❌ Los datos deben ser un diccionario.")
        return False

    required_fields = ['field1', 'field2', 'field3']  # Reemplazar con los campos requeridos

    for field in required_fields:
        if field not in data:
            print(f"❌ Falta el campo requerido: {field}")
            return False

    # Aquí se pueden agregar más validaciones según sea necesario

    print("✅ Los datos son válidos.")
    return True


def validate_date_format(date_string):
    """
    Valida el formato de una fecha en formato 'YYYY-MM-DD'.

    Args:
        date_string (str): Fecha a validar.

    Returns:
        bool: True si el formato es válido, False en caso contrario.
    """
    from datetime import datetime

    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        print("❌ Formato de fecha inválido. Debe ser 'YYYY-MM-DD'.")
        return False