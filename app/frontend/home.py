import flet as ft

def home(page: ft.Page):


    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.CENTER)

    #logica
    def minus(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()
    
    def plus(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    # Widget creados
    mas = ft.Row(
        [
            ft.IconButton(ft.Icons.REMOVE, on_click=minus),
            txt_number,
            ft.IconButton(ft.Icons.ADD, on_click=plus),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    return mas

