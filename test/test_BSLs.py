from modules.search import parseBSLs, SearchParameters
import unittest

defaultConfig = SearchParameters()


def assertDoesntParse(query):
    params = parseBSLs(query)
    assert params == defaultConfig, f"{query}: {params}"


class test_Parses_Empty_String_to_Defaults(unittest.TestCase):
    def test_Parses_Empty_String_to_Defaults(self):
        assert parseBSLs("") == defaultConfig


class test_Limit_Intererets_Positive_Intergers_Correctly(unittest.TestCase):
    def test_Regular_Value(self):
        assert parseBSLs("limit:10").limit == 10
        assert parseBSLs("limit:15").limit == 15
        assert parseBSLs("limit:33").limit == 33

    def test_All_Digits(self):
        assert parseBSLs("limit:1234567890").limit == 1234567890

    def test_Big_Number(self):
        x = 999999999999999999999999999999999999
        assert parseBSLs(f"limit:{x}").limit == x


class test_Limit_Shouldnt_Parse_Non_Positive_Intergers(unittest.TestCase):
    def test_Negative_Interger(self):
        assertDoesntParse("limit:-10")

    def test_Decimal_Number(self):
        assertDoesntParse("limit:0.1")

    def test_Text_Value(self):
        assertDoesntParse("limit:ten")
        assertDoesntParse("limit:_")

    def test_No_Value(self):
        assertDoesntParse("limit:")


class test_Limit_With_Leading_Zeros_Shouldnt_Be_Parsed(unittest.TestCase):
    def test_BSLs_Interperet_Value(self):
        assertDoesntParse("limit:0100")
        assertDoesntParse("limit:0")


class test_Limit_Invalid_Prefix_Shouldnt_Be_Parsed(unittest.TestCase):
    def test_Preceeding_Letter(self):
        assertDoesntParse("slimit:10")
        assertDoesntParse("0limit:10")
        assertDoesntParse("-limit:10")


class test_Limit_Invalid_Should_be_Prefixed_with_Start_or_Whitespace(unittest.TestCase):
    def test_Preceeding_WhiteSpace(self):
        assert parseBSLs(" limit:10").limit == 10
        assert parseBSLs("\nlimit:10").limit == 10
        assert parseBSLs("\r\nlimit:10").limit == 10


class test_Duplicate_Limit_Tags_Should_Use_First_Occuring_One(unittest.TestCase):
    def test_Duplicate_Limit_Tags_Should_Use_First_Occuring_One(self):
        assert parseBSLs("limit:15 limit:12").limit == 15


class test_Sort_Should_Correctly_Parse_Sort_Type(unittest.TestCase):
    def test_Regular_Sort_Type(self):
        assert parseBSLs("sort:id").sort == "id"
        assert parseBSLs("sort:name").sort == "name"
        assert parseBSLs("sort:created").sort == "created"


class test_Sort_Order_Suffix_is_Optional(unittest.TestCase):
    def test_No_Suffix(self):
        assert parseBSLs("sort:id").isAscending == False

class test_Sort_Order_Should_Be_Set_Correctly(unittest.TestCase):
    def test_Expected_Sort_Direction(self):
        assert parseBSLs("sort:id:asc").isAscending == True
        assert parseBSLs("sort:id:desc").isAscending == False
    def test_Invalid_Sort_Direction(self):
        assert parseBSLs("sort:id:example").isAscending == defaultConfig.isAscending


class test_Sort_Should_Not_Be_Parsed_With_Invalid_Value(unittest.TestCase):
    def test_Invalid_Value(self):
        assertDoesntParse("sort:")
        assertDoesntParse("sort:-")
        assertDoesntParse("sort:_")
        assertDoesntParse("sort:0")


class test_Sort_Invalid_Prefix_Shouldnt_Be_Parsed(unittest.TestCase):
    def test_Preceeding_Letter(self):
        assertDoesntParse("asort:example")
        assertDoesntParse("asort:example")
        assertDoesntParse("-sort:example")


class test_Sort_Invalid_Should_be_Prefixed_with_Start_or_Whitespace(unittest.TestCase):
    def test_Preceeding_WhiteSpace(self):
        assert parseBSLs(" sort:example").sort == "example"
        assert parseBSLs("\nsort:example").sort == "example"
        assert parseBSLs("\r\nsort:example").sort == "example"


class test_Parses_Regular_Tags_Correctly(unittest.TestCase):
    def test_regular(self):
        searchParams = parseBSLs("foo ")
        assert searchParams.include_tags == ["foo"]
    
    def test_multiple(self):
        searchParams = parseBSLs("foo bar beans eggs")
        assert set(searchParams.include_tags) == {"foo", "bar", "beans", "eggs"}

    def test_exclude(self):
        searchParams = parseBSLs("-foo -bar")
        assert set(searchParams.exclude_tags) == {"foo", "bar"}

    def test_regular_and_exclude(self):
        searchParams = parseBSLs("foo -bar")
        assert searchParams.include_tags == ["foo"]
        assert searchParams.exclude_tags == ["bar"]



class test_Duplicate_Tags_Should_be_Combined(unittest.TestCase):
    def test_exclude_tags(self):
        searchParams = parseBSLs("-bar -bar")
        assert searchParams.exclude_tags == ["bar"]

    def test_include_tags(self):
        searchParams = parseBSLs("bar bar")
        assert searchParams.include_tags == ["bar"]

