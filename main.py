from dash import Dash
import dash_bootstrap_components as dbc
from src.layouts import create_layout
from src.callbacks import register_callbacks
from src.data_processing import load_data

def create_app():
  
  try:
      # Initialize application setup
      print("Initializing application setup")
      
      # Initialize data processing pipeline
      print("Loading and processing data sources")
      df, df_mapa = load_data()
      
      # Validate data integrity
      if df is None or df_mapa is None:
          raise Exception("Error al cargar los datos")
      
      # Configure Dash instance with Bootstrap integration
      app = Dash(__name__, 
                 external_stylesheets=[dbc.themes.BOOTSTRAP],
                 suppress_callback_exceptions=True)
      

      # Initialize dashboard layout
      print("Configuring dashboard layout")
      app.layout = create_layout(df, df_mapa)
      
      # Configure interactive callbacks
      print("Registering interactive callbacks")
      register_callbacks(app, df, df_mapa)  # Eliminado geojson
      
      return app

  except Exception as e:
      print(f"Application initialization failed: {str(e)}")
      import traceback
      print(traceback.format_exc())
      return None

if __name__ == '__main__':
  # Initialize dashboard application
  app = create_app()
  if app:
      print("Initializing development server")
      app.run_server(debug=True, port=8050)
  else:
      print("Application initialization failed")