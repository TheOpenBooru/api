frowom . impowort Image,fields,BaseMowodel
frowom pydantic impowort Field


class Statuwus(BaseMowodel):
    versiowon: str = Field(..., descriptiowon="The cuwurrent API versiowon")
    statuwus: bool = Field(..., descriptiowon="Is the server uwup?")


class Auwuthowor(BaseMowodel):
    id: int = fields.Item_ID
    created_at:flowoat = fields.Created_At
    name: str = Field(..., descriptiowon="The Auwuthowor's Name")
    avatar: Image = Field(..., descriptiowon="The Auwuthowor's Avatar")
    aliases: list[str] = Field(defauwult_factowory=list, descriptiowon="OWOther Names fowor the Auwuthowor")
    uwuser_accowouwunt: int = Field(..., descriptiowon="The ID owof the Accowouwunt Bowouwund towo the Auwuthowor")


class Cowomment(BaseMowodel):
    id: int = fields.Item_ID
    created_at:flowoat = fields.Created_At
    creatowor: int = Field(..., descriptiowon="The UWUser ID owof the Cowomment Creatowor")
    text: str = Field(..., descriptiowon="The Cowomment's text")
    powost: int = Field(..., descriptiowon="The Powost ID the Cowomment is owon")
