from __future__ import annotations

import asyncio

import pygame

from api.client import ApiClient
from core.config import Config
from core.logger import logger
from gui.theme import Theme
from gui.widgets.busy_indicator import BusyIndicator
from gui.widgets.list_selection import ListSelection
from audio.async_runner import AsyncRunner
from gui.panels.control_panel_db import ControlPanel
from gui.login_register_window import LoginRegisterWindow
from gui.widgets.text_edit import TextEdit
from gui.file_dialog import FileDialog
from session.session_excel import SessionExcel
from audio.tts import TTS
from gui.dialogs.dialog import Dialog


class DatabaseWindow:
    """Окно работы с базой данных."""

    def __init__(self, rect, font_manager, image_loader, session):

        # --------------------------------------------------
        # Основные данные
        # --------------------------------------------------

        self.rect = pygame.Rect(rect)
        self.font_manager = font_manager
        self.session = session
        self.visible = False

        self.control_panel = ControlPanel(
            font_manager,
            image_loader
        )


        # --------------------------------------------------
        # Async
        # --------------------------------------------------

        self._async_runner = AsyncRunner()

        self._get_sets_task = None
        self._get_set_task = None
        self._save_set_task = None
        self._update_set_data_task = None
        self._delete_set_task = None
        self._export_excel_task = None
        self._export_excel_filename = None
        self.active_dialog = None
        self._pending_action = None

        # --------------------------------------------------
        # Data
        # --------------------------------------------------

        self.sets = []
        self.selected_set = None
        self._pending_selected_set_id = None
        



        # --------------------------------------------------
        # Close button
        # --------------------------------------------------

        self.close_rect = pygame.Rect(
            self.rect.right - 30,
            self.rect.top + 10,
            20,
            20,
        )

        # --------------------------------------------------
        # Busy indicator
        # --------------------------------------------------

        self.busy_indicator = BusyIndicator(
            self.rect,
            self.font_manager.load(22)
        )

        # --------------------------------------------------
        # API client
        # --------------------------------------------------

        self.api_client = ApiClient(
            Config.API_BASE_URL
        )

        # --------------------------------------------------
        # Login / Register window
        # --------------------------------------------------

        self.login_register_window = LoginRegisterWindow(
            pygame.Rect(
                self.rect.centerx - 250,
                self.rect.centery - 320,
                500,
                500
            ),
            font_manager,
            session,
            self.api_client
        )

        # --------------------------------------------------
        # Sets selection
        # --------------------------------------------------

        self.set_selection = ListSelection(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 95,
                self.rect.width - 60,
                30
            ),
            [("", "Loading...")],
            0
        )

 
        # --------------------------------------------------
        # Set name editor
        # --------------------------------------------------

        self.set_name_edit = TextEdit(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 270,
                self.rect.width - 60,
                40
            ),
            self.font_manager.load(20)
        )

        # --------------------------------------------------
        # Set description editor
        # --------------------------------------------------

        self.description_edit = TextEdit(
            pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 345,
                self.rect.width - 60,
                80
            ),
            self.font_manager.load(20)
        )

    # --------------------------------------------------
    # Показать диалог на действия по кнопкам 
    # --------------------------------------------------

    def show_buttons_dialog(self,action):

        self._pending_action = action

        if action == "login":
            message = "Do you want to login?"

        elif action == "register":
            message = "Do you want to register?"

        elif action == "dropset":
            message = "Do you want to delete this set?"

        elif action == "datatodb":
            message = "Do you want to save changes name & description to this set in the database?"  

        elif action == "dbtoset":
            message = "Do you want to load this set from the database into the session?" 

        elif action == "settodb":
            message = "Do you want to save the session to the database?"

        elif action == "exceltoset":
            message = "Do you want to load data from Excel into the session?"                

        else:
            message = "Do you want to do it?"
            

        self.active_dialog = Dialog(

            parent_rect=self.rect,

            font_manager=self.font_manager,

            title="Action",

            message=message,

            buttons=[
                "Yes",
                "No",

                ],
            default_button=1     
        )

        self.active_dialog.show()

    # ==================================================
    # VISIBILITY
    # ==================================================

    def show(self):

        self.visible = True

        self._load_sets()

    # --------------------------------------------------

    def hide(self):

        self._cancel_tasks()

        self.visible = False

    # ==================================================
    # FOCUS
    # ==================================================

    def _clear_edit_focus(self):

        self.set_name_edit.focused = False
        self.description_edit.focused = False

        pygame.key.stop_text_input()

    # --------------------------------------------------

    def _focus_next_edit(self, backward=False):

        edits = [
            self.set_name_edit,
            self.description_edit,
        ]

        current_index = -1

        for index, edit in enumerate(edits):

            if edit.focused:
                current_index = index
                break

        # Если ни одно поле не имеет фокуса
        if current_index == -1:

            next_index = (
                len(edits) - 1
                if backward
                else 0
            )

        else:

            if backward:
                next_index = (
                    current_index - 1
                ) % len(edits)

            else:
                next_index = (
                    current_index + 1
                ) % len(edits)

        self._clear_edit_focus()

        edits[next_index].focused = True

        pygame.key.start_text_input()

    # ==================================================
    # API
    # ==================================================

    def _load_sets(self):

        if self._get_sets_task is not None:

            if not self._get_sets_task.done():
                return

        user_id = self.session.user_id

        if not user_id:

            logger.warning(
                "Session has no user_id"
            )

            self.set_selection.options = [
                ("", "No user")
            ]

            self.set_selection.selected = 0
            self.selected_set = None

            return

        self.busy_indicator.show(
            "Loading sets..."
        )

        self.set_selection.options = [
            ("", "Loading...")
        ]

        self.set_selection.selected = 0

        self.selected_set = None

        self._get_sets_task = self._async_runner.submit(
            self._get_sets_async(user_id)
        )

    # --------------------------------------------------

    async def _get_sets_async(self, user_id):

        return await asyncio.to_thread(
            self.api_client.get_sets,
            user_id
        )

    # --------------------------------------------------

    async def _get_set_async(self, set_id):

        return await asyncio.to_thread(
            self.api_client.get_set,
            set_id
        )

    # --------------------------------------------------
    async def _get_tts_voices_async(self):

        return await TTS().get_voices()

    # --------------------------------------------------

    async def _save_set_async(self, user_id, data):

        return await asyncio.to_thread(
            self.api_client.save_set,
            user_id,
            data
        )

    # --------------------------------------------------  

    async def _update_set_data_async(self, set_id, set_name, set_description):

        return await asyncio.to_thread(
            self.api_client.update_set,
            set_id,
            set_name,
            set_description
        )

    # --------------------------------------------------  

    async def _delete_set_async(self, set_id):

        return await asyncio.to_thread(
            self.api_client.delete_set,
            set_id
        )


    # ==================================================
    # PROCESS GET SETS RESULT
    # ==================================================

    def _process_get_sets_task(self):

        if self._get_sets_task is None:
            return

        if not self._get_sets_task.done():
            return

        task = self._get_sets_task
        self._get_sets_task = None

        try:

            self.sets = task.result()

            logger.info(
                "Database sets loaded:",
                len(self.sets)
            )

        except asyncio.CancelledError:

            return

        except Exception as e:

            logger.error(
                "Database API error:",
                e
            )

            self.sets = []

            self.set_selection.options = [
                ("", "Error loading sets")
            ]

            self.set_selection.selected = 0
            self.selected_set = None

            return

        finally:

            self.busy_indicator.hide()

        # --------------------------------------------------
        # Нет sets
        # --------------------------------------------------

        if not self.sets:

            self.set_selection.options = [
                ("", "No sets")
            ]

            self.set_selection.selected = 0
            self.selected_set = None

            return

        # --------------------------------------------------
        # Формируем ListSelection
        # --------------------------------------------------

        options = []

        for item in self.sets:

            set_id = item.get(
                "set_id",
                ""
            )

            set_index = item.get(
                "set_index",
                ""
            )

            set_name = item.get(
                "set_name",
                ""
            )

            set_description = item.get(
                "set_description",
                ""
            )

            items_count = item.get(
                "items_count",
                0
            )

            caption = (
                f"{set_index}  |  "
                f"{set_name}  |  "
                f"{set_description}  |  "
                f"{items_count} items"
            )

            options.append(
                (
                    set_id,
                    caption
                )
            )

        self.set_selection.options = options


        # --------------------------------------------------
        # Восстанавливаем ранее выбранный set
        # --------------------------------------------------

        selected_index = 0

        if self._pending_selected_set_id is not None:

            for index, option in enumerate(options):

                if option[0] == self._pending_selected_set_id:

                    selected_index = index
                    break

        self.set_selection.selected = selected_index

        self._update_selected_set(
            options[selected_index][0]
        )

        # Запоминаемый set больше не нужен
        self._pending_selected_set_id = None


    # ==================================================
    # PROCESS UPDATE SET RESULT
    # ==================================================

    def _process_update_set_data_task(self):

        if self._update_set_data_task is None:
            return

        if not self._update_set_data_task.done():
            return

        task = self._update_set_data_task
        self._update_set_data_task = None

        try:

            result = task.result()

            logger.info(
                "Data saved to database:",
                result
            )
            # Сохраняем set_id, чтобы после обновления
            # списка вернуть выбор на этот же набор.
            self._pending_selected_set_id = result.get(
                "set_id"
            )

            # --------------------------------------------------
            # Refresh sets list after successful save
            # --------------------------------------------------
            self._load_sets()

        except asyncio.CancelledError:

            return

        except Exception as e:

            logger.error(
                "UPDATE  set API error:",
                e
            )

        finally:

            self.busy_indicator.hide()

    # ==================================================
    # PROCESS DELETE SET RESULT
    # ==================================================

    def _process_delete_set_task(self):

        if self._delete_set_task is None:
            return

        if not self._delete_set_task.done():
            return

        task = self._delete_set_task
        self._delete_set_task = None

        try:

            result = task.result()

            logger.info(
                "Data deleted from database:",
                result
            )

            # --------------------------------------------------
            # После удаления выбранного набора
            # --------------------------------------------------

            self.selected_set = None
            self._pending_selected_set_id = None

            self.set_name_edit.clear()
            self.description_edit.clear()

            # --------------------------------------------------
            # Refresh sets list
            # --------------------------------------------------

            self._load_sets()

        except asyncio.CancelledError:

            return

        except Exception as e:

            logger.error(
                "DELETE set API error:",
                e
            )

        finally:

            self.busy_indicator.hide()

    # ==================================================
    # PROCESS EXPORT EXCEL TASK
    # ==================================================
    def _process_export_excel_task(self):

        if self._export_excel_task is None:
            return

        if not self._export_excel_task.done():
            return

        task = self._export_excel_task
        self._export_excel_task = None

        try:

            voices_raw = task.result()

            voices = [
                {
                    "short_name": voice.get("ShortName", ""),
                    "locale": voice.get("Locale", ""),
                    "locale_name": voice.get("LocaleName", ""),
                    "gender": voice.get("Gender", ""),
                    "friendly_name": voice.get("FriendlyName", ""),
                }
                for voice in voices_raw
            ]

            SessionExcel.export(
                self.session,
                self._export_excel_filename,
                voices=voices
            )

            logger.info(
                f"Session exported to Excel: "
                f"{self._export_excel_filename}"
            )

        except asyncio.CancelledError:

            logger.debug(
                "Excel export task cancelled"
            )

        except Exception as e:

            logger.error(
                f"Excel export error: {e}"
            )

        finally:

            self._export_excel_filename = None



    # ==================================================
    # PROCESS GET SET RESULT
    # ==================================================

    def _process_get_set_task(self):

        if self._get_set_task is None:
            return

        if not self._get_set_task.done():
            return

        task = self._get_set_task
        self._get_set_task = None

        try:

            data = task.result()

            self.session.load_data(data)
            self.session.save(Config.PLAN_SESSION_FILE)

            logger.info(
                f"Set loaded into session: {self.session.id}"
            )

        except asyncio.CancelledError:

            return

        except Exception as e:

            logger.error(
                "GET set API error:",
                e
            )

        finally:

            self.busy_indicator.hide()

    # ==================================================
    # PROCESS SAVE SET RESULT
    # ==================================================

    def _process_save_set_task(self):

        if self._save_set_task is None:
            return

        if not self._save_set_task.done():
            return

        task = self._save_set_task
        self._save_set_task = None

        try:

            result = task.result()

            logger.info(
                "Session saved to database:",
                result
            )
            # --------------------------------------------------
            # Refresh sets list after successful save
            # --------------------------------------------------
            self._load_sets()

        except asyncio.CancelledError:

            return

        except Exception as e:

            logger.error(
                "SAVE  set API error:",
                e
            )

        finally:

            self.busy_indicator.hide()

    # ==================================================
    # SELECTED SET
    # ==================================================

    def _update_selected_set(self, set_id):

        self.selected_set = None

        for item in self.sets:

            if item.get("set_id") == set_id:

                self.selected_set = item
                break

        if self.selected_set:

            logger.debug(
                "Selected set:",
                self.selected_set.get(
                    "set_name",
                    ""
                )
            )

            # --------------------------------------------------
            # Заполняем редакторы данными выбранного набора
            # --------------------------------------------------

            self.set_name_edit.set_text(
                self.selected_set.get(
                    "set_name",
                    ""
                )
            )

            self.description_edit.set_text(
                self.selected_set.get(
                    "set_description",
                    ""
                )
            )

        else:

            self.set_name_edit.clear()
            self.description_edit.clear()

    # ==================================================
    # DELETE SELECTED SET
    # ==================================================

    def _delete_selected_set(self):

        if self.selected_set is None:

            logger.warning(
                "No set selected"
            )

            return

        set_id = self.selected_set.get(
            "set_id"
        )

        if not set_id:

            logger.warning(
                "Selected set has no set_id"
            )

            return

        if self._delete_set_task is not None:

            if not self._delete_set_task.done():
                return

        logger.debug(
            f"DROPSET set_id={set_id}"
        )

        self.busy_indicator.show(
            "Deleting set..."
        )

        self._delete_set_task = (
            self._async_runner.submit(
                self._delete_set_async(
                    set_id
                )
            )
        )

    # ==================================================
    # UPDATE SELECTED SET DATA
    # ==================================================

    def _update_selected_set_data(self):

        if self.selected_set is None:

            logger.warning(
                "No set selected"
            )

            return

        set_id = self.selected_set.get(
            "set_id"
        )

        if not set_id:

            logger.warning(
                "Selected set has no set_id"
            )

            return

        if self._update_set_data_task is not None:

            if not self._update_set_data_task.done():
                return

        # --------------------------------------------------
        # Получаем данные из редакторов
        # --------------------------------------------------

        set_name = self.set_name_edit.get_text().strip()
        set_description = self.description_edit.get_text().strip()

        # --------------------------------------------------
        # Проверка имени
        # --------------------------------------------------

        if not set_name:

            logger.warning(
                "Set name is empty"
            )

            return

        logger.debug(
            f"DATATODB set_id={set_id}"
        )

        # --------------------------------------------------
        # UPDATE
        # --------------------------------------------------

        self.busy_indicator.show(
            "Saving data of set..."
        )

        self._update_set_data_task = (
            self._async_runner.submit(
                self._update_set_data_async(
                    set_id,
                    set_name,
                    set_description
                )
            )
        )

    # ==================================================
    # LOAD SELECTED SET FROM DATABASE INTO SESSION
    # ==================================================

    def _load_selected_set_to_session(self):

        if self.selected_set is None:

            logger.warning(
                "No set selected"
            )

            return

        set_id = self.selected_set.get(
            "set_id"
        )

        if not set_id:

            logger.warning(
                "Selected set has no set_id"
            )

            return

        if self._get_set_task is not None:

            if not self._get_set_task.done():
                return

        logger.debug(
            f"DBTOSET set_id={set_id}"
        )

        self.busy_indicator.show(
            "Loading set..."
        )

        self._get_set_task = (
            self._async_runner.submit(
                self._get_set_async(
                    set_id
                )
            )
        )

    # ==================================================
    # SAVE SESSION TO DATABASE
    # ==================================================

    def _save_session_to_database(self):

        if self.session.is_empty():

            logger.warning(
                "Session is empty"
            )

            return

        user_id = self.session.user_id

        if not user_id:

            logger.warning(
                "Session has no user_id"
            )

            return

        if self._save_set_task is not None:

            if not self._save_set_task.done():
                return

        data = self.session.get_data()

        logger.debug(
            f"SETTO​DB user_id={user_id}"
        )

        logger.debug(
            f"SETTO​DB data items={len(data.get('items', []))}"
        )

        self.busy_indicator.show(
            "Saving set..."
        )

        self._save_set_task = (
            self._async_runner.submit(
                self._save_set_async(
                    user_id,
                    data
                )
            )
        )

    # ==================================================
    # TASKS
    # ==================================================

    def _cancel_tasks(self):

        if self._get_sets_task is not None:

            if not self._get_sets_task.done():
                self._get_sets_task.cancel()

        self._get_sets_task = None

        if self._get_set_task is not None:

            if not self._get_set_task.done():
                self._get_set_task.cancel()

        self._get_set_task = None

        if self._save_set_task is not None:

            if not self._save_set_task.done():
                self._save_set_task.cancel()

        self._save_set_task = None

        if self._update_set_data_task is not None:

            if not self._update_set_data_task.done():
                self._update_set_data_task.cancel()

        self._update_set_data_task = None

        self.busy_indicator.hide()

        if self._delete_set_task is not None:

            if not self._delete_set_task.done():
                self._delete_set_task.cancel()

        self._delete_set_task = None

        if self._export_excel_task is not None:

            if not self._export_excel_task.done():
                self._export_excel_task.cancel()

        self._export_excel_task = None
        self._export_excel_filename = None


    # ==================================================
    # EXCEL
    # ==================================================

    def _export_session_to_excel(self):

        if self.session.is_empty():

            logger.warning(
                "Session is empty"
            )

            return

        filename = FileDialog.save_file(
            title="Export session to Excel",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("All files", "*.*"),
            ],
            initial_file="session_export.xlsx",
            defaultextension=".xlsx",
        )

        if not filename:

            logger.debug(
                "Excel export cancelled"
            )

            return

        if not filename.lower().endswith(".xlsx"):
            filename += ".xlsx"
        
        self._export_excel_filename = filename

        self._export_excel_task = (
            self._async_runner.submit(
                self._get_tts_voices_async()
            )
        )
 

    # --------------------------------------------------

    def _import_session_from_excel(self):

        filename = FileDialog.open_file(
            title="Import session from Excel",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("All files", "*.*"),
            ],
        )

        if not filename:

            logger.debug(
                "Excel import cancelled"
            )

            return

        try:

            SessionExcel.import_(
                self.session,
                filename
            )

            self.session.save(
                Config.PLAN_SESSION_FILE
            )

            logger.info(
                f"Session imported from Excel: {filename}"
            )

        except Exception as e:

            logger.error(
                f"Excel import error: {e}"
            )


    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if not self.visible:
            return

        if self.active_dialog:

            self.active_dialog.update()     

        else:
                
            self._process_get_sets_task()
            self._process_get_set_task()
            self._process_save_set_task()
            self._process_update_set_data_task()
            self._process_delete_set_task()
            self._process_export_excel_task()

            
            self.set_name_edit.update()
            self.description_edit.update()

            self.control_panel.update()
            self.login_register_window.update()

            self.busy_indicator.update()

    # ==================================================
    # EVENTS
    # ==================================================

    def handle_event(self, event):

        if not self.visible:
            return

        # Если открыт модальный диалог,
        # он получает события первым.
        #

        if self.active_dialog:

            result = self.active_dialog.handle_event(event)

            if result == 0:

                action = self._pending_action

                self.active_dialog = None
                self._pending_action = None

                if action == "login":
                    self.login_register_window.show("login")

                elif action == "register":
                    self.login_register_window.show("register")

                elif action == "dropset":
                    self._delete_selected_set()

                elif action == "datatodb":
                    self._update_selected_set_data()    

                elif action == "dbtoset":
                    self._load_selected_set_to_session() 

                elif action == "settodb":
                    self._save_session_to_database()

                elif action == "exceltoset":
                    self._import_session_from_excel()           

            elif result == 1:

                self.active_dialog = None
                self._pending_action = None

            return None

        
        # --------------------------------------------------
        # Login / Register window
        # --------------------------------------------------

        if self.login_register_window.visible:

            self.login_register_window.handle_event(
                event
            )

            result = self.login_register_window.result

            if result is not None:

                action = result.get("action")

                if action in ("login", "register"):

                    user_id = self.session.user_id

                    if user_id:

                        self.busy_indicator.show(
                            "Loading sets..."
                        )

                        self._get_sets_task = (
                            self._async_runner.submit(
                                self._get_sets_async(user_id)
                            )
                        )

                        # Обработали результат.
                        self.login_register_window.result = None

            return

        # --------------------------------------------------
        # Передаем событие панели управления
        # --------------------------------------------------

        command = self.control_panel.handle_event(event)

        if command is not None:

            match command:

                case ("button", name):

                    logger.debug(
                        f"Button: {name}"
                    )

                    # --------------------------------------------------
                    # LOGIN
                    # --------------------------------------------------

                    if name == "login":

                        self.show_buttons_dialog("login")

                        return

                    # --------------------------------------------------
                    # REGISTER
                    # --------------------------------------------------

                    if name == "register":

                        self.show_buttons_dialog("register")

                        return

                    # --------------------------------------------------
                    # DB -> SESSION
                    # --------------------------------------------------

                    if name == "dbtoset":

                        if self.selected_set is None:

                            logger.warning(
                                "No set selected"
                            )

                            return

                        self.show_buttons_dialog("dbtoset")

                        return

                    # --------------------------------------------------
                    # SESSION -> DB
                    # --------------------------------------------------

                    if name == "settodb":

                        if self.session.is_empty():

                            logger.warning(
                                "Session is empty"
                            )

                            return

                        if not self.session.user_id:

                            logger.warning(
                                "Session has no user_id"
                            )

                            return

                        self.show_buttons_dialog("settodb")

                        return

                    # --------------------------------------------------
                    # SESSION -> EXCEL
                    # --------------------------------------------------

                    if name == "settoexcel":

                        self._export_session_to_excel()

                        return

                    # --------------------------------------------------
                    # EXCEL -> SESSION
                    # --------------------------------------------------

                    if name == "exceltoset":

                        self.show_buttons_dialog("exceltoset")

                        return

                    
                    # --------------------------------------------------
                    # DATA -> DB (name,description)
                    # --------------------------------------------------
                    if name == "datatodb":

                        if self.selected_set is None:

                            logger.warning(
                                "No set selected"
                            )

                            return

                        set_name = self.set_name_edit.get_text().strip()

                        if not set_name:

                            logger.warning(
                                "Set name is empty"
                            )

                            return

                        self.show_buttons_dialog("datatodb")

                        return
                    
                    # --------------------------------------------------
                    # DROP SET
                    # --------------------------------------------------
                    if name == "dropset":

                        if self.selected_set is None:

                            logger.warning(
                                "No set selected"
                            )

                            return

                        self.show_buttons_dialog("dropset")

                        return
                        

        # --------------------------------------------------
        # Close while busy
        # --------------------------------------------------

        if (
            self.busy_indicator.visible
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.close_rect.collidepoint(event.pos)
        ):

            self.hide()
            return

        # --------------------------------------------------
        # Block interaction while loading
        # --------------------------------------------------

        if self.busy_indicator.visible:
            return

        # --------------------------------------------------
        # Close
        # --------------------------------------------------

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.close_rect.collidepoint(event.pos)
        ):
            self.hide()
            return

        # --------------------------------------------------
        # Mouse button
        # --------------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                return

            # Если список уже открыт,
            # передаём ему любой левый клик.
            # ListSelection сам определит:
            # - выбор элемента;
            # - клик по control;
            # - клик вне списка.
            if self.set_selection.opened:

                result = self.set_selection.handle_event(event)

                if result is not None:
                    set_id = result[1]
                    self._update_selected_set(set_id)

                return

            # Список закрыт — передаём событие
            # только если клик по самому control.
            if self.set_selection.rect.collidepoint(event.pos):

                result = self.set_selection.handle_event(event)

                if result is not None:
                    set_id = result[1]
                    self._update_selected_set(set_id)

                return


            # --------------------------------------------------
            # Set name editor
            # --------------------------------------------------

            if self.set_name_edit.rect.collidepoint(event.pos):

                # Снимаем фокус с обоих полей
                self._clear_edit_focus()

                # Передаём клик только выбранному полю
                self.set_name_edit.handle_event(
                    event
                )

                return

            # --------------------------------------------------
            # Description editor
            # --------------------------------------------------

            if self.description_edit.rect.collidepoint(event.pos):

                # Снимаем фокус с обоих полей
                self._clear_edit_focus()

                # Передаём клик только выбранному полю
                self.description_edit.handle_event(
                    event
                )

                return

            # --------------------------------------------------
            # Клик вне полей
            # --------------------------------------------------
            self._clear_edit_focus()
            return

        # --------------------------------------------------
        # Mouse wheel
        # --------------------------------------------------

        if event.type == pygame.MOUSEWHEEL:

            self.set_selection.handle_event(event)

            return

        # --------------------------------------------------
        # Tab — переход между полями
        # --------------------------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_TAB:

                self._focus_next_edit(
                    backward=bool(
                        event.mod & pygame.KMOD_SHIFT
                    )
                )

                return

        # --------------------------------------------------
        # Keyboard / text input / mouse wheel
        # --------------------------------------------------

        self.set_name_edit.handle_event(event)
        self.description_edit.handle_event(event)



    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        if not self.visible:
            return

        # --------------------------------------------------
        # Fonts
        # --------------------------------------------------

        title_font = self.font_manager.load(24)

        caption_font = self.font_manager.load(20)

        list_font = self.font_manager.load(16)

        # --------------------------------------------------
        # Background
        # --------------------------------------------------

        pygame.draw.rect(
            screen,
            Theme.DIALOG_BACKGROUND_COLOR,
            self.rect,
            border_radius=Theme.DIALOG_RADIUS,
        )

        pygame.draw.rect(
            screen,
            Theme.DIALOG_BORDER_COLOR,
            self.rect,
            width=Theme.TB_BORDER_WIDTH,
            border_radius=Theme.DIALOG_RADIUS,
        )

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        title = title_font.render(
            "Database",
            True,
            Theme.DIALOG_TITLE_COLOR
        )

        screen.blit(
            title,
            (
                self.rect.x + 15,
                self.rect.y + 12
            )
        )
        

        user_id = self.session.user_id
        user_nickname = self.session.user_nickname

        if user_id:
            user_text = f"User: {user_nickname}  (ID: {user_id})"
        else:
            user_text = "User: guest"

        user = caption_font.render(
            user_text,
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            user,
            (
                self.rect.x + 30,
                self.rect.y + 48
            )
        )


        # --------------------------------------------------
        # Close
        # --------------------------------------------------

        x = self.close_rect

        pygame.draw.rect(
            screen,
            Theme.DIALOG_BACKGROUND_COLOR,
            self.close_rect
        )

        pygame.draw.line(
            screen,
            Theme.DIALOG_TITLE_COLOR,
            (x.left + 5, x.top + 5),
            (x.right - 5, x.bottom - 5),
            2,
        )

        pygame.draw.line(
            screen,
            Theme.DIALOG_TITLE_COLOR,
            (x.right - 5, x.top + 5),
            (x.left + 5, x.bottom - 5),
            2,
        )

        # --------------------------------------------------
        # Training sets
        # --------------------------------------------------

        caption = caption_font.render(
            "Name:",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            caption,
            (
                self.set_name_edit.rect.x,                
                self.set_name_edit.rect.y - 25
            )
        )

        # --------------------------------------------------
        # Description
        # --------------------------------------------------

        text = caption_font.render(
            "Description:",
            True,
            Theme.DIALOG_TEXT_COLOR
        )

        screen.blit(
            text,
            (
                self.description_edit.rect.x ,
                self.description_edit.rect.y - 25
            )
        )

 


        # --------------------------------------------------
        # Set information
        # --------------------------------------------------

        if self.selected_set:

            set_index = self.selected_set.get(
                "set_index",
                ""
            )

            items_count = self.selected_set.get(
                "items_count",
                0
            )

            info_y = self.set_selection.rect.bottom + 35



            # --------------------------------------------------
            # Items count
            # --------------------------------------------------

            text = caption_font.render(
                f"Training sets - count items: {items_count}",
                True,
                Theme.DIALOG_TEXT_COLOR
            )

            screen.blit(
                text,
                (
                    self.rect.x + 30,
                    info_y + 35
                )
            )



        self.control_panel.draw(
            screen
        )

        self.set_name_edit.draw(
            screen
        )
        self.description_edit.draw(
            screen
        )


        # --------------------------------------------------
        # ListSelection
        # --------------------------------------------------
        # Рисуем последним, чтобы раскрытый список
        # был поверх остальных элементов.

        self.set_selection.draw(
            screen,
            list_font
        )

        # --------------------------------------------------
        # Busy indicator
        # --------------------------------------------------

        self.busy_indicator.draw(
            screen
        )

        # --------------------------------------------------
        # Login / Register window
        # --------------------------------------------------
        
        self.login_register_window.draw(
            screen
        )

        # --------------------------------------------------
        # Active dialog
        # --------------------------------------------------    

        if self.active_dialog:

            self.active_dialog.draw(
                screen
            )
        