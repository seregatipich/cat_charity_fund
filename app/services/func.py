from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUD_TYPE, ModelType


def close_model(model: ModelType) -> ModelType:
    """Функция закрытия модели."""
    model.invested_amount = model.full_amount
    model.fully_invested = True
    model.close_date = datetime.utcnow()
    return model


async def invest(
        obj_id: int,
        crud_for_first_obj: CRUD_TYPE,
        crud_for_second_obj: CRUD_TYPE,
        session: AsyncSession,
) -> ModelType:
    """Корутина инвестирования"""
    objs_one = await crud_for_first_obj.get_multi_not_closed(session)
    obj_two = await crud_for_second_obj.get(obj_id, session)
    sum_obj_two = obj_two.full_amount - obj_two.invested_amount
    remainder = 0
    for id in objs_one:
        obj_one = await crud_for_first_obj.get(id, session)
        remainder = obj_one.full_amount - obj_one.invested_amount
        if remainder > sum_obj_two:
            obj_one.invested_amount = obj_one.invested_amount + sum_obj_two
            obj_two = close_model(obj_two)
            session.add(obj_one)
            break
        sum_obj_two -= remainder
        obj_one = close_model(obj_one)
        session.add(obj_one)
    if sum_obj_two == 0:
        obj_two = close_model(obj_two)
    elif sum_obj_two > 0 and objs_one:
        obj_two.invested_amount = obj_two.invested_amount + sum_obj_two
    session.add(obj_two)
    await session.commit()
    await session.refresh(obj_two)

    return obj_two
