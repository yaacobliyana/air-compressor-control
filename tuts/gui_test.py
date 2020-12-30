from guizero import App, Text, TextBox, PushButton, Slider

def say_my_name():
    welcome_message.value = my_name.value

def change_text_size(slider_value):
    welcome_message.size = slider_value

app = App(title = "Hello  World")

welcome_message = Text(app, text="Selamat Datang! ;)", size=35, font="Times New Roman", color="pink")
my_name = TextBox(app)
update_text = PushButton(app, command=say_my_name, text="Display my name")
text_size = Slider(app, command=change_text_size, start=10, end=80)

app.display()
