# Dashboard COVID-19 Colombia

## Descripción
Dashboard interactivo para la visualización y análisis de datos de COVID-19 en Colombia, desarrollado como parte del trabajo de Maestría en Inteligencia Artificial de la Universidad de La Salle. Esta herramienta, construida con Python, Dash y Plotly, permite explorar la distribución geográfica de casos, tendencias temporales y estadísticas demográficas.

## Características
- 🗺️ Mapa coroplético interactivo de casos por departamento
- 📊 Visualización de top 5 municipios más afectados
- 🥧 Distribución de casos por tipo
- 📈 Evolución temporal de casos
- 📉 Distribución por rangos de edad
- 🔍 Filtros dinámicos por departamento y año

## Tecnologías Utilizadas
- Python 3.8+
- Dash 2.x
- Plotly 5.x
- Pandas
- NumPy

## Estructura del Proyecto
covid_dashboard/
├── data/
│   ├── datos_covid.xlsx
│   └── colombia.geojson
├── src/
│   ├── init.py
│   ├── main.py
│   ├── layouts.py
│   ├── callbacks.py
│   ├── figures.py
│   ├── data_processing.py
│   └── utils.py
├── assets/
│   └── styles.css
├── requirements.txt
└── README.md

bash
python src/main.py

3. Abrir el navegador en `http://localhost:8050`

## Datos
El dashboard utiliza datos oficiales de COVID-19 en Colombia, incluyendo:
- Casos confirmados
- Distribución geográfica
- Información demográfica
- Series temporales

## Autor
Alex Puentes
- GitHub: [@kAIto](https://github.com/Alexpuen)
- LinkedIn: [Alex Puentes](https://www.linkedin.com/in/alex-puentes-7973ab141/)

## Contexto Académico
Este proyecto fue desarrollado como parte de la Maestría en Inteligencia Artificial de la Universidad de La Salle, Colombia. Representa una aplicación práctica de técnicas de visualización de datos y desarrollo web para el análisis de información epidemiológica.

## Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

