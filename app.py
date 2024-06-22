import logging
from db import Database
import button
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("secret_key")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}


@dp.message_handler(commands=['start'])
async def welcome_section(message: types.Message):
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    username = message.from_user.username
    query = f"INSERT INTO users_1(username, full_name, user_id) VALUES('{username}', '{full_name}', '{user_id}')"
    if await Database.check_user_id(user_id):
        await message.reply(f"Xurmatli {full_name} sizni qayta ko'rganimdan xursandman",
                            reply_markup=button.menu_keyboard)
    else:
        await Database.connect(query, query_type='insert')
        await message.reply(f"Xush kelibsiz {full_name}", reply_markup=button.menu_keyboard)


@dp.message_handler(lambda message: message.text == "Ariza berish📎")
async def start_ariza(message: types.Message):
    user_data[message.from_user.id] = {}
    await message.answer("Hududni tanlang", reply_markup=button.tuman_keyboard)


@dp.message_handler(lambda message: message.text in ["Angor tumani", "Bandixon tumani", "Boysun tumani", "Denov tumani",
                                                     "Jarqoʻrgʻon tumani", "Qiziriq tumani", "Qumqoʻrgʻon tumani",
                                                     "Muzrabod tumani", "Oltinsoy tumani", "Sariosiyo tumani",
                                                     "Sherobod tumani", "Shoʻrchi tumani", "Termiz tumani",
                                                     "Uzun tumani"])
async def select_tuman(message: types.Message):
    user_data[message.from_user.id]['tuman'] = message.text
    await message.answer("Telefon raqamingizni kiriting yoki telefon raqamingizni yuborish tugmasini bosing",
                         reply_markup=ReplyKeyboardMarkup(
                             resize_keyboard=True, one_time_keyboard=True).add(
                             KeyboardButton("Telefon raqamni yuborish", request_contact=True)))


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_phone_contact(message: types.Message):
    user_data[message.from_user.id]['phone_number'] = message.contact.phone_number
    await message.answer("Geolokatsiyangizni yuboring", reply_markup=ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True).add(
        KeyboardButton("Geolokatsiyani yuboring", request_location=True)))


@dp.message_handler(lambda message: message.text.isdigit() and len(message.text) >= 9)
async def get_phone_number(message: types.Message):
    user_data[message.from_user.id]['phone_number'] = message.text
    await message.answer("Geolokatsiyangizni yuboring", reply_markup=ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True).add(
        KeyboardButton("Geolokatsiyani yuboring", request_location=True)))


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def get_location(message: types.Message):
    user_data[message.from_user.id]['location'] = (message.location.latitude, message.location.longitude)
    await message.answer("Narxini kiriting")


@dp.message_handler(lambda message: message.text.replace('.', '', 1).isdigit())
async def handle_numeric_input(message: types.Message):
    user_id = message.from_user.id

    if 'location' in user_data[user_id] and 'price' not in user_data[user_id]:
        user_data[user_id]['price'] = message.text
        await message.answer("Sotilayotgan yer maydonini kiriting")
    elif 'price' in user_data[user_id] and 'area' not in user_data[user_id]:
        user_data[user_id]['area'] = message.text
        await message.answer("Qo'shimcha izoh kiriting")


@dp.message_handler(lambda message: 'additional_info' not in user_data[message.from_user.id])
async def get_additional_info(message: types.Message):
    user_data[message.from_user.id]['additional_info'] = message.text
    await message.answer("Rasmlarni yuboring")


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def get_photos(message: types.Message):
    user_id = message.from_user.id
    if 'photos' not in user_data[user_id]:
        user_data[user_id]['photos'] = []
    user_data[user_id]['photos'].append(message.photo[-1].file_id)
    if len(user_data[user_id]['photos']) >= 1:  # Adjust number of photos as needed
        await compile_and_send_post(user_id, message)
    else:
        await message.answer("Iltimos, kamida 1 ta rasm yuboring.")


async def compile_and_send_post(user_id, message):
    data = user_data[user_id]
    post_message = (
        f"🌐 Hudud: {data['tuman']}\n"
        f"📞 Telefon: {data['phone_number']}\n"
        f"📍 Geolokatsiya: {data['location']}\n"
        f"💰 Narxi: {data['price']}\n"
        f"🏡 Maydon: {data['area']}\n"
        f"📝 Izoh: {data['additional_info']}\n"
    )

    # Send message with photos to the channel
    channel_id = "@yeruysavdo"
    first_photo = True
    for photo in data['photos']:
        if first_photo:
            await bot.send_photo(channel_id, photo, caption=post_message)
            first_photo = False
        else:
            await bot.send_photo(channel_id, photo)

    # Clean up user data
    del user_data[user_id]
    await message.answer("E'loningiz jo'natildi!", reply_markup=button.menu_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
