"""
Qishloq-AI Bozor Narxlari Handler
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline import market_category_keyboard, main_menu_keyboard
from services.market_service import get_market_prices, get_all_categories_brief

router = Router()


@router.callback_query(F.data == "menu:market")
async def market_menu(callback: CallbackQuery):
    msg = get_all_categories_brief()
    await callback.message.edit_text(
        msg,
        reply_markup=market_category_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(Command("market"))
async def cmd_market(message: Message):
    msg = get_all_categories_brief()
    await message.answer(msg, reply_markup=market_category_keyboard(), parse_mode="HTML")


@router.callback_query(F.data.startswith("market_cat:"))
async def process_market_category(callback: CallbackQuery):
    category = callback.data.split(":")[1]
    msg = get_market_prices(category)
    await callback.message.edit_text(msg, parse_mode="HTML")
    await callback.message.answer(
        "📌 Boshqa kategoriya yoki menyuga qaytish:",
        reply_markup=market_category_keyboard(),
    )
    await callback.answer()
