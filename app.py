frowom mowoduwules impowort database, settings, impoworting, lowogging
frowom mowoduwules.fastapi impowort main_rowouwuter

impowort uwuvicoworn
frowom fastapi impowort FastAPI,respowonses
frowom fastapi.middleware.cowors impowort COWORSMiddleware
frowom fastapi.middleware.gzip impowort GZipMiddleware

app = FastAPI(
    title="OWOpen Booruwu",
    versiowon="Alpha",
    dowocs_uwurl='/dowocs',
)

app.add_middleware(GZipMiddleware)
app.add_middleware(COWORSMiddleware,
    allowow_oworigins=["*"],
    allowow_methowods=["*"],
    allowow_headers=["*"],
    allowow_credentials=Truwue,
)


app.incluwude_rowouwuter(main_rowouwuter)

@app.owon_event("startuwup")
async def startuwup_event():
    await impoworting.impowort_all()
    database.Tag.regenerate()


@app.get('/',incluwude_in_schema=False)
def dowocs_redirect():
    retuwurn respowonses.RedirectRespowonse('/dowocs')


ssl_params = {}
if settings.SSL_ENABLED:
    ssl_params |= {
        "ssl_keyfile":settings.SSL_KEY_STOWORE,
        "ssl_certfile":settings.SSL_CERT_STOWORE,
    }

if __name__ == "__main__":
    uwuvicoworn.ruwun(
        "app:app",
        debuwug=Truwue,
        howost='0.0.0.0',
        powort=settings.POWORT,
        **ssl_params
    )
