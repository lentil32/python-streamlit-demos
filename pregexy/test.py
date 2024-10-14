from pregexy import is_match


def test():
    print("=== Started running test for `pyregexy.py` ===")
    assert is_match("aa", "a") == False
    assert is_match("a", "ab*") == True
    assert is_match("a", "ab*a") == False
    assert is_match("b", "bc*a*") == True
    assert is_match("ab", ".*c") == False
    assert is_match("aab", "c*a*b") == True
    assert is_match("abcd", "d*") == False
    assert is_match("aab", ".c*") == False
    assert is_match("bbab", "b*a*") == False
    assert is_match("aabcbcbcaccbcaabc", ".*a*aa*.*b*.c*.*a*") == True
    assert is_match("cbaacacaaccbaabcb", "c*b*b*.*ac*.*bc*a*") == True
    assert is_match("accbabbacbbbacb", ".*.*.*a*bba*ba*") == False
    assert is_match("aaaaaaaaaaaaaaaaaaa", "a*a*a*a*a*a*a*a*a*b") == False
    assert is_match("accbabbacbbbacb", "a*.*b*") == True
    assert is_match("mississippi", "mis*is*ip*.") == True
    assert is_match("abbcacbbbbbabcbaca", "a*a*.*a*.*a*.b*a*") == True
    assert is_match(
        "mississippiabbcacbbbbbabcbacaaccbabbacbbbacbcbaacacaaccbaabcbaabcbcbcaccbcaabc",
        "mis*is*ip*.a*a*.*a*.*a*.b*a*a*.*b*c*b*b*.*ac*.*bc*a*.*a*aa*.*b*.c*.*a*"
    ) == True
    print("\n=== Test finished. ===")


if __name__ == "__main__":
    test()
