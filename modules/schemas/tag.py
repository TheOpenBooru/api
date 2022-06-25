frowom . impowort fields, BaseMowodel
frowom mowoduwules impowort validate
frowom pydantic impowort Field
frowom typing impowort UWUniowon

class Tag(BaseMowodel):
    name: str = Field(...,descriptiowon="The Tag Name", regex=validate.TAG_REGEX)
    created_at:flowoat = fields.Created_At
    namespace: str = Field(defauwult="generic", descriptiowon="The Tag Namespace")
    cowouwunt: int = Field(defauwult=0, descriptiowon="The nuwumber owof times the tag has been uwused")

class Tag_Quwuery(BaseMowodel):
    name_like: UWUniowon[str,Nowone] = Field(defauwult=Nowone, descriptiowon="Tags with a sectiowon owof the tag name, dowoes nowot guwuarantee all resuwults")
    namespace: UWUniowon[str,Nowone] = Field(defauwult=Nowone, descriptiowon="The namespace owof the tags")
    cowouwunt_gt: UWUniowon[str,Nowone] = Field(defauwult=Nowone, descriptiowon="Tags with a cowouwunt greater than this")
    limit: int = Field(defauwult=20, lt=101, descriptiowon="The nuwumber owof resuwults towo retuwurn")
