import telebot
import threading
import time
import os
import ctypes
import mss
from datetime import datetime
import platform
import psutil
import GPUtil
import emoji
import cv2


bot = telebot.TeleBot('7885287200:AAGyqKpwC4U2XX_AchYi08wXI2IHnhX4K5o')
chat_id = 1383436134
exit_flag = False  # Флаг для завершения работы
StopSD = False
offapp_flag = False
# Сообщение при запуске бота
def send_startup_message():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.send_message(chat_id, emoji.emojize(":red_exclamation_mark:", variant="emoji_type") + 'Ваш ПК был запущен.' + emoji.emojize(":red_exclamation_mark:", variant="emoji_type") + '\n\nЕсли это были не вы, напишите:\n/ShotDown для выключения ПК\n\n/exit для выключения программы\n\n/lock для блокировки ПК\n\n/Photo для просмотра мониторов.\n\n/system_info для получения сведений ПК\n\n/WebCam\n\n'+ f"Дата: {current_time}"+emoji.emojize(":two_o’clock:", variant="emoji_type"))

send_startup_message()





    

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
    #bot.reply_to(message, f'Ваш chat_id: {message.from_user.id}')
    

# Функция для создания папки, если она не существует
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
# Функция сворачивания консоли
def minimize_console():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
       ctypes.windll.user32.ShowWindow(hwnd, 2)  # 2 - SW_MINIMIZE

@bot.message_handler(content_types=['text'])
def handle_messages(message):
    global exit_flag
    global StopSD
    global offapp_flag
    global current_time 
    # Обновляем дату при каждом запросе
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if message.text == '/StopShotDown':
        try:
            StopSD = True
            bot.send_message(chat_id, "Отменяем выключение...")
            defalt()
        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка: {str(e)}")
    
    
    if message.text == '/WebCam':
        try:
            webcam_photo_dir = 'WebCam'
            create_directory_if_not_exists(webcam_photo_dir)
            
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                print("Не удалось открыть веб-камеру")
                bot.send_message(chat_id, "Не удалось открыть веб-камеру")
                
            
            ret, frame = cap.read()

            if ret:
                # Имя файла, по которому будет сохраняться фото
                filename = 'WebCam/photo.png'
                cv2.imwrite(filename, frame)  # Это заменит старое фото новым
                

                # Отправляем фото
                with open(filename, 'rb') as file_photo:
                    bot.send_document(chat_id, document=file_photo)
                    defalt()
            else:
                print("Не удалось захватить кадр")
                bot.send_message(chat_id, "Не удалось захватить кадр")

            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка: {str(e)}")



    
        
    if message.text == '/ShotDown':  
        try:
            bot.send_message(chat_id, f"Выключаем ПК.\nДата: {current_time}")
            os.system("shutdown /s /t 1")  # Для Windows
        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка: {str(e)}")
      
    
        
    if message.text == '/lock':
        try:
            os.system('rundll32.exe user32.dll, LockWorkStation')
            
        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка: {str(e)}")
    

    if message.text == "/system_info":
        try:
            system_info = {
                "ОС": platform.system(),
                "Версия ОС": platform.release(),
                "Имя ПК": platform.node(),
                "Процессор": platform.processor(),
                "Архитектура": platform.architecture()[0],
                "Количество ядер": psutil.cpu_count(logical=True),
                "Частота процессора (MHz)": psutil.cpu_freq().current,
                "Оперативная память (MB)": round(psutil.virtual_memory().total / (1024 ** 2), 2)
            }
            # Получаем информацию о видеокарте
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_info = gpus[0]  # Получаем первую видеокарту, если их несколько
                system_info["Видеокарта"] = gpu_info.name
            else:
                system_info["Видеокарта"] = "Не найдена"
            system_info_str = '\n'.join([f"{key}: {value}" for key, value in system_info.items()])
            bot.send_message(chat_id, f"Информация о системе:\n{system_info_str}\nДата: {current_time}")
            defalt()
            # Преобразуем словарь в строку для вывода
        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка: {str(e)}")
    
   
    if message.text == '/Photo':
        try:
            
            # Создаём папку для скриншотов, если её нет
            screenshot_dir = 'photos'
            create_directory_if_not_exists(screenshot_dir)


            with mss.mss() as sct:
                monitors = sct.monitors
                screenshot_paths = []

                for i, monitor in enumerate(monitors[1:], start=1):
                    screenshot = sct.grab(monitor)
                    screenshot_path = f"photos/screenshot_monitor_{i}.png"
                    mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_path)
                    screenshot_paths.append(screenshot_path)
                
                # Отправляем скриншоты пользователю
                for path in screenshot_paths:
                    with open(path, 'rb') as file_photo:
                        bot.send_document(chat_id, document=file_photo)
            defalt()
        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка: {str(e)}")
    
    
    if message.text == '/exit':
        try:
            offapp_flag = True
            bot.send_message(chat_id, "Подтвердите завершение\n\n/Yes         /No\n\nПри подтверждении бот прекратит свою работу.")
        except:
            bot.send_message(chat_id,"Ошибка команды /exit"+f'\n\nДата: {current_time}')

    if message.text == '/Yes' and offapp_flag == True:
        try:
            bot.send_message(chat_id, "Бот завершает свою работу...")
            offapp_flag = False
            exit_flag = True
        except:
            bot.send_message(chat_id,"Ошибка команды /Yes"+f'\n\nДата: {current_time}')

    if message.text == '/No' and offapp_flag == True:
        try:
            bot.send_message(chat_id, "Завершение отменено.")
            offapp_flag = False
            defalt()       
        except:
            bot.send_message(chat_id,"Ошибка команды /No"+f'\n\nДата: {current_time}')
        
        
