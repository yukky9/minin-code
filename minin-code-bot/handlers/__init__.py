from aiogram import Dispatcher
from .default_handlers import router as default_router
from .helper_handler import router as helper_router


def include_routers(dp: Dispatcher):
    dp.include_routers(helper_router)
    dp.include_routers(default_router)
