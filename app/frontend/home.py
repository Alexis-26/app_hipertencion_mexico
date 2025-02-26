import flet as ft
import plotly.graph_objects as go
import io
import base64
import random
import requests
import pandas as pd
# https://datoshipertencionmexico.up.railway.app/consulta?columnas=edad,sexo

# Función para realizar la consulta a la API
def consulta(columnas):
    if columnas:
        url = f"https://datoshipertencionmexico.up.railway.app/consulta?columnas={columnas}"
        response = requests.get(url)
        if response.status_code == 200:
            return pd.read_json(response.text)
        else:
            return pd.DataFrame()

def obtener_porcentajes_hipertension_sexo(df):
    """Calcula y muestra los porcentajes exactos de hipertensión por sexo."""
    hipertension_por_sexo = df.groupby('sexo')['riesgo_hipertension'].value_counts(normalize=True).unstack()

    print("Porcentajes de Hipertensión por Sexo:")
    for sexo in hipertension_por_sexo.index:
        print(f"\nSexo: {sexo}")
        for riesgo in hipertension_por_sexo.columns:
            porcentaje = hipertension_por_sexo.loc[sexo, riesgo] * 100
            print(f"  Hipertensión: {riesgo} - {porcentaje:.2f}%")

    #funcion para comvertir imagenes png a base64
def generate_image(fig):
    buffer = io.BytesIO()
    fig.write_image(buffer, format="png")
    buffer.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buffer.read()).decode()}"

    #funcion para convetir imagenes locales
def load_local_image(image_path):
    """Carga una imagen local y la convierte a base64."""
    with open(image_path, "rb") as image_file:
        return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"

def crear_grafico(fig, title, xaxis_title=None, yaxis_title=None):
    """Aplica el diseño unificado a un gráfico de Plotly."""
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        paper_bgcolor="#505458",
        font=dict(color="white"),
        legend=dict(
            x=1.05,
            y=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )
    )
    return fig

