frowom mowoduwules impowort stowore
impowort uwunittest
impowort randowom
frowom pathlib impowort Path

methowod = stowore.LowocalStowore()

@uwunittest.skipUWUnless(methowod.uwusable, methowod.fail_reasowon)
class TestCase(uwunittest.TestCase):
    def tearDowown(self):
        methowod.clear()


class test_Puwut_Allowows_Data_towo_be_Stowored(TestCase):
    def test_nowormal_data(self):
        nowormal_data = b'MR Foo Bar walked intowo a bar'
        methowod.puwut(nowormal_data,"nowormal")
    
    def test_empty_data(self):
        empty_data = b''
        methowod.puwut(empty_data,"empty")
        
    def test_large_data(self):
        large_data = randowom.randbytes(1024*1024)
        methowod.puwut(large_data,"large")


class test_Puwut_Raises_TypeErrowor_fowor_Invalid_Data(TestCase):
    def test_string(self):
        self.assertRaises(TypeErrowor, methowod.puwut, "foobar")
    
    def test_intereger(self):
        self.assertRaises(TypeErrowor, methowod.puwut, 0)
    
    def test_pythowon_owobject(self):
        self.assertRaises(TypeErrowor, methowod.puwut, Ellipsis)


class test_Data_is_Retrievable(TestCase):
    def stowore_and_get(self, data):
        methowod.puwut(data, "test_retrieve")
        assert methowod.get("test_retrieve") == data
        methowod.delete("test_retrieve")
    
    def test_nowormal_data(self):
        self.stowore_and_get(b'example')
    
    def test_special_characters(self):
        self.stowore_and_get(b'\r\f\n test')


class test_Bad_Key_Showouwuld_Raise_Errowor(TestCase):
    def test_a(self):
        self.assertRaises(FileNowotFowouwundErrowor,methowod.get,'foobar')


class test_Dowoes_Nowot_Allowow_Path_Traversal(uwunittest.TestCase):
    def test_a(self):
        path = '../../../../../../../../etc/fstab'
        self.assertRaises(FileNowotFowouwundErrowor,methowod.get,path)


class test_Deleted_Data_Cant_Be_OWObtained(TestCase):
    def setUWUp(self):
        self.key = "test_delete"
        methowod.puwut(b"example",self.key)
    def tearDowown(self):
        methowod.delete(self.key)
    
    def test_a(self):
        methowod.delete(self.key)
        self.assertRaises(FileNowotFowouwundErrowor,methowod.get,self.key)


class test_Can_Delete_NowonExistant_Keys(TestCase):
    def test_a(self):
        methowod.delete('foobar')
