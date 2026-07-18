SA_03

Структура на 18.07.2026

core/
gui/
    layout.py
    theme.py

widgets/
    image_button.py
    horizontal_slider.py

panels/
    control_panel.py

Принципы

- собственные виджеты
- Theme отвечает только за оформление
- Layout отвечает только за геометрию
- Config хранит пути и настройки
- Panel является контейнером виджетов