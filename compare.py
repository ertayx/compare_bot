import cv2 
import cvlib as cv

def detect_object(image_path):
    """Функция для детекции объектов на изображении"""
    image = cv2.imread(image_path)  # Загрузка изображения с заданного пути
    box, label, count = cv.detect_common_objects(image)  # Детекция объектов на изображении
    return label  # Возвращаем метки (label) найденных объектов

def compare_images(template_path, image_path):
    """Функция для сравнения изображений"""
    
    # Вычисление хэшей изображений
    template = calc_image_hash(template_path)  # Хэш шаблона
    image = calc_image_hash(image_path)  # Хэш изображения для сравнения
    
    # Детекция объектов на изображениях
    template_label = detect_object(template_path)  # Метки объектов на шаблоне
    image_label = detect_object(image_path)  # Метки объектов на изображении для сравнения

    # Рассчитываем процент пересечения меток объектов
    max_ = len(template_label)  # Максимальное количество объектов на шаблоне
    inter = len(set(template_label).intersection(image_label))  # Количество общих меток между шаблоном и изображением

    if max_ != 0 and inter != 0:
        percent_of_intersection = round(((max_ - inter) / max_) * 100, 0)  # Процент пересечения
    else:
        percent_of_intersection = 0

    # Сравниваем хэши изображений
    diff = compare_hash(template, image)  # Разница между хэшами
    diff = round(((64 - diff) / 64) * 100, 0)  # Процент сходства

    return diff, percent_of_intersection  # Возвращаем результаты сравнения

def calc_image_hash(FileName):
    """Функция для получения хэша изображения"""

    image = cv2.imread(FileName)  # Загружаем изображение
    resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Уменьшаем изображение до размера 8x8 пикселей
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Преобразуем изображение в оттенки серого
    avg = gray_image.mean()  # Вычисляем среднее значение яркости пикселей
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация изображения по порогу

    # Рассчитываем хэш изображения
    _hash = ""
    for x in range(8):
        for y in range(8):
            val = threshold_image[x, y]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"

    return _hash  # Возвращаем хэш

def compare_hash(hash1, hash2):
    """Функция для сравнения хэшей"""

    l = len(hash1)  # Длина хэша
    i = 0
    count = 0
    while i < l:
        if hash1[i] != hash2[i]:
            count = count + 1  # Увеличиваем счетчик различий
        i = i + 1
    return count  # Возвращаем количество различий между хэшами
