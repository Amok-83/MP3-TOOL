# MP3 Album Tool - Guia de Desinstalação

Este documento explica como desinstalar completamente o MP3 Album Tool do seu sistema.

## 📋 Opções de Desinstalação

### 1. **Desinstalador NSIS (Recomendado)**
Se instalou usando o instalador oficial:
- Vá a **Painel de Controle** → **Programas** → **Desinstalar um programa**
- Encontre "MP3 Album Tool" na lista
- Clique em **Desinstalar**

**OU**

- Vá ao **Menu Iniciar** → **MP3 Album Tool** → **Desinstalar**

### 2. **Script PowerShell (Completo)**
Para uma desinstalação mais completa:

```powershell
# Execute como Administrador
.\MP3AlbumTool_Uninstaller.ps1
```

**Como executar:**
1. Clique com o botão direito em `MP3AlbumTool_Uninstaller.ps1`
2. Selecione "Executar com PowerShell"
3. Aceite executar como Administrador

### 3. **Script Batch (Fácil)**
Para uma execução mais simples:

```batch
# Execute como Administrador
DesinstalarMP3AlbumTool.bat
```

**Como executar:**
1. Clique com o botão direito em `DesinstalarMP3AlbumTool.bat`
2. Selecione "Executar como administrador"

### 4. **Script Batch Simples (Sem PowerShell)**
Se o PowerShell não estiver disponível:

```batch
# Execute como Administrador
DesinstalarMP3AlbumTool_Simples.bat
```

## 🗑️ O que é Removido

Todos os scripts de desinstalação removem:

### ✅ **Arquivos e Pastas**
- Pasta de instalação: `C:\Program Files\MP3AlbumTool\`
- Executável principal: `MP3AlbumTool.exe`
- Arquivos de configuração
- Scripts de desinstalação

### ✅ **Atalhos**
- Atalho no Desktop: "MP3 Album Tool"
- Entrada no Menu Iniciar
- Pasta no Menu Iniciar (se existir)

### ✅ **Registro do Windows**
- Entrada de desinstalação
- Chaves de configuração da aplicação

### ✅ **Sistema**
- Remoção do PATH do sistema (se adicionado)
- Ficheiros temporários
- Cache da aplicação

### ✅ **Processos**
- Termina processos em execução da aplicação

## ⚠️ **Requisitos**

### **Privilégios de Administrador**
Todos os scripts requerem privilégios de administrador para:
- Remover arquivos de `Program Files`
- Modificar o registro do Windows
- Remover entradas do sistema

### **PowerShell (para scripts .ps1 e .bat)**
- Windows PowerShell 5.0 ou superior
- Política de execução permitindo scripts

## 🔧 **Resolução de Problemas**

### **Erro: "Acesso Negado"**
- Certifique-se de executar como Administrador
- Feche a aplicação antes de desinstalar

### **Erro: "PowerShell não encontrado"**
- Use o script `DesinstalarMP3AlbumTool_Simples.bat`
- Ou instale o PowerShell

### **Arquivos não removidos**
- Reinicie o computador
- Execute o script novamente
- Remova manualmente a pasta restante

### **Desinstalação Parcial**
Se alguns componentes não forem removidos:

1. **Remoção Manual da Pasta:**
   ```batch
   rmdir /s /q "C:\Program Files\MP3AlbumTool"
   ```

2. **Limpeza do Registro:**
   - Abra `regedit` como Administrador
   - Navegue para: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall`
   - Remova a entrada "MP3 Album Tool"

3. **Remoção de Atalhos:**
   ```batch
   del "%USERPROFILE%\Desktop\MP3 Album Tool.lnk"
   del "%ProgramData%\Microsoft\Windows\Start Menu\Programs\MP3 Album Tool.lnk"
   ```

## 📞 **Suporte**

Se encontrar problemas durante a desinstalação:

1. Verifique se tem privilégios de administrador
2. Tente reiniciar o computador
3. Use o script de desinstalação simples
4. Remova manualmente os componentes restantes

## 🔄 **Reinstalação**

Após a desinstalação completa, pode reinstalar a aplicação:
1. Baixe a versão mais recente
2. Execute o instalador como Administrador
3. Siga as instruções de instalação

---

**Nota:** Recomendamos fazer backup de quaisquer configurações personalizadas antes da desinstalação.