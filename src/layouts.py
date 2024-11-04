from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout(df, df_mapa):
  """Crea el layout principal de la aplicación"""
  try:
      # Obtener valores únicos para los dropdowns
      años_disponibles = sorted(df['AÑO'].unique())
      departamentos = sorted(df['DEPARTAMENTO'].unique())

      return html.Div([
          # Header con estilo mejorado
          html.Header([
              html.H1("Dashboard COVID-19 Colombia", 
                      className='dashboard-title text-center py-3')
          ], className='header mb-4'),
          
          # Contenedor de filtros
          html.Div([
              dbc.Row([
                  # Dropdown de Departamento
                  dbc.Col([
                      html.Label("Departamento:", className='mb-2'),
                      dcc.Dropdown(
                          id='department-dropdown',
                          options=[{'label': 'Todos', 'value': 'Todos'}] +
                                  [{'label': dept, 'value': dept} for dept in departamentos],
                          value='Todos',
                          clearable=False
                      )
                  ], width=6),
                  
                  # Dropdown de Año
                  dbc.Col([
                      html.Label("Año:", className='mb-2'),
                      dcc.Dropdown(
                          id='year-dropdown',
                          options=[{'label': 'Todos', 'value': 'Todos'}] +
                                  [{'label': str(año), 'value': año} for año in años_disponibles],
                          value='Todos',
                          clearable=False
                      )
                  ], width=6)
              ], className='mb-4')
          ], className='filters-container px-4'),
          
          # Contenedor de gráficas
          html.Div([
              # Primera fila: Mapa y Gráfico de Barras
              dbc.Row([
                  dbc.Col([
                      dcc.Loading(
                          id="loading-map",
                          type="default",
                          children=dcc.Graph(
                              id='map-graph',
                              style={'height': '500px'}
                          )
                      )
                  ], width=6),
                  
                  dbc.Col([
                      dcc.Loading(
                          id="loading-bar",
                          type="default",
                          children=dcc.Graph(
                              id='bar-graph',
                              style={'height': '500px'}
                          )
                      )
                  ], width=6)
              ], className='mb-4'),
              
              # Segunda fila: Gráfico de Pie e Histograma
              dbc.Row([
                  dbc.Col([
                      dcc.Loading(
                          id="loading-pie",
                          type="default",
                          children=dcc.Graph(
                              id='pie-graph',
                              style={'height': '500px'}
                          )
                      )
                  ], width=6),
                  
                  dbc.Col([
                      dcc.Loading(
                          id="loading-histogram",
                          type="default",
                          children=dcc.Graph(
                              id='histogram-graph',
                              style={'height': '500px'}
                          )
                      )
                  ], width=6)
              ])
          ], className='graphs-container px-4')
      ])

  except Exception as e:
      print(f"Error creando layout: {str(e)}")
      import traceback
      print(traceback.format_exc())
      return html.Div("Error al cargar el dashboard")