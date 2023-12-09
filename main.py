import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from message import START_CALCULATION, UNKNOWN_RECEIPT_TYPE

TOKEN = "6719269832:AAEU_L0fRQTWdySHjL-yBKfASCTMs6mb-iM"

dp = Dispatcher()


# calc_map = dict()
total_sum = 0
receipts_count = 0

CLICK = "click"
PAYME = "payme"
UNKNOWN = "no'malum"

CLICK_PART = " сум"
PAYME_PART = " сум"

CLICK_SEPARATOR = "."
PAYME_SEPARATOR = ","

CLICK_K_SEPARATOR = "'"
PAYME_K_SEPARATOR = " "


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(START_CALCULATION)


@dp.message(Command("finish"))
async def calculate(message: Message) -> None:
    global total_sum
    await message.answer(f"Hisoblangan cheklar soni: {receipts_count}ta\nJami: <b>{total_sum}</b> so'm")
    total_sum = 0


@dp.message()
async def echo_handler(message: Message) -> None:
    text = message.text
    amount_part = text.split("🇺🇿")[1].split("\n")[0]
    global total_sum, receipts_count
    if CLICK_PART in amount_part:
        amount = int("".join(amount_part.split(CLICK_PART)[0].split(CLICK_SEPARATOR)[0].split(CLICK_K_SEPARATOR)))
        receipt_type = CLICK
        receipts_count += 1
    elif PAYME_PART in amount_part:
        amount = int("".join(amount_part.split(PAYME_PART)[0].split(PAYME_SEPARATOR)[0].split(PAYME_K_SEPARATOR)))
        receipt_type = PAYME
        receipts_count += 1
    else:
        amount = 0
        receipt_type = UNKNOWN
        await message.answer(UNKNOWN_RECEIPT_TYPE)
    total_sum += amount
    await message.answer(f"TYPE: {receipt_type}\n\nSUM: <b>{amount}</b> so'm")


async def main_polling():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main_polling())
