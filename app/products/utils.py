import requests
from fastapi import HTTPException
from loguru import logger


async def fetch_product_data(artikul: int) -> dict:
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if "data" in data and "products" in data["data"]:
            products = data["data"]["products"]
            if products:
                product_info = products[0]
                return {
                    "name": product_info.get("name"),
                    "artikul": artikul,
                    "price": product_info.get("salePriceU", 0) / 100,
                    "rating": product_info.get("rating", 0),
                    "volume": product_info.get("volume", 0),
                }
            else:
                logger.warning(f"Товар с артикулом {artikul} не найден")
                raise HTTPException(status_code=404, detail=f"Товар с артикулом {artikul} не найден")
        else:
            logger.warning("Товары отсутствуют в ответе API")
            raise HTTPException(status_code=404, detail="Товары не найдены")

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к Wildberries API: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к Wildberries API: {e}")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        raise HTTPException(status_code=500, detail=f"Неизвестная ошибка: {e}")
