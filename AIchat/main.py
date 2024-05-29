import flet as ft
from llama_cpp import Llama

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
                    # ft.Text(message.text, selectable=True)
                    ft.Container(
                        content = ft.Text(message.text, selectable=True),
                        bgcolor = self.get_bgcolor(message.message_type), #背景色
                        border = ft.border.all(1, ft.colors.OUTLINE), # 囲い
                        border_radius = 5, # 囲いの丸み
                        padding = 5
                        )
                ],
                tight=True,
                spacing=5,
                expand=True #文字のスペースを埋める（テキストをはみ出ないようにした）
            ),
        ]
        
    # チャットの装飾
    def get_bgcolor(self, chat_type):
        if chat_type == 'ai':
            color = ft.colors.BLUE_GREY_50
        else:
            color = ft.colors.WHITE
            
        return color
        
    
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

llm = Llama(
    model_path="LLMのファイルパス",
    # n_gpu_layers=-1, # コメントをはずしてGPUを使う
    n_ctx=2048
)
def ai_chat(message):
    chat_history = [
        {"role": "system", "content": "あなたは日本語を話す優秀なアシスタントです。回答には必ず日本語で答えてください。"},
        {
            "role": "user",
            "content": message}
    ]

    output = llm.create_chat_completion(messages=chat_history)

    return output["choices"][0]["message"]["content"]


def main(page: ft.Page):
    page.title = 'AIチャット'
    
    def on_message(message: Message):
        m = ChatMessage(message)
        chat.controls.append(m)
        page.update()
    
    def message_creation(name, text, message_type):
        on_message(Message(user_name=name, text=text, message_type=message_type))
    
    def send_message_click(e):
        if new_message.value != "":
            message_creation('user', new_message.value, 'human')
            send_message = new_message.value
            new_message.value = ''
            progress.visible = True # プログレスバーの表示
            page.update()
            
            ai_mes = ai_chat(send_message)
            message_creation('AI', ai_mes, 'ai')
            
            progress.visible = False # プログレスバーの非表示
            new_message.focus()
            page.update()
            
    # プログレスバー
    progress = ft.ProgressBar(
        color = ft.colors.PINK, # 進むバーの色
        bgcolor = ft.colors.GREY_200, # バーの背景色
        visible = False # 非表示にする
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
    
    page.add(
        ft.Container(
            content = chat,
            border = ft.border.all(1, ft.colors.OUTLINE),
            border_radius = 5,
            padding = 10,
            expand = True,
        ),
        progress,
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