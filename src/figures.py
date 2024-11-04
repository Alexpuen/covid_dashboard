import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

def create_map_figure(df_mapa):
  """Crea un mapa de Colombia con casos COVID-19 por departamento"""
  try:
      # Crear figura
      fig = go.Figure()

      # Agregar puntos al mapa
      fig.add_trace(go.Scattergeo(
          lon=df_mapa['lon'],
          lat=df_mapa['lat'],
          text=df_mapa['DEPARTAMENTO'],
          mode='markers+text',
          marker=dict(
              size=df_mapa['CASOS'].apply(lambda x: max(5, min(50, x/1000))),
              color=df_mapa['CASOS'],
              colorscale='Reds',
              showscale=True,
              colorbar_title="Casos",
              sizemode='area'
          ),
          textposition="bottom center",
          hovertemplate="<b>%{text}</b><br>" +
                       "Casos: %{marker.color:,.0f}<br>" +
                       "<extra></extra>"
      ))

      # Configurar el mapa
      fig.update_geos(
          visible=True,
          resolution=50,
          scope="south america",
          showcountries=True,
          countrycolor="Black",
          showland=True,
          landcolor="lightgray",
          showocean=True,
          oceancolor="LightBlue",
          center=dict(lat=4.5709, lon=-74.2973),
          lataxis_range=[-4, 13],
          lonaxis_range=[-82, -67]
      )

      fig.update_layout(
          margin={"r":0,"t":30,"l":0,"b":0},
          height=600,
          showlegend=False,
          title=dict(
              text="Casos de COVID-19 por Departamento",
              x=0.5,
              y=0.95
          )
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
      fig = go.Figure(go.Bar(
          x=df_municipios['CASOS'],
          y=df_municipios['MUNICIPIO'],
          orientation='h',
          marker=dict(
              color=df_municipios['CASOS'],
              colorscale='Oranges',
              showscale=True
          ),
          text=df_municipios['CASOS'],
          textposition='auto',
      ))
      
      return update_figure_layout(
          fig, 
          'Top 5 Municipios con Mayor Número de Casos',
          500
      )
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

def create_line_figure(df_muertes_mensuales):
  """Crea gráfico de línea temporal"""
  try:
      fig = go.Figure(go.Scatter(
          x=df_muertes_mensuales['FECHA'],
          y=df_muertes_mensuales['CASOS'],
          mode='lines+markers',
          line=dict(width=3, color='#2ecc71'),
          marker=dict(size=8),
          hovertemplate="<b>Fecha: %{x|%B %Y}</b><br>Casos: %{y:,.0f}<br><extra></extra>"
      ))
      
      fig.update_layout(
          xaxis=dict(
              tickformat="%B %Y",
              tickangle=45
          )
      )
      
      return update_figure_layout(fig, 'Evolución Temporal de Casos de COVID-19')
  except Exception as e:
      print(f"Error en create_line_figure: {str(e)}")
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