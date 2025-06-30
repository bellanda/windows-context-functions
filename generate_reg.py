from constants.paths import BASE_DIR

pythons_scripts = BASE_DIR / "scripts" / "python"

# Cabeçalho do arquivo de registro
reg_base_content = """Windows Registry Editor Version 5.00

; ---------- SUBMENU PAI ----------
[HKEY_CLASSES_ROOT\\*\\shell\\PythonFuncs]      ; * = vale para qualquer tipo de arquivo
"MUIVerb"="Python Functions"                ; nome exibido
"Icon"="C:\\\\Users\\\\OU000150\\\\OneDrive\\\\Images\\\\Icons\\\\machinelearning.ico"        ; opcional – ícone
"SubCommands"=""                             ; habilita submenu
"""

for python_script in pythons_scripts.glob("*.py"):
    script_name = python_script.name  # Nome do arquivo com extensão
    display_name = python_script.stem.replace("_", " ").title()  # Nome amigável

    # Caminho completo do script com escape correto para registro
    script_path = str(python_script).replace("\\", "\\\\")
    exe_path = str(BASE_DIR / "run_silent.exe").replace("\\", "\\\\")

    print(f"Adicionando script: {script_name}")
    reg_base_content += f"""
; ---------- ITEM {python_script.stem} ----------
[HKEY_CLASSES_ROOT\\*\\shell\\PythonFuncs\\shell\\{python_script.stem}]
@="{display_name}"

[HKEY_CLASSES_ROOT\\*\\shell\\PythonFuncs\\shell\\{python_script.stem}\\command]
@="\\"{exe_path}\\" \\"{script_path}\\" \\"%1\\""
"""

# Salva o arquivo de registro
reg_file = BASE_DIR / "python_funcs_context_cpp.reg"
with open(reg_file, "w", encoding="utf-8") as file:
    file.write(reg_base_content)

print(f"✅ Arquivo de registro gerado: {reg_file}")
print(f"📁 Encontrados {len(list(pythons_scripts.glob('*.py')))} scripts Python")
print("\n🚀 Para usar:")
print("1. Compile o C++: compile.bat")
print("2. Importe o registro: regedit python_funcs_context_cpp.reg")