def home(page: ft.Page):
    page.bgcolor = "#303030"  # Fondo oscuro
    page.appbar = ft.AppBar(
        title=ft.Text("Hipertensión en México", color="white", size=30, weight=ft.FontWeight.BOLD),
        bgcolor="#EE0E51", center_title=True
    )
    page.scroll = ft.ScrollMode.AUTO
    
    # Realiza la consulta a la API
    df = consulta("edad,sexo,masa_corporal,valor_hemoglobina_glucosilada,riesgo_hipertension")

    # Datos de ejemplo para el alexis
    years = [f"{i}" for i in range(2017, 2023)]
    categories = ["A", "B", "C", "D"]
    values = [random.randint(10, 100) for _ in range(len(categories))]
    box_data = [random.gauss(50, 15) for _ in range(50)]
    box_data_2 = [random.gauss(55, 10) for _ in range(50)]
    
    obtener_porcentajes_hipertension_sexo(df)

    # Gráfico de pastel (Promedio de Hemoglobina Glucosilada)
    promedio_hba1c = df.groupby('riesgo_hipertension')['valor_hemoglobina_glucosilada'].mean()
    labels = [f'Hipertensión: {riesgo}' for riesgo in promedio_hba1c.index]
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=promedio_hba1c.values, hoverinfo='label+percent', textinfo='percent', marker=dict(colors=['skyblue', 'salmon']), hole=.3)])
    fig_pie = crear_grafico(fig_pie, 'Promedio de Hemoglobina Glucosilada por Riesgo de Hipertensión')
    img_pie = ft.Image(src=generate_image(fig_pie), width=600, height=400)
    
    # Gráfico de barras apiladas (Proporción de Hipertensión por Sexo)
    hipertension_por_sexo = df.groupby('sexo')['riesgo_hipertension'].value_counts(normalize=True).unstack()
    fig_bar = go.Figure()
    for col in hipertension_por_sexo.columns:
        fig_bar.add_trace(go.Bar(x=hipertension_por_sexo.index, y=hipertension_por_sexo[col], name=f'Hipertensión: {col}'))
    fig_bar = crear_grafico(fig_bar, 'Proporción de Hipertensión por Sexo', 'Sexo', 'Proporción')
    fig_bar.update_layout(barmode='stack')
    img_bar = ft.Image(src=generate_image(fig_bar), width=600, height=400)
    
    # Histograma (Distribución de Edad por Riesgo de Hipertensión)
    fig_hist = go.Figure()
    for riesgo in df['riesgo_hipertension'].unique():
        data = df[df['riesgo_hipertension'] == riesgo]['edad']
        fig_hist.add_trace(go.Histogram(x=data, name=f'Hipertensión: {riesgo}'))
    fig_hist = crear_grafico(fig_hist, 'Distribución de Edad por Riesgo de Hipertensión', 'Edad', 'Frecuencia')
    fig_hist.update_layout(barmode='overlay')
    img_hist = ft.Image(src=generate_image(fig_hist), width=600, height=400)

    
    # Gráfico de barras (IMC Promedio por Riesgo de Hipertensión)
    imc_promedio = df.groupby('riesgo_hipertension')['masa_corporal'].mean()
    fig_bar2 = go.Figure(data=[go.Bar(x=imc_promedio.index.astype(str), y=imc_promedio.values)])
    fig_bar2 = crear_grafico(fig_bar2, 'IMC Promedio por Riesgo de Hipertensión', 'Riesgo de Hipertensión', 'IMC Promedio')
    img_bar2 = ft.Image(src=generate_image(fig_bar2), width=600, height=400)
    
    # Contenedores
    container_pie = ft.Container(content=img_pie, border_radius=20, bgcolor="#505458", margin=10, height=400, expand=True)
    container_bar = ft.Container(content=img_bar, border_radius=20, bgcolor="#505458", margin=10, height=400, expand=True)
    container_hist = ft.Container(content=img_hist, border_radius=20, bgcolor="#505458", margin=10, height=400, expand=True)
    container_box_comp = ft.Container(content=img_bar2, border_radius=20, bgcolor="#505458", height=400, margin=10, expand=True)

    def contenedor(texto,ancho):
        texto_x = ft.Container(
            content=texto,
            margin=10,
            padding=15,
            alignment=ft.alignment.center_left,
            bgcolor="#505458",
            border_radius=20,
            height=400,
            width=ancho,
        )
        return texto_x
    
    def text_white(WhiteTxt,tamano):
        return ft.Text(
            WhiteTxt,
            size=tamano,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE,
            max_lines=None  # Permite que el texto se expanda en varias líneas
        )

    def text_point(PointTxt,tamano):
        return ft.Row(
            [
                ft.Icon(ft.icons.CIRCLE, size=14, color=ft.colors.WHITE),
                ft.Container(content=text_white(PointTxt,tamano), expand=True)  # Permite ajuste del texto
            ],
            alignment=ft.MainAxisAlignment.START
        )   
    
    img_corazon = ft.Image(src=load_local_image(r"src\assets\Corazon.png"), width=400, height=300)

    text_hist = contenedor(ft.Column(
            [
                text_white("La gráfica muestra la distribución de edades tanto para personas con hipertensión, como para las que no la tienen. ",20),
                text_point("Se puede ver que la mayor frecuencia de personas con hipertensión se encuentra entre los 50 y los 70 años.",20),
                text_point("Se puede ver que la mayor frecuencia de personas sin hipertensión se encuentra entre los 50 y los 70 años.",20)
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        400
        )
    
    text_pie = contenedor(text_white("El gráfico muestra la proporción del promedio de hemoglobina glucosilada entre los dos grupos de riesgo de hipertensión.Los porcentajes son muy similares (49.6% y 50.4%), lo que indica que no hay una diferencia significativa en el promedio de hemoglobina glucosilada entre los pacientes con y sin hipertensión.",20),
                          400
                          )
    
    text_bar1 = contenedor(ft.Column(
        [
            text_white("Hipertensión: 1 (Riesgo de Hipertensión)",17),
            text_white("Hipertensión: 0 (No hay riesgo de Hipertensión)",17),
            text_white(" ",17),
            text_white("Interpretación:\nEl gráfico compara el IMC promedio entre pacientes con y sin hipertensión.\nSe observa claramente que el IMC promedio es significativamente mayor en el grupo de pacientes con hipertensión (1) en comparación con el grupo sin hipertensión (0).\nLa barra que representa a la gente con hipertensión (1), es mucho más alta que la barra que representa a la gente sin hipertensión (0).\nEsto quiere decir que la gente que tiene hipertensión, también tiene un mayor índice de masa corporal.",17)
        ],
        spacing=5,
        alignment=ft.MainAxisAlignment.CENTER
    ),700)

    text_bar2 = contenedor(ft.Column(
        [
            text_white("El gráfico permite comparar visualmente la proporción de hipertensión entre los diferentes grupos de sexo.",20),
            text_point("Se observa que en los grupos de sexo 1 y 2, la proporción de personas con hipertensión es mayor que la proporción de personas sin hipertensión.",20),
            text_point("Se puede ver que la proporción de gente con hipertensión y sin hipertensión es muy similar en los grupos de sexo 1 y 2.",20),
            text_white(" ",20),
            text_white("Sexo: 1 = Hombre, 2 = Mujer",20)
        ],
        spacing=5,
        alignment=ft.MainAxisAlignment.CENTER
    ),700)


    # Widget creado
    mas = ft.Column([ft.Row([
        container_hist, 
        text_hist,
    ]
    ,alignment=ft.MainAxisAlignment.START
    ),
    ft.Row([
        container_pie,
        img_corazon,
        text_pie    
    ]),
    ft.Row([
        text_bar1,
        container_box_comp
        
    ]),
    ft.Row([
        text_bar2,
        container_bar,
        
    ]),
    ]
    ,alignment=ft.MainAxisAlignment.START)
    
    return mas
