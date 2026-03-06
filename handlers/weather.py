"""
Qishloq-AI Ob-havo Handler
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from database.db import async_session
from database.models import User
from keyboards.inline import viloyat_keyboard, weather_period_keyboard, main_menu_keyboard
from config import VILOYATLAR
from services.weather_service import get_weather, format_weather_message

router = Router()


class WeatherStates(StatesGroup):
    waiting_region = State()
    waiting_period = State()


@router.callback_query(F.data == "menu:weather")
async def weather_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    # Check user profile for region
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()

    if user and user.region:
        await state.update_data(region=user.region)
        await callback.message.edit_text(
            f"⛅ <b>Ob-havo — {user.region}</b>\n\n"
            "Qaysi davr uchun prognoz kerak?",
            reply_markup=weather_period_keyboard(),
            parse_mode="HTML",
        )
        await state.set_state(WeatherStates.waiting_period)
    else:
        await callback.message.edit_text(
            "⛅ <b>Ob-havo Prognozi</b>\n\nViloyatni tanlang:",
            reply_markup=viloyat_keyboard("weather_region"),
            parse_mode="HTML",
        )
        await state.set_state(WeatherStates.waiting_region)
    await callback.answer()


@router.message(Command("weather"))
async def cmd_weather(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "⛅ <b>Ob-havo Prognozi</b>\n\nViloyatni tanlang:",
        reply_markup=viloyat_keyboard("weather_region"),
        parse_mode="HTML",
    )
    await state.set_state(WeatherStates.waiting_region)


@router.callback_query(WeatherStates.waiting_region, F.data.startswith("weather_region:"))
async def process_weather_region(callback: CallbackQuery, state: FSMContext):
    idx = int(callback.data.split(":")[1])
    region = VILOYATLAR[idx]
    await state.update_data(region=region)
    await callback.message.edit_text(
        f"⛅ <b>Ob-havo — {region}</b>\n\nQaysi davr uchun?",
        reply_markup=weather_period_keyboard(),
        parse_mode="HTML",
    )
    await state.set_state(WeatherStates.waiting_period)
    await callback.answer()


@router.callback_query(WeatherStates.waiting_period, F.data.startswith("weather_period:"))
async def process_weather_period(callback: CallbackQuery, state: FSMContext):
    period = callback.data.split(":")[1]
    data = await state.get_data()
    region = data.get("region", "Toshkent viloyati")

    days_map = {"today": 1, "3days": 3, "week": 7}
    days = days_map.get(period, 1)

    forecasts = get_weather(region, days)
    await state.clear()

    if days == 1:
        msg = format_weather_message(forecasts[0], region)
        await callback.message.edit_text(msg, parse_mode="HTML")
    else:
        msg = f"⛅ <b>Ob-havo Prognozi — {region}</b>\n"
        msg += f"📅 {days} kunlik\n"
        msg += "━" * 30 + "\n\n"
        for f in forecasts:
            msg += f"📅 <b>{f['day_name']}, {f['date']}</b>\n"
            msg += f"  {f['condition']}  🌡 {f['temp_min']}°..{f['temp_max']}°C\n"
            msg += f"  💧 {f['humidity']}%  💨 {f['wind']} m/s"
            if f['rain_chance'] > 0:
                msg += f"  🌧 {f['rain_chance']}%"
            msg += "\n\n"

        if forecasts:
            msg += "🌾 <b>Dehqon uchun maslahat:</b>\n"
            for tip in forecasts[0]['tips']:
                msg += f"  {tip}\n"

        await callback.message.edit_text(msg, parse_mode="HTML")

    await callback.message.answer("📌 Menyuga qaytish:", reply_markup=main_menu_keyboard())
    await callback.answer()
