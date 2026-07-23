# SA_03 Shadowing App — GUI Architecture
Версия: 1.0

## 1. Общая схема

```
Application
    |
    v
MainWindow
    |
    +-- ControlPanel
    |       |
    |       +-- Widgets
    |
    +-- Dialog
            |
            +-- Widgets
```

Компоненты имеют собственную ответственность и минимальную связанность.

## 2. Главный цикл

Единственный главный цикл находится в `core/application.py`.

```python
while running:
    for event in pygame.event.get():
        window.handle_event(event)

    window.update()
    window.draw()
```

## 3. pygame.event.get()

`pygame.event.get()` вызывается только в `Application`.

Запрещено использовать его внутри:
- Window
- Dialog
- Button
- Slider
- Widget

Причина: метод очищает очередь событий.

## 4. Поток событий

```
Application
      |
      v
MainWindow
      |
      v
Widget
```

Каждый объект проверяет только свои события.

## 5. handle_event()

Назначение: обработка действий пользователя.

Обрабатывает:
- MouseButtonDown
- MouseButtonUp
- KeyDown
- Quit

Может:
- изменять своё состояние;
- возвращать команду родителю.

Не должен:
- рисовать;
- выполнять логику приложения;
- закрывать приложение напрямую.

## 6. update()

Вызывается каждый кадр.

Используется для:
- обновления состояния;
- проверки положения мыши;
- таймеров;
- анимации.

Допустимо:

```python
pygame.mouse.get_pos()
pygame.mouse.get_pressed()
```

## 7. draw()

Отвечает только за отображение.

Разрешено:
- pygame.draw()
- surface.blit()
- font.render()

Запрещено:
- обработка событий;
- изменение состояния;
- выполнение команд.

Модель:

```
state → draw → image
```

## 8. События и состояния

**Event** — что произошло.

Пример:
```
MOUSEBUTTONDOWN
```

Источник:
```python
pygame.event.get()
```

**State** — что происходит сейчас.

Пример:
```
курсор над кнопкой
мышь зажата
```

Источник:
```python
pygame.mouse.*
```

## 9. Стандарт виджета

```python
class Widget:

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass
```

Неиспользуемые методы могут быть пустыми.

## 10. Ответственность классов

**Application**
- запуск;
- главный цикл;
- завершение.

**MainWindow**
- структура окна;
- маршрутизация событий;
- обработка команд.

**Dialog**
- модальность;
- собственные элементы интерфейса.

**Widget**
- геометрия;
- состояние;
- отображение.

## 11. Передача команд

События идут вниз:

```
Application → MainWindow → Widget
```

Команды идут вверх:

```
Widget → MainWindow → Application
```

## 12. Состояние элементов

Каждый элемент хранит своё состояние:

```python
self.state
self.value
self.checked
self.dragging
```

Глобальный GUI state не используется.

## 13. Принципы SA_03 GUI

1. Один источник событий.
2. Один главный цикл.
3. Виджеты независимы.
4. `draw()` только отображает.
5. `update()` изменяет состояние.
6. `handle_event()` обрабатывает действия.
7. Простота важнее универсальности.
8. Решения документируются.

## Цель архитектуры

SA_03 не является универсальным GUI-фреймворком.

Это специализированная система интерфейса для Shadowing App, построенная вокруг pygame loop и собственных виджетов.