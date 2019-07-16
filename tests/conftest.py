from platform import system

collect_ignore = []
if system() == "Darwin":
    collect_ignore.append("test_linux.py")
    collect_ignore.append("test_windows.py")
    collect_ignore.append("test_windows_api.py")
elif system() == "Linux":
    collect_ignore.append("test_darwin.py")
    collect_ignore.append("test_windows.py")
    collect_ignore.append("test_windows_api.py")
elif system() == "Windows":
    collect_ignore.append("test_darwin.py")
    collect_ignore.append("test_linux.py")
