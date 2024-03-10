from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import var
import models

router = APIRouter() 


@router.get("/call")
async def get_all_calls():
    query = "SELECT * FROM `call` ORDER BY callTime DESC;"
    var.cur.execute(query)
    rows = var.cur.fetchall()
    return JSONResponse(jsonable_encoder(rows))
    
@router.post("/call/create")
async def create_call(userdata: models.Call):
    query = "INSERT INTO `call` (uid, callerName, callerNumber, callTime, callTag) VALUES (%s, %s, %s, %s, %s)"
    var.cur.execute(query, (userdata.uid,
                            userdata.callerName,
                            userdata.callerNumber,
                            userdata.callTime,
                            userdata.callTag))
    var.conn.commit()
    return "Success"


@router.put("/call/update")
async def update_call(userdata: models.CallUpdate, callid: int):
    query = "UPDATE `call` SET callerName = %s, callerNumber = %s, callTime = %s, callTag = %s WHERE cid = %s;"
    var.cur.execute(query, (userdata.callerName,
                            userdata.callerNumber,
                            userdata.callTime,
                            userdata.callTag,
                            callid))
    var.conn.commit()
    return "Success"


@router.delete("/call/delete")
async def delete_call(callid: int):
    query = "DELETE FROM `call` WHERE cid = %s;"
    var.cur.execute(query, (callid,))
    var.conn.commit()
    return "Success"