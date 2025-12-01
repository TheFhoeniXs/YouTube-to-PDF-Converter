import asyncio
import flet as ft
import re
from services.transcript import get_transcript 
from services.pdf_generate import create_pdf
from services.settings_manager import SettingsManager


class VideoQueue(ft.Container):
    #! Queue class that manages video tasks
    def __init__(self):
        super().__init__(bgcolor="#2a2a2a",padding=8,border_radius=8)
        self.tasks = []  #? List of all tasks
        self.current_task_index = 0  #? Index of currently running task
        self.is_started = False  #? Checks whether the queue has been started
        self.task_column = ft.Column(spacing=10,scroll=ft.ScrollMode.ALWAYS)  #? Column where tasks will be placed visually

        self.content = self.task_column

    def add_task(self, setting, title: str = ""):  #! Parameters order corrected
        #? Creates a new video task and adds it to the queue
        task = VideoTask(title=title, queue=self, setting=setting)
        self.tasks.insert(0, task)  #? New task is added to the beginning of the list
        self.task_column.controls = self.tasks  #? Also added to the beginning in UI
        self.expend_controle()
        self.update()
    
    def start_next_task(self):
        #? Starts the next task when a task is completed
        self.current_task_index += 1
        if self.current_task_index < len(self.tasks):
            if not self.tasks[self.current_task_index].is_running:
                next_task = self.tasks[self.current_task_index]
                next_task.start()
    
    def start_queue(self):
        #! Starts the queue and runs the first task
        if not self.is_started and len(self.tasks) > 0:
            if not self.tasks[0].is_running:
                self.is_started = True
                self.current_task_index = 0
                self.tasks[0].start()
                self.is_started = False
    
    def expend_controle(self):
        #? Controls expand property based on task count
        if 3 <= len(self.tasks):
            self.expand = True
        else:
            self.expand = False
    
    def remove_task(self, task):
        #! Removes task from queue and UI
        self.task_column.controls.remove(task)
        self.tasks.remove(task)
        self.expend_controle()
        self.update()


class VideoTask(ft.Container):
    #! Class representing a single video conversion task
    def __init__(self, title: str, queue: VideoQueue, setting: SettingsManager):
        super().__init__(bgcolor="#333131", border_radius=10, padding=15)
        self.title = title  #? Video ID or URL
        self.task = None  #? Asyncio task
        self.queue = queue  #? Reference to the queue it belongs to
        self.is_running = False  #? Whether the task is running
        self.is_complated = False  #? Whether the task is completed
        self.settings = setting

        #? UI components
        self.text = ft.Text(title, size=14, color=ft.Colors.WHITE70, overflow=ft.TextOverflow.ELLIPSIS, expand=True)
        self.status_bar = ft.ProgressBar(value=0, visible=False)  #? Progress bar
        self.status_text = ft.Text("API response awaited . . . ", size=13, visible=False, color="#008080")  #? Status message
        self.status_percent = ft.Text("%100", size=13, visible=False)  #? Percentage indicator
        
        #? Content of the task card
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(name=ft.Icons.PLAY_CIRCLE, color=ft.Colors.BLUE, size=30),
                        self.text,
                        ft.IconButton(icon=ft.Icons.CLOSE, icon_color=ft.Colors.WHITE70, icon_size=20, on_click=self.cancel_task)
                    ]
                ),
                self.status_bar,
                ft.Row(
                    [
                        self.status_text,
                        self.status_percent
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ]
        )
    
    def update_status(self, value: float, text: str):
        #? Updates task progress (progress bar and text)
        self.status_bar.visible = True
        self.status_percent.visible = True
        self.status_percent.value = f"%{int(value*100)}"
        self.status_text.visible = True
        self.status_text.value = text
        self.status_bar.value = value

        if value >= 1.0:  #? When task is completed, green color and "finished" message
            self.status_text.color = "#32cd32"
            self.status_text.value = "Finished"
        self.update()
    
    def cancel_task(self, e):
        #! Cancels the task and removes it from UI
        if self.task and not self.task.done():
            self.task.cancel()
        
        self.queue.remove_task(self)

    async def taskl(self):
        #! Main task function - get transcript and create PDF
        try:
            self.update_status(value=0.1, text="API response awaited . . . ")
            if self.settings.get_api_key():
                pdf_text_sheet = await get_transcript(self.title, api=self.settings.get_api_key())  #? Transcript is retrieved from API

            if self.settings.get_download_path():
                create_pdf(self.title, transcript_text=pdf_text_sheet, calback_func=self.update_status, output_dir=self.settings.get_download_path())  # type: ignore  #? PDF is created
            self.queue.start_next_task()  #? Move to next task after completion

        except asyncio.CancelledError:  #! If task is cancelled, move to next one
            if self.queue:
                self.queue.start_next_task()
    
    def start(self):
        #? Starts the task
        if not self.is_running and not self.is_complated:
            self.is_running = True
            self.task = self.page.run_task(self.taskl)  # type: ignore


