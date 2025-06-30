#include <windows.h>
#include <string>

// Function to convert string to wide string with proper UTF-8 handling
std::wstring stringToWideString(const std::string& str) {
    if (str.empty()) return std::wstring();
    
    // First, convert from current code page to UTF-8 if needed
    int size_needed = MultiByteToWideChar(CP_ACP, 0, &str[0], (int)str.size(), NULL, 0);
    std::wstring wstrTo(size_needed, 0);
    MultiByteToWideChar(CP_ACP, 0, &str[0], (int)str.size(), &wstrTo[0], size_needed);
    return wstrTo;
}

// Function to normalize long paths for Windows
std::wstring normalizeLongPath(const std::string& path) {
    std::wstring widePath = stringToWideString(path);
    
    // If path is longer than 260 characters, use UNC prefix
    if (widePath.length() > 260) {
        if (widePath.substr(0, 2) == L"\\\\") {
            // Already UNC path
            return L"\\\\?\\UNC\\" + widePath.substr(2);
        } else {
            // Local path
            return L"\\\\?\\" + widePath;
        }
    }
    
    return widePath;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        return 1; // Need at least 2 arguments (script_name and selected_file)
    }
    
    // argv[1] = nome do script Python
    // argv[2] = arquivo/pasta selecionado
    
    // Use uv run instead of direct python.exe to ensure proper environment
    std::string uvCommand = "uv";
    std::string scriptPath = argv[1];
    std::string selectedFile = argv[2];
    
    
    // Build command using uv run
    std::string command = "\"" + uvCommand + "\" run \"" + scriptPath + "\" \"" + selectedFile + "\"";
    
    
    // Convert to wide string for long path support
    std::wstring wideCommand = stringToWideString(command);
    
    // Define o diretório de trabalho
    std::string workingDir = "C:\\Users\\OU000150\\code\\exclude-from-compact\\windows-context-functions";
    std::wstring wideWorkingDir = stringToWideString(workingDir);
    
    
    // Configuração para execução silenciosa
    STARTUPINFOW si;
    PROCESS_INFORMATION pi;
    
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_HIDE; // Execute hidden
    
    ZeroMemory(&pi, sizeof(pi));
    
    // Create a mutable copy of the command string
    std::wstring mutableCommand = wideCommand;
    
    
    // Executa o comando usando CreateProcessW (wide version)
    BOOL result = CreateProcessW(
        NULL,                           // Nome do módulo
        &mutableCommand[0],             // Linha de comando (mutable)
        NULL,                           // Atributos de segurança do processo
        NULL,                           // Atributos de segurança da thread
        FALSE,                          // Herda handles
        CREATE_NO_WINDOW,               // Flags de criação (no window)
        NULL,                           // Ambiente
        wideWorkingDir.c_str(),         // Diretório atual
        &si,                           // Startup info
        &pi                            // Process info
    );
    
    if (result) {
        
        // Aguarda o processo terminar
        WaitForSingleObject(pi.hProcess, INFINITE);
        
        // Obtém o código de saída
        DWORD exitCode;
        GetExitCodeProcess(pi.hProcess, &exitCode);
        
        
        // Fecha os handles
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        
        return exitCode;
    } else {
        DWORD error = GetLastError();
        
        // Print detailed error message
        LPVOID lpMsgBuf;
        FormatMessage(
            FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
            NULL,
            error,
            MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
            (LPTSTR) &lpMsgBuf,
            0,
            NULL
        );
        
        LocalFree(lpMsgBuf);
    }
    
    return 1; // Erro na execução
} 