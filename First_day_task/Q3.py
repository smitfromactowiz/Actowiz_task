
def check(sen):
    l = []
    for i in sen:
        if i=="(":
            l.append(i)
        if i == ')':
            if l:
                l.pop()
            else:
                l.append(i)

                return "invalid"

    if l:
        return "invalid"
    else:
        return "valid"


print(check("((()()()))))"))