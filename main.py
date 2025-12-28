import flet as ft
import requests


def main(page: ft.Page):
    API = 'faffcba6653d0e42a641ceeff885620f'
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = 'Погодная приложуха'

    user_data = ft.TextField('', width=400, label='Введите город', border_color='#bbbbbb')
    weather_data = ft.Text('')

    def get_user_data(e):
        if len(user_data.value) < 2 or len(user_data.value) > 20:
            return

        url = f'https://api.openweathermap.org/data/2.5/weather?q={user_data.value}&appid={API}&units=metric'
        res = requests.get(url).json()

        if not res or res['cod'] == '404':
            weather_data.value = 'Данные по этому городу не найдены...'
            page.update()
            return

        temp = res['main']['temp']
        wind = res['wind']['speed']
        weather_data.value = f'Температура: {temp}°C, Скорость ветра: {wind}км/ч'
        page.update()

    def on_theme_change():
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    page.add(
        ft.Row([
            ft.IconButton(ft.icons.Icons.SUNNY, on_click=on_theme_change),
            ft.Text(page.title, color='#ff7700')
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([user_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([weather_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=10, color="transparent"),
        ft.Row([
            ft.Button('Показать', on_click=get_user_data)
        ], alignment=ft.MainAxisAlignment.CENTER),
    )

ft.run(main=main)
