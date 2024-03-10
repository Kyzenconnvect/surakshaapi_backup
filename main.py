import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from mysql.connector import connect
from dotenv import load_dotenv
import uvicorn
import var
from routers import authenticate, users, calls, sms, transaction, address, url, qr
from logger import logger

# from fastapi_pagination import add_paginationl̥
# import pyodbc

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting application")
        # var.conn = connect(host = 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
        #                port = '4000',
        #                user = '28nhe7xJsUWMyva.root',
        #                password = 'UIRj5kjVB7zkahdA',
        #                ssl_ca="",
        #                ssl_cert="",
        #                ssl_key="",
        #                database= 'suraksha'
        #             )
        var.conn = connect(host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
                        port = 4000,
                        user = "28nhe7xJsUWMyva.root",
                        password = "UIRj5kjVB7zkahdA",
                        database = "suraksha",
                        ssl_ca = "/etc/ssl/cert.pem"
                        # ssl_verify_cert = True
                        # ssl_verify_identity = True
                    )

        var.cur = var.conn.cursor( buffered = True)
        yield
    finally:
        logger.info("Stopping application")
        var.conn.disconnect()

app = FastAPI(title="Suraksha", version="1.0.0", lifespan=lifespan)
# add_pagination(app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET','POST','PUT','DELETE'],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1", tags=['User'])
app.include_router(calls.router, prefix="/api/v1", tags=['Call'])
app.include_router(sms.router, prefix="/api/v1", tags=['Sms'])
app.include_router(transaction.router, prefix="/api/v1", tags=['Transaction'])
app.include_router(address.router, prefix="/api/v1", tags=['Address'])
app.include_router(url.router, prefix="/api/v1", tags=['Url'])
app.include_router(qr.router, prefix="/api/v1", tags=['Qr'])
app.include_router(authenticate.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


# @app.on_event("startup")
# def startup():
#     conn = connect(host=host, port=port, user=user, password=passwd, database=database)
#     var.conn = connect(host = 'surakshaserver.mysql.database.azure.com',
#                        port = '3306',
#                        user = 'Theteddy2',
#                        password = 'N3dS@1Iu0',
#                        database= 'surakshaapp'
#                     )
#     var.conn = connect(host = 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
#                        port = '4000',
#                        user = '28nhe7xJsUWMyva.root',
#                        password = 'UIRj5kjVB7zkahdA',
#                        database= 'suraksha'
#                     )

#     var.cur = var.conn.cursor( buffered = True)

# @app.on_event("shutdown")
# def shutdown():
#     var.conn.disconnect()

# mysql://28nhe7xJsUWMyva.root:tFus0l5MP1vhf5vQ@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/suraksha
