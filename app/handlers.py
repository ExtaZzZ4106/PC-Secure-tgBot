#handlers.py
from aiogram.types import FSInputFile
import asyncio
import datetime
import time
from aiogram import F, Router, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.commands import *
import app.keyboard as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.commands import *
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
import io
from app.vars import *
import gc
mem_reduct_path = "C:\PP\Mem Reduct\memreduct.exe"
command_с = [mem_reduct_path, "/c"]

router = Router() # аналог диспетчера но только он собирает запросы и передаёт их ему  

class EXIT(StatesGroup):
    question = State()
    confirm = State()   
    
@router.message(F.text == 'Проверить состояние сервера')
async def checkStatePC(mes: Message):
    match, match2 = check_PC_state()

    if match or match2:
        await mes.answer("PC не запущен либо недоступен.", reply_markup=kb.main)
        subprocess.run(command_с, check=True)
    else:
        await mes.answer("PC запущен.", reply_markup=kb.main)
        subprocess.run(command_с, check=True)



@router.message(F.text == 'Выключить пк')
async def PC_OFF(mes: Message):
    try:
        await mes.answer("Выключаем пк...", reply_markup=kb.main)
        ShotDown()
    except:
        await mes.answer(f"Произошла ошибка", reply_markup=kb.main)


# Выход из программы
@router.message(F.text == 'Выключить бота')
async def exit_bot(mes: Message, state: FSMContext):
    await state.set_state(EXIT.question)
    await mes.answer("Вы правда хотите выключить бота?", reply_markup=kb.confB)

# Поддтверждение выхода
@router.callback_query(F.data == 'Y')
async def conf_yes(cbq: CallbackQuery, state: FSMContext):
    await state.set_state(EXIT.confirm)
    await cbq.answer("Бот завершает работу...")
    await cbq.message.answer("Бот завершает работу...", reply_markup=kb.main)
    await state.clear()
    sys.exit(1)

# Отмена выхода
@router.callback_query(F.data == 'N')
async def conf_no(cbq: CallbackQuery, state: FSMContext):
    await cbq.answer('Отмена выключения')
    await cbq.message.answer('Выключение отменено', reply_markup=kb.main)
    await state.clear()


@router.callback_query(F.data == 'cancel')
async def CancelSD(cbq: CallbackQuery):
    StopShotDown()
    await cbq.answer("Отменяем выключение")
    await cbq.message.answer("Отменяем выключение", reply_markup=kb.main)


@router.callback_query(F.data == 'shotdown')
async def CancelSD(cbq: CallbackQuery):
    await cbq.answer("Выключаем")
    await cbq.message.answer("Выключаем", reply_markup=kb.main)

@router.message(F.text == "Фото с вебки")
async def WebCam(mes: Message):

    await mes.answer("Делаю фото, скажите сыр...", reply_markup=kb.main)
    tmp = Make_photo()
    if isinstance(tmp, io.IOBase):
        await mes.answer(document=tmp, reply_markup=kb.main)
        subprocess.run(command_с, check=True)
    else:
        await mes.answer(":(")
        subprocess.run(command_с, check=True)


    #await mes.answer(document=tmp, reply_markup=kb.main)

@router.message(F.text == "Заблокировать")
async def LockScreen(cbq: CallbackQuery):
    await cbq.answer("lock_Screen")
    lock_Screen()
    subprocess.run(command_с, check=True)


@router.message(F.text == "Конфигурация ПК")
async def ConfOfPc(mes: Message):
    out = config_of_pc()
    await mes.answer(out)
    subprocess.run(command_с, check=True)


@router.message(F.text == "Сделать скриншот мониторов")
async def MakeScreenShots(mes: Message):
    out = make_screen_shots()
    await mes.answer("Делаю скриншоты, это может занять какоето время...")
    # Если возникла ошибка, возвращаем её пользователю
    if isinstance(out, str):
        await mes.answer(out)
        subprocess.run(command_с, check=True)
        return

    try:
        # Отправляем все скриншоты пользователю
        for screenshot_path in out:
            file = FSInputFile(screenshot_path)  # Создаём объект FSInputFile
            await mes.answer_document(file, reply_markup=kb.main)
            subprocess.run(command_с, check=True)
    except Exception as e:
        await mes.answer(f"Не удалось отправить скриншот: {str(e)}")
        subprocess.run(command_с, check=True)
