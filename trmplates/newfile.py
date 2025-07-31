from PIL import Image
from PIL.ExifTags import TAGS

def get_image_metadata(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()

        if exif_data:
            metadata = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                metadata[tag_name] = value
            return metadata
        else:
            return None
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден: {image_path}")
        return None
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        return None

# Пример использования
image_file = "/storage/emulated/0/Pictures/Screenshots/Screenshot_2025-07-06-09-11-42-17_d5b607e12e4d0869ac9018feef7598a9.jpg"
metadata = get_image_metadata(image_file)

if metadata:
    for key, value in metadata.items():
        if "date" in key.lower():
            print(f"{key}: {value}")
else:
    print("Метаданные не найдены или произошла ошибка.")(i+1)