import flet as ft
import time

def main(page: ft.Page):
    
    first_name = ft.TextField(label="first name", autofocus=True)
    last_name = ft.TextField(label="last name")
    greetings = ft.Column()
    
    def btu_click(e):
        greetings.controls.append(ft.Text(f"Hello, {first_name.value} {last_name.value}"))
        first_name.value = ''
        last_name.value = ''
        page.update()
        first_name.focus()
        
    page.add(
        first_name,
        last_name,
        ft.ElevatedButton("Say hello", on_click=btu_click),
        greetings
    )

ft.app(target=main)
