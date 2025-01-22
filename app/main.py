from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.apscheduler import scheduler
from app.dao.session_maker import TransactionSessionDep
from app.products.dao import ProductDAO
from app.products.utils import fetch_product_data
from app.products.schemas import SProductArtikul, SProduct

app = FastAPI()


@app.post("/api/v1/products", summary='Получение информации о товаре по артикулу')
async def get_products(request: SProductArtikul, session: AsyncSession = TransactionSessionDep):
    try:
        product_data = await fetch_product_data(request.artikul)
        if product_data is None:
            raise HTTPException(status_code=404, detail="Product not found")
        create_record = await ProductDAO.find_one_or_none(session=session, filters=request)
        if create_record:
            await ProductDAO.update(session=session, filters=request, values=SProduct(**product_data))
        else:
            await ProductDAO.add(session=session, values=SProduct(**product_data))
        return {
            "detail": "Product data saved successfully",
            "product": {
                "name": product_data["name"],
                "artikul": product_data["artikul"],
                "price": product_data["price"],
                "rating": product_data["rating"],
                "volume": product_data["volume"],
            },
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@app.get("/api/v1/subscribe/{artikul}")
async def subscribe_artikul(artikul: int, session: AsyncSession = TransactionSessionDep):
    job_id = f"channel_{artikul}"
    if scheduler.get_job(job_id):
        return {"message": f"Сбор данных для артикула {artikul} уже запущен"}

    artikul_request = SProductArtikul(artikul=artikul)

    scheduler.add_job(
        func=get_products,
        args=[artikul_request, session],
        trigger=IntervalTrigger(minutes=30),
        id=job_id,
        replace_existing=True,
    )
    return {"message": f"Сбор данных для артикула {artikul} запущен каждые 30 минут"}


@app.delete("/api/v1/delete/{artikul}")
async def unsubscribe_artikul(request: SProductArtikul):
    job_id = f"channel_{request.artikul}"
    job = scheduler.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    scheduler.remove_job(job_id)
    return {"message": f"Сбор данных для артикула {request.artikul} остановлен"}
