# This is a binary operator class
class BinaryOperator:
    def __init__(self, op: str, left: str, center: str, right: str):
        self.op = op
        self.l = left
        self.c = center
        self.r = right

    def apply(self, a: str, b: str):
        return self.l + a + self.c + b + self.r

def convert(text: str, hotfix=True: bool, debug=False: bool) -> str:
    if debug:
        with open('cin.txt', 'w') as f:
            f.write(text)

    res = _convert(text)

    if hotfix:
        # This may be neccesary if export doesn't change
        continue

    if debug:
        with open('cout.txt', 'w') as f:
            f.write(res)
    
    return res

def _convert(text: str) -> str:
    return ''

exText = '''[
{
x_(1)^2 + y^2 = 3 
x^(2 + 3^x) = 5 
}{
x+2 = y
y-5 = x^2
}
]
'''

print(convert(exText))

