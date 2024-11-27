import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QDate
import speech_recognition as sr
import pyttsx3

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Calendário Digital com Voz')
        self.setGeometry(100, 100, 400, 300)

        # Cria o widget de calendário
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)

        # Define a data mínima e máxima do calendário
        self.calendar.setMinimumDate(QDate(2020, 1, 1))
        self.calendar.setMaximumDate(QDate(2025, 12, 31))

        # Conecta o sinal de clique na data ao método de manipulação
        self.calendar.clicked[QDate].connect(self.show_date)

        # Cria o botão para ativar o reconhecimento de voz
        self.voice_button = QPushButton('Ativar Reconhecimento de Voz', self)
        self.voice_button.clicked.connect(self.activate_voice_recognition)

        # Cria o layout e adiciona o widget de calendário e o botão
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.voice_button)

        # Cria um contêiner para o layout
        container = QWidget()
        container.setLayout(layout)

        # Define o contêiner como o widget central da janela principal
        self.setCentralWidget(container)

        # Inicializa o mecanismo de síntese de fala
        self.engine = pyttsx3.init()

    def show_date(self, qDate):
        # Método para manipular o clique na data
        print(f"Data selecionada: {qDate.toString('dd.MM.yyyy')}")
        self.speak_date(qDate)

    def speak_date(self, qDate):
        # Método para falar a data selecionada
        date_str = qDate.toString('dd MMMM yyyy')
        self.engine.say(f"A data selecionada é {date_str}")
        self.engine.runAndWait()

    def activate_voice_recognition(self):
        # Método para ativar o reconhecimento de voz
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Diga algo...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {text}")
            self.process_voice_command(text)
        except sr.UnknownValueError:
            print("Não entendi o áudio")
        except sr.RequestError as e:
            print(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")

    def process_voice_command(self, command):
        # Método para processar o comando de voz
        if "dia" in command or "mês" in command or "ano" in command:
            current_date = QDate.currentDate()
            date_str = current_date.toString('dd MMMM yyyy')
            self.engine.say(f"A data de hoje é {date_str}")
            self.engine.runAndWait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = CalendarApp()
    mainWin.show()
    sys.exit(app.exec_())
