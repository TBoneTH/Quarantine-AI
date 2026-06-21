def get_file_type(extension):
    file_types = {
        ".txt": "Documento de Texto",
        ".pdf": "Documento PDF",
        ".docx": "Documento Word",
        ".xlsx": "Planilha Excel",
        ".pptx": "Apresentação PowerPoint",

        ".jpg": "Imagem JPEG",
        ".jpeg": "Imagem JPEG",
        ".png": "Imagem PNG",
        ".gif": "Imagem GIF",

        ".mp3": "Áudio MP3",
        ".wav": "Áudio WAV",

        ".mp4": "Vídeo MP4",
        ".avi": "Vídeo AVI",

        ".html": "Página Web",
        ".css": "Folha de Estilo CSS",
        ".js": "Script JavaScript",

        ".zip": "Arquivo Compactado ZIP",
        ".rar": "Arquivo Compactado RAR",
        ".7z": "Arquivo Compactado 7Z",

        ".exe": "Executável Windows",
        ".msi": "Instalador Windows",
        ".bat": "Script Batch",
        ".cmd": "Script CMD",
        ".ps1": "Script PowerShell",
        ".vbs": "Script VBScript"
    }

    return file_types.get(extension.lower(), "Tipo Desconhecido")