class SettingsPanel(ft.Container):
    #! Settings panel for configuring API key and download path
    def __init__(self, setting: SettingsManager, filepicker: ft.FilePicker):
        super().__init__()
        self.settings = setting
        self.filepicker = filepicker
        
        #? Temporary folder path (not yet saved)
        self.temp_download_path = setting.get_download_path()
        
        #? API TextField
        self.api = ft.TextField(
            hint_text="Enter Your API Key",
            prefix_icon=ft.Icons.API_SHARP,
            border_radius=25,
            filled=True,
            bgcolor="#2a2a2a",
            border_color=ft.Colors.BLUE,
            focused_border_color=ft.Colors.GREEN_300,
            width=300,
            text_size=13,
            value=setting.get_api_key()
        )
        
        #? Download folder display
        self.dw_path = ft.Text(
            value=setting.get_download_path() or "No folder selected",
            size=12,
            color=ft.Colors.WHITE70,
            width=250,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        
        #? Status message
        self.status_text = ft.Text(
            "Settings saved ✓",
            color=ft.Colors.GREEN_300,
            visible=False,
            size=14
        )
        
        #! Main content structure
        self.content = ft.Container(
            content=ft.Column(
                [
                    #? API Key section
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("API Key", size=16, weight=ft.FontWeight.BOLD),
                                self.api
                            ],
                            spacing=10
                        ),
                        padding=ft.padding.only(bottom=20)
                    ),
                    
                    #? Download folder section
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Download Folder", size=16, weight=ft.FontWeight.BOLD),
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            text="Select Folder",
                                            icon=ft.Icons.FOLDER_OPEN,
                                            on_click=self.pick_folder,
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.Colors.BLUE_GREY_800,
                                                color=ft.Colors.WHITE
                                            )
                                        ),
                                        self.dw_path
                                    ],
                                    spacing=15,
                                    alignment=ft.MainAxisAlignment.START
                                )
                            ],
                            spacing=10
                        ),
                        padding=ft.padding.only(bottom=20)
                    ),
                    
                    #? Status message display
                    self.status_text,
                    
                    #? Save button
                    ft.ElevatedButton(
                        text="Save Settings",
                        icon=ft.Icons.SAVE,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE,
                            padding=20
                        ),
                        height=60,
                        width=float('inf'),
                        on_click=self.save_settings
                    )
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=20
        )
    
    def pick_folder(self, e):
        #! Opens folder selection dialog
        self.filepicker.get_directory_path(dialog_title="Select download folder")
    
    def update_temp_folder_path(self, path: str):
        #? Temporarily update selected folder path (not yet saved)
        self.temp_download_path = path
        self.dw_path.value = path
        self.status_text.visible = False  #? Hide not-yet-saved message
        self.update()
    
    def save_settings(self, e):
        #! Permanently save settings
        #? Save API Key
        if self.api.value:
            self.settings.set_api_key(self.api.value)
        
        #? Save download folder
        if self.temp_download_path:
            self.settings.set_download_path(self.temp_download_path)
        
        #? Show success message
        self.status_text.visible = True
        self.update()
        
        #! Hide message after 2 seconds
        import threading
        def hide_status():
            import time
            time.sleep(2)
            self.status_text.visible = False
            self.update()
        
        threading.Thread(target=hide_status, daemon=True).start()


def check_api_dwpath(setting: SettingsManager):
    #! Check if API and download folder are configured
    if setting.get_api_key() == "":
        return False
    elif setting.get_download_path() == "":
        return False
    else:
        return True


