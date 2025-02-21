import flet as ft
from frontend.home import home
def main(page: ft.Page):
    page.add(home())

ft.app(main)
