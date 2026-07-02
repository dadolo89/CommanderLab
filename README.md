# CommanderLab 🧪

Un simulador de Magic: The Gathering Commander en Python.

## 📋 Características

- 🎮 **Simulador de Magic Commander** con 40 vidas iniciales
- 🔴🔵⚫ Soporte multi-color completo
- 📚 Sistema de cartas con efectos especiales
- 🎲 Motor de turnos y stack de hechizos
- 🦸 Villanos Marvel como comandantes y cartas

## 🏗️ Estructura del Proyecto

```
CommanderLab/
├── src/
│   ├── game/              # Lógica principal del juego
│   │   ├── game.py
│   │   ├── player.py
│   │   └── zone.py
│   ├── cards/             # Sistema de cartas
│   │   ├── card.py
│   │   ├── effects.py
│   │   └── deck.py
│   ├── rules/             # Motor de reglas
│   │   ├── stack.py
│   │   └── triggers.py
│   └── utils/
│       └── constants.py
├── tests/
├── decks/                 # Mazos de ejemplo
│   └── doctor_doom.txt
├── requirements.txt
└── main.py
```

## 🚀 Cómo empezar

```bash
pip install -r requirements.txt
python main.py
```

## 📖 Mazo incluido

- **Comandante:** Doctor Doom, King of Latveria
- **Colores:** Azul, Negro, Rojo
- **Estrategia:** Control y descarte forzado
