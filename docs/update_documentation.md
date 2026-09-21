# Обновление документации

После изменений в Python-коде выполнить из корня проекта.

### 1. Обновить страницы модулей

```powershell
py -m tools.docs_generator
```

### 2. Обновить карту импортов

```powershell
py -m tools.project_import_map
```

### 3. Обновить статистику проекта

```powershell
py -m tools.project_statistics
```

### 4. Обновить список зависимостей

```powershell
py -m tools.project_dependencies
```

### 5. Обновить структуру проекта

```powershell
py -m tools.project_tree
```

### 6. Проверить документацию

```powershell
py -m tools.docs_audit
```

### 7. Обновить навигацию

```powershell
py -m tools.docs_nav_generator
```

### 8. Проверить сборку

```powershell
mkdocs build --strict
```

### 9. Запустить документацию

```powershell
.\run_docs.bat
```

Документация:

```text
http://127.0.0.1:8000/
```

### 10. Проверить Git

```powershell
git status
git diff
```

## Полная последовательность

```powershell
py -m tools.docs_generator
py -m tools.project_import_map
py -m tools.project_statistics
py -m tools.project_dependencies
py -m tools.project_tree
py -m tools.docs_audit
py -m tools.docs_nav_generator
mkdocs build --strict
.\run_docs.bat
git status
git diff
```
