import flet as ft

def main(page: ft.Page):
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = 'Rusich App'

    field_label = ft.Text('SuperMega Text', color='#ff7700', size=22)
    form_field = ft.TextField('0', width=150, text_align=ft.TextAlign.CENTER, border_color='#ff7700')

    def get_info(e):
        field_label.value = f'Total: {form_field.value}'
        page.update()

    def clear(e):
        field_label.value = 'SuperMega Text'
        form_field.value = '0'
        page.update()

    page.add(
        ft.Row(
            controls=[
                ft.IconButton(ft.icons.Icons.HOME, on_click=get_info),
                ft.Icon(ft.icons.Icons.ARROW_BACK),
                ft.ElevatedButton('Clear', on_click=clear),
                ft.Checkbox(label='Check it', value=False)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            controls=[
                field_label,
                form_field,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
    )

ft.run(main=main)
