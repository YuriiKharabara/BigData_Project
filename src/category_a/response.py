from pydantic import BaseModel, Field


class StatisticsResponse(BaseModel):
    time_start: str = Field(..., title='Time start', example='12:00')
    time_end: str = Field(..., title='Time end', example='12:00')
    statistics: list = Field(..., title='Collected statistics')
