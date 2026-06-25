from aiogram.fsm.state import State, StatesGroup


class AddProduct(StatesGroup):
    delivery_type = State()
    category = State()
    name = State()
    price = State()
    description = State()
    content = State()


class ChangeBalance(StatesGroup):
    user_id = State()
    amount = State()

class DeleteProduct(StatesGroup):
    product_id = State()

class AddPromo(StatesGroup):
    code = State()
    amount = State()