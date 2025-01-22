from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.core.window import Window  # Importa Window

class ScrollingLabel(Label):
    def __init__(self, **kwargs):
        super(ScrollingLabel, self).__init__(**kwargs)
        self.anim = None
        self.bind(size=self.update_text_width)

    def update_text_width(self, *args):
        self.text_width = self.texture_size[0]

    def start_animation(self):
        if self.anim:
            self.anim.cancel(self)
        self.x = self.width
        distance = self.text_width + self.width  # Ajustar la distancia que se recorre
        self.anim = Animation(x=-self.text_width, duration=distance / 100.0, t='linear')
        self.anim.bind(on_complete=self.reset_position)
        self.anim.start(self)

    def reset_position(self, *args):
        self.start_animation()

class ElectronicSignApp(App):
    def build(self):
        Window.maximize()  # Maximizar la ventana al iniciar

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Layout para centrar el Spinner en la parte superior
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        top_layout.add_widget(Widget())  # Widget vacío para empujar al Spinner al centro
        self.option_spinner = Spinner(
            text='TIPO DE CONTRASTE',
            values=('Opción 1: Fondo negro con borde fluorescente', 'Opción 2: Fondo intermitente fluorescente'),
            size_hint=(None, None),
            size=(350, 30),
            background_color=(0, 0, 1, 1),  # Cambia el color del fondo
            color=(0, 1, 1, 1)  # Cambia el color del texto
        )
        self.option_spinner.bind(text=self.update_option)
        top_layout.add_widget(self.option_spinner)
        top_layout.add_widget(Widget())  # Widget vacío para empujar al Spinner al centro

        self.text_input = TextInput(
            hint_text='Escribe tu mensaje aquí',
            font_size=24,
            size_hint_y=None,
            height=100,
            multiline=False,
            padding=(10, 10)
        )

        self.label = ScrollingLabel(
            text='Aquí aparecerá tu mensaje',
            font_size=100,
            color=(1, 1, 1, 1),
            bold=True
        )

        self.buttons_layout = BoxLayout(size_hint_y=None, height=50, size_hint=(1, None), spacing=10, padding=(10, 0))

        self.button = Button(
            text='Mostrar Mensaje',
            size_hint=(None, None),
            size=(150, 40),
            background_color=(0.1, 0.5, 0.8, 1)
        )
        self.button.bind(on_press=self.show_message)
        self.buttons_layout.add_widget(self.button)

        self.siren_button1 = Button(
            text='Siren 1',
            size_hint=(None, None),
            size=(150, 40),
            background_color=(0.9, 0.1, 0.1, 1)
        )
        self.siren_button1.bind(on_press=lambda instance: self.toggle_siren('siren1.wav'))
        self.buttons_layout.add_widget(self.siren_button1)

        self.siren_button2 = Button(
            text='Siren 2',
            size_hint=(None, None),
            size=(150, 40),
            background_color=(0.9, 0.1, 0.1, 1)
        )
        self.siren_button2.bind(on_press=lambda instance: self.toggle_siren('siren2.wav'))
        self.buttons_layout.add_widget(self.siren_button2)

        self.siren_button3 = Button(
            text='Siren 3',
            size_hint=(None, None),
            size=(150, 40),
            background_color=(0.9, 0.1, 0.1, 1)
        )
        self.siren_button3.bind(on_press=lambda instance: self.toggle_siren('siren3.wav'))
        self.buttons_layout.add_widget(self.siren_button3)

        self.toggle_buttons_button = Button(
            text='Ocultar/Mostrar',
            size_hint=(None, None),
            size=(150, 40),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        self.toggle_buttons_button.bind(on_press=self.toggle_buttons_visibility)
        self.buttons_layout.add_widget(self.toggle_buttons_button)

        # Añadiendo los widgets en el orden correcto
        self.layout.add_widget(top_layout)  # Añadir el top_layout en lugar del spinner directamente
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.label)
        self.layout.add_widget(BoxLayout(size_hint_y=None, height=0))  # Espacio vacío
        self.layout.add_widget(self.buttons_layout)

        self.option = 1
        self.blinking = False
        self.siren_playing = False
        self.sounds = {
            'siren1.wav': SoundLoader.load('siren1.wav'),
            'siren2.wav': SoundLoader.load('siren2.wav'),
            'siren3.wav': SoundLoader.load('siren3.wav')
        }

        self.text_colors_neon = [(0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 0, 1)]  # Colores neón
        self.bg_colors_fluorescent = [(1, 0, 0, 1), (0, 0.5, 1, 1), (1, 1, 0, 1), (0, 1, 1, 1), (0.5, 1, 0, 1)]  # Colores fluorescentes
        self.current_color_index = 0

        Clock.schedule_interval(self.blink, 0.5)

        return self.layout

    def update_option(self, spinner, text):
        if text == 'Opción 1: Fondo negro con borde fluorescente':
            self.option = 1
            self.blinking = False
        else:
            self.option = 2
            self.blinking = True

    def show_message(self, instance):
        self.label.text = self.text_input.text
        self.label.start_animation()

    def blink(self, dt):
        self.current_color_index = (self.current_color_index + 1) % len(self.text_colors_neon)
        if self.option == 1:
            self.update_background_option1()
            self.label.color = self.text_colors_neon[self.current_color_index]
        else:
            self.update_background_option2()
            self.label.color = (0, 0, 0, 1)  # Texto negro

    def update_background_option1(self):
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            Color(0, 0, 0, 1)  # Fondo negro
            Rectangle(pos=self.layout.pos, size=self.layout.size)
            # Bordes fluorescentes
            Color(0, 0, 1, 1)
            Line(rectangle=(self.layout.x, self.layout.y, self.layout.width, self.layout.height), width=2)
            Color(0, 0, 1, 0.5)
            Line(rectangle=(self.layout.x + 3, self.layout.y + 3, self.layout.width - 6, self.layout.height - 6), width=2)
            Color(0, 0, 1, 0.25)
            Line(rectangle=(self.layout.x + 6, self.layout.y + 6, self.layout.width - 12, self.layout.height - 12), width=2)

    def update_background_option2(self):
        self.layout.canvas.before.clear()
        self.current_bg_color_index = (self.current_color_index + 1) % len(self.bg_colors_fluorescent)
        with self.layout.canvas.before:
            Color(*self.bg_colors_fluorescent[self.current_bg_color_index])
            Rectangle(pos=self.layout.pos, size=self.layout.size)

    def toggle_siren(self, sound_file):
        sound = self.sounds[sound_file]
        if sound.state == 'play':
            sound.stop()
        else:
            sound.play()

    def toggle_buttons_visibility(self, instance):
        if self.buttons_layout.height == 0:
            self.buttons_layout.height = 50
            self.text_input.height = 100
        else:
            self.buttons_layout.height = 0
            self.text_input.height = 0

if __name__ == '__main__':
    ElectronicSignApp().run()
