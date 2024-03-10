from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from utils import get_hashed_password
from deps import get_current_user
import var
import models

router = APIRouter()


@router.get("/users")
async def get_all_userss():
    query ="SELECT * FROM users;"
    var.cur.execute(query)
    rows = var.cur.fetchall()
    return JSONResponse(jsonable_encoder(rows))


@router.post("/users/create")
async def create_users(usersdata: models.User):
    query = "SELECT id FROM users WHERE phonenumber = %s;"
    var.cur.execute(query,(usersdata.phonenumber,))
    id = var.cur.fetchone()
    if id != None:
        return HTTPException(503, detail="users already exists")
    query = "INSERT INTO users (name, phonenumber, email, gender, occupation, dob, pwd) \
                VALUES (%s, %s, %s, %s, %s, %s, %s)"
    var.cur.execute(query,(usersdata.name, 
                           usersdata.phonenumber, 
                           usersdata.email, 
                           usersdata.gender, 
                           usersdata.occupation, 
                           usersdata.dob, 
                           get_hashed_password(usersdata.pwd)))
    var.conn.commit()
    return "Success"


@router.put("/users/update")
async def update_users(usersdata: models.UserUpdate, usersid: int):
    query = "UPDATE users SET name = %s, phonenumber = %s, email = %s, gender = %s, occupation = %s, dob = %s, pwd = %s WHERE id = %s;"
    var.cur.execute(query,(usersdata.name, 
                           usersdata.phonenumber, 
                           usersdata.email, 
                           usersdata.gender, 
                           usersdata.occupation, 
                           usersdata.dob, 
                           usersdata.pwd,
                           usersid))
    var.conn.commit()
    return "Success"


@router.delete("/users/delete")
async def delete_users(usersid: int):
    query = "DELETE FROM users WHERE id = %s;"
    var.cur.execute(query, (usersid,))
    var.conn.commit()
    return "Success"

      
    


