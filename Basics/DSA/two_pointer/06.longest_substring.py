# Longest substring without repeating characters. 

myStr = "cadbazxyvf"



def longest_substring_practice(s):
    lStr = ""
    for i in range(len(s)):
        seen = ""
        for j in range(i,len(s)):
            if s[j] in seen: break
            else:
                seen += s[j]
                if len(seen) > len(lStr) :
                    lStr = seen
    return lStr

print(longest_substring_practice(myStr))

