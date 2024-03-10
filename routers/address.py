from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import var
import models

router = APIRouter()


@router.get("/address")
async def get_all_addresses():
    query = "SELECT * FROM address;"
    var.cur.execute(query)
    rows = var.cur.fetchall()
    return JSONResponse(jsonable_encoder(rows))

@router.post("/address/create")
async def create_address(userdata: models.Address):
    query = "INSERT INTO address (addressline1, addressline2, pincode, city, state, country) VALUES (%s, %s, %s, %s, %s, %s)"
    var.cur.execute(query, (userdata.addressline1,
                            userdata.addressline2,
                            userdata.pincode,
                            userdata.city,
                            userdata.state,
                            userdata.country))
    var.conn.commit()
    return "Success"


@router.put("/address/update")
async def update_address(userdata: models.AddressUpdate, addrid: int): 
    query = "UPDATE address SET addressline1 = %s, addressline2 = %s, pincode = %s, city = %s, state = %s, country = %s WHERE id = %s;"
    var.cur.execute(query, (userdata.addressline1,
                            userdata.addressline2,
                            userdata.pincode,
                            userdata.city,
                            userdata.state,
                            userdata.country,
                            addrid))
                            
    var.conn.commit()
    return "Success"


@router.delete("/address/delete")
async def delete_address(addrid: int):
    query = "DELETE FROM address WHERE id = %s;"
    var.cur.execute(query, (addrid,))
    var.conn.commit()
    return "Success"