def extract_youtube_id(url: str) -> str | None:
    #! Extracts video ID from YouTube URL
    #? Different YouTube URL format patterns
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})(?:[&?]|$)',  #? watch?v= or youtu.be/
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',  #? embed/
        r'youtube\.com/v/([a-zA-Z0-9_-]{11})',  #? /v/
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def validate_youtube_url(e, queue: VideoQueue, setting: SettingsManager):
    #! YouTube URL validation and task addition function
    if not e.control.value:
        return
    
    url = e.control.value.strip()
    
    #? Extract video ID
    video_id = extract_youtube_id(url)

    if video_id:
        #! Valid URL
        e.control.error_text = None
        e.control.border_color = ft.Colors.BLUE
        queue.add_task(setting=setting, title=video_id)
        e.control.value = None  #? Clear input
    else:
        #! Invalid URL
        e.control.error_text = "❌ Invalid YouTube URL"
        e.control.border_color = ft.Colors.RED
    
    e.page.update()


def main(page: ft.Page):
    #! Main application function
    #? Window settings
    page.title = "Transcriptor"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 421
    page.window.height = 681
    page.window.resizable = False
    page.padding = 0
    page.bgcolor = "#1a1a1a"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    settings = SettingsManager("services/settings/settings.json")
    
    #! Store SettingsPanel reference
    settings_panel_ref = None
    
    def on_folder_result(e: ft.FilePickerResultEvent):
        #? FilePicker callback - runs when folder is selected
        if e.path and settings_panel_ref:
            #? Temporarily update (not yet saved)
            settings_panel_ref.update_temp_folder_path(e.path)
    
    #? Create FilePicker
    file_pickers = ft.FilePicker(on_result=on_folder_result)
    
    #! Create SettingsPanel and store reference
    settings_panel_ref = SettingsPanel(setting=settings, filepicker=file_pickers)

    #? Alert Dialog for settings
    dlg = ft.AlertDialog(
        title=ft.Text("Settings", size=20, weight=ft.FontWeight.BOLD),
        content=settings_panel_ref,
        alignment=ft.alignment.center,
    )

    page.overlay.append(file_pickers)
    
    video_queue = VideoQueue()  #? Create video queue
    
    #? Header section - Logo and title
    header = ft.Container(
        content=ft.Row(
            [
                ft.Icon(name=ft.Icons.PICTURE_AS_PDF, color=ft.Colors.BLUE, size=40),
                ft.Text("Transcriptor", size=32, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=20,
    )
    
    #? URL input field
    url_input = ft.TextField(
        hint_text="Enter YouTube Video URL",
        prefix_icon=ft.Icons.PLAY_CIRCLE_OUTLINE,
        border_radius=25,
        filled=True,
        bgcolor="#2a2a2a",
        border_color=ft.Colors.BLUE,
        focused_border_color=ft.Colors.BLUE_400,
        height=60,
        text_size=16,
        on_blur=lambda e: validate_youtube_url(e, video_queue, settings)  #? Validate URL on focus loss
    )
    
    #? YouTube video link display area
    video_link_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "YouTube Video Link",
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.WHITE,
                ),
                ft.Container(height=10),
            ],
            spacing=0,
        ),
        padding=ft.padding.only(top=20, bottom=20),
    )
    
    #? Convert to PDF button
    convert_button = ft.ElevatedButton(
        text="Convert to PDF",
        icon=ft.Icons.DOWNLOAD,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE,
            padding=20,
        ),
        height=60,
        width=float('inf'),
        on_click=lambda e: video_queue.start_queue() if check_api_dwpath(setting=settings) else page.open(dlg)  #? Open dialog if settings are missing
    )
    
    #? Main content container - Contains all components
    main_content = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.IconButton(icon=ft.Icons.SETTINGS, on_click=lambda e: page.open(dlg))], alignment=ft.MainAxisAlignment.END),
                header,
                ft.Container(height=20),
                url_input,
                video_link_container,
                video_queue,  #? Task queue is placed here
                ft.Container(height=20),
                convert_button,
            ],
            spacing=0,
        ),
        padding=20,
        expand=True,
    )
    
    #? Responsive container - Fixed width
    responsive_container = ft.Container(
        content=main_content,
        width=500,
        alignment=ft.alignment.top_center,
    )
    
    #! Add main container to page
    page.add(
        ft.Container(
            content=responsive_container,
            alignment=ft.alignment.top_center,
            expand=True,
        )
    )


#! Start the application
ft.app(target=main)