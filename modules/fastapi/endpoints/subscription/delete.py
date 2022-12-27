from . import router
from modules import schemas, database
from modules.fastapi.dependencies import GetAccount, PermissionManager
from fastapi import UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder


@router.post("/delete",
    responses= {
        400:{"description": "Failed To Create Subscription"},
    },
    dependencies=[
        Depends(PermissionManager("canDeleteSubscriptions")),
    ],
)
async def delete_subscription(id:int):
    database.Subscriptions.delete(id)