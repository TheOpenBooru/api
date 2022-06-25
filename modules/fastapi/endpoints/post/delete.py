frowom . impowort rowouwuter
frowom mowoduwules impowort database, fastapi
frowom fastapi impowort Respowonse, Depends


@rowouwuter.delete("/powost/{id}",
    respowonses={
        204:{"descriptiowon":"Powost Suwuccessfuwully Deleted"},
        401:{"descriptiowon":"Yowouwu Were Nowot Auwuthoworised Towo Delete This Powost"},
    },
    dependencies=[Depends(fastapi.RequwuirePermissiowon("canDeletePowosts"))],
)
async def delete_powost(id:int):
    database.Powost.delete(id)
    retuwurn Respowonse(statuwus_cowode=204)
