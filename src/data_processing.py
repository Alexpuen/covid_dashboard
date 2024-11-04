# data_processing.py
import pandas as pd
import os
from pathlib import Path

def get_project_root():
  return Path(__file__).parent.parent

def normalizar_nombre_departamento(nombre):
  """Normaliza los nombres de departamentos"""
  nombre = str(nombre).upper().strip()
  correcciones = {
      'NARINO': 'NARIÑO',
      'BOGOTA': 'SANTAFE DE BOGOTA D.C',
      'BOGOTA D.C.': 'SANTAFE DE BOGOTA D.C',
      'BOGOTÁ': 'SANTAFE DE BOGOTA D.C',
      'BOGOTÁ D.C.': 'SANTAFE DE BOGOTA D.C',
      'VALLE': 'VALLE DEL CAUCA',
      'SAN ANDRES': 'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA'
  }
  return correcciones.get(nombre, nombre)

def procesar_edad(edad):
  """Procesa la edad eliminando el sufijo entre paréntesis"""
  try:
      if pd.isna(edad):
          return None
      edad_str = str(edad)
      return int(edad_str.split('(')[0])
  except:
      return None

def load_data():
  try:
      print("Cargando datos...")
      root_dir = get_project_root()
      print(f"Directorio raíz: {root_dir}")
      
      # Construir ruta al archivo Excel
      ruta_excel = os.path.join(root_dir, 'data', 'datos_covid.xlsx')
      print(f"Buscando archivo en: {ruta_excel}")
      
      if not os.path.exists(ruta_excel):
          print(f"ERROR: El archivo no existe en {ruta_excel}")
          return None, None
          
      # Cargar datos
      df = pd.read_excel(ruta_excel)
      print("Datos cargados exitosamente")
      
      # Procesar datos
      df['DEPARTAMENTO'] = df['DEPARTAMENTO'].apply(normalizar_nombre_departamento)
      df['CASOS'] = 1
      df['EDAD'] = df['EDAD FALLECIDO'].apply(procesar_edad)
      
      # Procesar fechas
      for col in ['FECHA DEFUNCIÓN', 'FECHA REGISTRO']:
          if col in df.columns:
              df[col] = pd.to_datetime(df[col].astype(str).str.strip("'"), 
                                     format='%d/%m/%Y', 
                                     errors='coerce')
      
      if 'FECHA DEFUNCIÓN' in df.columns:
          df['AÑO'] = df['FECHA DEFUNCIÓN'].dt.year
          df['MES'] = df['FECHA DEFUNCIÓN'].dt.month
      
      # Crear df_mapa
      df_mapa = crear_dataset_mapa(df)
      
      print("Procesamiento de datos completado")
      return df, df_mapa
      
  except Exception as e:
      print(f"Error cargando datos: {str(e)}")
      import traceback
      print(traceback.format_exc())
      return None, None

def crear_dataset_mapa(df):
  try:
      df_mapa = df.groupby('DEPARTAMENTO', as_index=False).agg({
          'CASOS': 'sum'
      })
      
      coordenadas = {
          'AMAZONAS': [0.0, -71.9],
          'ANTIOQUIA': [7.0, -75.5],
          'ARAUCA': [6.5, -71.0],
          'ATLANTICO': [10.9, -74.8],
          'SANTAFE DE BOGOTA D.C': [4.6, -74.1],
          'BOLIVAR': [8.6, -74.0],
          'BOYACA': [5.5, -73.0],
          'CALDAS': [5.3, -75.3],
          'CAQUETA': [0.9, -74.0],
          'CASANARE': [5.3, -71.3],
          'CAUCA': [2.5, -76.6],
          'CESAR': [9.3, -73.5],
          'CHOCO': [5.7, -76.6],
          'CORDOBA': [8.3, -75.6],
          'CUNDINAMARCA': [5.0, -74.0],
          'GUAINIA': [2.5, -69.0],
          'GUAVIARE': [2.8, -72.8],
          'HUILA': [2.5, -75.5],
          'LA GUAJIRA': [11.5, -72.8],
          'MAGDALENA': [10.4, -74.4],
          'META': [3.5, -73.0],
          'NARIÑO': [1.2, -77.3],
          'NORTE DE SANTANDER': [7.9, -72.5],
          'PUTUMAYO': [0.4, -76.5],
          'QUINDIO': [4.5, -75.7],
          'RISARALDA': [5.3, -75.9],
          'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA': [12.5, -81.7],
          'SANTANDER': [6.6, -73.3],
          'SUCRE': [9.3, -75.4],
          'TOLIMA': [4.4, -75.2],
          'VALLE DEL CAUCA': [3.8, -76.5],
          'VAUPES': [0.5, -70.4],
          'VICHADA': [4.4, -69.8]
      }
      
      df_mapa['lat'] = df_mapa['DEPARTAMENTO'].map(lambda x: coordenadas.get(x, [None, None])[0])
      df_mapa['lon'] = df_mapa['DEPARTAMENTO'].map(lambda x: coordenadas.get(x, [None, None])[1])
      
      return df_mapa
  except Exception as e:
      print(f"Error creando dataset del mapa: {str(e)}")
      return pd.DataFrame()

def filtrar_datos(df, departamento=None, año=None):
  """
  Filtra los datos según el departamento y año seleccionados
  """
  try:
      df_filtrado = df.copy()
      
      if departamento and departamento != 'Todos':
          df_filtrado = df_filtrado[df_filtrado['DEPARTAMENTO'] == departamento]
          
      if año and año != 'Todos':
          df_filtrado = df_filtrado[df_filtrado['AÑO'] == año]
      
      return df_filtrado
  except Exception as e:
      print(f"Error en filtrar_datos: {str(e)}")
      return df

# Asegurarse de que estas funciones estén disponibles para importar
__all__ = ['load_data', 'filtrar_datos', 'crear_dataset_mapa']