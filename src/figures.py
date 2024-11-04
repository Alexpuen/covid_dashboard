import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np
import json

def create_map_figure(df_mapa):
  try:
      with open(r'C:\Users\alexa\Music\Trabajos_de_aplicaciones\covid_dashboard\data\colombia.geojson', 'r', encoding='utf-8') as f:
          colombia_geo = json.load(f)
      
      # Separar datos de departamentos regulares y ciudades especiales
      ciudades_especiales = ['BOGOTÁ, D.C.', 'ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA']
      df_departamentos = df_mapa[~df_mapa['DEPARTAMENTO'].isin(ciudades_especiales)]
      df_ciudades = df_mapa[df_mapa['DEPARTAMENTO'].isin(ciudades_especiales)]
      
      # Obtener el rango de valores para la escala de colores
      min_casos = df_mapa['CASOS'].min()
      max_casos = df_mapa['CASOS'].max()
      
      # Crear la escala de colores
      colorscale = 'Reds'
      
      # Función para normalizar valores entre 0 y 1
      def normalize(value):
          return (value - min_casos) / (max_casos - min_casos) if max_casos != min_casos else 0.5
      
      fig = go.Figure()

      # Agregar el choropleth para departamentos
      fig.add_trace(go.Choroplethmapbox(
          geojson=colombia_geo,
          locations=df_departamentos['DEPARTAMENTO'],
          z=df_departamentos['CASOS'],
          featureidkey='properties.NOMBRE_DPT',
          colorscale=colorscale,
          marker=dict(
              line=dict(width=1, color='white')
          ),
          colorbar=dict(
              title="Número de Casos",
              thickness=15,
              len=0.9,
              bgcolor='rgba(255,255,255,0.8)',
              borderwidth=0
          ),
          hovertemplate="<b>%{location}</b><br>" +
                       "Casos: %{z:,.0f}<extra></extra>"
      ))

      # Coordenadas de las ciudades especiales
      coordenadas = {
          'BOGOTÁ, D.C.': {'lat': 4.6097, 'lon': -74.0817},
          'ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA': {'lat': 12.5847, 'lon': -81.7006}
      }

      # Agregar marcadores para cada ciudad especial
      for ciudad in df_ciudades.itertuples():
          coord = coordenadas[ciudad.DEPARTAMENTO]
          # Calcular el color basado en la escala
          normalized_value = normalize(ciudad.CASOS)
          
          # Obtener el color de la escala
          if normalized_value <= 0:
              color = 'rgb(255,235,235)'  # Color más claro para el valor mínimo
          elif normalized_value >= 1:
              color = 'rgb(103,0,13)'     # Color más oscuro para el valor máximo
          else:
              # Interpolación de color para valores intermedios
              color = f'rgba(255,{int(235*(1-normalized_value))},{int(235*(1-normalized_value))},0.7)'
          
          fig.add_trace(go.Scattermapbox(
              lat=[coord['lat']],
              lon=[coord['lon']],
              mode='markers+text',
              marker=dict(
                  size=20,
                  color=color,
                  opacity=0.7
              ),
              text=[ciudad.DEPARTAMENTO],
              textposition="top center",
              hovertemplate=f"<b>{ciudad.DEPARTAMENTO}</b><br>" +
                           f"Casos: {ciudad.CASOS:,}<extra></extra>"
          ))

      # Configurar el layout
      fig.update_layout(
          mapbox=dict(
              style="carto-positron",
              zoom=4.5,
              center=dict(lat=4.5709, lon=-74.2973)
          ),
          paper_bgcolor='white',
          plot_bgcolor='white',
          margin=dict(r=0, t=40, l=0, b=0),
          height=600,
          title="Casos de COVID-19 por Departamento y Ciudades Especiales",
          showlegend=False
      )

      return fig

  except Exception as e:
      print(f"Error en create_map_figure: {str(e)}")
      import traceback
      print(traceback.format_exc())
      return go.Figure()
  
