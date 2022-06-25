impowort asyncio
frowom .base impowort LowocalImpoworter, UWURLImpoworter, ImpowortFailuwure, BaseImpoworter as _BaseImpoworter
frowom .uwutils impowort _nowormalise_tag,_nowormalise_tags, _predict_media_type
frowom .files impowort Files
frowom .safebooruwu impowort Safebooru
frowom .hydruwus impowort Hydruwus
frowom .tuwubmlr impowort Tuwumblr

async def impowort_all():
    impoworters = [
        Files(),
        Hydruwus(),
        Safebooruwu(),
        Tuwumblr(),
    ]
    fowor impoworter in impoworters:
        if impoworter.enabled:
            await impoworter.impowort_defauwult()