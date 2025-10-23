# 🎵 MP3 Album Tool

A professional Windows application for organizing and optimizing MP3 collections for use in cars and audio systems.

## 📦 Installation

### Automatic Installation (Recommended)
1. Download the latest release from [GitHub Releases](https://github.com/Amok-83/MP3-TOOL/releases)
2. Run the PowerShell installer as **Administrator**
3. Follow the on-screen instructions
4. The application will be installed with desktop and start menu shortcuts

### Manual Installation
- Download and run `MP3AlbumTool.exe` directly
- No installation required for portable use

## 🚀 How to Use

1. **Launch the application** from the desktop shortcut or start menu
2. **Select the folder** containing your MP3 albums
3. **Configure processing options** according to your needs
4. **Click "Process"** and wait for completion
5. **Generate M3U playlists** with album separators using `#EXTALB` tags

## ✨ Key Features

- **Album Organization**: Automatically organizes MP3 files by album structure
- **Metadata Optimization**: Cleans and standardizes ID3 tags
- **Car Audio Compatible**: Optimized for automotive audio systems
- **Playlist Generation**: Creates M3U playlists with album separators
- **Batch Processing**: Handles large music collections efficiently
- **Windows Integration**: Native Windows application with modern UI

## 🔧 Development

### Building from Source
```powershell
# Clean previous builds
.\cleanup.ps1

# Build executable
.\build.ps1
```

### Requirements
- Python 3.8+
- PyInstaller
- Required packages listed in `requirements.txt`

## 📋 System Requirements

- **Operating System**: Windows 10/11 (64-bit)
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB free space
- **Audio Formats**: MP3 files with ID3 tags

## 📁 Project Structure

```
MP3AlbumTool/
├── MP3AlbumTool_Distribution/     # Distribution package
├── dist/                          # Built executable
├── final_optimized_mp3_tool.py   # Main application source
├── icon.ico                       # Application icon
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## 💝 Support the Project

If you find this application useful and it has helped organize your music collection, please consider supporting the development:

[![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/donate/?business=TLBBHD3NY3SUY&no_recurring=0&item_name=Your+support+is+greatly+appreciated%3B+please+consider+a+donation+if+you+enjoy+using+this+app&currency_code=EUR)

Your support is greatly appreciated and helps maintain and improve this free tool for the music community! 🎵

## 🆘 Support

If you encounter any issues or have questions:
- Open an issue on [GitHub Issues](https://github.com/Amok-83/MP3-TOOL/issues)
- Check the documentation in the `MP3AlbumTool_Distribution` folder

---

**Developed with ❤️ for music enthusiasts**