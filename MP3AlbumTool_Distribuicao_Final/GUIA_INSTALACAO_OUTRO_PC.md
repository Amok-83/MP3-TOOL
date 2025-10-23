# 🎵 MP3 Album Tool - Guia de Instalação para Outro PC

## 📦 Ficheiros Necessários para Distribuição

Para instalar a aplicação noutro PC, precisa dos seguintes ficheiros:

### Opção 1: Pacote Mínimo (Recomendado)
```
📁 MP3AlbumTool_Portable/
├── MP3AlbumTool.exe          # Executável principal
├── config.json               # Configurações da aplicação
├── README.md                 # Documentação
├── LICENSE.txt               # Licença
└── INSTALAR.bat             # Instalador automático (opcional)
```

### Opção 2: Pacote Completo com Instalador
```
📁 MP3AlbumTool_Complete/
├── MP3AlbumTool.exe                    # Executável principal
├── config.json                        # Configurações
├── README.md                          # Documentação
├── LICENSE.txt                        # Licença
├── INSTALAR.bat                       # Instalador batch
├── MP3AlbumTool_Installer_Final.ps1   # Script PowerShell
└── Source/                            # Código fonte (opcional)
    ├── final_optimized_mp3_tool.py
    ├── requirements.txt
    └── build.ps1
```

## 🚀 Métodos de Instalação

### Método 1: Execução Portátil (Mais Simples)
1. **Copie os ficheiros** para uma pasta no PC de destino
2. **Execute diretamente** `MP3AlbumTool.exe`
3. **Pronto!** A aplicação funciona imediatamente

**Vantagens:**
- ✅ Não requer privilégios de administrador
- ✅ Não modifica o sistema
- ✅ Pode ser executado de qualquer pasta
- ✅ Ideal para pen drives ou pastas partilhadas

### Método 2: Instalação Automática
1. **Copie todos os ficheiros** para o PC de destino
2. **Clique com botão direito** em `INSTALAR.bat`
3. **Selecione "Executar como administrador"**
4. **Siga as instruções** na tela
5. **Use os atalhos** criados no Desktop/Menu Iniciar

**Vantagens:**
- ✅ Cria atalhos automáticos
- ✅ Instala na pasta padrão do sistema
- ✅ Adiciona ao Menu Iniciar
- ✅ Opção de adicionar ao PATH

### Método 3: Instalação Manual
1. **Crie uma pasta** (ex: `C:\Program Files\MP3AlbumTool`)
2. **Copie os ficheiros** para essa pasta
3. **Crie atalhos manualmente** se desejar
4. **Execute** `MP3AlbumTool.exe`

## 📋 Requisitos do Sistema

### Requisitos Mínimos
- **Sistema Operativo:** Windows 7/8/10/11 (32 ou 64 bits)
- **RAM:** 512 MB
- **Espaço em Disco:** 50 MB
- **Processador:** Qualquer processador moderno

### Requisitos Recomendados
- **Sistema Operativo:** Windows 10/11 (64 bits)
- **RAM:** 2 GB ou mais
- **Espaço em Disco:** 100 MB
- **Processador:** Dual-core ou superior

## 🔧 Resolução de Problemas

### Problema: "Windows protegeu o seu PC"
**Solução:**
1. Clique em "Mais informações"
2. Clique em "Executar mesmo assim"
3. Ou: Clique com botão direito → Propriedades → Desbloquear

### Problema: Antivírus bloqueia o executável
**Solução:**
1. Adicione exceção no antivírus para a pasta da aplicação
2. Ou: Desative temporariamente o antivírus durante a instalação

### Problema: Erro de permissões
**Solução:**
1. Execute como administrador
2. Ou: Instale numa pasta onde tem permissões (ex: Desktop)

## 📁 Estrutura Após Instalação

### Instalação Automática
```
C:\Program Files\MP3AlbumTool\
├── MP3AlbumTool.exe
├── config.json
├── README.md
└── LICENSE.txt

Atalhos criados:
├── Desktop\MP3 Album Tool.lnk
└── Menu Iniciar\MP3 Album Tool.lnk
```

### Execução Portátil
```
[Pasta escolhida]\
├── MP3AlbumTool.exe
├── config.json
├── README.md
└── LICENSE.txt
```

## 🎯 Primeiros Passos Após Instalação

1. **Execute a aplicação** através do atalho ou executável
2. **Teste com alguns MP3s** para verificar funcionamento
3. **Configure as preferências** se necessário
4. **Comece a organizar** a sua coleção de música!

## 📞 Suporte

Se encontrar problemas:
1. Consulte o ficheiro `README.md`
2. Verifique os requisitos do sistema
3. Tente executar como administrador
4. Verifique se o antivírus não está a bloquear

---
**MP3 Album Tool - Organize a sua música com facilidade! 🎵**