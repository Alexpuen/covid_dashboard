from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout(df, df_mapa):
  return html.Div([

    # Header
      html.Header([
          html.Div([
              html.H1("Dashboard COVID-19 Colombia", className='dashboard-title'),
              html.Div([
                  html.A("Mapa", href="#map-graph", className='nav-button'),
                  html.A("Top Municipios", href="#bar-graph", className='nav-button'),
                  html.A("Distribución", href="#pie-graph", className='nav-button'),
                  html.A("Edades", href="#histogram-graph", className='nav-button'),
                  html.A("Línea Temporal", href="#line-graph", className='nav-button'),
              ], className='nav-buttons')
          ], className='header-content')
      ], className='dashboard-header'),



      html.Div([
          # Filtros
          html.Div([
              dbc.Row([
                  dbc.Col([
                      html.Label("Departamento:", className='filter-label'),
                      dcc.Dropdown(id='department-dropdown',
                          options=[{'label': 'Todos', 'value': 'Todos'}] +
                                  [{'label': dept, 'value': dept} for dept in sorted(df['DEPARTAMENTO'].unique())],
                          value='Todos',
                          clearable=False
                      )
                  ], md=6),
                  dbc.Col([
                      html.Label("Año:", className='filter-label'),
                      dcc.Dropdown(id='year-dropdown',
                          options=[{'label': 'Todos', 'value': 'Todos'}] +
                                  [{'label': str(año), 'value': año} for año in sorted(df['AÑO'].unique())],
                          value='Todos',
                          clearable=False
                      )
                  ], md=6)
              ])
          ], className='filters-container'),
          
          # Grid de gráficos
          html.Div([
              html.Div([
                  html.H3("Casos por Departamento", className='graph-title'),
                  html.Div([
                      dcc.Graph(id='map-graph')
                  ], className='plotly-graph-wrapper')
              ], className='graph-container'),
              
              html.Div([
                  html.H3("Top 5 Municipios", className='graph-title'),
                  html.Div([
                      dcc.Graph(id='bar-graph')
                  ], className='plotly-graph-wrapper')
              ], className='graph-container'),
              
              html.Div([
                  html.H3("Distribución de Casos", className='graph-title'),
                  html.Div([
                      dcc.Graph(id='pie-graph')
                  ], className='plotly-graph-wrapper')
              ], className='graph-container'),
              
              html.Div([
                  html.H3("Distribución por Edad", className='graph-title'),
                  html.Div([
                      dcc.Graph(id='histogram-graph')
                  ], className='plotly-graph-wrapper')
              ], className='graph-container'),
          ], className='dashboard-grid'),
          
          html.Div([
              html.H3("Total de Fallecimientos por Mes", className='graph-title'),
              html.Div([
                  dcc.Graph(id='line-graph')
              ], className='plotly-graph-wrapper')
          ], className='graph-container'),
          
      ], className='container-fluid'),

            # Footer
      html.Footer([
          html.Div([
              html.P([
                  "Creado por Alex Puentes",
                  html.Br(),
                  "Maestría en Inteligencia Artificial",
                  html.Br(),
                  "Universidad de La Salle"
              ], className='footer-text'),
              html.P("© 2024 Todos los derechos reservados", className='copyright')
          ], className='footer-content')
      ], className='dashboard-footer')
  ])
