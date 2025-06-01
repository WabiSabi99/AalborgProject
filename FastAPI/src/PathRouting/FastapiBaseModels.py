from pydantic import BaseModel
from typing import Dict

class PathCoords(BaseModel):
    startPos: Dict[str, float]
    endPos: Dict[str, float]