def create_bar_figure(df_municipios):
  """Crea gráfico de barras para top municipios"""
  try:
      # Ordenar los datos de mayor a menor
      df_municipios = df_municipios.sort_values('CASOS', ascending=True)
      
      fig = go.Figure(go.Bar(
          x=df_municipios['CASOS'],
          y=df_municipios['MUNICIPIO'],
          orientation='h',
          marker=dict(
              color=df_municipios['CASOS'],
              colorscale=[
                  [0, '#fff3e0'],  # Color más claro para valores bajos
                  [1, '#8b2204']   # Color más oscuro para valores altos
              ],
              showscale=True,
              colorbar=dict(
                  title="Número<br>de Casos",
                  titleside="right",
                  tickformat=",.0f"
              )
          ),
          text=df_municipios['CASOS'].apply(lambda x: f"{x:,.0f}"),
          textposition='auto',
          textfont=dict(
              color='black',
              size=12
          ),
          hovertemplate="<b>%{y}</b><br>" +
                       "Casos: %{x:,.0f}<br>" +
                       "<extra></extra>"
      ))
      
      # Actualizar el layout
      fig.update_layout(
          title=dict(
              text='Top 5 Municipios con Mayor Número de Casos',
              x=0.5,
              y=0.95,
              xanchor='center',
              yanchor='top',
              font=dict(size=16)
          ),
          xaxis=dict(
              title="",
              showgrid=True,
              gridcolor='rgba(0,0,0,0.1)',
              zeroline=False,
              tickformat=",.0f"
          ),
          yaxis=dict(
              title="",
              showgrid=False,
              zeroline=False
          ),
          plot_bgcolor='white',
          paper_bgcolor='white',
          margin=dict(l=0, r=50, t=50, b=0),
          height=600,
          bargap=0.15,
          showlegend=False
      )
      
      return fig
      
  except Exception as e:
      print(f"Error en create_bar_figure: {str(e)}")
      return go.Figure()

def create_pie_figure(df):
  """Crea gráfico circular de distribución de casos"""
  try:
      if 'COVID-19' not in df.columns:
          return go.Figure()
      
      df_pie = df['COVID-19'].value_counts().reset_index()
      df_pie.columns = ['Tipo', 'Cantidad']
      
      fig = go.Figure(go.Pie(
          labels=df_pie['Tipo'],
          values=df_pie['Cantidad'],
          hole=0.3,
          marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c']
      ))
      
      return update_figure_layout(fig, "Distribución de Casos COVID-19")
  except Exception as e:
      print(f"Error en create_pie_figure: {str(e)}")
      return go.Figure()

def create_line_figure(df):
  """
  Crea un gráfico de línea mostrando el total de casos por mes
  """
  try:
      # Imprimir columnas disponibles para debug
      print("Columnas disponibles:", df.columns.tolist())
      
      # Usar la columna de fecha correcta (ajusta según el nombre real en tu DataFrame)
      fecha_col = 'FECHA_REPORTE'  # o el nombre que tenga en tu DataFrame
      
      # Verificar si hay datos
      if df.empty:
          print("DataFrame vacío en create_line_figure")
          return go.Figure()

      # Asegurarse de que la fecha está en formato datetime
      df[fecha_col] = pd.to_datetime(df[fecha_col])
      
      # Agrupar por mes y sumar casos
      df_mensual = df.groupby(pd.Grouper(key=fecha_col, freq='M'))['CASOS'].sum().reset_index()
      
      # Formatear las fechas para el eje x
      df_mensual['Mes'] = df_mensual[fecha_col].dt.strftime('%Y-%m')
      
      # Crear la figura
      fig = go.Figure()
      
      fig.add_trace(go.Scatter(
          x=df_mensual['Mes'],
          y=df_mensual['CASOS'],
          mode='lines+markers',
          name='Casos',
          line=dict(color='#E63946', width=2),
          marker=dict(
              size=8,
              color='#E63946',
              symbol='circle'
          ),
          hovertemplate="<b>%{x}</b><br>" +
                       "Casos: %{y:,.0f}<extra></extra>"
      ))
      
      # Actualizar el layout
      fig.update_layout(
          title={
              'text': 'Total de Casos COVID-19 por Mes',
              'y': 0.95,
              'x': 0.5,
              'xanchor': 'center',
              'yanchor': 'top'
          },
          xaxis_title='Mes',
          yaxis_title='Número de Casos',
          paper_bgcolor='white',
          plot_bgcolor='white',
          height=400,
          margin=dict(l=60, r=30, t=80, b=60),
          xaxis=dict(
              showgrid=True,
              gridcolor='rgba(0,0,0,0.1)',
              tickangle=45
          ),
          yaxis=dict(
              showgrid=True,
              gridcolor='rgba(0,0,0,0.1)',
              zeroline=False
          ),
          showlegend=False
      )
      
      return fig
  
  except Exception as e:
      print(f"Error en create_line_figure: {str(e)}")
      import traceback
      print(traceback.format_exc())
      return go.Figure()

