# app/schemas/export.py

from typing import Dict, List, Literal, Optional
from pydantic import BaseModel

class ExportRequest(BaseModel):
    filters: Dict[str, List[str]]
    columns: List[str]
    format: Literal["json", "yaml", "xml"] = "json"
    limit: Optional[int] = None