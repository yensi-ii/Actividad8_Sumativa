from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QMessageBox, QDoubleSpinBox, QTextEdit
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QDateTime, Qt
import sys, math

app = QApplication(sys.argv)

# Diccionario para carros que están adentro
# Guardamos: hora de entrada y tarifa
entradas = {}

# Lista para guardar historial completo (los que entran y salen)
historial = []

# ---------- FUNCIONES ----------
def registrar_entrada():
    placa = txt_placa.text().strip().upper()
    if not placa:
        QMessageBox.warning(ventana, "¡Ojo!", "Escribí la placa del carro primero.")
        return
    if placa in entradas:
        QMessageBox.warning(ventana, "Aviso", f"El carro {placa} ya está adentro.")
        return
    
    hora_entrada = QDateTime.currentDateTime()
    tarifa = spn_tarifa.value()  # Guardamos la tarifa en el momento de entrada
    
    # Guardamos en entradas (activo)
    entradas[placa] = {"entrada": hora_entrada, "tarifa": tarifa}
    
    # También lo guardamos en historial
    historial.append({
        "placa": placa,
        "entrada": hora_entrada,
        "salida": None,
        "monto": None,
        "tarifa": tarifa
    })
    
    QMessageBox.information(
        ventana, "Entrada guardada",
        f"Carro {placa}\nEntró a las: {hora_entrada.toString('dd/MM/yyyy HH:mm')}\n"
        f"Tarifa aplicada: ${tarifa:.2f} por hora"
    )
    txt_placa.clear()

def registrar_salida():
    placa = txt_placa.text().strip().upper()
    if placa not in entradas:
        QMessageBox.warning(ventana, "¡Error!", "Ese carro no está registrado adentro.")
        return
    
    datos = entradas.pop(placa)
    entrada = datos["entrada"]
    tarifa = datos["tarifa"]  # Tarifa guardada al entrar
    salida = QDateTime.currentDateTime()
    
    # Cálculo de minutos y tarifa
    minutos = max(1, int(entrada.msecsTo(salida) / 60000))
    horas = max(1, math.ceil(minutos / 60))
    monto = horas * tarifa
    
    # Actualizar historial
    for reg in historial:
        if reg["placa"] == placa and reg["salida"] is None:
            reg["salida"] = salida
            reg["monto"] = monto
            break
    
    QMessageBox.information(
        ventana, "Salida guardada",
        f"Carro: {placa}\nHora entrada: {entrada.toString('HH:mm')}\n"
        f"Hora salida: {salida.toString('HH:mm')}\n"
        f"Tiempo: {minutos} min\n"
        f"Tarifa aplicada: ${tarifa:.2f}\n"
        f"Total a pagar: ${monto:.2f}"
    )
    txt_placa.clear()

def ver_historial():
    ventana_historial = QWidget()
    ventana_historial.setWindowTitle("Historial de carros")
    ventana_historial.setGeometry(400, 400, 500, 400)

    layout_h = QVBoxLayout()

    txt_historial = QTextEdit()
    txt_historial.setReadOnly(True)

    if not historial:
        txt_historial.setPlainText("Todavía no hay carros registrados.")
    else:
        texto = ""
        for reg in historial:
            entrada = reg["entrada"].toString("dd/MM/yyyy HH:mm")
            salida = reg["salida"].toString("dd/MM/yyyy HH:mm") if reg["salida"] else "SIGUE ADENTRO"
            monto = f"${reg['monto']:.2f}" if reg["monto"] is not None else "-"
            tarifa = f"${reg['tarifa']:.2f}"
            texto += (f"Placa: {reg['placa']} | Entrada: {entrada} | "
                      f"Salida: {salida} | Tarifa: {tarifa} | Pago: {monto}\n")
        txt_historial.setPlainText(texto)

    layout_h.addWidget(txt_historial)
    ventana_historial.setLayout(layout_h)
    ventana_historial.show()
    ventana_historials.append(ventana_historial)

# ---------- INTERFAZ ----------
ventana = QWidget()
ventana.setWindowTitle("Parqueo UGB")
ventana.setGeometry(300, 300, 400, 300)
icono = QIcon("carro.png")
ventana.setWindowIcon(icono)

layout = QVBoxLayout()

# Logo arriba
lbl_logo = QLabel()
pixmap = QPixmap("logo.png")  
pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Tamaño pequeño
lbl_logo.setPixmap(pixmap)
lbl_logo.setAlignment(Qt.AlignCenter)

# Título y campos
lbl_titulo = QLabel("Sistema de Parqueo")
lbl_titulo.setAlignment(Qt.AlignCenter)
txt_placa = QLineEdit()
txt_placa.setPlaceholderText("Escribí la placa del carro aquí...")

# Tarifa
lbl_tarifa = QLabel("Tarifa por hora en $:")
spn_tarifa = QDoubleSpinBox()
spn_tarifa.setRange(0.0, 100.0)
spn_tarifa.setDecimals(2)
spn_tarifa.setSingleStep(0.25)
spn_tarifa.setValue(1.50)

# Botones
btn_entrada = QPushButton("Marcar ENTRADA")
btn_salida  = QPushButton("Marcar SALIDA")
btn_historial = QPushButton("Ver HISTORIAL de carros")

btn_entrada.clicked.connect(registrar_entrada)
btn_salida.clicked.connect(registrar_salida)
btn_historial.clicked.connect(ver_historial)

# Agregar widgets al layout (logo primero)
widgets = [lbl_logo, lbl_titulo, txt_placa, lbl_tarifa, spn_tarifa, btn_entrada, btn_salida, btn_historial]
for w in widgets:
    layout.addWidget(w)

ventana.setLayout(layout)

ventana_historials = []

ventana.show()
sys.exit(app.exec_())
