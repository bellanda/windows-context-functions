# Windows Context Functions

Sistema para adicionar funções Python no menu de contexto do Windows Explorer.

## 🚀 Nova Versão com C++

Esta versão substitui o VBS lento por um executável C++ muito mais rápido e eficiente.

### Vantagens do C++:

- ⚡ **Muito mais rápido** que VBS
- 🔧 **Menor overhead** de sistema
- 🎯 **Execução mais direta** do comando
- 📦 **Sem dependências** extras

## 📋 Como Usar

### 1. Gerar o Registro

```batch
# Gera o arquivo de registro baseado nos scripts Python disponíveis
python generate_reg_and_vbs.py
```

### 2. Compilar o Executável C++

```batch
# Execute o script de compilação
compile.bat
```

### 3. Registrar no Context Menu

```batch
# Importe o arquivo de registro
regedit python_funcs_context_cpp.reg
```

### 4. Testar

- Clique com botão direito em qualquer arquivo
- Vá em "Python Functions" → "Test" (ou outros scripts que você criou)

## 🔧 Estrutura

- `run_silent.cpp` - Programa C++ que executa Python silenciosamente
- `compile.bat` - Script para compilar o C++
- `generate_reg_and_vbs.py` - Gerador automático de registros
- `python_funcs_context_cpp.reg` - Arquivo de registro gerado automaticamente
- `scripts/python/` - Pasta com seus scripts Python

## 💡 Como Funciona

O `run_silent.exe` recebe dois argumentos:

1. **Nome do script Python** (ex: `test.py`)
2. **Arquivo/pasta selecionado** (passado pelo Windows)

Exemplo de execução:

```
run_silent.exe "test.py" "C:\Users\arquivo.txt"
```

## 📊 Performance

| Método | Tempo de Inicialização | Overhead |
| ------ | ---------------------- | -------- |
| VBS    | ~200ms                 | Alto     |
| C++    | ~10ms                  | Baixo    |

## 🛠️ Requisitos

- Windows 10/11
- Visual Studio Build Tools OU MinGW-w64
- Python com `uv` instalado

## 📝 Migração do VBS

Se você estava usando a versão VBS anterior:

1. Compile o novo executável C++
2. Importe o novo arquivo `.reg`
3. O antigo VBS pode ser removido

A funcionalidade permanece idêntica, apenas muito mais rápida!
