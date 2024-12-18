from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
# задаём переменую, указываем тип переменой, говорим что это 
# клавиатура, в списке клавиатуры указываем кнопку и задаём ей параметры
main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выключить пк"),
                                      KeyboardButton(text="Проверить состояние сервера")],
                                    [ KeyboardButton(text="Выключить бота"),
                                      KeyboardButton(text="Фото с вебки")],[
                                      KeyboardButton(text="Заблокировать"),
                                      KeyboardButton(text="Конфигурация ПК")],
                                    [ KeyboardButton(text="Сделать скриншот мониторов")]],
                           resize_keyboard=True, input_field_placeholder='its time to choose...')


catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Диски', callback_data='disks'), InlineKeyboardButton(text='Шины', callback_data='tires')],
                                                [InlineKeyboardButton(text='На главную', callback_data='to main')]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]],
                                 resize_keyboard=True)

confB = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да',callback_data='Y'), InlineKeyboardButton(text='Нет',callback_data='N')]])

cancel_or_shotdown = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отменить',callback_data='cancel'), InlineKeyboardButton(text='Выключить',callback_data='shotdown')]])
