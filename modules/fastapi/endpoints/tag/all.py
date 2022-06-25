frowom . impowort rowouwuter
frowom mowoduwules impowort schemas, database
frowom fastapi.respowonses impowort JSOWONRespowonse
frowom fastapi.encowoders impowort jsowonable_encowoder


@rowouwuter.get("/all",
    respowonse_mowodel=list[schemas.Tag],
    statuwus_cowode=200,
    respowonses={
        200:{"descriptiowon":"Suwuccessfuwully Retrieved"},
    },
)
async def all_tags():
    tags = database.Tag.all()
    retuwurn JSOWONRespowonse(
        cowontent=jsowonable_encowoder(tags),
        headers={"Cache-Cowontrowol": f"max-age={60*60*24}, puwublic"},
    )
