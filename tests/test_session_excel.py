from session.session_excel import SessionExcel

def test_import_set(tmp_path):
    from openpyxl import Workbook
    from session.session_excel import SessionExcel

    excel_file = tmp_path / "test_import_set.xlsx"

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Set"

    worksheet.append(["Field", "Value"])
    worksheet.append(["set_index", 25])
    worksheet.append(["set_name", "Test Set"])
    worksheet.append(["set_description", "Test description"])

    workbook.create_sheet("Items")
    workbook.create_sheet("Voices")

    workbook.save(excel_file)
    workbook.close()

    result = SessionExcel.import_set(excel_file)

    assert result == {
        "set_index": 25,
        "set_name": "Test Set",
        "set_description": "Test description",
    }

def test_import_items(tmp_path):
    from openpyxl import Workbook

    excel_file = tmp_path / "test_import_items.xlsx"

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Items"

    worksheet.append(SessionExcel.ITEM_COLUMNS)

    worksheet.append([
        1,
        "pl",
        "B1",
        "Co to jest napięcie elektryczne?",
        "ru",
        "Что такое электрическое напряжение?",
        1,
        1960,
        1.0,
        1,
        "pl-PL",
        "pl-PL-MarekNeural",
        "Male",
        "ru-RU",
        "ru-RU-SvetlanaNeural",
        "Female",
    ])

    worksheet.append([
        2,
        "en",
        "A1",
        "Hello dad",
        "ru",
        "Привет папа",
        1,
        1500,
        1.0,
        1,
        "en-GB",
        "en-GB-LibbyNeural",
        "Female",
        "ru-RU",
        "ru-RU-DmitryNeural",
        "Male",
    ])

    workbook.create_sheet("Set")
    workbook.create_sheet("Voices")

    workbook.save(excel_file)
    workbook.close()

    result = SessionExcel.import_items(excel_file)

    assert len(result) == 2

    assert result[0] == {
        "item_order": 1,
        "phrase_code": "pl",
        "language_level": "B1",
        "phrase_text": "Co to jest napięcie elektryczne?",
        "translate_code": "ru",
        "translate_text": "Что такое электрическое напряжение?",
        "difficulty": 1,
        "pause_ms": 1960,
        "speed": 1.0,
        "repeat_count": 1,
        "phrase_locale": "pl-PL",
        "phrase_voice": "pl-PL-MarekNeural",
        "phrase_voice_gender": "Male",
        "translate_locale": "ru-RU",
        "translate_voice": "ru-RU-SvetlanaNeural",
        "translate_voice_gender": "Female",
    }

    assert result[1]["item_order"] == 2
    assert result[1]["phrase_code"] == "en"
    assert result[1]["language_level"] == "A1"
    assert result[1]["phrase_text"] == "Hello dad"
    assert result[1]["translate_text"] == "Привет папа"

def test_import_real_excel():
    from pathlib import Path

    excel_file = Path(
        "test_output/session_export.xlsx"
    )

    assert excel_file.exists(), (
        f"Не найден Excel-файл: {excel_file}"
    )

    set_data = SessionExcel.import_set(
        excel_file
    )

    items = SessionExcel.import_items(
        excel_file
    )

    print()
    print("Imported Set:")
    print(f"  set_index:      {set_data.get('set_index')}")
    print(f"  set_name:       {set_data.get('set_name')}")
    print(f"  description:    {set_data.get('set_description')}")

    print()
    print(f"Imported items:   {len(items)}")

    assert set_data["set_index"] == 2
    assert set_data["set_name"] == "Polisн  B2"
    assert (
        set_data["set_description"]
        == "Różne rozmowy na tematy biznesowe"
    )

    assert len(items) == 14

    assert items[0]["item_order"] == 1
    assert items[0]["phrase_code"] == "pl"
    assert items[0]["language_level"] == "B1"
    assert (
        items[0]["phrase_text"]
        == "Co to jest napięcie elektryczne?"
    )

    assert items[0]["translate_code"] == "ru"
    assert (
        items[0]["translate_text"]
        == "Что такое электрическое напряжение?"
    )

    assert items[-1]["item_order"] == 26