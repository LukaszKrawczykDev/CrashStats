from fastapi import APIRouter, HTTPException
from zeep import Client
import json

router = APIRouter()

@router.get("/api/soap/stats")
def soap_stats():
    wsdl = "http://soap:8001/?wsdl"
    try:
        client = Client(wsdl)
        resp = client.service.get_stats()
        return json.loads(resp)
    except Exception as e:
        raise HTTPException(500, f"SOAP error: {e}")