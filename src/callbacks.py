# src/callbacks.py
from dash.dependencies import Input, Output
from .figures import (
  create_map_figure,
  create_bar_figure,
  create_pie_figure,
  create_histogram_figure
)
from .data_processing import filtrar_datos

def register_callbacks(app, df, df_mapa):
  """Registra todos los callbacks de la aplicación"""
  
  # Callback para el mapa
  @app.callback(
      Output('map-graph', 'figure'),
      [Input('department-dropdown', 'value'),
       Input('year-dropdown', 'value')]
  )
  def update_map(selected_dept, selected_year):
      print(f"Actualizando mapa: dept={selected_dept}, year={selected_year}")
      try:
          # Para el mapa, filtramos df_mapa directamente
          filtered_df = df_mapa
          if selected_dept != 'Todos':
              filtered_df = filtered_df[filtered_df['DEPARTAMENTO'] == selected_dept]
          
          fig = create_map_figure(filtered_df)
          print("Mapa actualizado exitosamente")
          return fig
      except Exception as e:
          print(f"Error actualizando mapa: {str(e)}")
          import traceback
          print(traceback.format_exc())
          return {}

  # Callback para el gráfico de barras
  @app.callback(
      Output('bar-graph', 'figure'),
      [Input('department-dropdown', 'value'),
       Input('year-dropdown', 'value')]
  )
  def update_bar(selected_dept, selected_year):
      print(f"Actualizando gráfico de barras: dept={selected_dept}, year={selected_year}")
      try:
          filtered_df = filtrar_datos(df, selected_dept, selected_year)
          
          # Agrupar por municipio y contar casos
          df_municipios = filtered_df.groupby('MUNICIPIO', as_index=False).agg({
              'CASOS': 'sum'
          }).sort_values('CASOS', ascending=True).tail(5)
          
          fig = create_bar_figure(df_municipios)
          print("Gráfico de barras actualizado exitosamente")
          return fig
      except Exception as e:
          print(f"Error actualizando gráfico de barras: {str(e)}")
          import traceback
          print(traceback.format_exc())
          return {}

  # Callback para el gráfico de pie
  @app.callback(
      Output('pie-graph', 'figure'),
      [Input('department-dropdown', 'value'),
       Input('year-dropdown', 'value')]
  )
  def update_pie(selected_dept, selected_year):
      print(f"Actualizando gráfico de pie: dept={selected_dept}, year={selected_year}")
      try:
          filtered_df = filtrar_datos(df, selected_dept, selected_year)
          fig = create_pie_figure(filtered_df)
          print("Gráfico de pie actualizado exitosamente")
          return fig
      except Exception as e:
          print(f"Error actualizando gráfico de pie: {str(e)}")
          import traceback
          print(traceback.format_exc())
          return {}

  # Callback para el histograma
  @app.callback(
      Output('histogram-graph', 'figure'),
      [Input('department-dropdown', 'value'),
       Input('year-dropdown', 'value')]
  )
  def update_histogram(selected_dept, selected_year):
      print(f"Actualizando histograma: dept={selected_dept}, year={selected_year}")
      try:
          filtered_df = filtrar_datos(df, selected_dept, selected_year)
          fig = create_histogram_figure(filtered_df)
          print("Histograma actualizado exitosamente")
          return fig
      except Exception as e:
          print(f"Error actualizando histograma: {str(e)}")
          import traceback
          print(traceback.format_exc())
          return {}