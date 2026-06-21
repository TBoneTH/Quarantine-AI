# Assinaturas binárias mais comuns (magic numbers).
# Cada entrada: bytes iniciais -> nome do tipo real detectado.
FILE_SIGNATURES = {
    b"\x4D\x5A": "Executável Windows (PE/EXE/DLL)",
    b"\x7F\x45\x4C\x46": "Executável Linux (ELF)",
    b"\x25\x50\x44\x46": "Documento PDF",
    b"\x50\x4B\x03\x04": "Arquivo ZIP/Office (zip, docx, xlsx, pptx...)",
    b"\x52\x61\x72\x21": "Arquivo RAR",
    b"\x37\x7A\xBC\xAF\x27\x1C": "Arquivo 7Z",
    b"\xFF\xD8\xFF": "Imagem JPEG",
    b"\x89\x50\x4E\x47": "Imagem PNG",
    b"\x47\x49\x46\x38": "Imagem GIF",
    b"\x49\x44\x33": "Áudio MP3 (ID3)",
    b"\x52\x49\x46\x46": "Arquivo RIFF (WAV/AVI)",
}

# Extensões esperadas para cada tipo real detectado.
EXPECTED_EXTENSIONS = {
    "Executável Windows (PE/EXE/DLL)": [".exe", ".dll", ".msi", ".scr", ".sys", ".com"],
    "Executável Linux (ELF)": [".elf", ".bin", ".out", ""],
    "Documento PDF": [".pdf"],
    "Arquivo ZIP/Office (zip, docx, xlsx, pptx...)": [
        ".zip", ".docx", ".xlsx", ".pptx", ".jar", ".apk"
    ],
    "Arquivo RAR": [".rar"],
    "Arquivo 7Z": [".7z"],
    "Imagem JPEG": [".jpg", ".jpeg"],
    "Imagem PNG": [".png"],
    "Imagem GIF": [".gif"],
    "Áudio MP3 (ID3)": [".mp3"],
    "Arquivo RIFF (WAV/AVI)": [".wav", ".avi"],
}


def detect_signature(filepath):
    """
    Lê os bytes iniciais do arquivo e tenta identificar o tipo real
    pelo cabeçalho binário. Retorna o nome do tipo detectado ou
    None se a assinatura não for reconhecida pela tabela.
    """
    try:
        with open(filepath, "rb") as file:
            header = file.read(16)
    except (OSError, IOError):
        return None

    for signature, file_type in FILE_SIGNATURES.items():
        if header.startswith(signature):
            return file_type

    return None


def check_extension_mismatch(filepath, extension):
    """
    Compara a extensão declarada do arquivo com o tipo real detectado
    pela assinatura binária.

    Retorna uma tupla (houve_mismatch, tipo_real):
    - houve_mismatch (bool): True se a extensão não bate com o
      conteúdo real detectado.
    - tipo_real (str | None): nome do tipo identificado pela
      assinatura, ou None se não reconhecido.
    """
    detected_type = detect_signature(filepath)

    if detected_type is None:
        return False, None

    expected_exts = EXPECTED_EXTENSIONS.get(detected_type, [])
    extension = extension.lower()

    if expected_exts and extension not in expected_exts:
        return True, detected_type

    return False, detected_type
