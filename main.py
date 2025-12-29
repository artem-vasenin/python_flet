import flet as ft
import sqlite3


def main(page: ft.Page):
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = 'Authorization'
    page.window.width = 350
    page.window.height = 400
    page.window.resizable = False

    def validate():
        if len(login_field.value) > 3 and len(pass_field.value) >= 6:
            submit.disabled = False
        else:
            submit.disabled = True
        page.update()

    def register():
        db = sqlite3.connect('db.sqlite')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login TEXT,
            password TEXT
        )""")

        cur.execute("SELECT * FROM users WHERE login=?", (login_field.value))
        user = cur.fetchone()
        if user:
            login_field.border_color = '#ff0000'
        else:
            cur.execute(f"""INSERT INTO users VALUES(NULL, '{login_field.value}', '{pass_field.value}')""")
            db.commit()
            login_field.value = ''
            pass_field.value = ''
            submit.disabled = True
        db.close()
        page.update()

    login_field = ft.TextField('', label='Login', border_color='#bbbbbb', on_change=validate)
    pass_field = ft.TextField('', label='Password', border_color='#bbbbbb', on_change=validate, password=True)
    submit = ft.OutlinedButton('Send', width=300, height=50, on_click=register, disabled=True)

    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    [
                        ft.Text('Registration Form'),
                        login_field,
                        pass_field,
                        submit,
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

ft.app(target=main)
