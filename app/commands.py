

import asyncio
import datetime
import time
from aiogram import F, Router, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboard as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import subprocess
import os, sys
import re
import threading
import time
import os
import ctypes
import mss
from datetime import datetime
import platform
import psutil
import GPUtil
import cv2

from app.vars import *

def is_session_locked():
    try:
        return any(proc.name() == "LogonUI.exe" for proc in psutil.process_iter())
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False


def ShotDown():
        try:
            os.system("shutdown /s /t 1")  # Для Windows
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")     


def check_PC_state():
    output = is_not_reachable(command_state)  
    output_text = ''.join(output)  
    print(output_text)
    match = re.search(r'Destination host unreachable', output_text)
    match2 = re.search(r'Request timed out', output_text)
    return match, match2


def is_not_reachable(host):
    try:
        # Устанавливаем локаль для вывода на английском
        output = subprocess.check_output("chcp 437 && ping -n 1 " + host, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output  # Возвращаем полный вывод
    except subprocess.CalledProcessError as e:
        return e.output  # Возвращаем вывод даже в случае ошибки
    

def StopShotDown():
    global StopSD
    StopSD = True

async def Secure_ShotDown():
    try:
        await asyncio.sleep(60)    
        if StopSD == False:
            ShotDown()
        else:
            await bot.send_message(admin_id, "Отмена выключения", reply_markup=kb.main)
            print("Отмена выключения")
    except Exception as e:
            print( f"Произошла ошибка: {str(e)}")

# Функция для создания папки, если она не существует
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def Make_photo():
    try:
            webcam_photo_dir = 'WebCam'
            create_directory_if_not_exists(webcam_photo_dir)
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Не удалось открыть веб-камеру")
                Mess = "Не удалось открыть веб-камеру"
                return Mess
            ret, frame = cap.read()
            if ret:
                # Имя файла, по которому будет сохраняться фото
                filename = 'WebCam/photo.png'
                cv2.imwrite(filename, frame)  # Это заменит старое фото новым
                # Отправляем фото
                with open(filename, 'rb') as file_photo:
                #await bot.send_document(admin_id, document=file_photo)
                    return file_photo
            else:
                print("Не удалось захватить кадр")
                Mess = "Не удалось захватить кадр"
                return Mess
                # await bot.send_message(admin_id, "Не удалось захватить кадр")
            cap.release()
            cv2.destroyAllWindows()
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

# Основной цикл программы для отслеживания завершения и состояния блокировки


# Асинхронная проверка состояния блокировки
async def lock_check():
    global StopSD
    was_locked = False  # Инициализируем флаг перед использованием
    while True:
        try:
            locked = is_session_locked()  # Проверяем состояние блокировки
            if locked and not was_locked:
                await bot.send_message(admin_id, "Система заблокирована", reply_markup=kb.main)
                print("Система заблокирована")
                was_locked = True  # Обновляем флаг на "заблокировано"
            elif not locked and was_locked:
                StopSD = False
                Mess = f'\nВнимание\nСистема была разблокирована\nесли это были не вы рекомендуем выключить пк для безопасности или нажмите отменить\n\nИначе система автоматически выключится через 60 секунд'
                await bot.send_message(admin_id, Mess, reply_markup=kb.cancel_or_shotdown)
                print("Система разблокирована")
                asyncio.create_task(Secure_ShotDown())
                was_locked = False  # Обновляем флаг на "разблокировано"
            await asyncio.sleep(1)  # Проверяем состояние раз в секунду
        except Exception as e:
            Mess = f"Произошла ошибка: {str(e)}"
            print(Mess)

def lock_Screen():
    try:
        os.system('rundll32.exe user32.dll, LockWorkStation')
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


    
def config_of_pc():
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
        out = f"Информация о системе:\n{system_info_str}"
        return out
    except Exception as e:
        out = f"Произошла ошибка: {str(e)}"
        return out
    
def make_screen_shots():
    try:
        # Создаём папку для скриншотов, если её нет
        screenshot_dir = 'photos'
        create_directory_if_not_exists(screenshot_dir)
        
        screenshot_paths = []  # Список для путей скриншотов
        with mss.mss() as sct:
            monitors = sct.monitors

            for i, monitor in enumerate(monitors[1:], start=1):
                screenshot = sct.grab(monitor)
                screenshot_path = f"{screenshot_dir}/screenshot_monitor_{i}.png"
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_path)
                screenshot_paths.append(screenshot_path)

        return screenshot_paths  # Возвращаем список путей
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"
