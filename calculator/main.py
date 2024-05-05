import flet as ft


new_operand = True # 計算結果を上書きするかどうかのフラグ
operand1 = 0 # 計算途中の値を一時的に記憶する変数
operator = '+' # 演算子

def calculate(num1, num2, operator):
    """
    2つの数値と演算子を渡すと、計算結果を返します。

    Args:
        num1: 1つ目の数値
        num2: 2つ目の数値
        operator: 演算子 ( +, -, *, / )

    Returns:
        計算結果
    """
    if operator == '+':
        return format_number(num1 + num2)
    elif operator == '-':
        return format_number(num1 - num2)
    elif operator == '*':
        return format_number(num1 * num2)
    elif operator == '/':
        if num2 == 0:
            return 'Error'
        else:
            return format_number(num1 / num2)
        
def format_number(num):
    """
    少数かどうかで、数値の書式を整えて返します。

    Args:
        num: 整数または浮動小数点数

    Returns:
        整数の場合は int 型、少数の場合 float 型の値
    """
    return int(num) if num % 1 == 0 else num


def main(page: ft.Page):
    page.title = '電卓'
    
    # ウィンドウサイズ
    page.window_width = 400
    page.window_height = 310
    
    result = ft.Ref[ft.Text]()
    
    def button_click(e):
        """
        ボタンイベント

        Args:
            e: ElevatedButtonの情報

        Returns:
        """
        global new_operand, operand1, operator
        
        data = e.control.data
        print(data)
        
        if data == 'ce' or result.current.value == 'Error':
            result.current.value = '0'
            new_operand = True
            operand1 = 0
            operator = '+'
        elif data in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'):
            if result.current.value == '0' or new_operand == True:
                result.current.value = data
                new_operand = False
            else:
                result.current.value += data
        elif data in ("+", "-", "*", "/"):
            result.current.value = calculate(operand1, float(result.current.value), operator)
            operator = data
            
            if result.current.value == 'Error':
                operand1 = 0
            else:
                operand1 = float(result.current.value)
            new_operand = True
        elif data in ('='):
            result.current.value = calculate(operand1, float(result.current.value), operator)
            new_operand = True
            operand1 = 0
            operator = '+'
        elif data in ('%'):
            result.current.value = float(result.current.value) / 100
            new_operand = True
            operand1 = 0
            operator = '+'
        elif data in ('+/-'):
            tmp = float(result.current.value)
            
            if tmp > 0:
                result.current.value = f"-{tmp}"
            else:
                result.current.value = str(format_number(abs(tmp)))
            
        page.update()

    
    page.add(
        ft.Container(
            padding=10,
            bgcolor=ft.colors.BLUE_200,
            content=ft.Column([
                ft.Row([ft.Text(ref=result, value=0, size=20)], alignment="end"),
                ft.Row([ft.ElevatedButton('ec', data='ce', expand=1, on_click=button_click), ft.ElevatedButton('+/-', data='+/-', expand=1, on_click=button_click), ft.ElevatedButton('%', data='%', expand=1, on_click=button_click), ft.ElevatedButton('/', data='/',expand=1, on_click=button_click)]),
                ft.Row([ft.ElevatedButton('7', data='7', expand=1, on_click=button_click), ft.ElevatedButton('8', data='8', expand=1, on_click=button_click), ft.ElevatedButton('9', data='9', expand=1, on_click=button_click), ft.ElevatedButton('*', data='*', expand=1, on_click=button_click)]),
                ft.Row([ft.ElevatedButton('4', data='4', expand=1, on_click=button_click), ft.ElevatedButton('5', data='5', expand=1, on_click=button_click), ft.ElevatedButton('6', data='6', expand=1, on_click=button_click), ft.ElevatedButton('-', data='-', expand=1, on_click=button_click)]),
                ft.Row([ft.ElevatedButton('1', data='1', expand=1, on_click=button_click), ft.ElevatedButton('2', data='2', expand=1, on_click=button_click), ft.ElevatedButton('3', data='3', expand=1, on_click=button_click), ft.ElevatedButton('+', data='+', expand=1, on_click=button_click)]),
                ft.Row([ft.ElevatedButton('0', data='0', expand=2, on_click=button_click), ft.ElevatedButton('.', data='.', expand=1, on_click=button_click), ft.ElevatedButton('=', data='=', expand=1, on_click=button_click)]),
            ])
        )
    )


ft.app(target=main)