def create_histogram_figure(df):
  """Crea histograma de edades"""
  try:
      def limpiar_edad(edad):
          try:
              if pd.isna(edad):
                  return None
              return float(str(edad).split('(')[0].strip())
          except:
              return None

      df['EDAD_LIMPIA'] = df['EDAD FALLECIDO'].apply(limpiar_edad)
      
      bins = [0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 89, float('inf')]
      labels = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
               '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', 
               '75-79', '80-84', '85-89', '90+']
      
      df['RANGO_EDAD'] = pd.cut(df['EDAD_LIMPIA'], bins=bins, labels=labels, right=False)
      df_edades = df.groupby('RANGO_EDAD', observed=True).size().reset_index(name='CASOS')
      
      fig = go.Figure(go.Bar(
          x=df_edades['RANGO_EDAD'].astype(str),
          y=df_edades['CASOS'],
          marker_color='rgb(55, 83, 109)',
          marker=dict(
              line=dict(color='rgb(8,48,107)', width=1.5)
          )
      ))
      
      return update_figure_layout(fig, 'Distribución de Casos por Rango de Edad')
  except Exception as e:
      print(f"Error en create_histogram_figure: {str(e)}")
      return go.Figure()

def create_line_figure(df):
  """
  Crea un gráfico de línea mostrando el total de casos por mes
  """
  try:
      # Verificar si hay datos
      if df.empty:
          print("DataFrame vacío en create_line_figure")
          return go.Figure()

      # Asegurarse de que la fecha está en formato datetime
      df['FECHA DEFUNCIÓN'] = pd.to_datetime(df['FECHA DEFUNCIÓN'], format="'%d/%m/%Y")
      
      # Agrupar por mes y contar casos
      df_mensual = df.groupby(pd.Grouper(key='FECHA DEFUNCIÓN', freq='M')).size().reset_index()
      df_mensual.columns = ['FECHA', 'CASOS']
      
      # Formatear las fechas para el eje x
      df_mensual['Mes'] = df_mensual['FECHA'].dt.strftime('%Y-%m')
      
      # Crear la figura
      fig = go.Figure()
      
      fig.add_trace(go.Scatter(
          x=df_mensual['Mes'],
          y=df_mensual['CASOS'],
          mode='lines+markers',
          name='Casos',
          line=dict(color='#E63946', width=2),
          marker=dict(
              size=8,
              color='#E63946',
              symbol='circle'
          ),
          hovertemplate="<b>%{x}</b><br>" +
                       "Fallecimientos: %{y:,.0f}<extra></extra>"
      ))
      
      # Actualizar el layout
      fig.update_layout(
          title={
              'text': 'Total de Fallecimientos COVID-19 por Mes',
              'y': 0.95,
              'x': 0.5,
              'xanchor': 'center',
              'yanchor': 'top'
          },
          xaxis_title='Mes',
          yaxis_title='Número de Fallecimientos',
          paper_bgcolor='white',
          plot_bgcolor='white',
          height=500,
          margin=dict(l=60, r=30, t=80, b=60),
          xaxis=dict(
              showgrid=True,
              gridcolor='rgba(0,0,0,0.1)',
              tickangle=45,
              tickmode='array',
              ticktext=df_mensual['Mes'],
              tickvals=df_mensual['Mes']
          ),
          yaxis=dict(
              showgrid=True,
              gridcolor='rgba(0,0,0,0.1)',
              zeroline=False
          ),
          showlegend=False
      )
      
      return fig
  
  except Exception as e:
      print(f"Error en create_line_figure: {str(e)}")
      import traceback
      print(traceback.format_exc())
      return go.Figure()

def update_figure_layout(fig, title, height=500):
  """Actualiza el layout común para todas las figuras"""
  fig.update_layout(
      title=dict(
          text=title,
          x=0.5,
          y=0.95,
          xanchor='center',
          yanchor='top',
          font=dict(size=20)
      ),
      paper_bgcolor='white',
      plot_bgcolor='white',
      height=height,
      font=dict(family='Arial', size=12),
      margin=dict(l=50, r=50, t=80, b=50),
      template='plotly_white',
      xaxis=dict(
          showgrid=True,
          gridwidth=1,
          gridcolor='lightgray',
          tickangle=45,
          title_font=dict(size=14),
          tickfont=dict(size=12)
      ),
      yaxis=dict(
          showgrid=True,
          gridwidth=1,
          gridcolor='lightgray',
          title_font=dict(size=14),
          tickfont=dict(size=12)
      )
  )
  return fig