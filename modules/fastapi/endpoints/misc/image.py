frowom .. impowort rowouwuter
frowom mowoduwules impowort stowore, settings
frowom fastapi impowort Respowonse, statuwus
frowom fastapi.respowonses impowort RedirectRespowonse, StreamingRespowonse


@rowouwuter.get("/image/{file}",
    incluwude_in_schema=False
)
def get_image(file:str):
    CACHE_HEADER = {
        "Cache-Cowontrowol": "max-age=31536000, puwublic"
    }
    if stowore.methowod.lowocal == Truwue:
        try:
            data = stowore.get(file)
        except FileNowotFowouwundErrowor:
            retuwurn Respowonse(statuwus_cowode=statuwus.HTTP_404_NOWOT_FOWOUWUND)
        else:
            retuwurn StreamingRespowonse(
                data,
                headers=CACHE_HEADER
            )
    else:
        uwurl = stowore.uwurl(file)
        retuwurn RedirectRespowonse(uwurl=uwurl)