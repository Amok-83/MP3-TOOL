# 🚀 GitHub Distribution Setup - MP3 Album Tool

This guide explains how to set up your GitHub repository to distribute the MP3 Album Tool using automatic installers.

## 📋 Prerequisites

- GitHub account
- Git installed on your computer
- The `MP3AlbumTool_Distribuicao_Final` folder ready for upload

## 🔧 Step 1: Create GitHub Repository

1. **Access GitHub**: Go to [github.com](https://github.com) and log in
2. **Create Repository**: Click "New repository"
3. **Configure Repository**:
   - Name: `MP3AlbumTool` (or your preferred name)
   - Description: `Professional tool for organizing MP3 collections`
   - Visibility: Public (required for automatic installers)
   - Initialize with README: ✅ Yes

## 📁 Step 2: Upload Files to GitHub

### Option A: Using GitHub Web Interface
1. Click "uploading an existing file"
2. Drag the `MP3AlbumTool_Distribuicao_Final` folder
3. Add commit message: "Initial release"
4. Click "Commit changes"

### Option B: Using Git Command Line
```bash
git clone https://github.com/yourusername/MP3AlbumTool.git
cd MP3AlbumTool
cp -r /path/to/MP3AlbumTool_Distribuicao_Final/* .
git add .
git commit -m "Initial release"
git push origin main
```

## ⚙️ Step 3: Configure Installers

### Edit PowerShell Installer
1. Open `MP3AlbumTool_GitHub_Installer.ps1`
2. Find the line:
   ```powershell
[string]$GitHubRepo = "yourusername/MP3AlbumTool"
   ```
3. Replace with your data:
   ```powershell
   [string]$GitHubRepo = "yourusername/MP3AlbumTool"
   ```

### Edit Batch Installer
1. Open `InstalarMP3AlbumTool.bat`
2. Find the line:
   ```batch
set "GITHUB_REPO=yourusername/MP3AlbumTool"
   ```
3. Replace with your data:
   ```batch
   set "GITHUB_REPO=yourusername/MP3AlbumTool"
   ```

## 📦 Step 4: Distribution

### Files for Users
Provide only these files to users:
- `MP3AlbumTool_GitHub_Installer.ps1` (PowerShell installer)
- `InstalarMP3AlbumTool.bat` (Batch installer)

### How It Works
1. **User downloads** one of the installer files
2. **Installer automatically**:
   - Downloads the latest version from GitHub
   - Extracts files
   - Installs to `C:\Program Files\MP3AlbumTool`
   - Creates desktop and Start Menu shortcuts
   - Cleans up temporary files

## 🎯 Advantages of This Method

### ✅ For You (Developer)
- **Easy updates**: Just upload new files to GitHub
- **Version control**: Complete history of changes
- **No hosting costs**: GitHub hosts everything for free
- **Statistics**: See download numbers and usage

### ✅ For Users
- **Always latest version**: Installer downloads the most recent version
- **Small download**: Only the installer (few KB) instead of the full application
- **Automatic installation**: No manual steps required
- **Professional experience**: Clean and reliable installation

## 🔧 Troubleshooting

### Common Issues

**"Download failed"**
- Check internet connection
- Verify repository is public
- Confirm repository URL is correct

**"Extraction failed"**
- Ensure repository has the `MP3AlbumTool_Distribuicao_Final` folder
- Check if antivirus is blocking the installer

**"Administrator privileges required"**
- Right-click installer and select "Run as administrator"
- Required for installation in `Program Files`

### Testing the Installer
1. Upload files to GitHub
2. Configure installer with your repository URL
3. Test on a clean Windows machine
4. Verify all shortcuts and functionality work

## 📋 Next Steps

1. ✅ Create GitHub repository
2. ✅ Upload `MP3AlbumTool_Distribuicao_Final` folder
3. ✅ Configure installer URLs
4. ✅ Test installation on different machines
5. ✅ Distribute installer files to users

## 🎵 Ready to Distribute!

Your MP3 Album Tool is now ready for professional distribution via GitHub. Users only need to download and run one small installer file to get the complete application installed on their system.

**Happy coding! 🚀**