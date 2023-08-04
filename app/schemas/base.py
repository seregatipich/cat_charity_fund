from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class CommonBase(BaseModel):
    full_amount: Optional[PositiveInt]
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
