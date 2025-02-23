import flet as ft
import plotly.graph_objects as go
import io
import base64
import random

    #funcion para comvertir imagenes png a base64
def generate_image(fig):
    buffer = io.BytesIO()
    fig.write_image(buffer, format="png")
    buffer.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buffer.read()).decode()}"

def home(page: ft.Page):
    page.bgcolor = "#303030"  # Fondo oscuro
    page.appbar = ft.AppBar(
        title=ft.Text("Gráficas con Flet y Plotly", color="white", size=20, weight=ft.FontWeight.BOLD),
        bgcolor="#EE0E51",
    )
    page.scroll = ft.ScrollMode.AUTO
    
    # Datos de ejemplo para el alexis
    years = [f"{i}" for i in range(2017, 2023)]
    categories = ["A", "B", "C", "D"]
    values = [random.randint(10, 100) for _ in range(len(categories))]
    box_data = [random.gauss(50, 15) for _ in range(50)]
    box_data_2 = [random.gauss(55, 10) for _ in range(50)]
    
    # Gráficos con Plotly
    fig_pie = go.Figure(data=[go.Pie(labels=categories, values=values)])
    fig_pie.update_layout(paper_bgcolor="#505458")
    img_pie = ft.Image(src=generate_image(fig_pie), width=400, height=300)
    
    fig_bar = go.Figure(data=[go.Bar(x=categories, y=values)])
    fig_bar.update_layout(paper_bgcolor="#505458")
    img_bar = ft.Image(src=generate_image(fig_bar), width=400, height=300)
    
    fig_hist = go.Figure(data=[go.Histogram(x=box_data)])
    fig_hist.update_layout(paper_bgcolor="#505458")
    img_hist = ft.Image(src=generate_image(fig_hist), width=400, height=300)
    
    fig_box = go.Figure(data=[go.Box(y=box_data)])
    fig_box.update_layout(paper_bgcolor="#505458")
    img_box = ft.Image(src=generate_image(fig_box), width=400, height=300)
    
    fig_box_comp = go.Figure()
    fig_box_comp.add_trace(go.Box(y=box_data, name="Grupo 1"))
    fig_box_comp.add_trace(go.Box(y=box_data_2, name="Grupo 2"))
    fig_box_comp.update_layout(paper_bgcolor="#505458")
    img_box_comp = ft.Image(src=generate_image(fig_box_comp), width=400, height=300)
    
    # Contenedores
    container_pie = ft.Container(content=img_pie, border_radius=20, bgcolor="#505458", margin=10, height=400, expand=True)
    container_bar = ft.Container(content=img_bar, border_radius=20, bgcolor="#505458", margin=10, height=400, expand=True)
    container_hist = ft.Container(content=img_hist, border_radius=20, bgcolor="#505458", margin=10, height=400, expand=True)
    container_box = ft.Container(content=img_box, border_radius=20, bgcolor="#505458", margin=10, height=400, expand=True)
    container_box_comp = ft.Container(content=img_box_comp, border_radius=20, bgcolor="#505458", height=400, margin=10, expand=True)

    texto_x = ft.Container(
        content=ft.Column([
            ft.Text("Años", color="white", size=15, weight=ft.FontWeight.BOLD),
        ], alignment=ft.MainAxisAlignment.CENTER),
        margin=10,
        padding=10,
        alignment=ft.alignment.center_left,
        bgcolor="#505458",
        border_radius=20,
        expand=True,
        height=400
    )

    # Widget creado
    mas = ft.Column([ft.Row([
        container_hist, 
        texto_x,
    ]
    ,alignment=ft.MainAxisAlignment.START
    ),
    ft.Row([
        container_pie,
        texto_x
    ]),
    ft.Row([
        container_box_comp,
        texto_x
    ]),
    ft.Row([
        container_bar,
        texto_x
    ]),
    ]
    ,alignment=ft.MainAxisAlignment.START)
    
    return mas