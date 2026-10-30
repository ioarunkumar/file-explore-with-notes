import sys
import os
import sqlite3
from datetime import datetime

from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QDesktopServices, QIcon, QPainter, QPixmap, QColor
from PySide6.QtWidgets import QFileIconProvider
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QColorDialog,
)


# ============================================================
# TODO LIST
# ============================================================

TODO = [
    "Create Windows desktop application",
    "Browse files and folders",
    "Show Name column",
    "Show Date Modified column",
    "Show Type column",
    "Show Size column",
    "Add Notes column",
    "Save notes using SQLite",
    "Edit notes directly in the table",
    "Open folders by double-clicking",
    "Open files using Windows default application",
    "Add Back navigation",
    "Add path/address bar",
    "Search filenames",
    "Search notes",
    "Keep folders above files",

    # Future improvements
    "TODO: Add Forward navigation",
    "TODO: Add file and folder icons",
    "TODO: Add breadcrumbs navigation",
    "TODO: Add right-click context menu",
    "TODO: Add tags",
    "TODO: Add favorites",
    "TODO: Make notes survive file renaming/moving",
    "TODO: Package application as .exe",
]


# ============================================================
# DATABASE
# ============================================================

class NotesDatabase:

    def __init__(self):
        self.connection = sqlite3.connect("file_notes.db")
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                path TEXT PRIMARY KEY,
                note TEXT DEFAULT '',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.connection.commit()

    def get_note(self, path):
        cursor = self.connection.cursor()
        cursor.execute("SELECT note FROM notes WHERE path = ?", (path,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return ""

    def save_note(self, path, note):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO notes (path, note)
            VALUES (?, ?)

            ON CONFLICT(path)
            DO UPDATE SET
                note = excluded.note,
                updated_at = CURRENT_TIMESTAMP
            """,
            (path, note),
        )
        self.connection.commit()

    def close(self):
        self.connection.close()


# ============================================================
# FILE HELPERS
# ============================================================

E_DRIVE_ROOT = "E:\\"
FOLDER_ICON_COLOR = "#4A90E2"


def build_folder_icon(color_name=FOLDER_ICON_COLOR, size=22):
    pixmap = QPixmap(QSize(size, size))
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    color = QColor(color_name)
    body = QColor(color)
    body.setAlpha(220)

    painter.setBrush(body)
    painter.setPen(Qt.NoPen)

    painter.drawRoundedRect(3, 8, size - 6, size - 10, 4, 4)
    painter.drawRoundedRect(5, 6, size * 0.45, 8, 3, 3)

    painter.end()
    return QIcon(pixmap)


def get_item_icon(path, color_name=FOLDER_ICON_COLOR):
    if os.path.isdir(path):
        return build_folder_icon(color_name)

    provider = QFileIconProvider()
    return provider.icon(QFileIconProvider.File)


def is_in_e_drive(path):
    try:
        drive = os.path.splitdrive(os.path.abspath(path))[0].upper()
        return drive == "E:"
    except OSError:
        return False


def get_default_e_path():
    if os.path.isdir(E_DRIVE_ROOT):
        return E_DRIVE_ROOT
    return "E:"


def format_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024

    return f"{size:.1f} PB"


def get_folder_size(path):
    total_size = 0

    try:
        with os.scandir(path) as entries:
            for entry in entries:
                try:
                    if entry.is_dir(follow_symlinks=False):
                        total_size += get_folder_size(entry.path)
                    else:
                        total_size += entry.stat(follow_symlinks=False).st_size
                except OSError:
                    continue
    except OSError:
        return 0

    return total_size


def get_file_info(path):
    name = os.path.basename(path)

    try:
        stat = os.stat(path)
        modified_time = datetime.fromtimestamp(stat.st_mtime).strftime("%d-%m-%Y %H:%M")
        size = stat.st_size
    except OSError:
        modified_time = ""
        size = 0

    is_folder = os.path.isdir(path)

    if is_folder:
        file_type = "File folder"
        size_text = format_size(get_folder_size(path))
    else:
        extension = os.path.splitext(path)[1]
        if extension:
            file_type = extension.upper()[1:] + " File"
        else:
            file_type = "File"
        size_text = format_size(size)

    return {
        "name": name,
        "path": path,
        "modified": modified_time,
        "type": file_type,
        "size": size_text,
        "is_folder": is_folder,
    }


def get_directory_items(directory):
    try:
        paths = []

        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            paths.append(full_path)

        paths.sort(key=lambda path: (not os.path.isdir(path), os.path.basename(path).lower()))
        return [get_file_info(path) for path in paths]

    except (PermissionError, OSError):
        return []


# ============================================================
# MAIN WINDOW
# ============================================================

class FileNotesExplorer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FileNotes Explorer - E Drive")
        self.resize(1200, 700)

        self.folder_color = FOLDER_ICON_COLOR
        self.database = NotesDatabase()
        self.current_path = get_default_e_path()

        self.setup_ui()
        self.load_directory(self.current_path)

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # ----------------------------------------------------
        # Navigation
        # ----------------------------------------------------
        navigation_layout = QHBoxLayout()

        self.back_button = QPushButton("← Back")
        self.back_button.clicked.connect(self.go_back)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_directory)

        self.folder_color_button = QPushButton("Folder color")
        self.folder_color_button.clicked.connect(self.change_folder_color)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Enter E: drive folder path...")
        self.path_input.returnPressed.connect(self.navigate_to_path)

        navigation_layout.addWidget(self.back_button)
        navigation_layout.addWidget(self.refresh_button)
        navigation_layout.addWidget(self.folder_color_button)
        navigation_layout.addWidget(self.path_input)
        main_layout.addLayout(navigation_layout)

        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search files or notes...")
        self.search_input.textChanged.connect(self.filter_items)
        main_layout.addWidget(self.search_input)

        # ----------------------------------------------------
        # File Table
        # ----------------------------------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Name",
            "Date Modified",
            "Type",
            "Size",
            "📝 Notes",
        ])

        self.table.cellDoubleClicked.connect(self.handle_double_click)
        self.table.itemChanged.connect(self.handle_note_change)
        self.table.setEditTriggers(QTableWidget.DoubleClicked)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        main_layout.addWidget(self.table)

    # ========================================================
    # LOAD DIRECTORY
    # ========================================================

    def load_directory(self, path):
        requested_path = os.path.abspath(path) if path else get_default_e_path()

        if not is_in_e_drive(requested_path):
            QMessageBox.warning(self, "Access Restricted", "This app is limited to the E: drive.")
            requested_path = self.current_path if is_in_e_drive(self.current_path) else get_default_e_path()

        if not os.path.isdir(requested_path):
            QMessageBox.warning(self, "Invalid Folder", "The selected path is not a valid folder on the E: drive.")
            return

        self.current_path = requested_path
        self.path_input.setText(self.current_path)

        self.table.blockSignals(True)
        self.table.setRowCount(0)

        items = get_directory_items(self.current_path)

        for file_data in items:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Name
            name_item = QTableWidgetItem(file_data["name"])
            name_item.setData(Qt.UserRole, file_data["path"])
            name_item.setIcon(get_item_icon(file_data["path"], self.folder_color))
            name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 0, name_item)

            # Date Modified
            date_item = QTableWidgetItem(file_data["modified"])
            date_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 1, date_item)

            # Type
            type_item = QTableWidgetItem(file_data["type"])
            type_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 2, type_item)

            # Size
            size_item = QTableWidgetItem(file_data["size"])
            size_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 3, size_item)

            # Notes
            note = self.database.get_note(file_data["path"])
            note_item = QTableWidgetItem(note)
            self.table.setItem(row, 4, note_item)

        self.table.blockSignals(False)

    # ========================================================
    # DOUBLE CLICK
    # ========================================================

    def handle_double_click(self, row, column):
        if column == 4:
            return

        name_item = self.table.item(row, 0)
        if not name_item:
            return

        path = name_item.data(Qt.UserRole)

        if not is_in_e_drive(path):
            QMessageBox.warning(self, "Access Restricted", "This app is limited to the E: drive.")
            return

        if os.path.isdir(path):
            self.load_directory(path)
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    # ========================================================
    # SAVE NOTE
    # ========================================================

    def handle_note_change(self, item):
        if item.column() != 4:
            return

        row = item.row()
        name_item = self.table.item(row, 0)
        if not name_item:
            return

        path = name_item.data(Qt.UserRole)
        note = item.text()
        self.database.save_note(path, note)

    # ========================================================
    # BACK NAVIGATION
    # ========================================================

    def go_back(self):
        if self.current_path == get_default_e_path():
            return

        parent = os.path.dirname(self.current_path)
        if parent != self.current_path and is_in_e_drive(parent):
            self.load_directory(parent)

    # ========================================================
    # REFRESH CURRENT DIRECTORY
    # ========================================================

    def refresh_directory(self):
        self.load_directory(self.current_path)

    def change_folder_color(self):
        color = QColorDialog.getColor(QColor(self.folder_color), self, "Choose folder color")
        if color.isValid():
            self.folder_color = color.name()
            self.refresh_directory()

    # ========================================================
    # ADDRESS BAR NAVIGATION
    # ========================================================

    def navigate_to_path(self):
        path = self.path_input.text().strip() or get_default_e_path()
        self.load_directory(path)

    # ========================================================
    # SEARCH
    # ========================================================

    def filter_items(self, search_text):
        search_text = search_text.lower()

        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 0)
            note_item = self.table.item(row, 4)

            if not name_item or not note_item:
                continue

            name = name_item.text().lower()
            note = note_item.text().lower()
            match = search_text in name or search_text in note
            self.table.setRowHidden(row, not match)

    # ========================================================
    # CLOSE DATABASE
    # ========================================================

    def closeEvent(self, event):
        self.database.close()
        event.accept()


# ============================================================
# START APPLICATION
# ============================================================

def main():
    app = QApplication(sys.argv)
    window = FileNotesExplorer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
