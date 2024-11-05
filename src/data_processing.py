import pandas as pd
import os
from pathlib import Path

def get_project_root():
  """Resolves and returns the project's root directory path"""
  return Path(__file__).parent.parent

def normalizar_nombre_departamento(nombre):
  """Standardizes department names by resolving naming variations and inconsistencies"""

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
 
  """Extracts and validates the numeric age value from complex string formats"""
  try:
      if pd.isna(edad):
          return None
      edad_str = str(edad)
      return int(edad_str.split('(')[0])
  except:
      return None

def load_data():
  
  """
  Core data processing pipeline for COVID-19 dataset
  
  Handles data loading, cleaning, and transformation stages including:
  - Date formatting and temporal feature extraction
  - Geographic data standardization
  - Age data processing
  - Case counting aggregation
  """
  try:
      print("Loading data...")
      root_dir = get_project_root()
      print(f"Root directory: {root_dir}")
      
      ruta_excel = os.path.join(root_dir, 'data', 'datos_covid.xlsx')
      print(f"Looking for file at: {ruta_excel}")
      
      if not os.path.exists(ruta_excel):
          print(f"ERROR: File not found at {ruta_excel}")
          return None, None
          
      # Load dataset
      df = pd.read_excel(ruta_excel)
      print("Datos cargados exitosamente")
      
      # Data transformation pipeline
      df['DEPARTAMENTO'] = df['DEPARTAMENTO'].apply(normalizar_nombre_departamento)
      df['CASOS'] = 1
      df['EDAD'] = df['EDAD FALLECIDO'].apply(procesar_edad)
      
      # Temporal features extraction
      for col in ['FECHA DEFUNCIÓN', 'FECHA REGISTRO']:
          if col in df.columns:
              df[col] = pd.to_datetime(df[col].astype(str).str.strip("'"), 
                                     format='%d/%m/%Y', 
                                     errors='coerce')
      
      if 'FECHA DEFUNCIÓN' in df.columns:
          df['AÑO'] = df['FECHA DEFUNCIÓN'].dt.year
          df['MES'] = df['FECHA DEFUNCIÓN'].dt.month
      
      df_mapa = crear_dataset_mapa(df)
      
      print("Processing pipeline completed")
      return df, df_mapa
      
  except Exception as e:
      print(f"Pipeline execution failed: {str(e)}")
      import traceback
      print(traceback.format_exc())
      return None, None

def crear_dataset_mapa(df):
  
  """
  Generates geographical visualization dataset with department-level aggregations
  and corresponding coordinate mappings for spatial representation
  """

  try:
      df_mapa = df.groupby('DEPARTAMENTO', as_index=False).agg({
          'CASOS': 'sum'
      })
      
      # Geographic coordinate reference system
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
      print(f"Geographic data processing failed: {str(e)}")
      return pd.DataFrame()

def filtrar_datos(df, departamento=None, año=None):
  """
  Applies conditional filtering to the dataset based on geographic and temporal parameters
  
  Parameters:
      df: Primary DataFrame
      departamento: Geographic filter criterion
      año: Temporal filter criterion
  """
  try:
      df_filtrado = df.copy()
      
      if departamento and departamento != 'Todos':
          df_filtrado = df_filtrado[df_filtrado['DEPARTAMENTO'] == departamento]
          
      if año and año != 'Todos':
          df_filtrado = df_filtrado[df_filtrado['AÑO'] == año]
      
      return df_filtrado
  except Exception as e:
      print(f"Filter application failed: {str(e)}")
      return df

# Module exports
__all__ = ['load_data', 'filtrar_datos', 'crear_dataset_mapa']