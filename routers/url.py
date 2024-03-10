from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from var import cur, conn
import models

router = APIRouter()


@router.get("/url")
async def get_all_urls():
    query = "SELECT FROM url;"
    cur.execute(query)
    rows = cur.fetchall()
    return JSONResponse(jsonable_encoder(rows))

@router.post("/url/create")
async def create_url(userdata: models.Url):
    query = "INSERT INTO url (uid, tag, score) VALUES (%s, %s, %s)"
    cur.execute(query, (userdata.uid,
                            userdata.tag,
                            userdata.score))
    conn.commit()
    return "Success"

@router.put("/update/url")
async def update_url(userdata: models.UrlUpdate, urlid: int):
    query = "UPDATE url SET tag = %s, score = %s WHERE id = %s;"
    cur.execute(query, (userdata.tag,
                            userdata.score,
                            urlid))
    conn.commit()
    return "Success"


@router.delete("/delete/url")
async def delete_url(urlid: int):
    query = "DELETE FROM url WHERE id = %s;"
    cur.execute(query, (urlid,))
    conn.commit()
    return "Success"

