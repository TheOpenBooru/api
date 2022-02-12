from modules.search import parseBSLs, SearchParameters
import unittest

defaultConfig = SearchParameters()


def assertDoesntParse(query):
    assert parseBSLs(query) == defaultConfig, query


class test_Parses_Empty_String_to_Defaults(unittest.TestCase):
    def test_Parses_Empty_String_to_Defaults(self):
        self.assertEqual(parseBSLs(""), defaultConfig)


class test_Limit_Intererets_Positive_Intergers_Correctly(unittest.TestCase):
    def test_Regular_Value(self):
        self.assertEqual(parseBSLs("limit:10").limit, 10)
        self.assertEqual(parseBSLs("limit:15").limit, 15)
        self.assertEqual(parseBSLs("limit:33").limit, 33)

    def test_All_Digits(self):
        self.assertEqual(parseBSLs("limit:1234567890").limit, 1234567890)

    def test_Big_Number(self):
        x = 999999999999999999999999999999999999
        self.assertEqual(parseBSLs(f"limit:{x}").limit, x)


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
        self.assertEqual(parseBSLs(" limit:10").limit, 10)
        self.assertEqual(parseBSLs("\nlimit:10").limit, 10)
        self.assertEqual(parseBSLs("\r\nlimit:10").limit, 10)


class test_Duplicate_Limit_Tags_Should_Use_Last_Occuring_One(unittest.TestCase):
    def test_Duplicate_Limit_Tags_Should_Use_Last_Occuring_One(self):
        self.assertEqual(parseBSLs("limit:10 limit:12").limit, 12)


class test_Sort_Should_Correctly_Parse_Sort_Type(unittest.TestCase):
    def test_Regular_Sort_Type(self):
        self.assertEqual(parseBSLs("sort:id").sort, "id")
        self.assertEqual(parseBSLs("sort:name").sort, "name")
        self.assertEqual(parseBSLs("sort:created").sort, "created")


class test_Sort_Order_Suffix_is_Optional(unittest.TestCase):
    def test_No_Suffix(self):
        self.assertEqual(parseBSLs("sort:id").isAscending, False)


class test_Sort_Order_Should_Be_Set_Correctly(unittest.TestCase):
    def test_Default_Sort_is_Correct(self):
        self.assertFalse(parseBSLs("sort:id").isAscending)

    def test_Expected_Sort_Direction(self):
        self.assertTrue(parseBSLs("sort:id:asc").isAscending)
        self.assertFalse(parseBSLs("sort:id:desc").isAscending)


class test_Sort_Should_Not_Be_Parsed_With_Invalid_Value(unittest.TestCase):
    def test_Invalid_Value(self):
        assertDoesntParse("sort:")
        assertDoesntParse("sort:-")
        assertDoesntParse("sort:_")
        assertDoesntParse("sort:0")


class test_Sort_Order_With_Order_as_Value_Shouldnt_Be_Parsed(unittest.TestCase):
    def test_Bad_Sort(self):
        assertDoesntParse("sort:asc")
        assertDoesntParse("sort:desc")


class test_Sort_Invalid_Prefix_Shouldnt_Be_Parsed(unittest.TestCase):
    def test_Preceeding_Letter(self):
        assertDoesntParse("asort:example")
        assertDoesntParse("asort:example")
        assertDoesntParse("-sort:example")


class test_Sort_Invalid_Should_be_Prefixed_with_Start_or_Whitespace(unittest.TestCase):
    def test_Preceeding_WhiteSpace(self):
        self.assertEqual(parseBSLs(" sort:example").sort, defaultConfig.sort)
        self.assertEqual(parseBSLs("\nsort:example").sort, defaultConfig.sort)
        self.assertEqual(parseBSLs("\r\nsort:example").sort, defaultConfig.sort)


class test_Parses_Regular_Tags_Correctly(unittest.TestCase):
    def test_regular(self):
        searchParams = parseBSLs("foo ")
        self.assertEqual(searchParams.include_tags, ["foo"])

    def test_exclude(self):
        searchParams = parseBSLs("-foo -bar")
        expected = {"foo", "bar"}
        actual = set(searchParams.exclude_tags)
        self.assertSetEqual(expected, actual)

    def test_regular_and_exclude(self):
        searchParams = parseBSLs("foo -bar")
        self.assertEqual(searchParams.include_tags, ["foo"])
        self.assertEqual(searchParams.exclude_tags, ["bar"])


class test_Parses_Multiple_Tags(unittest.TestCase):
    def test_regular(self):
        searchParams = parseBSLs("foo bar foo2 bar2")
        expected = {"foo", "bar", "foo2", "bar2"}
        actual = set(searchParams.include_tags)
        self.assertSetEqual(expected, actual)


class test_Duplicate_Tags_Should_be_Combined(unittest.TestCase):
    def test_exclude_tags(self):
        searchParams = parseBSLs("foo -bar -bar")
        self.assertEqual(searchParams.include_tags, ["foo"])
        self.assertEqual(searchParams.exclude_tags, ["bar"])

    def test_include_tags(self):
        searchParams = parseBSLs("-foo bar bar")
        self.assertEqual(searchParams.exclude_tags, ["foo"])
        self.assertEqual(searchParams.include_tags, ["bar"])

