from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from app.database import SessionLocal
from app.models.date import Date
from app.models.accident import Accident

class CrashStatsService(ServiceBase):
    @rpc(Integer, _returns=Integer)
    def get_accident_count_by_year(ctx, year):
        db = SessionLocal()
        count = db.query(Accident).join(Date).filter(Date.year == year).count()
        db.close()
        return count

soap_app = Application(
    [CrashStatsService],
    tns='crashstats.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

soap_wsgi_app = WsgiApplication(soap_app)