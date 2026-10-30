<div align="center">

# 📝 FileNotes Explorer

### Browse your files like Windows Explorer, and attach a note to every file and folder.

A lightweight Windows desktop app built with Python and PySide6. Notes are saved locally in a SQLite database, so you can remember what each file is for, and search by filename or note.

<br />

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6_(Qt)-41CD52?style=flat-square&logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white)

[Features](#-features) · [Quick Start](#-quick-start) · [How It Works](#-how-it-works) · [Roadmap](#-roadmap) · [Report a Bug](https://github.com/ioarunkumar/file-explore-with-notes/issues)

</div>

---

## 📸 Screenshots

<!-- Add a real screenshot: save it as docs/screenshot.png, then uncomment the line below. -->
<!-- ![FileNotes Explorer screenshot](./docs/screenshot.png) -->

---

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">
<h3>📂 File Browser</h3>
<p>Browse folders in a table with Name, Date Modified, Type and Size columns. Folders are always listed above files.</p>
</td>
<td width="50%" valign="top">
<h3>📝 Notes Column</h3>
<p>Double-click the Notes cell of any file or folder and type. Notes are saved automatically as you edit.</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3>🔍 Search</h3>
<p>Type in the search box to filter the current folder by filename or note text.</p>
</td>
<td width="50%" valign="top">
<h3>🧭 Navigation</h3>
<p>Open folders by double-clicking, go up with Back, or type a path into the address bar.</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3>🚀 Open Files</h3>
<p>Double-click a file to open it with your Windows default application.</p>
</td>
<td width="50%" valign="top">
<h3>🎨 Folder Colors</h3>
<p>Pick a custom color for folder icons with the Folder color button.</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3>💾 Local Storage</h3>
<p>Notes are stored in a local SQLite file (<code>file_notes.db</code>). There is no account and no cloud sync.</p>
</td>
<td width="50%" valign="top">
<h3>📏 Folder Sizes</h3>
<p>Folder sizes are calculated by adding up everything inside them, just like in a file manager.</p>
</td>
</tr>
</table>

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Application logic |
| **GUI** | ![PySide6](https://img.shields.io/badge/-PySide6-41CD52?logo=qt&logoColor=white) | Windows, table, dialogs |
| **Database** | ![SQLite](https://img.shields.io/badge/-SQLite-003B57?logo=sqlite&logoColor=white) | Saving notes (`sqlite3` from the standard library) |

---

## 🚀 Quick Start

### Prerequisites

- **Windows** (the app is currently limited to the `E:` drive)
- **Python 3** with `pip`

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/ioarunkumar/file-explore-with-notes.git
cd file-explore-with-notes

# 2. Install the only dependency
pip install PySide6

# 3. Run the app
python file_notes_explorer.py
```

> [!NOTE]
> `run_file_notes.bat` is included as a shortcut, but it contains hard-coded paths for the author's computer. Edit the Python and script paths inside it before using it.

---

## 🧭 How It Works

| Step | Action | What Happens |
| :---: | :--- | :--- |
| **1** | 🚀 **Launch the app** | Opens at the root of the `E:` drive. |
| **2** | 📂 **Open a folder** | Double-click a folder, or type a path in the address bar and press Enter. |
| **3** | 📝 **Add a note** | Double-click the Notes cell of any row and type. It is saved to SQLite right away. |
| **4** | 🔍 **Search** | Type in the search box to filter rows by name or note. |
| **5** | ⬅️ **Go back** | Click **← Back** to move to the parent folder. |

<details>
<summary><b>🗂️ Project Structure</b> (click to expand)</summary>

<br />

```text
file-explore-with-notes/
├── file_notes_explorer.py   # The whole application (UI, file helpers, database)
└── run_file_notes.bat       # Windows launcher (edit the paths before use)
```

`file_notes.db` is created automatically the first time you run the app.

</details>

---

## ⚠️ Notes & Limitations

> [!WARNING]
> **Limited to the `E:` drive.** The app refuses to open paths on any other drive. To use another drive, change `E_DRIVE_ROOT` and `is_in_e_drive` in `file_notes_explorer.py`.

> [!WARNING]
> **Notes are tied to the full file path.** If you rename or move a file or folder, its note will no longer show up. Making notes survive renames is on the roadmap.

> [!NOTE]
> **`file_notes.db` is created in the folder you run the app from**, so launching it from a different folder starts a new, empty notes database.

> [!NOTE]
> **Search only covers the current folder**, not subfolders.

- Folder sizes are calculated each time a folder opens, so large folders may load slowly.
- Notes cannot be deleted explicitly. Clear the cell text to blank a note.

---

## 🗺️ Roadmap

- [x] Browse files and folders
- [x] Name, Date Modified, Type and Size columns
- [x] Notes column saved with SQLite
- [x] Open folders and files by double-clicking
- [x] Back navigation and address bar
- [x] Search filenames and notes
- [x] Folders listed above files
- [ ] Forward navigation
- [ ] Real file-type icons
- [ ] Breadcrumb navigation
- [ ] Right-click context menu
- [ ] Tags
- [ ] Favorites
- [ ] Notes that survive renaming and moving
- [ ] Package as a standalone `.exe`

---

## 🤝 Contributing

Contributions and suggestions are welcome!

1. 🍴 **Fork** the repository
2. 🌿 **Create a branch** for your change
3. 🛠️ **Make and test** your changes by running the app on Windows
4. 📬 **Open a pull request** with a clear description of what changed

Found a bug or have an idea? **[Open an issue](https://github.com/ioarunkumar/file-explore-with-notes/issues)**.

---

## 📜 License

No license needed use it how you want to.

---

<div align="center">

**Built with ❤️ by [Arun Kumar](https://github.com/ioarunkumar)**

⭐ If FileNotes Explorer is useful to you, consider giving it a star!

</div>
