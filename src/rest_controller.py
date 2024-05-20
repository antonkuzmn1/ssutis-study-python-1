# rest_controller.py
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from config import BACKEND_APP, BACKEND_PORT, BACKEND_RELOAD, BACKEND_HOST, ALLOWED_ORIGINS
from src.database import get_db
from src.models import Item
from src.parse_data import get_data

app = FastAPI()

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_players/")
def get_players(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items


@app.get("/parse_data/")
def parse_data(db: Session = Depends(get_db)):
    DATA: list[list[str, int]] = get_data()
    print('Received data:', DATA)

    for LIST_ITEM in DATA:
        print("row:", LIST_ITEM)
        if len(LIST_ITEM) > 0:
            ROW: Item = db.query(Item).get(LIST_ITEM[0])

            if ROW is None:
                item = Item(position=LIST_ITEM[0],
                            full_name=LIST_ITEM[1],
                            logo_url=LIST_ITEM[2],
                            total_goals=LIST_ITEM[3],
                            penalty_goals=LIST_ITEM[4],
                            matches=LIST_ITEM[5])
                db.add(item)

            else:
                ROW.full_name = LIST_ITEM[1]
                ROW.logo_url = LIST_ITEM[2]
                ROW.total_goals = LIST_ITEM[3]
                ROW.penalty_goals = LIST_ITEM[4]
                ROW.matches = LIST_ITEM[5]

            db.commit()

    return {"status": "success"}


def start_server():
    uvicorn.run(app=BACKEND_APP,
                host=BACKEND_HOST,
                port=BACKEND_PORT,
                reload=BACKEND_RELOAD)
