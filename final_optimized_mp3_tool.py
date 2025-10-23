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
    def init_translations(self):
        """Initialize translation system"""
        self.translations = {
            'en': {
                'app_title': 'MP3 Album Tool - Professional Edition',
                'playlist_creator': 'M3U Playlist Creator',
                'instructions': 'How to use:\n1. Add folders containing your MP3 files\n2. Configure sorting and subfolder options\n3. Enter playlist name\n4. Click "Create Playlist" and choose where to save',
                'selected_folders': 'Selected Folders',
                'add_folder': 'Add Folder',
                'remove': 'Remove',
                'move_up': 'Move Up',
                'move_down': 'Move Down',
                'options': 'Options',
                'sort_files': 'Sort files alphabetically within each folder',
                'include_subfolders': 'Include subfolders',
                'playlist_name': 'Playlist Name:',
                'create_playlist': 'Create Playlist',
                'cancel': 'Cancel',
                'save_location': 'Choose where to save the playlist M3U:',
                'desktop': 'Desktop',
                'usb_root': 'USB Root (For Car)',
                'choose_location': 'Choose Location',
                'warning': 'Warning',
                'select_folder_warning': 'Select at least one folder to create the playlist.',
                'success': 'Success',
                'playlist_created': 'M3U Playlist created successfully!',
                'error': 'Error',
                'no_usb_detected': 'No USB/Pendrive detected.\nPlease connect a USB and try again.',
                'choose_usb': 'Choose USB',
                'save_playlist_title': 'Save M3U Playlist - Choose location and filename',
                'force_covers': 'Force Cover Update',
                'title_field': 'Title',
                'album_field': 'Album',
                'car_info': 'If your car creates separate albums for each song,\nuncheck "Artist" and "Title" for better organization.',
                'restore_defaults': 'Restore Defaults',
                'source_settings': 'Source Settings',
                'rename_sources': 'Sources for Renaming',
                'search_precision': 'Search Precision',
            'fill_artist_title_first': 'Please fill in artist and title first!',
            'albums': 'Albums',
            'all_albums_consistent': 'All albums are consistent!',
            'fix_inconsistent_albums': 'Fix Inconsistent Albums',
            'albums_fixed_successfully': 'Albums fixed successfully!',
            'no_files_loaded_check_albums': 'No files loaded to check albums.',
            'no_files_loaded': 'No files loaded!',
            'select_folder_first': 'Please select a folder first!',
            'apply_corrections': 'Apply Corrections',
            'm3u_compatibility': 'M3U Compatibility',
            'choose_path_format': 'Choose path format for maximum compatibility:',
            'absolute_paths': 'Absolute paths (Windows Media Player)',
            'relative_paths': 'Relative paths (VLC, Universal players)',
                'manual_edit': 'Manual Edit',
                'inconsistent_albums': 'Albums with inconsistent names found:',
                'apply_corrections': 'Apply Corrections',
                'process_subfolders': 'Process Subfolders',
                'capitalize_names': 'Capitalize Names',
                'mp3_folder': 'MP3 Folder:',
                'browse_folder': 'Browse Folder',
                'add_files': 'Add Files',
                'configure_sources': 'Configure Sources',
                'configure_metadata': 'Configure Metadata',
                'create_m3u_playlist': 'Create M3U Playlist',
                'language_settings': 'Language/Idioma',
                'process_mp3s': 'Process MP3s',
                'save_changes': 'Save Changes',
                'pause': 'Pause',
                'stop': 'Stop',
                'edit': 'Edit',
                'cover': 'Cover',
                'album': 'Album',
                'fix_albums': 'Fix Albums',
                'metadata_settings': 'Metadata Settings',
                'metadata_to_save': 'Metadata to Save',
                'select_metadata_info': 'Select which metadata should be saved to MP3 files',
                'artist': 'Artist',
                'title': 'Title',
                'albumartist': 'AlbumArtist',
            'year': 'Year',
            'track': 'Track',
            'tip_for_cars': 'Tip for Cars',
            'car_tip_text': 'If your car creates separate albums for each song,\nuncheck \'Artist\' and \'Title\' for better organization.',
            'select_folder_title': 'Select folder with MP3 files',
            'select_files_title': 'Select MP3 Files',
            'error_loading_file': 'Error loading',
            'files_added': 'Added {} file(s) to the list',
            'no_new_files_added': 'No new files were added (duplicates or invalid files)',
            'tip_add_files': '💡 Tip: Use \'Add Files\' button to select MP3 files from any location',
            'rename_sources': 'Rename Sources',
            'cover_sources': 'Cover Sources',
            'search_precision': 'Search Precision',
            'ok': 'OK'
            },
            'pt': {
                'app_title': 'MP3 Album Tool - Edição Profissional',
                'playlist_creator': 'Criador de Playlists M3U',
                'instructions': 'Como usar:\n1. Adicione as pastas que contêm suas músicas MP3\n2. Configure as opções de ordenação e subpastas\n3. Digite o nome da playlist\n4. Clique em "Criar Playlist" e escolha onde salvar',
                'selected_folders': 'Pastas Selecionadas',
                'add_folder': 'Adicionar Pasta',
                'remove': 'Remover',
                'move_up': 'Subir',
                'move_down': 'Descer',
                'options': 'Opções',
                'sort_files': 'Ordenar arquivos alfabeticamente dentro de cada pasta',
                'include_subfolders': 'Incluir subpastas',
                'playlist_name': 'Nome da Playlist:',
                'create_playlist': 'Criar Playlist',
                'cancel': 'Cancelar',
                'save_location': 'Escolha onde salvar a playlist M3U:',
                'desktop': 'Área de Trabalho',
                'usb_root': 'Raiz do USB (Para Carro)',
                'choose_location': 'Escolher Local',
                'warning': 'Aviso',
                'select_folder_warning': 'Selecione pelo menos uma pasta para criar a playlist.',
                'success': 'Sucesso',
                'playlist_created': 'Playlist M3U criada com sucesso!',
                'error': 'Erro',
                'no_usb_detected': 'Nenhum USB/Pendrive detectado.\nPor favor, conecte um USB e tente novamente.',
                'choose_usb': 'Escolher USB',
                'save_playlist_title': 'Salvar Playlist M3U - Escolha o local e nome do arquivo',
                'force_covers': 'Forçar Atualização de Capas',
                'title_field': 'Título',
                'album_field': 'Álbum',
                'car_info': 'Se o seu carro cria álbuns separados para cada música,\ndesmarque "Artista" e "Título" para melhor organização.',
                'restore_defaults': 'Restaurar Padrões',
                'source_settings': 'Configurações de Fontes',
                'rename_sources': 'Fontes para Renomeação',
                'search_precision': 'Precisão de Busca',
            'fill_artist_title_first': 'Preencha artista e título primeiro!',
            'albums': 'Álbuns',
            'all_albums_consistent': 'Todos os álbuns estão consistentes!',
            'fix_inconsistent_albums': 'Corrigir Álbuns Inconsistentes',
            'albums_fixed_successfully': 'Álbuns corrigidos com sucesso!',
            'no_files_loaded_check_albums': 'Nenhum ficheiro carregado para verificar álbuns.',
            'no_files_loaded': 'Nenhum arquivo carregado!',
            'select_folder_first': 'Selecione uma pasta primeiro!',
            'apply_corrections': 'Aplicar Correções',
            'm3u_compatibility': 'Compatibilidade M3U',
            'choose_path_format': 'Escolha o formato de caminho para máxima compatibilidade:',
            'absolute_paths': 'Caminhos absolutos (Windows Media Player)',
            'relative_paths': 'Caminhos relativos (VLC, Players universais)',
                'manual_edit': 'Edição Manual',
                'inconsistent_albums': 'Álbuns com nomes inconsistentes encontrados:',
                'apply_corrections': 'Aplicar Correções',
                'process_subfolders': 'Processar Subpastas',
                'capitalize_names': 'Capitalizar Nomes',
                'mp3_folder': 'Pasta MP3:',
                'browse_folder': 'Procurar Pasta',
                'add_files': 'Adicionar Arquivos',
                'configure_sources': 'Configurar Fontes',
                'configure_metadata': 'Configurar Metadados',
                'create_m3u_playlist': 'Criar Playlist M3U',
                'language_settings': 'Language/Idioma',
                'process_mp3s': 'Processar MP3s',
                'save_changes': 'Salvar Alterações',
                'pause': 'Pausar',
                'stop': 'Parar',
                'edit': 'Editar',
                'cover': 'Capa',
                'album': 'Álbum',
                'fix_albums': 'Corrigir Álbuns',
                'metadata_settings': 'Configurações de Metadados',
                'metadata_to_save': 'Metadados para Gravar',
                'select_metadata_info': 'Selecione quais metadados devem ser gravados nos arquivos MP3',
                'artist': 'Artista',
                'title': 'Título',
                'albumartist': 'AlbumArtist',
            'year': 'Ano',
            'track': 'Faixa',
            'tip_for_cars': 'Dica para Carros',
            'car_tip_text': 'Se o seu carro cria álbuns separados para cada música,\ndesmarque \'Artista\' e \'Título\' para melhor organização.',
            'select_folder_title': 'Selecionar pasta com arquivos MP3',
            'select_files_title': 'Selecionar Arquivos MP3',
            'error_loading_file': 'Erro ao carregar',
            'files_added': 'Adicionados {} arquivo(s) à lista',
            'no_new_files_added': 'Nenhum arquivo novo foi adicionado (duplicados ou arquivos inválidos)',
            'tip_add_files': '💡 Dica: Use o botão \'Adicionar Arquivos\' para selecionar arquivos MP3 de qualquer local',
            'rename_sources': 'Fontes para Renomeação',
            'cover_sources': 'Fontes para Capas',
            'search_precision': 'Precisão de Busca',
            'ok': 'OK'
            }
        }
        
    def load_settings(self):
        """Load user settings from config file"""
        self.settings_file = 'mp3_tool_settings.json'
        self.default_settings = {
            'language': 'en',
            'sort_files_default': False,
            'include_subfolders_default': True,
            'last_playlist_name': 'My_Playlist'
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            else:
                self.settings = self.default_settings.copy()
        except:
            self.settings = self.default_settings.copy()
            
        # Ensure all default settings exist
        for key, value in self.default_settings.items():
            if key not in self.settings:
                self.settings[key] = value
                
    def save_settings(self):
        """Save user settings to config file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def t(self, key):
        """Get translated text"""
        return self.translations.get(self.settings['language'], self.translations['en']).get(key, key)

    def __init__(self):
        # Initialize translations and settings
        self.init_translations()
        self.load_settings()
        
        self.root = tk.Tk()
        self.root.title(f"🎵 {self.t('app_title')}")
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
        
        # Configurações de metadados para gravação (para resolver problema do carro)
        self.save_artist_tag = tk.BooleanVar(value=True)
        self.save_title_tag = tk.BooleanVar(value=True)
        self.save_album_tag = tk.BooleanVar(value=True)
        self.save_albumartist_tag = tk.BooleanVar(value=True)
        self.save_year_tag = tk.BooleanVar(value=False)
        self.save_track_tag = tk.BooleanVar(value=False)
        
        self.files_data = []
        self.covers_cache = {}
        self.editing_item = None
        self.processed = False
        
        # YouTube Music API instance (reutilizar para evitar conflitos)
        self.ytmusic_instance = None
        
        # Progress tracking variables
        self.current_progress = 0
        self.total_files = 0
        self.progress_var = tk.DoubleVar()  # For progress percentage
        self.progress_text = tk.StringVar(value="Ready")
        
        # Sorting control
        self.sort_reverse = False
        
        self.setup_ui()
        
    def get_ytmusic_instance(self):
        """Obtém instância do YTMusic com retry e tratamento robusto"""
        if self.ytmusic_instance is not None:
            return self.ytmusic_instance
        
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                self.log_message(f"📡 Tentativa {attempt}/{max_attempts} - Inicializando YouTube Music...")
                
                # Importar aqui para evitar problemas de inicialização
                from ytmusicapi import YTMusic
                
                # Criar instância
                self.ytmusic_instance = YTMusic()
                
                # Teste rápido para verificar se está funcionando
                test_results = self.ytmusic_instance.search("test", filter="songs", limit=1)
                
                self.log_message(f"✅ YouTube Music inicializado com sucesso (tentativa {attempt})")
                return self.ytmusic_instance
                
            except Exception as e:
                self.log_message(f"❌ Tentativa {attempt} falhou: {e}")
                
                if attempt < max_attempts:
                    wait_time = attempt * 2  # Backoff progressivo
                    self.log_message(f"⏳ Aguardando {wait_time}s antes da próxima tentativa...")
                    time.sleep(wait_time)
                else:
                    self.log_message("❌ Todas as tentativas de inicialização do YouTube Music falharam")
        
        return None
    
    def reset_ytmusic_instance(self):
        """Reseta a instância do YouTube Music para forçar uma nova inicialização"""
        self.log_message("🔄 Resetando instância do YouTube Music...")
        self.ytmusic_instance = None
        
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
        
        # Info button (blue)
        style.configure('Info.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       foreground='#000000',  # Explicit black hex
                       background='#3498db',  # Nice blue
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        style.map('Info.TButton', 
                 background=[('active', '#2980b9'), ('pressed', '#21618c')],
                 foreground=[('active', '#000000'), ('pressed', '#000000')])
        
        # Secondary button (gray)
        style.configure('Secondary.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       foreground='#000000',  # Explicit black hex
                       background='#95a5a6',  # Nice gray
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        style.map('Secondary.TButton', 
                 background=[('active', '#7f8c8d'), ('pressed', '#6c7b7d')],
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
        
        ttk.Label(folder_frame, text=f"📁 {self.t('mp3_folder')}", 
                 style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 15))
        
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.selected_folder, 
                                     width=70, font=('Segoe UI', 10), style='Modern.TEntry')
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        ttk.Button(folder_frame, text=f"📂 {self.t('browse_folder')}", 
                  command=self.select_folder, style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(folder_frame, text=f"📄 {self.t('add_files')}", 
                  command=self.select_files, style='Secondary.TButton').pack(side=tk.LEFT)
        
        # Quick options row
        quick_options_frame = ttk.Frame(config_frame)
        quick_options_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Checkbutton(quick_options_frame, text=f"📁 {self.t('process_subfolders')}", 
                       variable=self.recursive_var,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 30))
        
        ttk.Checkbutton(quick_options_frame, text=f"🔄 {self.t('force_covers')}", 
                       variable=self.force_cover_var,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 30))
        
        ttk.Checkbutton(quick_options_frame, text=f"🔤 {self.t('capitalize_names')}", 
                       variable=self.capitalize_names_var,
                       style='Modern.TCheckbutton').pack(side=tk.LEFT, padx=(0, 30))
        
        # Configuration buttons row
        config_buttons_frame = ttk.Frame(config_frame)
        config_buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(config_buttons_frame, text=f"🔍 {self.t('configure_sources')}", 
                  command=self.open_sources_settings, style='Info.TButton').pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(config_buttons_frame, text=f"🏷️ {self.t('configure_metadata')}", 
                  command=self.open_metadata_settings, style='Info.TButton').pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(config_buttons_frame, text=f"🎵 {self.t('create_m3u_playlist')}", 
                  command=self.open_playlist_creator, style='Success.TButton').pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(config_buttons_frame, text=f"🌐 {self.t('language_settings')}", 
                  command=self.open_language_settings, style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 15))
        
        # Modern action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=20)
        
        self.process_btn = ttk.Button(action_frame, text=f"🚀 {self.t('process_mp3s')}", 
                                     command=self.start_processing, style='Primary.TButton')
        self.process_btn.pack(side=tk.LEFT, padx=(0, 15))
        

        
        self.save_btn = ttk.Button(action_frame, text=f"💾 {self.t('save_changes')}", 
                                  command=self.save_changes, state="disabled", style='Success.TButton')
        self.save_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Control buttons
        self.pause_btn = ttk.Button(action_frame, text=f"⏸️ {self.t('pause')}", 
                                   command=self.toggle_pause, state="disabled", style='Orange.TButton')
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(action_frame, text=f"⏹️ {self.t('stop')}", 
                                  command=self.request_stop, state="disabled", style='Danger.TButton')
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # File action buttons in the same row
        ttk.Button(action_frame, text=f"✏️ {self.t('edit')}", 
                  command=self.edit_selected_file, style='Info.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text=f"🔍 {self.t('cover')}", 
                  command=self.search_cover_selected, style='Info.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text="📝➡️🏷️", 
                  command=self.copy_filename_to_tag_selected, style='Info.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text="🏷️➡️📝", 
                  command=self.copy_tag_to_filename_selected, style='Info.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text="🗑️", 
                  command=self.remove_selected_file, style='Danger.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text=f"💿 {self.t('album')}", 
                  command=self.set_album_name_all, style='Warning.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(action_frame, text=f"🔧 {self.t('fix_albums')}", 
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
        
    def open_metadata_settings(self):
        """Abre janela de configurações de metadados"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title(f"⚙️ {self.t('metadata_settings')}")
        settings_window.geometry("500x400")
        settings_window.configure(bg=self.colors['background'])
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Centralizar janela
        settings_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        main_frame = ttk.Frame(settings_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text=f"🏷️ {self.t('metadata_to_save')}", 
                               font=('Segoe UI', 12, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = ttk.Label(main_frame, 
                                  text=self.t('select_metadata_info'),
                                  font=('Segoe UI', 9))
        subtitle_label.pack(pady=(0, 20))
        
        # Checkboxes frame
        checkboxes_frame = ttk.Frame(main_frame)
        checkboxes_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Organizar em duas colunas
        left_frame = ttk.Frame(checkboxes_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        right_frame = ttk.Frame(checkboxes_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Checkboxes da esquerda
        ttk.Checkbutton(left_frame, text=f"🎤 {self.t('artist')}", 
                       variable=self.save_artist_tag).pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(left_frame, text=f"🎵 {self.t('title')}", 
                       variable=self.save_title_tag).pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(left_frame, text=f"💿 {self.t('album')}", 
                       variable=self.save_album_tag).pack(anchor=tk.W, pady=5)
        
        # Checkboxes da direita
        ttk.Checkbutton(right_frame, text=f"👥 {self.t('albumartist')}", 
                       variable=self.save_albumartist_tag).pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(right_frame, text=f"📅 {self.t('year')}", 
                       variable=self.save_year_tag).pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(right_frame, text=f"🔢 {self.t('track')}", 
                       variable=self.save_track_tag).pack(anchor=tk.W, pady=5)
        
        # Info sobre compatibilidade com carros
        info_frame = ttk.LabelFrame(main_frame, text=f"💡 {self.t('tip_for_cars')}", padding="15")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_text = ttk.Label(info_frame, 
                             text=self.t('car_tip_text'),
                             font=('Segoe UI', 9),
                             justify=tk.LEFT)
        info_text.pack()
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text=f"✅ {self.t('ok')}", 
                  command=settings_window.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(buttons_frame, text=f"🔄 {self.t('restore_defaults')}", 
                  command=self.restore_metadata_defaults).pack(side=tk.RIGHT)
    
    def open_sources_settings(self):
        """Abre janela de configurações de fontes"""
        sources_window = tk.Toplevel(self.root)
        sources_window.title(f"🔍 {self.t('source_settings')}")
        sources_window.geometry("600x500")
        sources_window.configure(bg=self.colors['background'])
        sources_window.transient(self.root)
        sources_window.grab_set()
        
        # Centralizar janela
        sources_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        main_frame = ttk.Frame(sources_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text=f"🔍 {self.t('source_settings')}", 
                               font=('Segoe UI', 12, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Seção de Renomeação
        rename_frame = ttk.LabelFrame(main_frame, text=f"📝 {self.t('rename_sources')}", padding="15")
        rename_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Checkbutton(rename_frame, text="🎵 Deezer", 
                       variable=self.use_deezer_rename).pack(anchor=tk.W, pady=3)
        
        ttk.Checkbutton(rename_frame, text="🎸 TheAudioDB", 
                       variable=self.use_theaudiodb_rename).pack(anchor=tk.W, pady=3)
        
        ttk.Checkbutton(rename_frame, text="📺 YouTube Music (Free)", 
                       variable=self.use_ytmusic_rename).pack(anchor=tk.W, pady=3)
        
        # Seção de Capas
        cover_frame = ttk.LabelFrame(main_frame, text=f"🖼️ {self.t('cover_sources')}", padding="15")
        cover_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Checkbutton(cover_frame, text="🎵 Deezer", 
                       variable=self.use_deezer_cover).pack(anchor=tk.W, pady=3)
        
        ttk.Checkbutton(cover_frame, text="🎸 TheAudioDB", 
                       variable=self.use_theaudiodb_cover).pack(anchor=tk.W, pady=3)
        
        ttk.Checkbutton(cover_frame, text="📺 YouTube Music", 
                       variable=self.use_ytmusic_cover).pack(anchor=tk.W, pady=3)
        
        ttk.Checkbutton(cover_frame, text="🔍 Google Images", 
                       variable=self.use_google_covers).pack(anchor=tk.W, pady=3)
        
        # Threshold
        threshold_frame = ttk.LabelFrame(main_frame, text=f"🎯 {self.t('search_precision')}", padding="15")
        threshold_frame.pack(fill=tk.X, pady=(0, 20))
        
        threshold_inner = ttk.Frame(threshold_frame)
        threshold_inner.pack(fill=tk.X)
        
        ttk.Label(threshold_inner, text="Match Threshold:").pack(side=tk.LEFT)
        
        threshold_scale = ttk.Scale(threshold_inner, from_=50, to=100, 
                                   variable=self.fuzzy_threshold, orient=tk.HORIZONTAL)
        threshold_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        
        threshold_label = ttk.Label(threshold_inner, text=f"{self.fuzzy_threshold.get()}%")
        threshold_label.pack(side=tk.RIGHT)
        
        def update_threshold_display(value):
            threshold_label.config(text=f"{int(float(value))}%")
        
        threshold_scale.configure(command=update_threshold_display)
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text=f"✅ {self.t('ok')}", 
                  command=sources_window.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(buttons_frame, text=f"🔄 {self.t('restore_defaults')}", 
                  command=self.restore_sources_defaults).pack(side=tk.RIGHT)
    
    def open_language_settings(self):
        """Opens language settings window"""
        lang_window = tk.Toplevel(self.root)
        lang_window.title("🌐 Language Settings / Configurações de Idioma")
        lang_window.geometry("500x400")
        lang_window.configure(bg=self.colors['background'])
        lang_window.transient(self.root)
        lang_window.grab_set()
        lang_window.resizable(False, False)
        
        # Centralizar janela
        lang_window.update_idletasks()
        x = (lang_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (lang_window.winfo_screenheight() // 2) - (400 // 2)
        lang_window.geometry(f"500x400+{x}+{y}")
        
        main_frame = ttk.Frame(lang_window, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="🌐 Choose Language / Escolher Idioma", 
                               font=('Segoe UI', 12, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Informações
        info_text = ("Select your preferred language for the application interface.\n"
                    "Selecione seu idioma preferido para a interface da aplicação.\n\n"
                    f"Current language / Idioma atual: {self.settings['language'].upper()}")
        
        info_label = ttk.Label(main_frame, text=info_text, 
                              font=('Segoe UI', 9), foreground='#666666')
        info_label.pack(pady=(0, 20))
        
        # Opções de idioma
        lang_frame = ttk.LabelFrame(main_frame, text="Available Languages / Idiomas Disponíveis", padding="15")
        lang_frame.pack(fill=tk.X, pady=(0, 20))
        
        current_lang = tk.StringVar(value=self.settings['language'])
        
        # English
        ttk.Radiobutton(lang_frame, text="🇺🇸 English", 
                       variable=current_lang, value='en').pack(anchor=tk.W, pady=5)
        
        # Portuguese
        ttk.Radiobutton(lang_frame, text="🇵🇹 Português", 
                       variable=current_lang, value='pt').pack(anchor=tk.W, pady=5)
        
        def apply_language():
            new_lang = current_lang.get()
            if new_lang != self.settings['language']:
                self.settings['language'] = new_lang
                self.save_settings()
                
                # Show restart message
                if new_lang == 'en':
                    restart_msg = ("Language changed to English!\n\n"
                                  "Please restart the application to see all changes.\n"
                                  "Some interface elements will update immediately.")
                else:
                    restart_msg = ("Idioma alterado para Português!\n\n"
                                  "Por favor, reinicie a aplicação para ver todas as mudanças.\n"
                                  "Alguns elementos da interface serão atualizados imediatamente.")
                
                messagebox.showinfo("Language Changed / Idioma Alterado", restart_msg)
            
            lang_window.destroy()
        
        def cancel_changes():
            lang_window.destroy()
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(30, 0))
        
        # Adicionar espaçamento
        ttk.Label(buttons_frame, text="").pack(side=tk.LEFT, expand=True)
        
        ttk.Button(buttons_frame, text="❌ Cancel / Cancelar", 
                  command=cancel_changes).pack(side=tk.RIGHT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="✅ Apply / Aplicar", 
                  command=apply_language).pack(side=tk.RIGHT)
    
    def open_playlist_creator(self):
        """Opens window for M3U playlist creation"""
        self.playlist_window = tk.Toplevel(self.root)
        self.playlist_window.title(f"🎵 {self.t('playlist_creator')}")
        self.playlist_window.geometry("800x600")
        self.playlist_window.configure(bg=self.colors['background'])
        self.playlist_window.transient(self.root)
        self.playlist_window.grab_set()
        
        # Centralizar janela
        self.playlist_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        main_frame = ttk.Frame(self.playlist_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título e instruções
        title_label = ttk.Label(main_frame, text=f"🎵 {self.t('playlist_creator')}", 
                               font=('Segoe UI', 12, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Instruções
        instructions_label = ttk.Label(main_frame, text=f"💡 {self.t('instructions')}", 
                                     font=('Segoe UI', 9), foreground='#666666')
        instructions_label.pack(pady=(0, 15))
        
        # Frame para seleção de pastas
        folders_frame = ttk.LabelFrame(main_frame, text=f"📁 {self.t('selected_folders')}", padding="10")
        folders_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Lista de pastas com scrollbar
        folders_list_frame = ttk.Frame(folders_frame)
        folders_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.folders_listbox = tk.Listbox(folders_list_frame, height=10)
        folders_scrollbar = ttk.Scrollbar(folders_list_frame, orient=tk.VERTICAL, command=self.folders_listbox.yview)
        self.folders_listbox.configure(yscrollcommand=folders_scrollbar.set)
        
        self.folders_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        folders_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botões para gerenciar pastas
        folders_buttons_frame = ttk.Frame(folders_frame)
        folders_buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(folders_buttons_frame, text=f"➕ {self.t('add_folder')}", 
                  command=self.add_folder_to_playlist).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(folders_buttons_frame, text=f"🗑️ {self.t('remove')}", 
                  command=self.remove_folder_from_playlist).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(folders_buttons_frame, text=f"⬆️ {self.t('move_up')}", 
                  command=self.move_folder_up).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(folders_buttons_frame, text=f"⬇️ {self.t('move_down')}", 
                  command=self.move_folder_down).pack(side=tk.LEFT, padx=(0, 10))
        
        # Opções de ordenação
        options_frame = ttk.LabelFrame(main_frame, text=f"⚙️ {self.t('options')}", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.sort_files_var = tk.BooleanVar(value=self.settings['sort_files_default'])
        ttk.Checkbutton(options_frame, text=f"📊 {self.t('sort_files')}", 
                       variable=self.sort_files_var).pack(anchor=tk.W)
        
        self.include_subfolders_var = tk.BooleanVar(value=self.settings['include_subfolders_default'])
        ttk.Checkbutton(options_frame, text=f"📁 {self.t('include_subfolders')}", 
                       variable=self.include_subfolders_var).pack(anchor=tk.W)
        
        # Nome da playlist
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(name_frame, text=f"📝 {self.t('playlist_name')}").pack(side=tk.LEFT, padx=(0, 10))
        
        self.playlist_name_var = tk.StringVar(value=self.settings['last_playlist_name'])
        playlist_name_entry = ttk.Entry(name_frame, textvariable=self.playlist_name_var, width=30)
        playlist_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botões finais
        final_buttons_frame = ttk.Frame(main_frame)
        final_buttons_frame.pack(fill=tk.X)
        
        ttk.Button(final_buttons_frame, text=f"💾 {self.t('create_playlist')}", 
                  command=self.create_m3u_playlist).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(final_buttons_frame, text=f"❌ {self.t('cancel')}", 
                  command=self.playlist_window.destroy).pack(side=tk.RIGHT)
        
        # Inicializar lista de pastas
        self.playlist_folders = []
    
    def restore_metadata_defaults(self):
        """Restaura configurações padrão de metadados"""
        self.save_artist_tag.set(True)
        self.save_title_tag.set(True)
        self.save_album_tag.set(True)
        self.save_albumartist_tag.set(True)
        self.save_year_tag.set(False)
        self.save_track_tag.set(False)
    
    def restore_sources_defaults(self):
        """Restaura configurações padrão de fontes"""
        self.use_deezer_rename.set(True)
        self.use_theaudiodb_rename.set(True)
        self.use_ytmusic_rename.set(True)
        self.use_deezer_cover.set(True)
        self.use_theaudiodb_cover.set(True)
        self.use_ytmusic_cover.set(True)
        self.use_google_covers.set(True)
        self.fuzzy_threshold.set(80)
    
    def add_folder_to_playlist(self):
        """Adiciona uma pasta à lista de pastas da playlist"""
        folder = filedialog.askdirectory(
            title="Selecionar pasta para adicionar à playlist",
            initialdir=os.path.expanduser("~")
        )
        if folder and folder not in self.playlist_folders:
            self.playlist_folders.append(folder)
            self.folders_listbox.insert(tk.END, folder)
    
    def remove_folder_from_playlist(self):
        """Remove a pasta selecionada da lista"""
        selection = self.folders_listbox.curselection()
        if selection:
            index = selection[0]
            self.folders_listbox.delete(index)
            del self.playlist_folders[index]
    
    def move_folder_up(self):
        """Move a pasta selecionada para cima na lista"""
        selection = self.folders_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            # Trocar posições na lista
            self.playlist_folders[index], self.playlist_folders[index-1] = \
                self.playlist_folders[index-1], self.playlist_folders[index]
            
            # Atualizar listbox
            self.folders_listbox.delete(index)
            self.folders_listbox.insert(index-1, self.playlist_folders[index-1])
            self.folders_listbox.selection_set(index-1)
    
    def move_folder_down(self):
        """Move a pasta selecionada para baixo na lista"""
        selection = self.folders_listbox.curselection()
        if selection and selection[0] < len(self.playlist_folders) - 1:
            index = selection[0]
            # Trocar posições na lista
            self.playlist_folders[index], self.playlist_folders[index+1] = \
                self.playlist_folders[index+1], self.playlist_folders[index]
            
            # Atualizar listbox
            self.folders_listbox.delete(index)
            self.folders_listbox.insert(index+1, self.playlist_folders[index+1])
            self.folders_listbox.selection_set(index+1)
    
    def create_m3u_playlist(self):
        """Creates M3U playlist with selected folders"""
        if not self.playlist_folders:
            messagebox.showwarning(self.t('warning'), self.t('select_folder_warning'))
            return
        
        playlist_name = self.playlist_name_var.get().strip()
        if not playlist_name:
            playlist_name = self.settings['last_playlist_name']
            
        # Save current settings
        self.settings['last_playlist_name'] = playlist_name
        self.settings['sort_files_default'] = self.sort_files_var.get()
        self.settings['include_subfolders_default'] = self.include_subfolders_var.get()
        self.save_settings()
        
        # Garantir que o nome termine com .m3u
        if not playlist_name.lower().endswith('.m3u'):
            playlist_name += '.m3u'
        
        # Mostrar informações sobre as pastas selecionadas
        folder_info = f"{self.t('selected_folders')} ({len(self.playlist_folders)}):\n"
        for i, folder in enumerate(self.playlist_folders[:5], 1):  # Mostrar apenas as primeiras 5
            folder_info += f"{i}. {os.path.basename(folder)}\n"
        if len(self.playlist_folders) > 5:
            folder_info += f"... and {len(self.playlist_folders) - 5} more folders\n"
        
        yes_no = {True: "Yes", False: "No"} if self.settings['language'] == 'en' else {True: "Sim", False: "Não"}
        folder_info += f"\n{self.t('include_subfolders')}: {yes_no[self.include_subfolders_var.get()]}\n"
        folder_info += f"{self.t('sort_files')}: {yes_no[self.sort_files_var.get()]}\n\n"
        folder_info += self.t('save_location')
        
        # Mostrar informações e opções de salvamento
        save_options = (f"{folder_info}\n\n"
                       f"💾 {self.t('save_location')}\n\n"
                       f"🖥️ {self.t('desktop')} - For computer use\n"
                       f"🚗 {self.t('usb_root')} - For car use\n"
                       f"📁 {self.t('choose_location')}")
        
        # Criar janela personalizada para escolha
        save_window = tk.Toplevel(self.playlist_window)
        save_window.title(self.t('save_playlist_title'))
        save_window.geometry("500x500")
        save_window.resizable(False, False)
        save_window.transient(self.playlist_window)
        save_window.grab_set()
        
        # Centralizar janela
        save_window.update_idletasks()
        x = (save_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (save_window.winfo_screenheight() // 2) - (500 // 2)
        save_window.geometry(f"500x500+{x}+{y}")
        
        main_frame = ttk.Frame(save_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Informações
        info_text = tk.Text(main_frame, height=8, wrap=tk.WORD, font=('Segoe UI', 9))
        info_text.pack(fill=tk.X, pady=(0, 20))
        info_text.insert(tk.END, save_options)
        info_text.config(state=tk.DISABLED)
        
        # Seção de compatibilidade M3U
        compat_frame = ttk.LabelFrame(main_frame, text=f"🎵 {self.t('m3u_compatibility')}", padding="10")
        compat_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Variável para formato de caminho (padrão: relativos para compatibilidade universal)
        path_format_var = tk.StringVar(value="relative")
        
        ttk.Label(compat_frame, text=self.t('choose_path_format'), 
                 font=('Segoe UI', 9)).pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Radiobutton(compat_frame, text=f"🖥️ {self.t('absolute_paths')}", 
                       variable=path_format_var, value="absolute").pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(compat_frame, text=f"🌐 {self.t('relative_paths')}", 
                       variable=path_format_var, value="relative").pack(anchor=tk.W, pady=2)
        
        # Variável para armazenar a escolha
        save_choice = tk.StringVar()
        save_path = None
        
        def save_to_desktop():
            nonlocal save_path
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            save_path = os.path.join(desktop_path, playlist_name)
            save_window.destroy()
        
        def save_to_usb():
            nonlocal save_path
            # Detectar drives disponíveis (incluindo USB)
            import string
            drives = []
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    try:
                        # Tentar verificar se é removível usando ctypes
                        import ctypes
                        drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)
                        # DRIVE_REMOVABLE = 2, DRIVE_FIXED = 3
                        if drive_type == 2:  # Removível (USB, etc.)
                            drives.append(drive)
                        elif drive != "C:\\":  # Incluir outros drives que não sejam C:
                            drives.append(drive)
                    except:
                        # Se não conseguir detectar, incluir drives que não sejam C:
                        if drive != "C:\\":
                            drives.append(drive)
            
            if not drives:
                messagebox.showwarning(self.t('warning'), self.t('no_usb_detected'))
                return
            
            if len(drives) == 1:
                save_path = os.path.join(drives[0], playlist_name)
                save_window.destroy()
            else:
                # Mostrar opções de USB
                usb_window = tk.Toplevel(save_window)
                usb_window.title(self.t('choose_usb'))
                usb_window.geometry("300x200")
                usb_window.transient(save_window)
                usb_window.grab_set()
                
                ttk.Label(usb_window, text=f"{self.t('choose_usb')}:", font=('Segoe UI', 10, 'bold')).pack(pady=10)
                
                for drive in drives:
                    def select_drive(d=drive):
                        nonlocal save_path
                        save_path = os.path.join(d, playlist_name)
                        usb_window.destroy()
                        save_window.destroy()
                    
                    ttk.Button(usb_window, text=f"💾 Drive {drive}", 
                              command=select_drive).pack(pady=5)
        
        def save_custom():
            nonlocal save_path
            # Temporarily hide the save window to avoid dialog issues
            save_window.withdraw()
            try:
                # Use the main window as parent instead of playlist_window to avoid issues
                save_path = filedialog.asksaveasfilename(
                    title=self.t('save_playlist_title'),
                    defaultextension=".m3u",
                    filetypes=[("M3U Playlist", "*.m3u"), ("All files", "*.*")],
                    initialfile=playlist_name,
                    parent=self.root
                )
                if save_path:
                    save_window.destroy()
                else:
                    save_window.deiconify()  # Show window again if cancelled
            except Exception as e:
                save_window.deiconify()  # Show window again if error
                messagebox.showerror(self.t('error'), f"Erro ao abrir diálogo de salvamento: {e}")
                print(f"Error in save dialog: {e}")
        
        def cancel_save():
            save_window.destroy()
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(buttons_frame, text=f"🖥️ {self.t('desktop')}", 
                  command=save_to_desktop).pack(fill=tk.X, pady=2)
        
        ttk.Button(buttons_frame, text=f"🚗 {self.t('usb_root')}", 
                  command=save_to_usb).pack(fill=tk.X, pady=2)
        
        ttk.Button(buttons_frame, text=f"📁 {self.t('choose_location')}", 
                  command=save_custom).pack(fill=tk.X, pady=2)
        
        ttk.Button(buttons_frame, text=f"❌ {self.t('cancel')}", 
                  command=cancel_save).pack(fill=tk.X, pady=(10, 0))
        
        # Aguardar escolha
        save_window.wait_window()
        
        if not save_path:
            return
        
        try:
            with open(save_path, 'w', encoding='utf-8') as playlist_file:
                playlist_file.write("#EXTM3U\n")
                
                total_files = 0
                all_mp3_files = []
                
                # Coletar todos os arquivos MP3 de todas as pastas
                for folder in self.playlist_folders:
                    if not os.path.exists(folder):
                        continue
                    
                    # Coletar arquivos MP3
                    mp3_files = []
                    
                    if self.include_subfolders_var.get():
                        # Incluir subpastas
                        for root, dirs, files in os.walk(folder):
                            for file in files:
                                if file.lower().endswith('.mp3'):
                                    mp3_files.append(os.path.join(root, file))
                    else:
                        # Apenas pasta atual
                        for file in os.listdir(folder):
                            file_path = os.path.join(folder, file)
                            if os.path.isfile(file_path) and file.lower().endswith('.mp3'):
                                mp3_files.append(file_path)
                    
                    all_mp3_files.extend(mp3_files)
                
                # Ordenar arquivos se solicitado
                if self.sort_files_var.get():
                    all_mp3_files.sort()
                
                # Agrupar arquivos por álbum
                albums = {}
                files_without_album = []
                
                for mp3_file in all_mp3_files:
                    try:
                        # Extrair metadados incluindo álbum
                        artist, title = self.extract_existing_metadata(mp3_file)
                        
                        # Tentar extrair álbum usando mutagen
                        try:
                            from mutagen.mp3 import MP3
                            from mutagen.id3 import ID3NoHeaderError
                            
                            audio = MP3(mp3_file)
                            album = None
                            
                            # Tentar diferentes tags de álbum
                            if 'TALB' in audio:
                                album = str(audio['TALB'][0]).strip()
                            elif 'TIT2' in audio:  # Se não há álbum, usar título como fallback
                                album = "Singles"
                            
                            if album and album != "":
                                if album not in albums:
                                    albums[album] = []
                                albums[album].append((mp3_file, artist, title))
                            else:
                                files_without_album.append((mp3_file, artist, title))
                                
                        except:
                            files_without_album.append((mp3_file, artist, title))
                            
                    except:
                        files_without_album.append((mp3_file, None, None))
                
                # Escrever arquivos agrupados por álbum usando tags #EXTALB
                for album_name in sorted(albums.keys()):
                    for mp3_file, artist, title in albums[album_name]:
                        # Adicionar tag de álbum padrão M3U
                        playlist_file.write(f"#EXTALB:{album_name}\n")
                        
                        # Criar linha EXTINF
                        if artist and title:
                            extinf_line = f"#EXTINF:-1,{artist} - {title}\n"
                        else:
                            # Usar nome do arquivo sem extensão
                            filename = os.path.splitext(os.path.basename(mp3_file))[0]
                            extinf_line = f"#EXTINF:-1,{filename}\n"
                        
                        # Determinar o caminho a usar baseado na opção selecionada
                        if path_format_var.get() == "relative":
                            # Usar caminho relativo ao arquivo M3U
                            try:
                                file_path_to_write = os.path.relpath(mp3_file, os.path.dirname(save_path))
                                # Converter barras invertidas para barras normais (padrão Unix/Web)
                                file_path_to_write = file_path_to_write.replace('\\', '/')
                            except ValueError:
                                # Se não conseguir criar caminho relativo, usar absoluto
                                file_path_to_write = mp3_file
                        else:
                            # Usar caminho absoluto
                            file_path_to_write = mp3_file
                        
                        playlist_file.write(extinf_line)
                        playlist_file.write(f"{file_path_to_write}\n")
                        total_files += 1
                
                # Processar arquivos sem álbum
                if files_without_album:
                    for mp3_file, artist, title in files_without_album:
                        # Para arquivos sem álbum, usar tag genérica
                        playlist_file.write(f"#EXTALB:Singles\n")
                        
                        # Criar linha EXTINF
                        if artist and title:
                            extinf_line = f"#EXTINF:-1,{artist} - {title}\n"
                        else:
                            # Usar nome do arquivo sem extensão
                            filename = os.path.splitext(os.path.basename(mp3_file))[0]
                            extinf_line = f"#EXTINF:-1,{filename}\n"
                        
                        # Determinar o caminho a usar baseado na opção selecionada
                        if path_format_var.get() == "relative":
                            try:
                                file_path_to_write = os.path.relpath(mp3_file, os.path.dirname(save_path))
                                file_path_to_write = file_path_to_write.replace('\\', '/')
                            except ValueError:
                                file_path_to_write = mp3_file
                        else:
                            file_path_to_write = mp3_file
                        
                        playlist_file.write(extinf_line)
                        playlist_file.write(f"{file_path_to_write}\n")
                        total_files += 1
            
            # Mostrar mensagem de sucesso com informações detalhadas
            folder_name = os.path.dirname(save_path)
            file_name = os.path.basename(save_path)
            
            if self.settings['language'] == 'en':
                success_msg = (f"✅ {self.t('playlist_created')}\n\n"
                              f"📁 Folder: {folder_name}\n"
                              f"📄 File: {file_name}\n"
                              f"🎵 Total songs: {total_files}\n\n"
                              f"💡 Tip: You can open this file in any music player "
                              f"that supports M3U playlists (VLC, Windows Media Player, etc.)")
            else:
                success_msg = (f"✅ {self.t('playlist_created')}\n\n"
                              f"📁 Pasta: {folder_name}\n"
                              f"📄 Arquivo: {file_name}\n"
                              f"🎵 Total de músicas: {total_files}\n\n"
                              f"💡 Dica: Você pode abrir este arquivo em qualquer player de música "
                              f"que suporte playlists M3U (VLC, Windows Media Player, etc.)")
            
            messagebox.showinfo(self.t('success'), success_msg)
            
        except Exception as e:
            messagebox.showerror(self.t('error'), f"{self.t('error')}: {str(e)}")
        
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
            title=self.t('select_folder_title'),
            initialdir=os.path.expanduser("~")
        )
        if folder:
            self.selected_folder.set(folder)
            self.load_mp3_files(folder)
            
    def select_files(self):
        """Select individual MP3 files from any location"""
        file_paths = filedialog.askopenfilenames(
            title=self.t('select_files_title'),
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
                    self.log_message(f"❌ {self.t('error_loading_file')} {os.path.basename(file_path)}: {e}")
        
        if added_count > 0:
            # Refresh the tree view
            self.refresh_tree_view()
            self.log_message(f"📁 {self.t('files_added').format(added_count)}")
            
            # Load covers for new files
            self.load_existing_covers()
        else:
             self.log_message(f"⚠️ {self.t('no_new_files_added')}")
             
    def setup_drag_and_drop(self):
        """Setup basic drag and drop functionality"""
        # For now, we'll focus on the file selection functionality
        # Advanced drag and drop can be added later with tkinterdnd2 if needed
        self.log_message(f"💡 {self.t('tip_add_files')}")
            
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
        """Busca informações no YouTube Music com retry automático"""
        max_attempts = 2
        
        for attempt in range(1, max_attempts + 1):
            try:
                artist_guess, title_guess = self.extract_artist_title(filename)
                
                if not artist_guess or not title_guess:
                    return None, None
                
                # Obter instância reutilizável do YouTube Music API
                ytmusic = self.get_ytmusic_instance()
                if not ytmusic:
                    return None, None
                
                # Buscar por artista e título
                search_query = f"{artist_guess} {title_guess}"
                self.log_message(f"🔍 YouTube Music: Buscando '{search_query}' (tentativa {attempt})")
                
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
                                self.log_message(f"✅ YouTube Music: Encontrado '{artist} - {title}'")
                                return artist, title
                
                self.log_message(f"⚠️ YouTube Music: Nenhum resultado encontrado para '{search_query}'")
                return None, None
                
            except Exception as e:
                self.log_message(f"❌ YouTube Music tentativa {attempt} falhou: {e}")
                
                if attempt < max_attempts:
                    # Reset da instância para tentar novamente
                    self.reset_ytmusic_instance()
                    time.sleep(1)
                else:
                    self.log_message("❌ YouTube Music: Todas as tentativas falharam")
        
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
        """Busca capa no YouTube Music com retry automático"""
        max_attempts = 2
        
        for attempt in range(1, max_attempts + 1):
            try:
                # Obter instância reutilizável do YouTube Music API
                ytmusic = self.get_ytmusic_instance()
                if not ytmusic:
                    return None
                
                # Buscar por artista e título
                search_query = f"{artist} {title}"
                self.log_message(f"🖼️ YouTube Music: Buscando capa para '{search_query}' (tentativa {attempt})")
                
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
                                        self.log_message(f"✅ YouTube Music: Capa encontrada {image.size[0]}x{image.size[1]}")
                                        
                                        return image
                
                self.log_message(f"⚠️ YouTube Music: Nenhuma capa encontrada para '{search_query}'")
                return None
                
            except Exception as e:
                self.log_message(f"❌ YouTube Music capa tentativa {attempt} falhou: {e}")
                
                if attempt < max_attempts:
                    # Reset da instância para tentar novamente
                    self.reset_ytmusic_instance()
                    time.sleep(1)
                else:
                    self.log_message("❌ YouTube Music capa: Todas as tentativas falharam")
        
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
        
    def sanitize_filename(self, filename):
        """Remove caracteres especiais que causam problemas no Windows"""
        if not filename:
            return filename
            
        # Caracteres proibidos no Windows: < > : " | ? * \
        # Também remover / que pode causar problemas
        forbidden_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        
        # Substituir caracteres proibidos por equivalentes seguros ou remover
        replacements = {
            '<': '(',
            '>': ')',
            ':': ' -',
            '"': "'",
            '|': '-',
            '?': '',
            '*': '',
            '\\': '-',
            '/': '-'
        }
        
        sanitized = filename
        for char in forbidden_chars:
            if char in replacements:
                sanitized = sanitized.replace(char, replacements[char])
            else:
                sanitized = sanitized.replace(char, '')
        
        # Limpar espaços múltiplos e caracteres no início/fim
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        # Remover pontos no final (problemático no Windows)
        sanitized = sanitized.rstrip('.')
        
        # Garantir que não está vazio
        if not sanitized.strip():
            sanitized = "arquivo_sem_nome"
            
        return sanitized
        
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
            messagebox.showerror(self.t('error'), self.t('select_folder_first'))
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
        
        ttk.Label(main_frame, text=f"{self.t('title_field')}:", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 5))
        title_entry = ttk.Entry(main_frame, width=70, font=('Arial', 10))
        title_entry.pack(fill=tk.X, pady=(0, 15))
        title_entry.insert(0, file_data['title'])
        
        ttk.Label(main_frame, text=f"{self.t('album_field')}:", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 5))
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
                messagebox.showwarning(self.t('warning'), self.t('fill_artist_title_first'))
        
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
            messagebox.showinfo(self.t('albums'), self.t('all_albums_consistent'))
    
    def show_album_correction_dialog(self, inconsistencies):
        """Mostra diálogo para corrigir inconsistências de álbum"""
        dialog = tk.Toplevel(self.root)
        dialog.title(self.t('fix_inconsistent_albums'))
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
            messagebox.showinfo(self.t('success'), self.t('albums_fixed_successfully'))
        
        ttk.Button(button_frame, text=self.t('apply_corrections'), 
                  command=apply_corrections, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text=self.t('cancel'), 
                  command=dialog.destroy).pack(side=tk.LEFT)
    
    def fix_album_inconsistencies(self):
        """Detecta e corrige inconsistências nos nomes dos álbuns"""
        if not self.files_data:
            messagebox.showwarning(self.t('no_files'), self.t('no_files_loaded_check_albums'))
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
            messagebox.showwarning(self.t('warning'), self.t('no_files_loaded'))
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
                        # Sanitizar nome do arquivo para remover caracteres especiais
                        filename = self.sanitize_filename(filename)
                        if not filename.endswith('.mp3'):
                            filename += '.mp3'
                        new_path = os.path.join(self.save_destination, filename)
                    else:
                        # Save in original location with new name if changed
                        if file_data.get('new') and file_data['new'] != file_data['original']:
                            # Sanitizar nome do arquivo para remover caracteres especiais
                            sanitized_name = self.sanitize_filename(file_data['new'])
                            new_path = os.path.join(os.path.dirname(old_path), sanitized_name + '.mp3')
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
            from mutagen.id3 import ID3, TIT2, TPE1, TALB, TPE2, TDRC, TRCK, ID3NoHeaderError, Encoding
            
            try:
                tags = ID3(path)
            except ID3NoHeaderError:
                tags = ID3()
            
            # LIMPAR CAMPOS DESNECESSÁRIOS que podem causar problemas em carros
            campos_para_remover = ['TPE3', 'TPE4', 'TCOM', 'TCON', 'TPOS', 'TPUB', 'TCOP', 'TENC', 'TSSE', 'TLAN', 'TIPL', 'TMCL']
            campos_removidos = []
            for campo in campos_para_remover:
                if campo in tags:
                    del tags[campo]
                    campos_removidos.append(campo)
            
            if campos_removidos:
                self.log_message(f"  🧹 Removidos campos desnecessários: {', '.join(campos_removidos)}")
            
            # Configurar codificação UTF-16 para ID3v2.3
            encoding = Encoding.UTF16
            
            # GRAVAÇÃO SELETIVA: Gravar ou remover tags baseado nas configurações
            if artist and self.save_artist_tag.get():
                artist_clean = self.transliterate_if_needed(artist)
                tags["TPE1"] = TPE1(encoding=encoding, text=[artist_clean])
                self.log_message(f"  🎤 Tag Artista gravada: {artist_clean}")
            elif not self.save_artist_tag.get():
                # Remover tag de artista se checkbox estiver desmarcado
                if "TPE1" in tags:
                    del tags["TPE1"]
                    self.log_message(f"  🗑️ Tag Artista removida (checkbox desmarcado)")
            
            if title and self.save_title_tag.get():
                title_clean = self.transliterate_if_needed(title)
                tags["TIT2"] = TIT2(encoding=encoding, text=[title_clean])
                self.log_message(f"  🎵 Tag Título gravada: {title_clean}")
            elif not self.save_title_tag.get():
                # Remover tag de título se checkbox estiver desmarcado
                if "TIT2" in tags:
                    del tags["TIT2"]
                    self.log_message(f"  🗑️ Tag Título removida (checkbox desmarcado)")
            
            if album and self.save_album_tag.get():
                album_normalized = self.transliterate_if_needed(album)
                tags["TALB"] = TALB(encoding=encoding, text=[album_normalized])
                self.log_message(f"  💿 Tag Álbum gravada: {album_normalized}")
            elif not self.save_album_tag.get():
                # Remover tag de álbum se checkbox estiver desmarcado
                if "TALB" in tags:
                    del tags["TALB"]
                    self.log_message(f"  🗑️ Tag Álbum removida (checkbox desmarcado)")
            
            # IMPORTANTE: TPE2 (AlbumArtist) para sistemas de carros - só se habilitado
            if album and self.save_album_tag.get() and self.save_albumartist_tag.get():
                album_normalized = self.transliterate_if_needed(album)
                album_artist = self.determine_album_artist(album_normalized, artist)
                tags["TPE2"] = TPE2(encoding=encoding, text=[album_artist])
                self.log_message(f"  👥 Tag AlbumArtist gravada: {album_artist}")
            elif not self.save_albumartist_tag.get():
                # Remover tag de AlbumArtist se checkbox estiver desmarcado
                if "TPE2" in tags:
                    del tags["TPE2"]
                    self.log_message(f"  🗑️ Tag AlbumArtist removida (checkbox desmarcado)")
                
            if year and self.save_year_tag.get():
                tags["TDRC"] = TDRC(encoding=encoding, text=[str(year)])
                self.log_message(f"  📅 Tag Ano gravada: {year}")
            elif not self.save_year_tag.get():
                # Remover tag de ano se checkbox estiver desmarcado
                if "TDRC" in tags:
                    del tags["TDRC"]
                    self.log_message(f"  🗑️ Tag Ano removida (checkbox desmarcado)")
                
            if track_number and self.save_track_tag.get():
                tags["TRCK"] = TRCK(encoding=encoding, text=[str(track_number)])
                self.log_message(f"  🔢 Tag Faixa gravada: {track_number}")
            elif not self.save_track_tag.get():
                # Remover tag de faixa se checkbox estiver desmarcado
                if "TRCK" in tags:
                    del tags["TRCK"]
                    self.log_message(f"  🗑️ Tag Faixa removida (checkbox desmarcado)")
            
            # Salvar com ID3 v2.3 e UTF-16
            tags.save(path, v2_version=3)
            
            # LIMPEZA FINAL: Verificar se campos problemáticos foram re-adicionados
            try:
                final_tags = ID3(path)
                campos_problematicos = ['TSSE', 'TPE3', 'TPE4', 'TCOM', 'TCON', 'TIPL', 'TMCL']
                campos_removidos_final = []
                
                for campo in campos_problematicos:
                    if campo in final_tags:
                        del final_tags[campo]
                        campos_removidos_final.append(campo)
                
                if campos_removidos_final:
                    final_tags.save(path, v2_version=3)
                    self.log_message(f"  🧹 Limpeza final: removidos {', '.join(campos_removidos_final)}")
            except:
                pass
            
        except Exception as e:
            # Fallback para EasyID3 se houver erro
            try:
                # PRIMEIRO: Limpar campos desnecessários usando ID3 direto
                try:
                    from mutagen.id3 import ID3, ID3NoHeaderError
                    id3_tags = ID3(path)
                    campos_para_remover = ['TPE3', 'TPE4', 'TCOM', 'TCON', 'TPOS', 'TPUB', 'TCOP', 'TENC', 'TSSE', 'TLAN', 'TIPL', 'TMCL']
                    campos_removidos = []
                    for campo in campos_para_remover:
                        if campo in id3_tags:
                            del id3_tags[campo]
                            campos_removidos.append(campo)
                    if campos_removidos:
                        self.log_message(f"  🧹 [Fallback] Removidos: {', '.join(campos_removidos)}")
                        id3_tags.save(path, v2_version=3)
                except:
                    pass
                
                # DEPOIS: Usar EasyID3 para definir campos essenciais - GRAVAÇÃO SELETIVA
                tags = self.ensure_easyid3(path)
                
                # Artista
                if artist and self.save_artist_tag.get():
                    tags["artist"] = self.transliterate_if_needed(artist)
                    self.log_message(f"  🎤 [Fallback] Tag Artista gravada: {artist}")
                elif not self.save_artist_tag.get():
                    if "artist" in tags:
                        del tags["artist"]
                        self.log_message(f"  🗑️ [Fallback] Tag Artista removida (checkbox desmarcado)")
                
                # Título
                if title and self.save_title_tag.get():
                    tags["title"] = self.transliterate_if_needed(title)
                    self.log_message(f"  🎵 [Fallback] Tag Título gravada: {title}")
                elif not self.save_title_tag.get():
                    if "title" in tags:
                        del tags["title"]
                        self.log_message(f"  🗑️ [Fallback] Tag Título removida (checkbox desmarcado)")
                
                # Álbum
                if album and self.save_album_tag.get():
                    album_normalized = self.transliterate_if_needed(album)
                    tags["album"] = album_normalized
                    self.log_message(f"  💿 [Fallback] Tag Álbum gravada: {album_normalized}")
                elif not self.save_album_tag.get():
                    if "album" in tags:
                        del tags["album"]
                        self.log_message(f"  🗑️ [Fallback] Tag Álbum removida (checkbox desmarcado)")
                
                # AlbumArtist
                if album and self.save_album_tag.get() and self.save_albumartist_tag.get():
                    album_normalized = self.transliterate_if_needed(album)
                    album_artist = self.determine_album_artist(album_normalized, artist)
                    tags["albumartist"] = album_artist
                    self.log_message(f"  👥 [Fallback] Tag AlbumArtist gravada: {album_artist}")
                elif not self.save_albumartist_tag.get():
                    if "albumartist" in tags:
                        del tags["albumartist"]
                        self.log_message(f"  🗑️ [Fallback] Tag AlbumArtist removida (checkbox desmarcado)")
                
                # Ano
                if year and self.save_year_tag.get():
                    tags["date"] = str(year)
                    self.log_message(f"  📅 [Fallback] Tag Ano gravada: {year}")
                elif not self.save_year_tag.get():
                    if "date" in tags:
                        del tags["date"]
                        self.log_message(f"  🗑️ [Fallback] Tag Ano removida (checkbox desmarcado)")
                
                # Faixa
                if track_number and self.save_track_tag.get():
                    tags["tracknumber"] = str(track_number)
                    self.log_message(f"  🔢 [Fallback] Tag Faixa gravada: {track_number}")
                elif not self.save_track_tag.get():
                    if "tracknumber" in tags:
                        del tags["tracknumber"]
                        self.log_message(f"  🗑️ [Fallback] Tag Faixa removida (checkbox desmarcado)")
                tags.save(v2_version=3)
                
                # LIMPEZA FINAL: Verificar se TSSE foi adicionado automaticamente e removê-lo
                try:
                    from mutagen.id3 import ID3
                    final_tags = ID3(path)
                    if 'TSSE' in final_tags:
                        del final_tags['TSSE']
                        final_tags.save(path, v2_version=3)
                        self.log_message(f"  🧹 [Fallback] TSSE removido após salvamento")
                except:
                    pass
                    
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
