from dash.dependencies import Input, Output
from .figures import (
  create_map_figure,
  create_bar_figure,
  create_pie_figure,
  create_histogram_figure,
  create_line_figure
)
from .data_processing import filtrar_datos

def register_callbacks(app, df, df_mapa):
  """
  Establishes interactive visualization updates based on user filter selections
  
  Implements reactive callbacks for:
  - Geographic distribution map
  - Top municipalities bar chart
  - Case distribution pie chart
  - Age distribution histogram
  - Temporal evolution line chart
  """
  
  @app.callback(
      Output('map-graph', 'figure'),
      [Input('department-dropdown', 'value'),
       Input('year-dropdown', 'value')]
  )
  def update_map(selected_dept, selected_year):
      """Geographic distribution visualization handler"""
      try:
          # Primary dataset filtering
          filtered_df = df.copy()
          if selected_year != 'Todos':
              filtered_df = filtered_df[filtered_df['AÑO'] == selected_year]
          
          # Geographic aggregation
          df_mapa_filtered = filtered_df.groupby('DEPARTAMENTO', as_index=False)['CASOS'].sum()
          
          if selected_dept != 'Todos':
              df_mapa_filtered = df_mapa_filtered[df_mapa_filtered['DEPARTAMENTO'] == selected_dept]
          
          return create_map_figure(df_mapa_filtered)
      except Exception as e:
          print(f"Map visualization failed: {str(e)}")
          import traceback
          print(traceback.format_exc())
          return {}

  @app.callback(
      Output('bar-graph', 'figure'),
      [Input('department-dropdown', 'value'),
       Input('year-dropdown', 'value')]
  )
  def update_bar(selected_dept, selected_year):
      """Top municipalities visualization handler"""
      try:
          filtered_df = filtrar_datos(df, selected_dept, selected_year)
          
          # Municipality-level aggregation
          df_municipios = filtered_df.groupby('MUNICIPIO', as_index=False).agg({
              'CASOS': 'sum'
          }).sort_values('CASOS', ascending=True).tail(5)
          
          return create_bar_figure(df_municipios)
      except Exception as e:
          print(f"Bar chart generation failed: {str(e)}")
          import traceback
          print(traceback.format_exc())
          return {}

  @app.callback(
      Output('pie-graph', 'figure'),
      [Input('department-dropdown', 'value'),
       Input('year-dropdown', 'value')]
  )
  def update_pie(selected_dept, selected_year):
      """Case distribution visualization handler"""
      try:
          filtered_df = filtrar_datos(df, selected_dept, selected_year)
          return create_pie_figure(filtered_df)
      except Exception as e:
          print(f"Pie chart generation failed: {str(e)}")
          import traceback
          print(traceback.format_exc())
          return {}

  @app.callback(
      Output('line-graph', 'figure'),
      [Input('department-dropdown', 'value'),
       Input('year-dropdown', 'value')]
  )
  def update_line(selected_dept, selected_year):
      """Temporal evolution visualization handler"""
      try:
          filtered_df = filtrar_datos(df, selected_dept, selected_year)
          return create_line_figure(filtered_df)
      except Exception as e:
          print(f"Time series visualization failed: {str(e)}")
          import traceback
          print(traceback.format_exc())
          return {}

  @app.callback(
      Output('histogram-graph', 'figure'),
      [Input('department-dropdown', 'value'),
       Input('year-dropdown', 'value')]
  )
  def update_histogram(selected_dept, selected_year):
      """Age distribution visualization handler"""
      try:
          filtered_df = filtrar_datos(df, selected_dept, selected_year)
          return create_histogram_figure(filtered_df)
      except Exception as e:
          print(f"Histogram generation failed: {str(e)}")
          import traceback
          print(traceback.format_exc())
          return {}