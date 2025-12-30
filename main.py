import flet as ft
import sqlite3


def main(page: ft.Page):
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = 'Admin panel'
    page.window.width = 350
    page.window.height = 400
    page.window.resizable = False

    def validate():
        if len(login_field.value) > 3 and len(pass_field.value) >= 6:
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True
        page.update()

    def register():
        db = sqlite3.connect('db.sqlite')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, login TEXT, password TEXT)""")

        cur.execute("SELECT * FROM users WHERE login=?", (login_field.value,))
        user = cur.fetchone()

        if user:
            login_field.border_color = '#ff0000'
            page.bottom_appbar = ft.SnackBar(ft.Text('This Login already exist'))
            page.bottom_appbar.open = True
        else:
            cur.execute(f"""INSERT INTO users VALUES(NULL, '{login_field.value}', '{pass_field.value}')""")
            db.commit()
            login_field.value = ''
            pass_field.value = ''
            btn_reg.disabled = True
        db.close()
        page.update()

    def authorization():
        db = sqlite3.connect('db.sqlite')
        cur = db.cursor()

        cur.execute(
            "SELECT * FROM users WHERE login=? AND password=?",
            (login_field.value, pass_field.value),
        )
        user = cur.fetchone()
        if not user:
            login_field.border_color = '#ff0000'
            pass_field.border_color = '#ff0000'
            page.bottom_appbar = ft.SnackBar(ft.Text('This Login is not exist'))
            page.bottom_appbar.open = True
        else:
            page.navigation_bar.destinations.append(
                ft.NavigationBarDestination(ft.icons.Icons.MAN, label='Main Page'),
            )
            page.navigation_bar.destinations[1].disabled = True

        db.close()
        page.update()

    login_field = ft.TextField('', label='Login', border_color='#bbbbbb', on_change=validate)
    pass_field = ft.TextField('', label='Password', border_color='#bbbbbb', on_change=validate, password=True)
    btn_reg = ft.OutlinedButton('Register', width=300, height=50, on_click=register, disabled=True)
    btn_auth = ft.OutlinedButton('Login', width=300, height=50, on_click=authorization, disabled=True)
    users_list = ft.ListView(spacing=10, padding=20)

    panel_register = [
        ft.Row(
            [ft.Text('Registration', size=24, color='#ff7700')], alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            controls=[ft.Column([login_field, pass_field, btn_reg])],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ]

    panel_auth = [
        ft.Row(
            [ft.Text('Authorization', size=24, color='#ff7700')], alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            controls=[ft.Column([login_field, pass_field, btn_auth])],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ]

    panel_lk = [
        ft.Row(
            [ft.Text('Main Page', size=24, color='#ff7700')], alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            [ft.Column([
                users_list,
            ])], alignment=ft.MainAxisAlignment.CENTER,
        ),
    ]

    def navigate(e):
        idx = page.navigation_bar.selected_index
        page.clean()

        if idx == 1:
            page.add(*panel_auth)
        elif idx == 2:
            users_list.controls.clear()
            db = sqlite3.connect('db.sqlite')
            cur = db.cursor()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            db.close()
            for i in users:
                users_list.controls.append(ft.Row([
                    ft.Icon(ft.Icons.FACE),
                    ft.Text(i[1]),
                ]))
            page.add(*panel_lk)
        else:
            page.add(*panel_register)
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(ft.icons.Icons.VERIFIED_USER, label='Sign In'),
            ft.NavigationBarDestination(ft.icons.Icons.LOGIN, label='Log In'),
        ], on_change=navigate,
    )

    page.add(*panel_register)

ft.app(target=main)
