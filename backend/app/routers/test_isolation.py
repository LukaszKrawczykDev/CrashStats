from fastapi import APIRouter
from app.db.session import get_isolated_session
from sqlalchemy import text

router = APIRouter(prefix="/test", tags=["Test"])

@router.get("/isolation")
def test_isolation():
    try:
        session = get_isolated_session("REPEATABLE READ")
        result = session.execute(text("SELECT COUNT(*) FROM accidents")).scalar()
        session.close()
        return {"count": result}
    except Exception as e:
        return {"error": str(e)}