def defalt():
    bot.send_message(chat_id, f'/ShotDown\n\n/exit\n\n/lock\n\n/Photo\n\n/system_info\n\n/WebCam\n\nДата: {current_time}')

# Функция для запуска бота в отдельном потоке
def start_bot():
    bot.polling(none_stop=True)

# Запуск бота в отдельном потоке
bot_thread = threading.Thread(target=start_bot)
bot_thread.start()
minimize_console()

def is_session_locked():
    try:
        return any(proc.name() == "LogonUI.exe" for proc in psutil.process_iter())
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False


def ShotDown():
    try:
        time.sleep(60)    
        if StopSD == False:
            bot.send_message(chat_id, f'Выключаем систему')
            print("Выключаем систему")
            os.system("shutdown /s /t 1")  # Для Windows
        
        else:
            print("Отмена выключения")
            bot.send_message(chat_id, f"Выключение отменено")
    except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка: {str(e)}")

    
# Основной цикл программы для отслеживания завершения и состояния блокировки
was_locked = False  # Флаг для отслеживания состояния блокировки
while True:
    try:
        if exit_flag == True:  # Если установлен флаг выхода
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Дата: {current_time}\nБот завершает работу...")
            bot.stop_polling()  # Останавливаем polling для завершения работы бота
            print("1")
            bot_thread.join()  # Ждем завершения потока с ботом
            print("2")
            bot.send_message(chat_id, f"Дата: {current_time}\nБот завершил работу.")
            break

        locked = is_session_locked()  # Проверяем состояние блокировки
        if locked and not was_locked:
            print("Система заблокирована")
            was_locked = True  # Обновляем флаг на "заблокировано"
        elif not locked and was_locked:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            StopSD = True
            print("Система разблокирована")
            bot.send_message(chat_id, emoji.emojize(":red_exclamation_mark:", variant="emoji_type") + 
                            f'Внимание' + 
                            emoji.emojize(":red_exclamation_mark:", variant="emoji_type") + 
                            f'\nСистема была разблокирована\nесли это были не вы рекомендуем ввести\n/ShotDown-для выключения\n\n/StopShotDown для отмены выключения\n\nИначе система автоматически выключится через 60 секунд\n\nДата:{current_time}')
            ShotDown()
            


            was_locked = False  # Обновляем флаг на "разблокировано"
    
        time.sleep(1)  # Проверяем флаг и состояние блокировки раз в секунду
    except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка: {str(e)}")