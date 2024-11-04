from dash import Dash
import dash_bootstrap_components as dbc
from src.layouts import create_layout
from src.callbacks import register_callbacks
from src.data_processing import load_data

def create_app():
  try:
      print("Iniciando aplicación...")
      
      # Cargar datos
      print("Cargando datos...")
      df, df_mapa = load_data()  # Volvemos a 2 valores
      
      if df is None or df_mapa is None:
          raise Exception("Error al cargar los datos")
      
      # Crear aplicación
      app = Dash(__name__, 
                 external_stylesheets=[dbc.themes.BOOTSTRAP],
                 suppress_callback_exceptions=True)
      
      print("Creando layout...")
      app.layout = create_layout(df, df_mapa)
      
      print("Registrando callbacks...")
      register_callbacks(app, df, df_mapa)  # Eliminado geojson
      
      return app

  except Exception as e:
      print(f"Error creando app: {str(e)}")
      import traceback
      print(traceback.format_exc())
      return None

if __name__ == '__main__':
  app = create_app()
  if app:
      print("Iniciando servidor...")
      app.run_server(debug=True, port=8050)
  else:
      print("Error: No se pudo crear la aplicación")