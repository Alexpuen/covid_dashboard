
def normalizar_nombre_departamento(nombre):
  """
  Standardizes department names by applying consistent formatting and resolving naming variations.
  
  Args:
      nombre (str): Raw department name input
  
  Returns:
      str: Standardized department name
  """

  try:
      # Reference mapping for official department names
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
      
      nombre_norm = mapping.get(nombre.upper(), nombre.upper())
      return nombre_norm
      
  except Exception as e:
      print(f"Error normalizando nombre {nombre}: {str(e)}")
      return nombre