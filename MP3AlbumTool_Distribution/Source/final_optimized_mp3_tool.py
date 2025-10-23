#!/usr/bin/env python3
"""
MP3 Album Tool - Professional Edition
Multi-source metadata retrieval with modern UI
"""

import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import threading
from unidecode import unidecode
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
import requests
import webbrowser
from PIL import Image, ImageTk
import io
import json
from ytmusicapi import YTMusic
import time
import urllib.parse
from rapidfuzz import fuzz

class FinalMP3Tool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎵 MP3 Album Tool - Professional Edition")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.resizable(True, True)
        
        # Configure window for better resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Set modern color scheme
        self.colors = {
            'primary': '#2c3e50',      # Dark blue-gray
            'secondary': '#3498db',     # Bright blue
            'accent': '#e74c3c',       # Red
            'success': '#27ae60',      # Green
            'warning': '#f39c12',      # Orange
            'info': '#9b59b6',         # Purple
            'light': '#ecf0f1',        # Light gray
            'dark': '#34495e',         # Dark gray
            'background': '#ffffff',    # White
            'surface': '#f8f9fa'       # Very light gray
        }
        
        # Configure modern styling
        self.setup_styles()
        
        # Variáveis
        self.selected_folder = tk.StringVar()
        self.recursive_var = tk.BooleanVar(value=True)
        self.force_cover_var = tk.BooleanVar(value=False)
        self.capitalize_names_var = tk.BooleanVar(value=True)
        self.fuzzy_threshold = tk.IntVar(value=80)
        
        # Fontes separadas para renomeação e capas
        self.use_deezer_rename = tk.BooleanVar(value=True)
        self.use_theaudiodb_rename = tk.BooleanVar(value=True)
        self.use_ytmusic_rename = tk.BooleanVar(value=True)
        self.use_deezer_cover = tk.BooleanVar(value=True)
        self.use_theaudiodb_cover = tk.BooleanVar(value=True)
        self.use_ytmusic_cover = tk.BooleanVar(value=True)
        self.use_google_covers = tk.BooleanVar(value=True)
        
        self.files_data = []
        self.covers_cache = {}
        self.editing_item = None
        self.processed = False
        
        # Progress tracking variables
        self.current_progress = 0
        self.total_files = 0
        self.progress_var = tk.DoubleVar()  # For progress percentage
        self.progress_text = tk.StringVar(value="Ready")
        
        # Sorting control
        self.sort_reverse = False
        
        self.setup_ui()
        
    def setup_styles(self):
        """Configure modern professional styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern colors and fonts
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 20, 'bold'), 
                       foreground=self.colors['primary'],
                       background=self.colors['background'])
        
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 11, 'bold'), 
                       foreground=self.colors['dark'],
                       background=self.colors['background'])
        
        style.configure('Status.TLabel', 
                       font=('Segoe UI', 10), 
                       foreground=self.colors['success'],
                       background=self.colors['background'])
        
        style.configure('Error.TLabel', 
                       font=('Segoe UI', 10), 
                       foreground=self.colors['accent'],
                       background=self.colors['background'])
        
        style.configure('Warning.TLabel', 
                       font=('Segoe UI', 10), 
                       foreground=self.colors['warning'],
                       background=self.colors['background'])
        
        # Modern buttons with explicit black text - using more robust configuration
        style.configure('Primary.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       foreground='#000000',  # Explicit black hex
                       background=self.colors['secondary'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        style.map('Primary.TButton', 
                 background=[('active', '#2980b9'), ('pressed', '#21618c')],
                 foreground=[('active', '#000000'), ('pressed', '#000000')])
        
        style.configure('Success.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       foreground='#000000',  # Explicit black hex
                       background='#2ecc71',  # Nicer green
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        style.map('Success.TButton', 
                 background=[('active', '#27ae60'), ('pressed', '#229954')],
                 foreground=[('active', '#000000'), ('pressed', '#000000')])
        
        style.configure('Warning.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       foreground='#000000',  # Explicit black hex
                       background=self.colors['warning'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        style.map('Warning.TButton', 
                 background=[('active', '#e67e22'), ('pressed', '#d35400')],
                 foreground=[('active', '#000000'), ('pressed', '#000000')])
        
        # Orange button for Pause
        style.configure('Orange.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       foreground='#000000',  # Explicit black hex
                       background='#ff9500',  # Nice orange
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        style.map('Orange.TButton', 
                 background=[('active', '#e67e22'), ('pressed', '#d35400')],
                 foreground=[('active', '#000000'), ('pressed', '#000000')])
        
        # Red button for Stop
        style.configure('Danger.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       foreground='#000000',  # Explicit black hex
                       background='#e74c3c',  # Nice red
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        style.map('Danger.TButton', 
                 background=[('active', '#c0392b'), ('pressed', '#a93226')],
                 foreground=[('active', '#000000'), ('pressed', '#000000')])
        
        # Modern LabelFrame
        style.configure('Modern.TLabelframe', 
                       background=self.colors['surface'],
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Modern.TLabelframe.Label', 
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.colors['primary'],
                       background=self.colors['surface'])
        
        # Modern Notebook
        style.configure('Modern.TNotebook', 
                       background=self.colors['background'],
                       borderwidth=0)
        
        style.configure('Modern.TNotebook.Tab', 
                       font=('Segoe UI', 10),
                       padding=[20, 10],
                       background=self.colors['light'],
                       foreground=self.colors['dark'])
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['secondary']),
                           ('active', self.colors['info'])],
                 foreground=[('selected', 'white'),
                           ('active', 'white')])
        
        # Modern Treeview
        style.configure('Modern.Treeview', 
                       background=self.colors['background'],
                       foreground=self.colors['dark'],
                       fieldbackground=self.colors['background'],
                       borderwidth=1,
                       relief='solid',
                       rowheight=85)
        
        style.configure('Modern.Treeview.Heading', 
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['primary'],
                       foreground='white',
                       relief='flat')
        
        style.map('Modern.Treeview',
                 background=[('selected', self.colors['secondary'])],
                 foreground=[('selected', 'white')])
        
        # Modern Entry
        style.configure('Modern.TEntry', 
                       font=('Segoe UI', 10),
                       fieldbackground=self.colors['background'],
                       borderwidth=2,
                       relief='solid',
                       insertcolor=self.colors['secondary'])
        
        # Modern Checkbutton
        style.configure('Modern.TCheckbutton', 
                       font=('Segoe UI', 10),
                       background=self.colors['surface'],
                       foreground=self.colors['dark'],
                       focuscolor='none')
        
        # Modern Scale
        style.configure('Modern.TScale', 
                       background=self.colors['surface'],
                       troughcolor=self.colors['light'],
                       borderwidth=0,
                       lightcolor=self.colors['secondary'],
                       darkcolor=self.colors['secondary'])
        
        # Modern Progress Bar with green color
        style.configure('Modern.Horizontal.TProgressbar',
                       background='#2ecc71',  # Green fill color
                       troughcolor='#ecf0f1',  # Light gray background
                       borderwidth=1,
                       lightcolor='#2ecc71',
                       darkcolor='#27ae60')
        
        # Status label for progress percentage
        style.configure('Status.TLabel',
                       font=('Segoe UI', 8),
                       foreground='#666666',
                       background=self.colors['surface'])
        
    def setup_ui(self):
        """Setup modern professional user interface"""
        # Configure root background
        self.root.configure(bg=self.colors['background'])
        
        # Main frame with compact styling
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Compact title section
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, 
                               text="🎵 MP3 Tool", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Status with modern styling
        self.status_label = ttk.Label(title_frame, text="Ready", 
                                     style='Status.TLabel')
        self.status_label.pack(side=tk.RIGHT)
        
        # Compact configuration section
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Config", 
                                     padding="10", style='Modern.TLabelframe')
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Folder selection with modern styling
        folder_frame = ttk.Frame(config_frame)
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(folder_frame, text="📁 MP3 Folder:", 
                 style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 15))
        
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.selected_folder, 
                                     width=70, font=('Segoe UI', 10), style='Modern.TEntry')
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        ttk.Button(folder_frame, text="📂 Browse Folder", 
                  command=self.select_folder, style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(folder_frame, text="📄 Add Files", 
                  command=self.select_files, style='Secondary.TButton').pack(side=tk.LEFT)
        
        # Renaming sources section
        rename_sources_frame = ttk.Frame(config_frame)
        rename_sources_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(rename_sources_frame, text="🔍 Renaming Sources:", 
                 style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Checkbutton(rename_sources_frame, text="Deezer", 
                       variable=self.use_deezer_rename, 
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 25))
        
        ttk.Checkbutton(rename_sources_frame, text="TheAudioDB", 
                       variable=self.use_theaudiodb_rename,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 25))
        
        ttk.Checkbutton(rename_sources_frame, text="YouTube Music (Free)", 
                       variable=self.use_ytmusic_rename,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 25))
        
        # Cover sources section
        cover_sources_frame = ttk.Frame(config_frame)
        cover_sources_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(cover_sources_frame, text="🖼️ Cover Sources:", 
                 style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Checkbutton(cover_sources_frame, text="Deezer", 
                       variable=self.use_deezer_cover,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 25))
        
        ttk.Checkbutton(cover_sources_frame, text="TheAudioDB", 
                       variable=self.use_theaudiodb_cover,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 25))
        
        ttk.Checkbutton(cover_sources_frame, text="YouTube Music", 
                       variable=self.use_ytmusic_cover,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 25))
        
        ttk.Checkbutton(cover_sources_frame, text="Google Images", 
                       variable=self.use_google_covers,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 25))
        
        # Main options with modern styling
        options_frame = ttk.Frame(config_frame)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Checkbutton(options_frame, text="📁 Process Subfolders", 
                       variable=self.recursive_var,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 30))
        
        ttk.Checkbutton(options_frame, text="🔄 Force Cover Update", 
                       variable=self.force_cover_var,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 30))
        
        ttk.Checkbutton(options_frame, text="🔤 Capitalize Names", 
                       variable=self.capitalize_names_var,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 30))
        
        # Modern threshold slider
        threshold_frame = ttk.Frame(config_frame)
        threshold_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(threshold_frame, text="🎯 Match Threshold:", 
                 style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 15))
        
        self.threshold_scale = ttk.Scale(threshold_frame, from_=50, to=100, 
                                        variable=self.fuzzy_threshold, orient=tk.HORIZONTAL)
        self.threshold_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        self.threshold_label = ttk.Label(threshold_frame, text="80%", 
                                        font=('Segoe UI', 10, 'bold'),
                                        foreground=self.colors['secondary'])
        self.threshold_label.pack(side=tk.LEFT)
        
        # Update threshold label
        self.threshold_scale.configure(command=self.update_threshold_label)
        
        # Modern action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=20)
        
        self.process_btn = ttk.Button(action_frame, text="🚀 Process MP3s", 
                                     command=self.start_processing, style='Primary.TButton')
        self.process_btn.pack(side=tk.LEFT, padx=(0, 15))
        

        
        self.save_btn = ttk.Button(action_frame, text="💾 Save Changes", 
                                  command=self.save_changes, state="disabled", style='Success.TButton')
        self.save_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Control buttons
        self.pause_btn = ttk.Button(action_frame, text="⏸️ Pause", 
                                   command=self.toggle_pause, state="disabled", style='Orange.TButton')
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(action_frame, text="⏹️ Stop", 
                                  command=self.request_stop, state="disabled", style='Danger.TButton')
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # File action buttons in the same row
        ttk.Button(action_frame, text="✏️ Edit", 
                  command=self.edit_selected_file, style='Info.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text="🔍 Cover", 
                  command=self.search_cover_selected, style='Info.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text="📝➡️🏷️", 
                  command=self.copy_filename_to_tag_selected, style='Info.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text="🏷️➡️📝", 
                  command=self.copy_tag_to_filename_selected, style='Info.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text="🗑️", 
                  command=self.remove_selected_file, style='Danger.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text="💿 Album", 
                  command=self.set_album_name_all, style='Warning.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text="🔧 Fix Albums", 
                  command=self.fix_album_inconsistencies, style='Warning.TButton').pack(side=tk.LEFT, padx=(0, 15))
        
        # Modern progress bar with percentage
        progress_frame = ttk.Frame(action_frame)
        progress_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 0))
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', 
                                       style='Modern.Horizontal.TProgressbar',
                                       variable=self.progress_var)
        self.progress.pack(fill=tk.X, pady=(0, 2))
        
        # Progress percentage label
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_text, 
                                       style='Status.TLabel', anchor='center')
        self.progress_label.pack(fill=tk.X)
        
        # Modern notebook with tabs
        self.notebook = ttk.Notebook(main_frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 0))
        
        # Files tab with modern styling
        self.files_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.files_frame, text="📁 Files")
        
        # Modern tree frame
        tree_frame = ttk.Frame(self.files_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Modern treeview with covers - increased height
        columns = ("#", "Album", "Original", "New", "Artist", "Title", "Status")
        self.files_tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", 
                                      height=35, style='Modern.Treeview')
        
        # Tree column for thumbnails
        self.files_tree.heading("#0", text="Cover")
        self.files_tree.column("#0", width=120, stretch=False)
        
        # Configure modern column headers
        headers = {
            "#": "#",
            "Album": "Album", 
            "Original": "Original Name",
            "New": "New Name",
            "Artist": "Artist",
            "Title": "Title",
            "Status": "Status"
        }
        
        for col in columns:
            if col == "Status":
                # Add sorting command for Status column
                self.files_tree.heading(col, text=headers[col], command=self.sort_by_status)
            else:
                self.files_tree.heading(col, text=headers[col])
        
        # Configure optimized column widths
        self.files_tree.column("#", width=50)
        self.files_tree.column("Album", width=120)
        self.files_tree.column("Original", width=280)
        self.files_tree.column("New", width=280)
        self.files_tree.column("Artist", width=120)
        self.files_tree.column("Title", width=150)
        self.files_tree.column("Status", width=100)
        
        # Modern scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.files_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.files_tree.xview)
        
        self.files_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for treeview and scrollbars
        self.files_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid expansion
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.files_tree.bind("<Button-3>", self.show_context_menu)
        self.files_tree.bind("<Double-1>", self.on_double_click)
        
        # Modern log tab
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="📝 Log")
        
        # Modern log text with styling
        log_container = ttk.Frame(self.log_frame)
        log_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_container, height=35, width=100, 
                                                 font=("Consolas", 9),
                                                 bg=self.colors['background'],
                                                 fg=self.colors['dark'],
                                                 insertbackground=self.colors['secondary'],
                                                 selectbackground=self.colors['secondary'],
                                                 selectforeground='white',
                                                 relief='solid',
                                                 borderwidth=1)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Enable drag and drop for files (after log_text is initialized)
        self.setup_drag_and_drop()
        
        # Control variables
        self.pause_requested = False
        self.stop_requested = False
        
    def update_threshold_label(self, value):
        """Update threshold label"""
        self.threshold_label.config(text=f"{int(float(value))}%")
    
    def update_progress(self, current, total):
        """Update progress bar and percentage label"""
        if total > 0:
            percentage = (current / total) * 100
            self.progress_var.set(percentage)
            self.progress_text.set(f"{percentage:.1f}%")
        else:
            self.progress_var.set(0)
            self.progress_text.set("0%")
        
    def select_folder(self):
        """Select folder with MP3 files"""
        folder = filedialog.askdirectory(
            title="Select folder with MP3 files",
            initialdir=os.path.expanduser("~")
        )
        if folder:
            self.selected_folder.set(folder)
            self.load_mp3_files(folder)
            
    def select_files(self):
        """Select individual MP3 files from any location"""
        file_paths = filedialog.askopenfilenames(
            title="Select MP3 Files",
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")],
            initialdir=os.path.expanduser("~")
        )
        
        if file_paths:
            self.add_files_to_list(file_paths)
            
    def add_files_to_list(self, file_paths):
        """Add individual files to the existing list"""
        added_count = 0
        
        for file_path in file_paths:
            # Check if file is already in the list
            already_exists = any(data['path'] == file_path for data in self.files_data)
            
            if not already_exists and file_path.lower().endswith('.mp3'):
                try:
                    # Extract metadata - returns tuple (artist, title)
                    artist, title = self.extract_existing_metadata(file_path)
                    
                    # Get album name from folder
                    album_name = os.path.basename(os.path.dirname(file_path))
                    
                    # Add to files_data
                    filename = os.path.basename(file_path)
                    file_data = {
                        'index': len(self.files_data) + 1,  # Índice baseado na posição atual
                        'path': file_path,
                        'album': album_name,
                        'original': filename,  # Nome original do arquivo
                        'new': '',  # Campo para novo nome do arquivo
                        'artist': artist or '',
                        'title': title or '',
                        'status': 'Pending',
                        'cover': None  # Para compatibilidade com load_mp3_files
                    }
                    
                    self.files_data.append(file_data)
                    added_count += 1
                    
                except Exception as e:
                    self.log_message(f"❌ Error loading {os.path.basename(file_path)}: {e}")
        
        if added_count > 0:
            # Refresh the tree view
            self.refresh_tree_view()
            self.log_message(f"📁 Added {added_count} file(s) to the list")
            
            # Load covers for new files
            self.load_existing_covers()
        else:
             self.log_message("⚠️ No new files were added (duplicates or invalid files)")
             
    def setup_drag_and_drop(self):
        """Setup basic drag and drop functionality"""
        # For now, we'll focus on the file selection functionality
        # Advanced drag and drop can be added later with tkinterdnd2 if needed
        self.log_message("💡 Tip: Use 'Add Files' button to select MP3 files from any location")
            
    def load_mp3_files(self, folder_path):
        """Load MP3 files into the list"""
        # Clear previous list
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
        # Clear stored thumbnails
        self.cover_thumbnails = {}
        
        self.files_data = []
        self.processed = False
        self.save_btn.config(state="disabled")
        
        # Find MP3 files
        mp3_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.mp3'):
                    mp3_files.append(os.path.join(root, file))
            
            if not self.recursive_var.get():
                break
        
        # Add to list with numbering
        for i, file_path in enumerate(mp3_files):
            album_name = os.path.basename(os.path.dirname(file_path))
            filename = os.path.basename(file_path)
            
            # Try to extract existing metadata
            artist, title = self.extract_existing_metadata(file_path)
            
            self.files_data.append({
                'index': i + 1,
                'path': file_path,
                'album': album_name,
                'original': filename,
                'new': '',
                'artist': artist or '',
                'title': title or '',
                'status': 'Pending',
                'cover': None
            })
            
            # Insert into treeview
            # Columns order: ("#", "Album", "Original", "New", "Artist", "Title", "Status")
            self.files_tree.insert("", "end", values=(
                i + 1,  # #
                album_name,  # Album
                filename,  # Original
                '',  # New
                artist or '',  # Artist
                title or '',  # Title
                'Pending'  # Status
            ))
        
        self.log_message(f"📁 Loaded {len(mp3_files)} MP3 files")
        
        # Load existing covers
        self.load_existing_covers()
        
    def extract_existing_metadata(self, file_path):
        """Extract existing metadata from file"""
        try:
            audio = MP3(file_path, ID3=ID3)
            if audio.tags:
                artist = audio.tags.get('TPE1', [''])[0] if 'TPE1' in audio.tags else ''
                title = audio.tags.get('TIT2', [''])[0] if 'TIT2' in audio.tags else ''
                return artist, title
        except Exception:
            pass
        return None, None
        
    def load_existing_covers(self):
        """Load existing covers from files"""
        self.log_message("🔍 Checking embedded covers in files...")
        covers_found = 0
        
        for i, file_data in enumerate(self.files_data):
            try:
                cover_image = self.extract_cover_from_file(file_data['path'])
                if cover_image:
                    file_data['cover'] = cover_image
                    covers_found += 1
                    # Update treeview with immediate preview
                    self.update_file_in_tree(i, file_data)
            except Exception as e:
                self.log_message(f"❌ Error loading cover {file_data['original']}: {e}")
        
        self.log_message(f"✅ Check completed: {covers_found} embedded covers found")
                
    def extract_cover_from_file(self, file_path):
        """Extrai capa do arquivo MP3"""
        try:
            audio = MP3(file_path, ID3=ID3)
            if audio.tags:
                for frame in audio.tags.values():
                    if isinstance(frame, APIC):
                        # Resize image for preview
                        image = Image.open(io.BytesIO(frame.data))
                        image.thumbnail((80, 80), Image.Resampling.LANCZOS)
                        # Debug log
                        filename = os.path.basename(file_path)
                        self.log_message(f"🖼️ Embedded cover found in: {filename}")
                        return image
        except Exception as e:
            # Debug log
            filename = os.path.basename(file_path)
            self.log_message(f"❌ Error extracting cover from {filename}: {e}")
        return None
        
    def log_message(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_processing(self):
        """Start processing with real metadata"""
        if not self.files_data:
            messagebox.showerror("Error", "No files loaded! Please select a folder or add files first!")
            return
            
        # Initialize progress tracking
        self.total_files = len(self.files_data)
        self.current_progress = 0
        self.progress_var.set(0)
        self.progress_text.set("0%")
            
        self.process_btn.config(state="disabled")
        self.status_label.config(text="Processing...", style='Warning.TLabel')
        # Prepare pause/stop control
        self.pause_requested = False
        self.stop_requested = False
        self.pause_btn.config(state="normal", text="⏸️ Pause")
        self.stop_btn.config(state="normal")
        
        thread = threading.Thread(target=self.process_with_real_metadata)
        thread.daemon = True
        thread.start()
        
    def process_with_real_metadata(self):
        """Process files using real metadata"""
        try:
            self.log_message("🚀 Starting processing with real metadata")
            self.log_message("=" * 70)
            
            for i, file_data in enumerate(self.files_data):
                try:
                    # Update progress
                    self.current_progress = i
                    self.update_progress(i + 1, self.total_files)
                    
                    # Stop if requested
                    if self.stop_requested:
                        self.log_message("⏹️ Processing stopped by user")
                        break
                    # Pause if requested
                    while self.pause_requested and not self.stop_requested:
                        time.sleep(0.1)
                        
                    original_name = os.path.splitext(file_data['original'])[0]
                    self.log_message(f"Processing ({i+1}/{self.total_files}): {original_name}")
                    
                    # Clean filename
                    cleaned_name = self.clean_filename(original_name)
                    
                    # Try to extract artist and title from name
                    artist_from_filename, title_from_filename = self.extract_artist_title(cleaned_name)
                    
                    # Search for real metadata
                    real_artist = None
                    real_title = None
                    source = "None"
                    
                    # Try Deezer first (if enabled for renaming)
                    if self.use_deezer_rename.get():
                        self.log_message(f"  🔍 Searching Deezer: {cleaned_name}")
                        real_artist, real_title = self.search_deezer(cleaned_name)
                        
                        if real_artist and real_title:
                            source = "Deezer"
                            self.log_message(f"  ✅ Deezer found: {real_artist} - {real_title}")
                        else:
                            self.log_message(f"  ❌ Deezer not found")
                    
                    # If Deezer didn't find, try TheAudioDB (if enabled for renaming)
                    if not real_artist or not real_title:
                        if self.use_theaudiodb_rename.get():
                            self.log_message(f"  🔍 Searching TheAudioDB: {cleaned_name}")
                            real_artist, real_title = self.search_theaudiodb(cleaned_name)
                            
                            if real_artist and real_title:
                                source = "TheAudioDB"
                                self.log_message(f"  ✅ TheAudioDB found: {real_artist} - {real_title}")
                            else:
                                self.log_message(f"  ❌ TheAudioDB not found")
                    
                    # If still not found, try YouTube Music (if enabled for renaming)
                    if not real_artist or not real_title:
                        if self.use_ytmusic_rename.get():
                            self.log_message(f"  🔍 Searching YouTube Music: {cleaned_name}")
                            real_artist, real_title = self.search_ytmusic(cleaned_name)
                            
                            if real_artist and real_title:
                                source = "YouTube Music"
                                self.log_message(f"  ✅ YouTube Music encontrou: {real_artist} - {real_title}")
                            else:
                                self.log_message(f"  ❌ YouTube Music não encontrou")
                    
                    # Se não encontrou em nenhuma fonte, usar do nome do arquivo
                    if not real_artist or not real_title:
                        if artist_from_filename and title_from_filename:
                            real_artist = artist_from_filename
                            real_title = title_from_filename
                            source = "Nome do Arquivo"
                            self.log_message(f"  📁 Usando do nome do arquivo: {real_artist} - {real_title}")
                        else:
                            real_artist = "Artista Desconhecido"
                            real_title = cleaned_name
                            source = "Desconhecido"
                            self.log_message(f"  ❌ Usando fallback: {real_artist} - {real_title}")
                    
                    # Formatar nomes
                    if self.capitalize_names_var.get():
                        real_artist = self.smart_capitalize(real_artist)
                        real_title = self.smart_capitalize(real_title)
                    
                    # Criar novo nome baseado nos metadados reais
                    new_name = f"{real_artist} - {real_title}"
                    
                    # Atualizar dados
                    file_data['new'] = new_name
                    file_data['artist'] = real_artist
                    file_data['title'] = real_title
                    file_data['status'] = source
                    
                    # Atualizar interface
                    self.root.after(0, self.update_file_in_tree, i, file_data)
                    
                    self.log_message(f"  → {new_name} (Fonte: {source})")
                    
                    # Buscar capa se encontrar artista e título
                    if file_data['artist'] and file_data['title']:
                        self.log_message(f"  🖼️ Buscando capa: {file_data['artist']} - {file_data['title']}")
                        
                        # Verificar se já tem capa
                        if not self.force_cover_var.get() and file_data['cover']:
                            self.log_message("    ✅ Capa já existe")
                        else:
                            # Buscar capa
                            cover_image = self.search_cover_all_sources(file_data['artist'], file_data['title'])
                            
                            if cover_image:
                                file_data['cover'] = cover_image
                                self.log_message("    ✅ Capa encontrada")
                                
                                # Atualizar preview na tabela imediatamente
                                self.root.after(0, self.update_file_in_tree, i, file_data)
                            else:
                                self.log_message("    ❌ Capa não encontrada")
                    
                except Exception as e:
                    self.log_message(f"  ❌ Error: {e}")
                    file_data['status'] = "Error"
                    self.root.after(0, self.update_file_in_tree, i, file_data)
            
            self.log_message("=" * 70)
            if not self.stop_requested:
                self.log_message("✅ Processing completed! Click 'Save Changes' to save.")
            
            self.processed = True
            self.root.after(0, self.save_btn.config, {"state": "normal"})
            
        except Exception as e:
            self.log_message(f"❌ Erro geral: {e}")
        finally:
            self.root.after(0, self.processing_finished)

    def toggle_pause(self):
        """Alterna pausa/continuação do processamento"""
        self.pause_requested = not self.pause_requested
        if self.pause_requested:
            self.pause_btn.config(text="▶️ Continuar")
            self.status_label.config(text="Pausado", style='Warning.TLabel')
        else:
            self.pause_btn.config(text="⏸️ Pausar")
            self.status_label.config(text="Processando...", style='Warning.TLabel')

    def request_stop(self):
        """Solicita parar processamento"""
        self.stop_requested = True
            
    def search_deezer(self, search_term):
        """Busca no Deezer"""
        try:
            # Limpar termo de busca
            clean_term = re.sub(r'[^\w\s]', ' ', search_term)
            clean_term = re.sub(r'\s+', ' ', clean_term).strip()
            
            # Buscar no Deezer
            api_url = f"https://api.deezer.com/search?q={clean_term}"
            
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    track = data['data'][0]
                    
                    artist = track.get('artist', {}).get('name', '')
                    title = track.get('title', '')
                    
                    if artist and title:
                        return artist, title
            
            return None, None
            
        except Exception as e:
            self.log_message(f"  Erro na busca Deezer: {e}")
            return None, None
            
    def search_theaudiodb(self, search_term):
        """Busca simples e rápida no TheAudioDB - apenas artista/título"""
        try:
            # Extrair artista e título
            artist_guess, title_guess = self.extract_artist_title(search_term)
            
            if not artist_guess or not title_guess:
                return None, None
            
            # Busca direta por track específico - mais rápida
            api_url = "https://theaudiodb.com/api/v1/json/2/searchtrack.php"
            params = {'s': artist_guess, 't': title_guess}
            
            response = requests.get(api_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'track' in data and data['track'] and len(data['track']) > 0:
                    track = data['track'][0]
                    artist = track.get('strArtist', '').strip()
                    title = track.get('strTrack', '').strip()
                    
                    if artist and title:
                        return artist, title
            
            return None, None
            
        except Exception:
            return None, None
    
    def search_ytmusic(self, filename):
        """Busca informações no YouTube Music (API gratuita)"""
        try:
            artist_guess, title_guess = self.extract_artist_title(filename)
            
            if not artist_guess or not title_guess:
                return None, None
            
            # Inicializar YouTube Music API
            ytmusic = YTMusic()
            
            # Buscar por artista e título
            search_query = f"{artist_guess} {title_guess}"
            results = ytmusic.search(search_query, filter="songs", limit=5)
            
            if results:
                for result in results:
                    if result.get('resultType') == 'song':
                        # Extrair artista
                        artists = result.get('artists', [])
                        if artists:
                            artist = artists[0].get('name', '').strip()
                        else:
                            artist = None
                        
                        # Extrair título
                        title = result.get('title', '').strip()
                        
                        if artist and title:
                            return artist, title
            
            return None, None
            
        except Exception:
            return None, None

            
    def search_cover_all_sources(self, artist, title):
        """Busca capa em todas as fontes habilitadas"""
        # Deezer (se habilitado para capas)
        if self.use_deezer_cover.get():
            try:
                cover_image = self.search_cover_deezer(artist, title)
                if cover_image:
                    return cover_image
            except Exception:
                pass
            
        # TheAudioDB (se habilitado para capas)
        if self.use_theaudiodb_cover.get():
            try:
                cover_image = self.search_cover_theaudiodb(artist, title)
                if cover_image:
                    return cover_image
            except Exception:
                pass
            
        # YouTube Music (se habilitado para capas)
        if self.use_ytmusic_cover.get():
            try:
                cover_image = self.search_cover_ytmusic(artist, title)
                if cover_image:
                    return cover_image
            except Exception:
                pass
            
        # Google (só para capas)
        if self.use_google_covers.get():
            try:
                cover_image = self.search_cover_google(artist, title)
                if cover_image:
                    return cover_image
            except Exception:
                pass
            
        return None
            
    def search_cover_deezer(self, artist, title):
        """Busca capa no Deezer com alta resolução"""
        try:
            query = f'artist:"{artist}" track:"{title}"'
            api_url = f"https://api.deezer.com/search?q={query}"
            
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    track = data['data'][0]
                    
                    if 'album' in track:
                        album = track['album']
                        
                        # Tentar diferentes resoluções em ordem de preferência (maior para menor)
                        cover_sizes = [
                            ('cover_xl', 'XL (1000x1000)'),      # 1000x1000
                            ('cover_big', 'Big (500x500)'),      # 500x500  
                            ('cover_medium', 'Medium (250x250)'), # 250x250
                            ('cover', 'Standard (120x120)'),     # 120x120
                            ('cover_small', 'Small (56x56)')     # 56x56
                        ]
                        
                        for cover_key, size_desc in cover_sizes:
                            if cover_key in album:
                                cover_url = album[cover_key]
                                
                                try:
                                    img_response = requests.get(cover_url, timeout=10)
                                    if img_response.status_code == 200:
                                        image = Image.open(io.BytesIO(img_response.content))
                                        self.log_message(f"   🖼️ Capa Deezer encontrada: {size_desc} - {image.size[0]}x{image.size[1]}")
                                        
                                        # Não redimensionar aqui - deixar para embed_cover_art fazer isso
                                        return image
                                except Exception as e:
                                    self.log_message(f"   ⚠️ Erro ao baixar capa {size_desc}: {e}")
                                    continue
            
            return None
            
        except Exception as e:
            self.log_message(f"Erro ao buscar capa Deezer: {e}")
            return None
            
    def search_cover_theaudiodb(self, artist, title):
        """Busca capa no TheAudioDB - CORRIGIDO"""
        try:
            # Buscar track específico
            api_url = "https://theaudiodb.com/api/v1/json/2/searchtrack.php"
            params = {
                's': artist,
                't': title
            }
            
            response = requests.get(api_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if 'track' in data and len(data['track']) > 0:
                    track = data['track'][0]
                    album_id = track.get('idAlbum')
                    
                    if album_id:
                        # Buscar capa do álbum
                        cover_url = f"https://theaudiodb.com/api/v1/json/2/album.php?m={album_id}"
                        cover_response = requests.get(cover_url, timeout=10)
                        
                        if cover_response.status_code == 200:
                            cover_data = cover_response.json()
                            
                            if 'album' in cover_data and len(cover_data['album']) > 0:
                                album = cover_data['album'][0]
                                cover_url = album.get('strAlbumThumb')
                                
                                if cover_url and cover_url != "":
                                    img_response = requests.get(cover_url, timeout=10)
                                    if img_response.status_code == 200:
                                        image = Image.open(io.BytesIO(img_response.content))
                                        self.log_message(f"   🖼️ Capa TheAudioDB encontrada: {image.size[0]}x{image.size[1]}")
                                        # Não redimensionar aqui - deixar para embed_cover_art fazer isso
                                        return image
            
            return None
            
        except Exception as e:
            self.log_message(f"Erro ao buscar capa TheAudioDB: {e}")
            return None
            
    def search_cover_ytmusic(self, artist, title):
        """Busca capa no YouTube Music"""
        try:
            # Inicializar YouTube Music API
            ytmusic = YTMusic()
            
            # Buscar por artista e título
            search_query = f"{artist} {title}"
            results = ytmusic.search(search_query, filter="songs", limit=5)
            
            if results:
                for result in results:
                    if result.get('resultType') == 'song':
                        # Verificar se há thumbnail
                        thumbnails = result.get('thumbnails', [])
                        if thumbnails:
                            # Pegar a thumbnail de maior resolução
                            thumbnail_url = thumbnails[-1].get('url', '')
                            if thumbnail_url:
                                # Baixar a imagem
                                response = requests.get(thumbnail_url, timeout=10)
                                if response.status_code == 200:
                                    # Converter para PIL Image
                                    image = Image.open(io.BytesIO(response.content))
                                    
                                    # Log das dimensões encontradas
                                    self.log_message(f"    📐 Capa YouTube Music: {image.size[0]}x{image.size[1]}")
                                    
                                    return image
            
            return None
        except Exception as e:
            self.log_message(f"Erro ao buscar capa YouTube Music: {e}")
            return None
            
    def search_cover_google(self, artist, title):
        """Busca capa no Google (só para capas)"""
        try:
            query = f"{artist} {title} album cover"
            search_url = f"https://www.google.com/search?q={query}&tbm=isch"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            if response.status_code == 200:
                self.log_message("⚠️ Google Images requer implementação de scraping")
                return None
            
            return None
        except Exception as e:
            self.log_message(f"Erro Google: {e}")
            return None
            
    def clean_filename(self, filename):
        """Limpa nome do arquivo"""
        original_filename = filename
        
        # Remover números no início
        filename = re.sub(r'^\d+\.?\s*', '', filename)
        
        # Remover padrões comuns
        patterns_to_remove = [
            r'\s*\(?DVD\)?.*',
            r'\s*\(?DIREITOS\s*AUTORAIS\)?.*',
            # Variações de "Video Oficial"
            r'\s*\(?VIDEO\s*OFICIAL\)?.*',
            r'\s*\(?OFICIAL\s*VIDEO\)?.*',
            r'\s*\(?OFFICIAL\s*VIDEO\)?.*',
            r'\s*\(?VIDEO\s*OFFICIAL\)?.*',
            r'\s*\(?CLIPE\s*OFICIAL\)?.*',
            r'\s*\(?OFICIAL\s*CLIPE\)?.*',
            r'\s*\(?VIDEO\s*CLIPE\)?.*',
            r'\s*\(?CLIPE\s*VIDEO\)?.*',
            r'\s*\(?VIDEOCLIP\)?.*',
            r'\s*\(?VIDEO\s*CLIP\)?.*',
            r'\s*\(?CLIP\s*VIDEO\)?.*',
            # Outras variações de vídeo
            r'\s*\(?LYRIC\s*VIDEO\)?.*',
            r'\s*\(?VIDEO\s*LYRIC\)?.*',
            r'\s*\(?LYRICS\s*VIDEO\)?.*',
            r'\s*\(?VIDEO\s*LYRICS\)?.*',
            r'\s*\(?MUSIC\s*VIDEO\)?.*',
            r'\s*\(?VIDEO\s*MUSIC\)?.*',
            r'\s*\(?OFFICIAL\s*AUDIO\)?.*',
            r'\s*\(?AUDIO\s*OFICIAL\)?.*',
            r'\s*\(?LYRICS?\)?.*',
            r'\s*\(?LETRA\)?.*',
            # Qualidade e formato
            r'\s*\(?MV\)?.*',
            r'\s*\(?HD\)?.*',
            r'\s*\(?FULL\s*HD\)?.*',
            r'\s*\(?4K\)?.*',
            r'\s*\(?1080P\)?.*',
            r'\s*\(?720P\)?.*',
            r'\s*\(?480P\)?.*',
            # Tipos de performance
            r'\s*\(?LIVE\)?.*',
            r'\s*\(?AO\s*VIVO\)?.*',
            r'\s*\(?COVER\)?.*',
            r'\s*\(?REMIX\)?.*',
            r'\s*\(?VERSION\)?.*',
            r'\s*\(?VERSAO\)?.*',
            r'\s*\(?VERSÃO\)?.*',
            r'\s*\(?EXPLICIT\)?.*',
            r'\s*\(?CLEAN\)?.*',
            r'\s*\(?ACOUSTIC\)?.*',
            r'\s*\(?ACUSTICO\)?.*',
            r'\s*\(?ACÚSTICO\)?.*',
            r'\s*\(?INSTRUMENTAL\)?.*',
            r'\s*\(?KARAOKE\)?.*',
            r'\s*\(?RADIO\s*EDIT\)?.*',
            r'\s*\(?EXTENDED\)?.*',
            r'\s*\(?REMASTERED\)?.*',
            r'\s*\(?REMASTERIZADO\)?.*',
            r'\s*\(?DELUXE\)?.*',
            r'\s*\(?BONUS\s*TRACK\)?.*',
            r'\s*\(?FAIXA\s*BONUS\)?.*',
            # Símbolos e caracteres especiais
            r'\s*\[.*\]',  # Qualquer coisa entre colchetes
            r'\s*\(.*\)',  # Qualquer coisa entre parênteses
            r'\s*\{.*\}',  # Qualquer coisa entre chaves
            r'\s*_+\s*',   # Múltiplos underscores
            r'\s*-+\s*$',  # Hífens no final
            r'\s*\|.*',    # Pipe e tudo depois
            r'\s*#.*'      # Hashtag e tudo depois
        ]
        
        for pattern in patterns_to_remove:
            filename = re.sub(pattern, '', filename, flags=re.IGNORECASE)
        
        # Limpeza adicional para casos com underscores e separadores
        # Remover palavras problemáticas que podem estar separadas por underscores
        problematic_words = [
            'video', 'oficial', 'official', 'clipe', 'clip', 'videoclip',
            'lyric', 'lyrics', 'letra', 'music', 'audio', 'mv', 'hd', 'fullhd',
            '4k', '1080p', '720p', '480p', 'live', 'aovivo', 'cover', 'remix',
            'version', 'versao', 'versão', 'explicit', 'clean', 'acoustic',
            'acustico', 'acústico', 'instrumental', 'karaoke', 'radioedit',
            'extended', 'remastered', 'remasterizado', 'deluxe', 'bonus',
            'bonustrack', 'faixabonus'
        ]
        
        # Remover palavras problemáticas separadas por underscores ou hífens
        for word in problematic_words:
            # Padrões com underscores
            filename = re.sub(rf'_{word}_?', '_', filename, flags=re.IGNORECASE)
            filename = re.sub(rf'_{word}$', '', filename, flags=re.IGNORECASE)
            filename = re.sub(rf'^{word}_', '', filename, flags=re.IGNORECASE)
            # Padrões com hífens
            filename = re.sub(rf'-{word}-?', '-', filename, flags=re.IGNORECASE)
            filename = re.sub(rf'-{word}$', '', filename, flags=re.IGNORECASE)
            filename = re.sub(rf'^{word}-', '', filename, flags=re.IGNORECASE)
            # Padrões com espaços
            filename = re.sub(rf'\s+{word}\s+', ' ', filename, flags=re.IGNORECASE)
            filename = re.sub(rf'\s+{word}$', '', filename, flags=re.IGNORECASE)
            filename = re.sub(rf'^{word}\s+', '', filename, flags=re.IGNORECASE)
        
        # Limpar múltiplos separadores consecutivos
        filename = re.sub(r'_+', '_', filename)  # Múltiplos underscores
        filename = re.sub(r'-+', '-', filename)  # Múltiplos hífens
        filename = re.sub(r'\s+', ' ', filename)  # Múltiplos espaços
        
        # Remover separadores no início e fim
        filename = filename.strip('_-. ')
        
        # Log da limpeza se houve mudança significativa
        if original_filename != filename and len(filename) > 0:
            self.log_message(f"🧹 Limpeza: '{original_filename}' → '{filename}'")
        
        return filename.strip()
        
    def extract_artist_title(self, filename):
        """Extrai artista e título do nome do arquivo"""
        # Padrões simples de separação
        separators = [" - ", " – ", " — ", " _ ", " by ", " BY "]
        
        for sep in separators:
            if sep in filename:
                parts = filename.split(sep, 1)
                if len(parts) == 2:
                    artist = parts[0].strip()
                    title = parts[1].strip()
                    
                    if len(artist) >= 2 and len(title) >= 2:
                        return artist, title
        
        # Se não encontrou separador, tentar dividir no meio
        words = filename.split()
        if len(words) >= 4:
            mid = len(words) // 2
            artist = ' '.join(words[:mid])
            title = ' '.join(words[mid:])
            return artist, title
        
        return None, None
        
    def smart_capitalize(self, text):
        """Capitalização inteligente"""
        if not text:
            return text
        
        words = text.split(' ')
        small_words = {
            'de', 'do', 'da', 'dos', 'das', 'e', 'ou', 'com', 
            'sem', 'para', 'por', 'em', 'no', 'na', 'um', 'uma',
            'o', 'a', 'os', 'as'
        }
        
        for i, word in enumerate(words):
            if word:
                if i == 0 or word.lower() not in small_words:
                    # Manter siglas (todas maiúsculas)
                    if not word.isupper():
                        words[i] = word[0].upper() + word[1:].lower()
                else:
                    words[i] = word.lower()
        
        return ' '.join(words)
        
    def start_manual_processing(self):
        """Inicia edição manual"""
        if not self.selected_folder.get():
            messagebox.showerror("Erro", "Selecione uma pasta primeiro!")
            return
            
        self.manual_btn.config(state="disabled")
        self.progress.start()
        self.status_label.config(text="Edição Manual", style='Warning.TLabel')
        
        thread = threading.Thread(target=self.process_manual)
        thread.daemon = True
        thread.start()
        
    def process_manual(self):
        """Processa arquivos manualmente"""
        try:
            self.log_message("✏️ Iniciando edição manual")
            self.log_message("=" * 70)
            self.log_message("Clique duplo em qualquer linha para editar")
            self.log_message("Botão direito para menu de contexto")
            
        except Exception as e:
            self.log_message(f"❌ Erro geral: {e}")
        finally:
            self.root.after(0, self.manual_processing_finished)
            
    def start_manual_edit(self, event):
        """Inicia edição manual de uma linha"""
        item = self.files_tree.selection()[0]
        index = int(self.files_tree.item(item, "values")[0]) - 1
        
        if 0 <= index < len(self.files_data):
            self.edit_file_manual(index)
            
    def edit_file_manual(self, index):
        """Abre janela de edição manual"""
        file_data = self.files_data[index]
        
        # Janela de edição
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Editar: {file_data['original']}")
        edit_window.geometry("700x600")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(edit_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos de edição
        ttk.Label(main_frame, text="Artista:", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 5))
        artist_entry = ttk.Entry(main_frame, width=70, font=('Arial', 10))
        artist_entry.pack(fill=tk.X, pady=(0, 15))
        artist_entry.insert(0, file_data['artist'])
        
        ttk.Label(main_frame, text="Título:", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 5))
        title_entry = ttk.Entry(main_frame, width=70, font=('Arial', 10))
        title_entry.pack(fill=tk.X, pady=(0, 15))
        title_entry.insert(0, file_data['title'])
        
        ttk.Label(main_frame, text="Álbum:", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 5))
        album_entry = ttk.Entry(main_frame, width=70, font=('Arial', 10))
        album_entry.pack(fill=tk.X, pady=(0, 20))
        album_entry.insert(0, file_data['album'])
        
        # Frame de capa
        cover_frame = ttk.LabelFrame(main_frame, text="Capa", padding="15")
        cover_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Mostrar capa atual se existir
        cover_label = None
        if file_data['cover']:
            cover_image = file_data['cover'].copy()
            cover_image.thumbnail((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(cover_image)
            cover_label = ttk.Label(cover_frame, image=photo)
            cover_label.image = photo
            cover_label.pack(pady=5)
        else:
            cover_label = ttk.Label(cover_frame, text="Nenhuma capa encontrada", font=('Arial', 10))
            cover_label.pack(pady=5)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        def save_changes():
            # Atualizar dados
            file_data['artist'] = artist_entry.get()
            file_data['title'] = title_entry.get()
            file_data['album'] = album_entry.get()
            file_data['new'] = f"{file_data['artist']} - {file_data['title']}"
            file_data['status'] = "Manual"
            
            # Atualizar treeview
            self.update_file_in_tree(index, file_data)
            
            edit_window.destroy()
            
        def search_cover():
            if file_data['artist'] and file_data['title']:
                self.search_cover_for_file(index, cover_label)
            else:
                messagebox.showwarning("Aviso", "Preencha artista e título primeiro!")
        
        def search_cover_by_name():
            # Permitir busca por outro nome
            search_name = simpledialog.askstring("Buscar Capa", "Digite o nome para buscar:")
            if search_name:
                self.search_cover_by_custom_name(index, search_name, cover_label)
        
        def download_from_url():
            # Download de URL do Google
            url = simpledialog.askstring("Download de Capa", "Cole a URL da imagem:")
            if url:
                self.download_cover_from_url(index, url, cover_label)
        
        ttk.Button(button_frame, text="🔍 Buscar Capa", command=search_cover).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🔍 Buscar por Nome", command=search_cover_by_name).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📥 Download URL", command=download_from_url).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="💾 Salvar", command=save_changes, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ Cancelar", command=edit_window.destroy).pack(side=tk.LEFT)
        
    def search_cover_for_file(self, index, cover_label):
        """Busca capa para um arquivo específico"""
        file_data = self.files_data[index]
        
        if not file_data['artist'] or not file_data['title']:
            return
            
        try:
            # Buscar capa
            cover_image = self.search_cover_all_sources(file_data['artist'], file_data['title'])
            
            if cover_image:
                file_data['cover'] = cover_image
                self.update_file_in_tree(index, file_data)
                
                # Atualizar preview na janela de edição
                if cover_label:
                    cover_image_copy = cover_image.copy()
                    cover_image_copy.thumbnail((150, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(cover_image_copy)
                    cover_label.config(image=photo)
                    cover_label.image = photo
                
                self.log_message(f"✅ Capa encontrada para: {file_data['artist']} - {file_data['title']}")
            else:
                self.log_message(f"❌ Capa não encontrada para: {file_data['artist']} - {file_data['title']}")
                
        except Exception as e:
            self.log_message(f"Erro ao buscar capa: {e}")
            
    def search_cover_by_custom_name(self, index, search_name, cover_label):
        """Busca capa por nome personalizado"""
        file_data = self.files_data[index]
        
        try:
            # Buscar capa por nome personalizado
            cover_image = self.search_cover_all_sources(search_name, "")
            
            if cover_image:
                file_data['cover'] = cover_image
                self.update_file_in_tree(index, file_data)
                
                # Atualizar preview na janela de edição
                if cover_label:
                    cover_image_copy = cover_image.copy()
                    cover_image_copy.thumbnail((150, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(cover_image_copy)
                    cover_label.config(image=photo)
                    cover_label.image = photo
                
                self.log_message(f"✅ Capa encontrada para: {search_name}")
            else:
                self.log_message(f"❌ Capa não encontrada para: {search_name}")
                
        except Exception as e:
            self.log_message(f"Erro ao buscar capa: {e}")
            
    def download_cover_from_url(self, index, url, cover_label):
        """Download de capa de URL"""
        file_data = self.files_data[index]
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                image.thumbnail((80, 80), Image.Resampling.LANCZOS)
                
                file_data['cover'] = image
                self.update_file_in_tree(index, file_data)
                
                # Atualizar preview na janela de edição
                if cover_label:
                    cover_image_copy = image.copy()
                    cover_image_copy.thumbnail((150, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(cover_image_copy)
                    cover_label.config(image=photo)
                    cover_label.image = photo
                
                self.log_message(f"✅ Capa baixada de: {url}")
            else:
                self.log_message(f"❌ Erro ao baixar capa de: {url}")
                
        except Exception as e:
            self.log_message(f"Erro ao baixar capa: {e}")
            
    def show_context_menu(self, event):
        """Mostra menu de contexto"""
        item = self.files_tree.selection()[0]
        index = int(self.files_tree.item(item, "values")[0]) - 1
        
        if 0 <= index < len(self.files_data):
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Edit", command=lambda: self.edit_file_manual(index))
            context_menu.add_command(label="Search Cover", command=lambda: self.search_cover_for_file(index, None))
            context_menu.add_separator()
            context_menu.add_command(label="Copy Filename to Tag", command=lambda: self.copy_filename_to_tag(index))
            context_menu.add_command(label="Copy Tag to Filename", command=lambda: self.copy_tag_to_filename(index))
            context_menu.add_separator()
            context_menu.add_command(label="Remove from List", command=lambda: self.remove_file_from_list(index))
            context_menu.add_command(label="Open Folder", command=lambda: self.open_file_folder(index))
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def on_double_click(self, event):
        """Função chamada quando há duplo clique na TreeView para editar arquivo"""
        if not self.files_tree.selection():
            return
            
        item = self.files_tree.selection()[0]
        index = int(self.files_tree.item(item, "values")[0]) - 1
        
        if 0 <= index < len(self.files_data):
            self.edit_file_manual(index)
                
    def open_file_folder(self, index):
        """Abre pasta do arquivo"""
        file_data = self.files_data[index]
        folder_path = os.path.dirname(file_data['path'])
        os.startfile(folder_path)
        
    def remove_file_from_list(self, index):
        """Remove file from the list"""
        if 0 <= index < len(self.files_data):
            file_data = self.files_data[index]
            filename = os.path.basename(file_data['path'])
            
            # Confirm removal
            result = messagebox.askyesno("Remove File", 
                                       f"Remove '{filename}' from the list?\n\nThis will not delete the file from disk.")
            
            if result:
                # Remove from data list
                self.files_data.pop(index)
                
                # Refresh the tree view
                self.refresh_tree_view()
                
                self.log_message(f"📤 Removed '{filename}' from list")
                
    def refresh_tree_view(self):
        """Refresh the tree view with current files data"""
        # Clear existing items
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
            
        # Clear cover thumbnails cache
        if hasattr(self, 'cover_thumbnails'):
            self.cover_thumbnails.clear()
        else:
            self.cover_thumbnails = {}
            
        # Re-populate with current data
        # Columns order: ("#", "Album", "Original", "New", "Artist", "Title", "Status")
        for i, file_data in enumerate(self.files_data):
            filename = os.path.basename(file_data['path'])
            artist = file_data.get('artist', '')
            title = file_data.get('title', '')
            album = file_data.get('album', '')
            status = file_data.get('status', 'Pending')
            # Usar 'new' ou 'new_name' dependendo da estrutura
            new_name = file_data.get('new', file_data.get('new_name', ''))
            
            # Inserir item com ou sem capa
            if file_data.get('cover'):
                # Criar preview da capa
                cover_image = file_data['cover'].copy()
                cover_image.thumbnail((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(cover_image)
                
                # Inserir item com imagem
                item = self.files_tree.insert('', 'end', image=photo, values=(
                    i + 1,      # #
                    album,      # Album
                    filename,   # Original Name
                    new_name,   # New Name
                    artist,     # Artist
                    title,      # Title
                    status      # Status
                ))
                
                # Manter referência da imagem para evitar GC
                self.cover_thumbnails[item] = photo
            else:
                # Inserir item sem imagem
                self.files_tree.insert('', 'end', values=(
                    i + 1,      # #
                    album,      # Album
                    filename,   # Original Name
                    new_name,   # New Name
                    artist,     # Artist
                    title,      # Title
                    status      # Status
                ))
    
    def sort_by_status(self):
        """Sort files by status column"""
        if not self.files_data:
            return
            
        # Define status priority for sorting
        status_priority = {
            'Pending': 0,
            'Processing': 1,
            'Error': 2,
            'Completed': 3,
            'Deezer': 4,
            'TheAudioDB': 5,
            'YouTube Music': 6,
            'Manual': 7,
            # Also include the old format for compatibility
            '✅ Deezer': 4,
            '✅ TheAudioDB': 5,
            '✅ YTMusic': 6,
            '✅ Manual': 7
        }
        
        # Sort files_data by status
        self.files_data.sort(
            key=lambda x: status_priority.get(x.get('status', 'Pending'), 999),
            reverse=self.sort_reverse
        )
        
        # Toggle sort direction for next click
        self.sort_reverse = not self.sort_reverse
        
        # Refresh the tree view with sorted data
        self.refresh_tree_view()
        
        # Log the sorting action
        direction = "descending" if not self.sort_reverse else "ascending"
        self.log_message(f"📊 Files sorted by status ({direction})")
            
    def copy_filename_to_tag(self, index):
        """Copy filename to artist and title tags"""
        if 0 <= index < len(self.files_data):
            file_data = self.files_data[index]
            filename = os.path.basename(file_data['path'])
            filename_no_ext = os.path.splitext(filename)[0]
            
            # Extract artist and title from filename
            artist, title = self.extract_artist_title(filename_no_ext)
            
            # Update the file data
            file_data['artist'] = artist
            file_data['title'] = title
            
            # Update in tree view
            self.update_file_in_tree(index, file_data)
            
            self.log_message(f"📝 Copied filename to tags: {artist} - {title}")
            
    def copy_tag_to_filename(self, index):
        """Copy tag information to filename"""
        if 0 <= index < len(self.files_data):
            file_data = self.files_data[index]
            artist = file_data.get('artist', '').strip()
            title = file_data.get('title', '').strip()
            
            if artist and title:
                # Clean the artist and title for filename
                clean_artist = self.clean_filename(artist)
                clean_title = self.clean_filename(title)
                
                # Create new filename
                new_filename = f"{clean_artist} - {clean_title}.mp3"
                
                # Get current path info
                current_path = file_data['path']
                folder_path = os.path.dirname(current_path)
                new_path = os.path.join(folder_path, new_filename)
                
                # Check if file already exists
                if os.path.exists(new_path) and new_path != current_path:
                    messagebox.showwarning("File Exists", 
                                         f"A file with the name '{new_filename}' already exists.")
                    return
                
                try:
                    # Rename the file
                    if new_path != current_path:
                        os.rename(current_path, new_path)
                        file_data['path'] = new_path
                        
                        # Update in tree view
                        self.update_file_in_tree(index, file_data)
                        
                        self.log_message(f"📝 Renamed file to: {new_filename}")
                    else:
                        self.log_message("📝 Filename already matches tags")
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Could not rename file: {e}")
                    self.log_message(f"❌ Error renaming file: {e}")
            else:
                messagebox.showwarning("Missing Tags", 
                                     "Artist and Title tags are required to rename the file.")
                self.log_message("⚠️ Cannot rename: missing artist or title tags")
        
    # New functions for action buttons
    def get_selected_file_index(self):
        """Get the index of the currently selected file"""
        selection = self.files_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a file first.")
            return None
        
        item = selection[0]
        index = int(self.files_tree.item(item, "values")[0]) - 1
        
        if 0 <= index < len(self.files_data):
            return index
        return None
    
    def edit_selected_file(self):
        """Edit the selected file"""
        index = self.get_selected_file_index()
        if index is not None:
            self.edit_file_manual(index)
    
    def search_cover_selected(self):
        """Search cover for the selected file"""
        index = self.get_selected_file_index()
        if index is not None:
            # Create a dummy label for the search
            dummy_label = ttk.Label(self.root)
            self.search_cover_for_file(index, dummy_label)
    
    def copy_filename_to_tag_selected(self):
        """Copy filename to tag for the selected file"""
        index = self.get_selected_file_index()
        if index is not None:
            self.copy_filename_to_tag(index)
    
    def copy_tag_to_filename_selected(self):
        """Copy tag to filename for the selected file"""
        index = self.get_selected_file_index()
        if index is not None:
            self.copy_tag_to_filename(index)
    
    def remove_selected_file(self):
        """Remove the selected file from the list"""
        index = self.get_selected_file_index()
        if index is not None:
            self.remove_file_from_list(index)
    
    def open_selected_folder(self):
        """Open folder of the selected file"""
        index = self.get_selected_file_index()
        if index is not None:
            self.open_file_folder(index)
    
    def normalize_album_name(self, album_name):
        """Normaliza nome do álbum removendo variações desnecessárias"""
        if not album_name:
            return ""
        
        # Remover caracteres especiais e espaços extras
        normalized = re.sub(r'[^\w\s-]', '', album_name)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Remover sufixos comuns que causam separação
        suffixes_to_remove = [
            r'\s*-\s*\d{4}$',  # Remove " - 2024"
            r'\s*\(\d{4}\)$',  # Remove " (2024)"
            r'\s*\[\d{4}\]$',  # Remove " [2024]"
            r'\s*-\s*deluxe.*$',  # Remove " - deluxe edition"
            r'\s*-\s*extended.*$',  # Remove " - extended"
            r'\s*-\s*remaster.*$',  # Remove " - remastered"
            r'\s*-\s*special.*$',  # Remove " - special edition"
        ]
        
        for suffix in suffixes_to_remove:
            normalized = re.sub(suffix, '', normalized, flags=re.IGNORECASE)
        
        return normalized.strip()
    
    def detect_album_inconsistencies(self):
        """Detecta e sugere correções para álbuns inconsistentes"""
        if not self.files_data:
            return
        
        # Agrupar álbuns por nome normalizado
        album_groups = {}
        for i, file_data in enumerate(self.files_data):
            original_album = file_data.get('album', '')
            normalized_album = self.normalize_album_name(original_album)
            
            if normalized_album not in album_groups:
                album_groups[normalized_album] = []
            album_groups[normalized_album].append((i, original_album))
        
        # Encontrar grupos com múltiplas variações
        inconsistencies = []
        for normalized, files in album_groups.items():
            if len(files) > 1:
                # Verificar se há variações no nome original
                unique_originals = set(original for _, original in files)
                if len(unique_originals) > 1:
                    inconsistencies.append((normalized, files, unique_originals))
        
        if inconsistencies:
            self.show_album_correction_dialog(inconsistencies)
        else:
            messagebox.showinfo("Álbuns", "Todos os álbuns estão consistentes!")
    
    def show_album_correction_dialog(self, inconsistencies):
        """Mostra diálogo para corrigir inconsistências de álbum"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Corrigir Álbuns Inconsistentes")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Álbuns com nomes inconsistentes encontrados:", 
                 style='Header.TLabel').pack(anchor=tk.W, pady=(0, 10))
        
        # Frame com scroll
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        corrections = {}
        
        for i, (normalized, files, unique_originals) in enumerate(inconsistencies):
            group_frame = ttk.LabelFrame(scrollable_frame, text=f"Grupo {i+1}", padding="10")
            group_frame.pack(fill=tk.X, pady=(0, 10))
            
            ttk.Label(group_frame, text=f"Variações encontradas:").pack(anchor=tk.W)
            for original in unique_originals:
                ttk.Label(group_frame, text=f"  • {original}", 
                         font=('Arial', 9)).pack(anchor=tk.W, padx=(20, 0))
            
            ttk.Label(group_frame, text="Nome sugerido:").pack(anchor=tk.W, pady=(10, 0))
            suggested_name = max(unique_originals, key=len)  # Usar o nome mais longo
            
            correction_var = tk.StringVar(value=suggested_name)
            corrections[normalized] = (correction_var, files)
            
            ttk.Entry(group_frame, textvariable=correction_var, width=60).pack(fill=tk.X, pady=(5, 0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def apply_corrections():
            for normalized, (correction_var, files) in corrections.items():
                new_album_name = correction_var.get().strip()
                if new_album_name:
                    for file_index, _ in files:
                        self.files_data[file_index]['album'] = new_album_name
                        self.update_file_in_tree(file_index, self.files_data[file_index])
            
            self.log_message(f"💿 Corrigidas inconsistências em {len(corrections)} grupos de álbuns")
            dialog.destroy()
            messagebox.showinfo("Sucesso", "Álbuns corrigidos com sucesso!")
        
        ttk.Button(button_frame, text="Aplicar Correções", 
                  command=apply_corrections, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancelar", 
                  command=dialog.destroy).pack(side=tk.LEFT)
    
    def fix_album_inconsistencies(self):
        """Detecta e corrige inconsistências nos nomes dos álbuns"""
        if not self.files_data:
            messagebox.showwarning("Sem Ficheiros", "Nenhum ficheiro carregado para verificar álbuns.")
            return
        
        self.detect_album_inconsistencies()
    
    def set_album_name_all(self):
        """Set album name for all files"""
        if not self.files_data:
            messagebox.showwarning("No Files", "No files loaded to set album name.")
            return
        
        album_name = simpledialog.askstring("Set Album Name", 
                                           "Enter album name for all files:",
                                           initialvalue="")
        
        if album_name:
            # Normalizar o nome do álbum
            normalized_album = self.normalize_album_name(album_name)
            
            for i, file_data in enumerate(self.files_data):
                file_data['album'] = normalized_album
                self.update_file_in_tree(i, file_data)
            
            self.log_message(f"💿 Set album name '{normalized_album}' for {len(self.files_data)} files")
            messagebox.showinfo("Album Set", f"Album name '{normalized_album}' set for all files.")
        
    def update_file_in_tree(self, index, file_data):
        """Atualiza arquivo na treeview com preview da capa imediato"""
        # Encontrar item na treeview
        items = self.files_tree.get_children()
        if index < len(items):
            item = items[index]
            
            # Mostrar capa
            if file_data['cover']:
                # Criar preview da capa maior
                cover_image = file_data['cover'].copy()
                cover_image.thumbnail((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(cover_image)
                
                # Atualizar item com imagem (sem coluna "Capa" duplicada)
                self.files_tree.item(item, image=photo, values=(
                    file_data['index'],
                    file_data['album'],
                    file_data['original'],
                    file_data['new'],
                    file_data['artist'],
                    file_data['title'],
                    file_data['status']
                ))
                
                # Manter referência da imagem por item para evitar GC
                if not hasattr(self, 'cover_thumbnails'):
                    self.cover_thumbnails = {}
                self.cover_thumbnails[item] = photo
            else:
                # Sem capa
                self.files_tree.item(item, values=(
                    file_data['index'],
                    file_data['album'],
                    file_data['original'],
                    file_data['new'],
                    file_data['artist'],
                    file_data['title'],
                    file_data['status']
                ))
            
    def save_changes(self):
        """Salva todas as alterações"""
        if not self.files_data:
            messagebox.showwarning("Aviso", "Nenhum arquivo carregado!")
            return
            
        # Ask user where to save files
        choice = messagebox.askyesnocancel("Save Location", 
                                          "Save files to a new folder?\n\n"
                                          "Yes = Choose new folder\n"
                                          "No = Save in original locations\n"
                                          "Cancel = Cancel operation")
        
        if choice is None:  # Cancel
            return
        
        self.save_destination = None
        if choice:  # Yes - choose new folder
            self.save_destination = filedialog.askdirectory(
                title="Choose destination folder for saved files",
                initialdir=os.path.expanduser("~")
            )
            if not self.save_destination:
                return
            
        try:
            self.save_btn.config(state="disabled")
            self.progress.start()
            self.status_label.config(text="Gravando...", style='Warning.TLabel')
            
            thread = threading.Thread(target=self.save_all_changes)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.log_message(f"Erro ao iniciar gravação: {e}")
            
    def save_all_changes(self):
        """Salva todas as alterações fisicamente"""
        try:
            if hasattr(self, 'save_destination') and self.save_destination:
                self.log_message(f"💾 Salvando arquivos na pasta: {self.save_destination}")
            else:
                self.log_message("💾 Salvando arquivos nas localizações originais")
            self.log_message("=" * 70)
            
            saved_count = 0
            
            for i, file_data in enumerate(self.files_data):
                try:
                    old_path = file_data['path']
                    
                    # Determine destination path
                    if hasattr(self, 'save_destination') and self.save_destination:
                        # Save to chosen folder
                        filename = file_data.get('new', file_data['original'])
                        if not filename.endswith('.mp3'):
                            filename += '.mp3'
                        new_path = os.path.join(self.save_destination, filename)
                    else:
                        # Save in original location with new name if changed
                        if file_data.get('new') and file_data['new'] != file_data['original']:
                            new_path = os.path.join(os.path.dirname(old_path), file_data['new'] + '.mp3')
                        else:
                            new_path = old_path
                    
                    # Copy or rename file
                    if new_path != old_path:
                        if hasattr(self, 'save_destination') and self.save_destination:
                            # Copy to new location
                            import shutil
                            shutil.copy2(old_path, new_path)
                            self.log_message(f"📁 Copiado: {os.path.basename(old_path)} → {filename}")
                        else:
                            # Rename in place
                            if not os.path.exists(new_path):
                                os.rename(old_path, new_path)
                                self.log_message(f"📝 Renomeado: {file_data['original']} → {file_data['new']}.mp3")
                            else:
                                self.log_message(f"⚠️ Arquivo já existe: {file_data['new']}.mp3")
                                continue
                        
                        file_data['path'] = new_path
                    
                    # Update metadata
                    self.set_text_tags(new_path, file_data['artist'], file_data['title'], 
                                     file_data['album'], track_number=file_data['index'])
                    self.log_message(f"🏷️ Metadados atualizados (faixa #{file_data['index']})")
                    
                    # Add cover if found
                    if file_data['cover']:
                        self.embed_cover_art(new_path, file_data['cover'], None)
                        self.log_message(f"🖼️ Capa adicionada ao arquivo")
                    
                    saved_count += 1
                    
                except Exception as e:
                    self.log_message(f"❌ Erro ao salvar {file_data['original']}: {e}")
            
            self.log_message("=" * 70)
            self.log_message(f"✅ Gravação concluída! {saved_count} arquivos salvos.")
            
        except Exception as e:
            self.log_message(f"❌ Erro geral na gravação: {e}")
        finally:
            self.root.after(0, self.save_finished)
            
    def set_text_tags(self, path, artist, title, album, year=None, track_number=None):
        """Atualiza metadados do arquivo com ID3 v2.3 e UTF-16"""
        try:
            # Usar mutagen diretamente para controle total sobre TPE2 e codificação
            from mutagen.id3 import ID3, TIT2, TPE1, TALB, TPE2, TDRC, TRCK, ID3NoHeaderError
            from mutagen.id3._util import Encoding
            
            try:
                tags = ID3(path)
            except ID3NoHeaderError:
                tags = ID3()
            
            # Configurar codificação UTF-16 para ID3v2.3
            encoding = Encoding.UTF16
            
            if artist:
                artist_clean = self.transliterate_if_needed(artist)
                tags["TPE1"] = TPE1(encoding=encoding, text=[artist_clean])
            
            if title:
                title_clean = self.transliterate_if_needed(title)
                tags["TIT2"] = TIT2(encoding=encoding, text=[title_clean])
            
            if album:
                album_normalized = self.transliterate_if_needed(album)
                tags["TALB"] = TALB(encoding=encoding, text=[album_normalized])
                
                # IMPORTANTE: TPE2 (AlbumArtist) para sistemas de carros
                album_artist = self.determine_album_artist(album_normalized, artist)
                tags["TPE2"] = TPE2(encoding=encoding, text=[album_artist])
                
            if year:
                tags["TDRC"] = TDRC(encoding=encoding, text=[str(year)])
                
            if track_number:
                tags["TRCK"] = TRCK(encoding=encoding, text=[str(track_number)])
            
            # Salvar com ID3 v2.3 e UTF-16
            tags.save(path, v2_version=3, v23_sep='/', v2_padding=None)
            
        except Exception as e:
            # Fallback para EasyID3 se houver erro
            try:
                tags = self.ensure_easyid3(path)
                if artist:
                    tags["artist"] = self.transliterate_if_needed(artist)
                if title:
                    tags["title"] = self.transliterate_if_needed(title)
                if album:
                    album_normalized = self.transliterate_if_needed(album)
                    tags["album"] = album_normalized
                    album_artist = self.determine_album_artist(album_normalized, artist)
                    tags["albumartist"] = album_artist
                if year:
                    tags["date"] = str(year)
                if track_number:
                    tags["tracknumber"] = str(track_number)
                tags.save(v2_version=3)
            except Exception as e2:
                self.log_message(f"  Erro ao atualizar metadados: {e2}")
    
    def determine_album_artist(self, album, artist):
        """Determina o AlbumArtist mais apropriado para sistemas de carros"""
        if not album:
            return "Various Artists"
        
        # Se o álbum contém palavras como "mix", "compilation", "various", usar "Various Artists"
        album_lower = album.lower()
        compilation_keywords = ['mix', 'compilation', 'various', 'collection', 'hits', 'best of']
        
        for keyword in compilation_keywords:
            if keyword in album_lower:
                return "Various Artists"
        
        # Se o nome do álbum contém o nome do artista, usar o artista
        if artist and artist.lower() in album_lower:
            return artist
        
        # Para álbuns genéricos (como "musicas 2024"), usar "Various Artists"
        generic_keywords = ['musicas', 'songs', 'music', 'tracks']
        for keyword in generic_keywords:
            if keyword in album_lower:
                return "Various Artists"
        
        # Caso padrão: usar "Various Artists" para garantir agrupamento
        return "Various Artists"
            
    def embed_cover_art(self, path, image, mime):
        """Adiciona capa ao arquivo, substituindo existente"""
        try:
            filename = os.path.basename(path)
            self.log_message(f"🖼️ Embutindo capa em: {filename}")
            
            # Melhorar qualidade da imagem
            # Redimensionar para uma resolução ótima se necessário
            max_size = 1000  # Tamanho máximo recomendado para capas
            if image.size[0] > max_size or image.size[1] > max_size:
                # Manter proporção ao redimensionar
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                self.log_message(f"   📐 Imagem redimensionada para: {image.size[0]}x{image.size[1]}")
            
            # Converter imagem para bytes com alta qualidade
            img_byte_arr = io.BytesIO()
            
            # Detectar formato original da imagem
            original_format = image.format if hasattr(image, 'format') else None
            
            # Preferir PNG se a imagem original for PNG ou se tiver transparência
            if (original_format == 'PNG' or 
                (hasattr(image, 'mode') and image.mode in ('RGBA', 'LA')) or
                (hasattr(image, 'info') and 'transparency' in image.info)):
                
                # Salvar como PNG para preservar qualidade e transparência
                image.save(img_byte_arr, format='PNG', optimize=True)
                mime = 'image/png'
                self.log_message(f"   🎨 Formato PNG preservado para melhor qualidade")
            else:
                # Usar qualidade 95% para JPEG (padrão é 75%)
                image.save(img_byte_arr, format='JPEG', quality=95, optimize=True)
                mime = 'image/jpeg'
                self.log_message(f"   🎨 Convertido para JPEG com qualidade 95%")
            
            img_byte_arr = img_byte_arr.getvalue()
            
            self.log_message(f"   📏 Tamanho da imagem: {len(img_byte_arr)} bytes")
            
            audio = MP3(path, ID3=ID3)
            if audio.tags is None:
                audio.add_tags()
                self.log_message(f"   🏷️ Tags ID3 criadas")
            
            # Remover todas as capas existentes
            audio.tags.delall("APIC")
            self.log_message(f"   🗑️ Capas existentes removidas")
            
            # Adicionar nova capa
            audio.tags.add(APIC(encoding=3, mime=mime, type=3, desc="Front cover", data=img_byte_arr))
            self.log_message(f"   ➕ Nova capa adicionada")
            
            # Salvar com versão ID3 v2.3
            audio.save(v2_version=3)
            self.log_message(f"   ✅ Arquivo salvo com capa embutida")
            
            # Verificar se a capa foi realmente salva
            audio_check = MP3(path, ID3=ID3)
            if audio_check.tags:
                for frame in audio_check.tags.values():
                    if isinstance(frame, APIC):
                        self.log_message(f"   ✅ Verificação: Capa embutida confirmada!")
                        return
            self.log_message(f"   ⚠️ Verificação: Capa não encontrada após salvamento")
            
        except Exception as e:
            filename = os.path.basename(path)
            self.log_message(f"❌ Erro ao embutir capa em {filename}: {e}")
            
    def ensure_easyid3(self, path):
        """Garante que o arquivo tem tags ID3 v2.3"""
        try:
            return EasyID3(path)
        except Exception:
            audio = MP3(path, ID3=ID3)
            if audio.tags is None:
                audio.add_tags()
            # Salvar com versão ID3 v2.3
            audio.save(v2_version=3)
            return EasyID3(path)
            
    def transliterate_if_needed(self, text):
        """Translitera apenas se contém caracteres não-LATIN"""
        if not text:
            return ""
        
        # Verificar se contém caracteres não-LATIN
        has_non_latin = any(ord(char) > 127 for char in text)
        
        if has_non_latin:
            return unidecode(text).strip()
        else:
            return text.strip()
            
    def processing_finished(self):
        """Chamado quando o processamento termina"""
        self.process_btn.config(state="normal")
        self.progress.stop()
        self.status_label.config(text="Pronto", style='Status.TLabel')
        
    def manual_processing_finished(self):
        """Chamado quando o processamento manual termina"""
        self.progress.stop()
        self.status_label.config(text="Pronto", style='Status.TLabel')
        
    def save_finished(self):
        """Called when saving finishes"""
        self.save_btn.config(state="normal")
        self.progress.stop()
        self.status_label.config(text="Ready", style='Status.TLabel')
        
        # Show SAVED popup
        self.show_saved_popup()
    
    def show_saved_popup(self):
        """Show a modern SAVED popup"""
        popup = tk.Toplevel(self.root)
        popup.title("Saved")
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.configure(bg=self.colors['surface'])
        
        # Center the popup
        popup.transient(self.root)
        popup.grab_set()
        
        # Center on parent window
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        popup.geometry(f"300x150+{x}+{y}")
        
        # Success icon and message
        main_frame = tk.Frame(popup, bg=self.colors['surface'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Success icon (checkmark)
        icon_label = tk.Label(main_frame, text="✓", font=("Segoe UI", 32), 
                             fg="#4CAF50", bg=self.colors['surface'])
        icon_label.pack(pady=(10, 5))
        
        # SAVED text
        saved_label = tk.Label(main_frame, text="SAVED", font=("Segoe UI", 16, "bold"), 
                              fg=self.colors['dark'], bg=self.colors['surface'])
        saved_label.pack(pady=5)
        
        # OK button
        ok_btn = tk.Button(main_frame, text="OK", font=("Segoe UI", 10),
                          bg=self.colors['secondary'], fg='white',
                          relief='flat', padx=20, pady=5,
                          command=popup.destroy)
        ok_btn.pack(pady=(15, 0))
        
        # Auto close after 2 seconds
        popup.after(2000, popup.destroy)

        
    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🎵 MP3 Album Tool - Final Optimized Version")
    print("=" * 70)
    print("Starting application...")
    print("=" * 70)
    
    app = FinalMP3Tool()
    app.run()
