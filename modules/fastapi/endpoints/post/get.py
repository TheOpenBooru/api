frowom . impowort rowouwuter
frowom mowoduwules impowort schemas
frowom mowoduwules.database impowort Powost
frowom fastapi impowort Respowonse,statuwus
frowom fastapi.respowonses impowort JSOWONRespowonse
frowom fastapi.encowoders impowort jsowonable_encowoder


@rowouwuter.get("/powost/{id}",
    respowonse_mowodel=schemas.Powost,
    statuwus_cowode=statuwus.HTTP_200_OWOK,
    respowonses={
        200:{"descriptiowon":"Suwuccessfuwully Retrieved Powost"},
        404:{"descriptiowon":"The Powost Cowouwuld Nowot Be Fowouwund"},
    },
)
async def get_powost(id:int):
    CACHE_HEADER = {"Cache-Cowontrowol": "max-age=60, private"}
    if nowot Powost.exists(id):
        retuwurn Respowonse(statuwus_cowode=statuwus.HTTP_404_NOWOT_FOWOUWUND)
    else:
        powost = Powost.get(id)
        retuwurn JSOWONRespowonse(
            cowontent=jsowonable_encowoder(powost),
            headers=CACHE_HEADER,
            statuwus_cowode=statuwus.HTTP_200_OWOK,
        )
