"""
LC0010. Regular Expression Matching
https://leetcode.com/problems/regular-expression-matching/description/

TC: O(TP)
SC: O(TP)
"""

DOT = "."
STAR = "*"


def is_match(s: str, p: str) -> bool:

    def dp(si, pi) -> bool:
        if (si, pi) in mem:
            return mem[si, pi]

        if pi == P:
            res = si == S
            mem[si, pi] = res
            return res

        # f s a*::pattern = s == a::tail && f tail a*::pattern ||
        #                   f s pattern
        head_matches = si < S and p[pi] in {s[si], DOT}
        if pi + 1 < P and p[pi + 1] == STAR:
            res = head_matches and dp(si + 1, pi) or dp(si, pi + 2)
        else:
            # f s a::pattern = s == a::tail && f tail pattern
            res = head_matches and dp(si + 1, pi + 1)
        mem[si, pi] = res
        return res

    S = len(s)
    p = compress_expression(p)
    P = len(p)
    mem = {}

    return dp(0, 0)


# TODO Compress to right either
def compress_expression(p) -> str:
    res = ""
    prev = ""
    i = 0
    while i < len(p):
        if i == len(p) - 1 or p[i + 1] != STAR:
            res += p[i]
            prev = ""
            i += 1
        else:
            if prev != DOT:
                if p[i] == DOT:
                    prev = DOT
                    res += ".*"
                elif p[i] != prev:
                    res += f"{p[i]}*"
                    prev = p[i]
            i += 2
    return res
