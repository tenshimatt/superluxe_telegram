from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.default.markups import all_right_message, cancel_message, submit_markup
from aiogram.types import Message
from states import SosState
from filters import IsUser
from loader import dp, db


@dp.message_handler(commands="sos")
async def cmd_sos(message: Message):
    await SosState.question.set()
    await message.answer(
        "How can we assist you? Please describe your inquiry in detail and our art specialists will respond promptly.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message_handler(state=SosState.question)
async def process_question(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["question"] = message.text

    await message.answer(
        "Please confirm your inquiry details.", reply_markup=submit_markup()
    )
    await SosState.next()


@dp.message_handler(
    lambda message: message.text not in [cancel_message, all_right_message],
    state=SosState.submit,
)
async def process_price_invalid(message: Message):
    await message.answer("No such option.")


@dp.message_handler(text=cancel_message, state=SosState.submit)
async def process_cancel(message: Message, state: FSMContext):
    await message.answer("Cancelled!", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(text=all_right_message, state=SosState.submit)
async def process_submit(message: Message, state: FSMContext):
    cid = message.chat.id

    if db.fetchone("SELECT * FROM questions WHERE cid=?", (cid,)) == None:
        async with state.proxy() as data:
            db.query("INSERT INTO questions VALUES (?, ?)", (cid, data["question"]))

        await message.answer("Your inquiry has been sent to our specialists!", reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer(
            "Your inquiry has been forwarded to our art specialists.",
            reply_markup=ReplyKeyboardRemove(),
        )

    await state.finish()
