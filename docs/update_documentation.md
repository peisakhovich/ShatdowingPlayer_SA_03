# Обновление документации

После изменений в Python-коде выполнить из корня проекта:

### 1. Обновить страницы модулей

```powershell
py docs_generator.py
```

### 2. Обновить карту импортов

```powershell
py project_import_map.py
```

### 3. Обновить навигацию

```powershell
py docs_nav_generator.py
```

### 4. Обновить статистику проекта

```powershell
py project_statistics.py
```

### 5. Проверить сборку

```powershell
mkdocs build --strict
```

### 6. Запустить документацию

```powershell
.\run_docs.bat
```

Документация:

```text
http://127.0.0.1:8000/
```

### 7. Проверить Git

```powershell
git status
git diff
```

## Полная последовательность

```powershell
py docs_generator.py
py project_import_map.py
py docs_nav_generator.py
py project_statistics.py
mkdocs build --strict
.\run_docs.bat
git status
git diff
```
