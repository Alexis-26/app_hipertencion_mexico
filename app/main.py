import flet as ft
from frontend.home import home


def main(page: ft.Page): 
    page.title = "grafica flet"
    page.bgcolor = "#363540"
    
    # Agregar elementos a la página
    page.add(
        home(page)
    )
 
# Ejecutar la app en Flet 
ft.app(target=main, view=ft.WEB_BROWSER)
