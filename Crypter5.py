import os
import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
import pyperclip
import platform
from colorama import init, Fore

init(autoreset=True)

def choose_file(title="Выберите файл"):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title=title)

def encrypt_file():
    file_path = choose_file("Выберите файл или архив для шифрования")
    if not file_path:
        print("❌ Файл не выбран.")
        return

    key = Fernet.generate_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as f:
        data = f.read()

    encrypted = fernet.encrypt(data)
    new_path = file_path + ".encrypted"

    with open(new_path, 'wb') as f:
        f.write(encrypted)

    pyperclip.copy(key.decode())
    print(f"\n✅ Файл зашифрован как: {new_path}")
    print(f"🔑 Ключ скопирован в буфер обмена:\n{key.decode()}")

def decrypt_file():
    file_path = choose_file("Выберите файл для расшифровки (.encrypted)")
    if not file_path:
        print("❌ Файл не выбран.")
        return

    key_input = input("🔑 Введите ключ: ").strip()
    try:
        fernet = Fernet(key_input.encode())
    except Exception:
        print("❌ Ошибка: недопустимый ключ.")
        return

    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    try:
        decrypted = fernet.decrypt(encrypted_data)
    except Exception:
        print("❌ Не удалось расшифровать. Неверный ключ или повреждённый файл.")
        return

    if file_path.endswith(".encrypted"):
        output_path = file_path[:-10]  # Убираем ".encrypted"
    else:
        output_path = file_path

    with open(output_path, 'wb') as f:
        f.write(decrypted)

    print(f"\n✅ Файл расшифрован и восстановлен как: {output_path}")

def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def main():
    while True:
        print("\n🔐 Меню:")
        print(Fore.RED + "[1] Зашифровать файл или архив")
        print(Fore.GREEN + "[2] Расшифровать файл")
        print("[3] Очистить консоль")
        print("[4] Выйти")

        choice = input("\nВыберите действие: ").strip()
        if choice == '1':
            encrypt_file()
        elif choice == '2':
            decrypt_file()
        elif choice == '3':
            clear_console()
        elif choice == '4':
            print("👋 Выход.")
            break
        else:
            print("❌ Неверный ввод. Введите 1, 2, 3 или 4.")

if __name__ == "__main__":
    main()

