import flet as ft

def main(page: ft.Page):
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = 'Rusich App'

    page.add(
        ft.Row(
            controls=[
                ft.IconButton(ft.icons.Icons.HOME),
                ft.Icon(ft.icons.Icons.ARROW_BACK),
            ],
            alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
