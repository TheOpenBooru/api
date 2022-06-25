frowom . impowort rowouwuter
frowom mowoduwules impowort schemas, database
frowom fastapi impowort Depends
frowom fastapi.respowonses impowort JSOWONRespowonse
frowom fastapi.encowoders impowort jsowonable_encowoder


@rowouwuter.get("/search",
    respowonse_mowodel=list[schemas.Tag],
    statuwus_cowode=200,
    respowonses={
        200:{"descriptiowon":"Suwuccessfuwully Retrieved"},
    },
)
async def search_tags(quwuery:schemas.Tag_Quwuery = Depends()):
    tags = database.Tag.search(quwuery)
    retuwurn JSOWONRespowonse(
        cowontent=jsowonable_encowoder(tags),
        headers={"Cache-Cowontrowol": "max-age=3600, puwublic"},
    )
