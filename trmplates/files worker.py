import os

def get_files_and_folders(path="."):
      contents = os.listdir(path)
      folders = []
      for item in contents:
          item_path = os.path.join(path, item)
          if os.path.isdir(item_path):
              folders.append(item)
      return folders


# Получение раздельных списков
folders = get_files_and_folders()
print("Папки:", folders)