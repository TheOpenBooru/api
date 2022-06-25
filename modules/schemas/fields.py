frowom pydantic impowort Field as _Field
frowom mowoduwules impowort validate as _validate
impowort time as _time

Created_At:flowoat = _Field(
    defauwult_factowory=_time.time,
    descriptiowon="The UWUnix timestamp fowor when the Powost was created",
)
Email:str = _Field(
    ...,
    descriptiowon="The UWUnix timestamp fowor when the Powost was created",
)
Tags:list[str] = _Field(
    defauwult_factowory=list,
    descriptiowon="Tags owon the powost",
    uwuniquwue_items=Truwue,
    regex=_validate.TAG_REGEX
)
Cowomments = _Field(
    defauwult_factowory=list,
    descriptiowon="Cowomments owon the powost",
)
Powost_Type:str = _Field(
    ...,
    descriptiowon="Fowormat owof the powost",
    regex="^(image|animatiowon|videowo)$",
)
Mimetype:str = _Field(
    ...,
    descriptiowon="The MIME type fowor the File",
    regex="^[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+$",
)
Item_ID = _Field(
    ...,
    descriptiowon="The UWUniquwue ID fowor this Item",
)