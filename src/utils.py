
def normalizar_nombre_departamento(nombre):
  """
  Normaliza los nombres de departamentos eliminando tildes y caracteres especiales.
  
  Args:
      nombre (str): Nombre del departamento a normalizar
  
  Returns:
      str: Nombre del departamento normalizado
  """
  try:
      # Diccionario de normalización
      mapping = {
          'ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA': 'SAN ANDRES',
          'BOGOTÁ, D.C.': 'BOGOTA',
          'BOGOTÁ D.C.': 'BOGOTA',
          'BOGOTA D.C.': 'BOGOTA',
          'BOLÍVAR': 'BOLIVAR',
          'BOYACÁ': 'BOYACA',
          'CAQUETÁ': 'CAQUETA',
          'CHOCÓ': 'CHOCO',
          'CÓRDOBA': 'CORDOBA',
          'GUAINÍA': 'GUAINIA',
          'QUINDÍO': 'QUINDIO',
          'ATLÁNTICO': 'ATLANTICO',
          'NARIÑO': 'NARINO',
          'VAUPÉS': 'VAUPES',
          'VALLE DEL CAUCA': 'VALLE',
          'LA GUAJIRA': 'GUAJIRA'
      }
      
      # Normalizar el nombre
      nombre_norm = mapping.get(nombre.upper(), nombre.upper())
      return nombre_norm
      
  except Exception as e:
      print(f"Error normalizando nombre {nombre}: {str(e)}")
      return nombre