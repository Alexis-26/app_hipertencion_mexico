import flet as ft

def home():
    mas = ft.Row(
        [
            ft.IconButton(ft.Icons.REMOVE),
            ft.TextField(text_align=ft.TextAlign.CENTER),
            ft.IconButton(ft.Icons.ADD),
        ]
    )
    return mas
