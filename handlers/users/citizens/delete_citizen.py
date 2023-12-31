from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline.inline_citizen_button import inline_user_button, confirm
from loader import dp, db, bot  # , db
from states.citizen_state import DeleteUserState


@dp.message_handler(Text(equals="✅ orqaga qaytish"),  state="*")
async def get_cancel_back(message: types.Message, state: FSMContext):
    await message.answer_photo(photo="https://www.atf.gov/sites/default/files/media/2015/08/people.jpg",
                         reply_markup=inline_user_button())
    await state.finish()


@dp.message_handler(state=DeleteUserState.id)
async def delete_user(message:types.Message):

        try:
                global user_id
                user_id = int(message.text)
                pass
                user = db.get_user(id=user_id)

                if user:
                       await bot.send_location(chat_id=message.chat.id,
                                               latitude=user[5],
                                               longitude=user[6])
                       await message.answer(text=
                                            f"🧾 <b>Fuqaroning ismi  : {user[1]}\n\n"
                                            f"✅ Fuqaroning yoshi  : {user[2]}\n\n"
                                            f"📞 Fuqaroning telefon raqami : {user[3]}\n\n"
                                            f"🌍 Fuqaroning turar joy manzili  : {user[4]}\n\n</b>")
                       await message.answer(text="Haqiqatdan shu id ga ega fuqroni o'chirmoqchimisiz ?"
                                                     ,reply_markup=confirm())
                       await DeleteUserState.confirm.set()

                else:
                        await message.answer('Bu id ga ega fuqaro topilmadi')


        except ValueError :
                await message.answer("ID raqam bo'lsin")


@dp.callback_query_handler(state=DeleteUserState.confirm)
async def check_confirm(callback:types.CallbackQuery, state:FSMContext):
        if callback.data == "ha":
                global user_id
                db.delete_user(id=user_id)
                await callback.message.answer(text=" <b><i>Fuqaro muvaffaqiyatli ravishda o'chirildi </i></b>"
                                              )
                await callback.message.answer_photo(photo='https://www.atf.gov/sites/default/files/media/2015/08/people.jpg',
                                                    reply_markup=inline_user_button())
                await state.finish()

        else:
                await callback.message.answer_photo(photo="https://www.atf.gov/sites/default/files/media/2015/08/people.jpg",
                                              reply_markup=inline_user_button())
                await state.finish()






