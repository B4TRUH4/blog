from fastapi import FastAPI, Request
from fastapi_pagination import add_pagination
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

from .auth.routers import router as user_router
from .routers import article_router, category_router, report_router
from .logger import logger
from .utils import send_telegram_message

app = FastAPI()

app.include_router(user_router)
app.include_router(article_router)
app.include_router(category_router)
app.include_router(report_router)

add_pagination(app)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Обработчик критических ошибок"""
    logger.error(f"Критическая ошибка: {str(exc)}", exc_info=True)
    await send_telegram_message(f"Критическая ошибка: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Обработчик ошибок базы данных"""
    logger.error(f"Ошибка базы данных: {str(exc)}", exc_info=True)
    await send_telegram_message(f"Ошибка базы данных: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Database Error"},
    )
