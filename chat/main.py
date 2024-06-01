import flet as ft

class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class ChatMessage(ft.Row):
    def __init__(self, message:Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name)
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True)
                ],
                tight=True,
                spacing=5,
            )
        ]
    
    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()
    
    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
    
        return colors_lookup[hash(user_name) % len(colors_lookup)]
        

def main(page: ft.Page):
    page.title = 'チャット'
    
    # chat = ft.Column()
    # new_message = ft.TextField()
    
    def on_message(message: Message):
        if message.message_type == "chat_message":
            # chat.controls.append(ft.Text(f"{message.user}: {message.text}"))
            m = ChatMessage(message)
        elif message.message_type =="login_message":
            # chat.controls.append(
            #     ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
            # )
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()
        
    page.pubsub.subscribe(on_message)
    
    # def send_click(e):
    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(Message(user_name=page.session.get('user_name'), text=new_message.value, message_type="chat_message"))
            new_message.value = ''
            new_message.focus()
            page.update()
        
    join_user_name  = ft.TextField(label="Enter your name")
    
    def join_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            page.pubsub.send_all(Message(user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.", message_type="login_message"))
            page.update()
        
    page.dialog = ft.AlertDialog(
        open = True,
        modal = True,
        title = ft.Text("Welcome!"),
        content = ft.Column([join_user_name], tight=True),
        actions = [ft.ElevatedButton(text="Join chat", on_click=join_click)],
        actions_alignment = "end"
    )
    
    chat = ft.ListView(
        expand = True,
        spacing = 10,
        auto_scroll = True
    )
    
    new_message = ft.TextField(
        hint_text = "Write a message...",
        autocorrect = True,
        shift_enter = True,
        min_lines = 1,
        max_lines = 5,
        filled = True,
        expand = True,
        on_submit = send_message_click
    )
        
    # page.add(
    #     chat, ft.Row(controls=[new_message, ft.ElevatedButton("Send", on_click=send_click)])
    # )
    
    page.add(
        ft.Container(
            content = chat,
            border = ft.border.all(1, ft.colors.OUTLINE),
            border_radius = 5,
            padding = 10,
            expand = True,
        ),
        ft.Row(
            [
                new_message, 
                ft.IconButton(
                    icon = ft.icons.SEND_ROUNDED,
                    tooltip = "Send message",
                    on_click = send_message_click
                )
            ]
        )
    )


ft.app(target=main, view=ft.AppView.WEB_BROWSER)

