import json
from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.accident import Accident

DATABASE_URL = "postgresql://crashuser:crashpass@db:5432/crashstats"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

class StatsService(ServiceBase):

    @rpc(_returns=String)
    def get_stats(ctx):
        db = SessionLocal()
        try:
            total = db.query(Accident).count()
            unique_locs = db.query(Accident.location_id).distinct().count()
            unique_dates = db.query(Accident.date_id).distinct().count()
            rows = db.query(Accident.collision_type, Accident.primary_factor).all()
            types = {}
            factors = {}
            for t,f in rows:
                types[t] = types.get(t,0) + 1
                factors[f] = factors.get(f,0) + 1
            most_common_type = max(types, key=types.get) if types else ""
            most_common_factor = max(factors, key=factors.get) if factors else ""

            result = {
                "accidents_total": total,
                "unique_locations": unique_locs,
                "unique_dates": unique_dates,
                "most_common_type": most_common_type,
                "most_common_factor": most_common_factor
            }
            return json.dumps(result)
        finally:
            db.close()

soap_app = Application(
    [StatsService],
    tns="spyne.stats.soap",
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

soap_wsgi_app = WsgiApplication(soap_app)