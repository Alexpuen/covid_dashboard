import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np
import json

def create_map_figure(df_mapa):
  """
  Generates choropleth map visualization with special handling for major cities
  
  Implements:
  - Department-level choropleth mapping
  - Special markers for Bogotá and San Andrés
  - Dynamic color scaling based on case counts
  """
  try:
      with open(r'C:\Users\alexa\Music\Trabajos_de_aplicaciones\covid_dashboard\data\colombia.geojson', 'r', encoding='utf-8') as f:
          colombia_geo = json.load(f)
      
      ciudades_especiales = ['BOGOTÁ, D.C.', 'ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA']
      df_departamentos = df_mapa[~df_mapa['DEPARTAMENTO'].isin(ciudades_especiales)]
      df_ciudades = df_mapa[df_mapa['DEPARTAMENTO'].isin(ciudades_especiales)]
      
      min_casos = df_mapa['CASOS'].min()
      max_casos = df_mapa['CASOS'].max()
      
      def normalize(value):
          return (value - min_casos) / (max_casos - min_casos) if max_casos != min_casos else 0.5
      
      fig = go.Figure()

      # Department choropleth layer
      fig.add_trace(go.Choroplethmapbox(
          geojson=colombia_geo,
          locations=df_departamentos['DEPARTAMENTO'],
          z=df_departamentos['CASOS'],
          featureidkey='properties.NOMBRE_DPT',
          colorscale='Reds',
          marker=dict(line=dict(width=1, color='white')),
          colorbar=dict(
              title="Número de Casos",
              thickness=15,
              len=0.9,
              bgcolor='rgba(255,255,255,0.8)',
              borderwidth=0
          ),
          hovertemplate="<b>%{location}</b><br>Casos: %{z:,.0f}<extra></extra>"
      ))

      # Special cities coordinates mapping
      coordenadas = {
          'BOGOTÁ, D.C.': {'lat': 4.6097, 'lon': -74.0817},
          'ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA': {'lat': 12.5847, 'lon': -81.7006}
      }

      # Special cities markers
      for ciudad in df_ciudades.itertuples():
          coord = coordenadas[ciudad.DEPARTAMENTO]
          normalized_value = normalize(ciudad.CASOS)
          
          color = ('rgb(255,235,235)' if normalized_value <= 0 else
                  'rgb(103,0,13)' if normalized_value >= 1 else
                  f'rgba(255,{int(235*(1-normalized_value))},{int(235*(1-normalized_value))},0.7)')
          
          fig.add_trace(go.Scattermapbox(
              lat=[coord['lat']],
              lon=[coord['lon']],
              mode='markers+text',
              marker=dict(size=20, color=color, opacity=0.7),
              text=[ciudad.DEPARTAMENTO],
              textposition="top center",
              hovertemplate=f"<b>{ciudad.DEPARTAMENTO}</b><br>Casos: {ciudad.CASOS:,}<extra></extra>"
          ))

      # Map layout configuration
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
      print(f"Map visualization generation failed: {str(e)}")
      import traceback
      print(traceback.format_exc())
      return go.Figure()

def create_bar_figure(df_municipios):
  """
  Generates horizontal bar chart for top municipalities
  
  Features:
  - Dynamic color scaling
  - Automatic text positioning
  - Custom hover information
  """
  try:
      df_municipios = df_municipios.sort_values('CASOS', ascending=True)
      
      fig = go.Figure(go.Bar(
          x=df_municipios['CASOS'],
          y=df_municipios['MUNICIPIO'],
          orientation='h',
          marker=dict(
              color=df_municipios['CASOS'],
              colorscale=[[0, '#fff3e0'], [1, '#8b2204']],
              showscale=True,
              colorbar=dict(
                  title="Número<br>de Casos",
                  titleside="right",
                  tickformat=",.0f"
              )
          ),
          text=df_municipios['CASOS'].apply(lambda x: f"{x:,.0f}"),
          textposition='auto',
          textfont=dict(color='black', size=12),
          hovertemplate="<b>%{y}</b><br>Casos: %{x:,.0f}<extra></extra>"
      ))
      
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
      print(f"Bar chart generation failed: {str(e)}")
      return go.Figure()

def create_pie_figure(df):
  """
  Generates donut chart for COVID-19 case distribution
  
  Features:
  - Central hole design
  - Custom color scheme
  - Standardized layout
  """
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
      print(f"Pie chart generation failed: {str(e)}")
      return go.Figure()

def create_histogram_figure(df):
  """
  Generates age distribution histogram with custom binning
  
  Features:
  - Age range categorization
  - Custom bin intervals
  - Standardized styling
  """
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
      print(f"Histogram generation failed: {str(e)}")
      return go.Figure()

def create_line_figure(df):
  """
  Generates temporal evolution visualization of COVID-19 cases
  
  Features:
  - Monthly aggregation
  - Interactive hover information
  - Custom styling for clarity
  """
  try:
      if df.empty:
          return go.Figure()

      df['FECHA DEFUNCIÓN'] = pd.to_datetime(df['FECHA DEFUNCIÓN'], format="'%d/%m/%Y")
      df_mensual = df.groupby(pd.Grouper(key='FECHA DEFUNCIÓN', freq='ME')).size().reset_index()  # Corrección del warning
      df_mensual.columns = ['FECHA', 'CASOS']
      
      df_mensual['Mes'] = df_mensual['FECHA'].dt.strftime('%Y-%m')
      
      fig = go.Figure(go.Scatter(
          x=df_mensual['Mes'],
          y=df_mensual['CASOS'],
          mode='lines+markers',
          name='Casos',
          line=dict(color='#E63946', width=2),
          marker=dict(size=8, color='#E63946', symbol='circle'),
          hovertemplate="<b>%{x}</b><br>Fallecimientos: %{y:,.0f}<extra></extra>"
      ))
      
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
      print(f"Time series visualization failed: {str(e)}")
      import traceback
      print(traceback.format_exc())
      return go.Figure()

def update_figure_layout(fig, title, height=500):
  """
  Applies standardized layout configuration to visualization figures
  
  Parameters:
      fig: Plotly figure object
      title: Chart title
      height: Figure height in pixels
  """
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