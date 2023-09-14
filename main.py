import telebot
import os
from compare import compare_images

bot = telebot.TeleBot('6618485986:AAEf1qtNHjbYxfQMgqeYGvPY9eiO-3Rif50')  # Инициализация Telegram бота с заданным токеном

# Обработчик для команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне шаблонное изображение, затем простое изображение для сравнения.")

# Обработчик для приема изображений
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Получаем ID чата и ID сообщения с изображением
        chat_id = message.chat.id
        photo = message.photo[-1]  # Берем последнее (самое большое) изображение

        # Сохраняем изображение в текущую директорию с уникальным именем
        file_id = photo.file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)
        file_extension = os.path.splitext(file_path)[-1].lower()
        
        file_name = f"{message.id}{file_extension}"
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Отправляем подтверждение и путь к сохраненному изображению
        bot.reply_to(message, "Изображение успешно сохранено!")

        # Проверяем, есть ли уже шаблонное изображение
        if chat_id not in templates:
            templates[chat_id] = file_name
            bot.reply_to(message, "Отлично, теперь отправьте простое изображение для сравнения.")
        else:
            # Выполняем операцию сравнения изображений
            diff, percent = compare_images(templates[chat_id], file_name)
            bot.reply_to(message, f"Результат сравнения: {diff}%\nРезультат сравнения объектов: {percent}%")

            # Удаляем временные файлы
            os.remove(templates[chat_id])
            os.remove(file_name)
            del templates[chat_id]

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

if __name__ == '__main__':
    templates = {}  # Словарь для хранения шаблонных изображений
    bot.polling(none_stop=True)  # Запуск бота в режиме опроса событий
