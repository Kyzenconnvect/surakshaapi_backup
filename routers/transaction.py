from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from deps import get_current_user
import var
import models

router = APIRouter()


@router.get("/transaction")
async def get_all_transactions():
    query = "SELECT * FROM transaction;"
    var.cur.execute(query)
    rows = var.cur.fetchall()
    return JSONResponse(jsonable_encoder(rows))
    
@router.post("/transaction/create")
async def create_transaction(userdata: models.Transaction):
    query = "INSERT INTO transaction (uid, senderName, senderUpi, paymentApp, transactionTag) VALUES (%s, %s, %s, %s, %s)"
    var.cur.execute(query, (userdata.uid,
                            userdata.senderName,
                            userdata.senderUpi,
                            userdata.paymentApp,
                            userdata.transactionTag))
    var.conn.commit()
    return "Success"

@router.put("/transaction/update")
async def update_transaction(userdata: models.TransactionUpdate, transid: int):
    query = "UPDATE transaction SET senderName = %s, senderupi = %s, paymentApp = %s, transactionTag = %s WHERE id = %s;"
    var.cur.execute(query, (
                            userdata.senderName,
                            userdata.senderUpi,
                            userdata.paymentApp,
                            userdata.transactionTag,
                            transid))
    var.conn.commit()
    return "Success"

@router.delete("/transaction/delete")
async def delete_transaction(transid: int):
    query = "DELETE FROM transaction WHERE id = %s;"
    var.cur.execute(query, (transid,))
    var.conn.commit()
    return "Success"
