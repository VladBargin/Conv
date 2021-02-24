from pdflatex import PDFLaTeX

# This is a binary operator class
class BinaryOperator:
    def __init__(self, op: str, left: str, center: str, right: str):
        self.op = op
        self.l = left
        self.c = center
        self.r = right

    def apply(self, a: str, b: str):
        return self.l + a + self.c + b + self.r

def convert(text: str, debug: bool=False, hotfix: bool=False) -> str:
    if debug:
        with open('cin.txt', 'w') as f:
            f.write(text)

    res = conv(text)
    
    if hotfix:
        # This may be neccesary if the export module doesn't change
        # For now, I am going to ignore this part because my job is to create a LaTeX file
        print('Nothing to see here!')
    else:
		# We need to include all necessary packages
        res = '' + res + ''
				
    if debug:
        with open('cout.txt', 'w') as f:
            f.write(res)
    
    return res

def find_next_bracket(text: str, i: int, brackets: tuple, balance=0, step=1):
    while i >= 0 and i < len(text):
        if text[i] == brackets[0]:
            balance += 1
        elif text[i] == brackets[1]:
            balance -= 1
            
        if balance == 0:
            return i
        i += step
    
    # Couldn't find any bracket
    return -1
    
def find(text: str, i: int, step: int) -> int:
    stop_symbols = {'{', '[', ']', '}', '\n'}
    cnt_spaces = 0
    while i > 0 and i + 1 < len(text) and text[i + step] not in stop_symbols:
        if text[i + step] == ' ':
            cnt_spaces += 1
            
        if cnt_spaces >= 2:
            break
            
        if text[i + step] == ')':
            i = find_next_bracket(text, i + step, (')', '('), 0, -1)
            break
        elif text[i + step] == '(':
            i = find_next_bracket(text, i + step, ('(', ')'))
            break
            
        i += step 
    
    if i < 0:
        if step < 0:
            return 0
        else:
            return len(text) - 1
    return i

def _convert(text: str) -> str:
    # Here are the priorities:
    # 1. Search for [] and {}
    # 2. Search for ()
    # 3. Search for operators

    result = ''
    
    bop = {}
    bop['/'] = BinaryOperator('/', '\\frac@', '`@', '`')
    
    while True:
        can_break = True
        for i in range(len(text)):
            if text[i] in bop:
                can_break = False
                l, r = find(text, i, -1), find(text, i, 1)
                
                op_a, op_b = text[l:i-1], text[i+2:r+1]
                if text[l] == '(':
                    op_a = text[l+1:i-2]
                if text[r] == ')':
                    op_b = text[i+3:r]
                    
                text = text[:l] + bop[text[i]].apply(op_a, op_b) + text[r+1:]
                break
        if can_break:
            break
    
    i = 0
    while i < len(text):
        if text[i] == '{':
            next_i = find_next_bracket(text, i, ('{', '}'))
            if next_i < 0:
                return text
            result += '\\begin{dcases}\n' + _convert(text[i + 2: next_i]) + '\end{dcases}'
            i = next_i + 1
        elif text[i] == '[':
            next_i = find_next_bracket(text, i, ('[', ']'))
            if next_i < 0:
                return text
            result += '\\begin{dsqcases}\n' + _convert(text[i + 2: next_i]) + '\end{dsqcases}'
            i = next_i + 1
        elif text[i] == '_' or text[i] == '^':
            result += text[i]
            if i + 1 < len(text) and text[i + 1] == '(':
                next_i = find_next_bracket(text, i + 1, ('(', ')'))
                if next_i < 0:
                    return text
                result += '{' + text[i+2:next_i] + '}'
                i = next_i + 1
            else:
                i += 1
        elif text[i:i+2] == '**':
            result += '**'
            if i + 2 < len(text) and text[i + 2] == '(':
                next_i = find_next_bracket(text, i + 2, ('(', ')'))
                if next_i < 0:
                    return text
                result += '{' + text[i+3:next_i] + '}'
                i = next_i + 1
            else:
                i += 2
        elif text[i] == '\n':
            result += ' \\\\ \n'
            i += 1
        else:
            if i > 0 and text[i-1: i+1] == '  ':
                result += ' \\ '
            else:
                result += text[i]
            i += 1

    return result
    
def conv(text: str) -> str:
    h, ft = '', ''
    with open('header.txt') as f:
        for l in f:
            h += l

    with open('footer.txt') as f:
        for l in f:
            ft += l
    
    return h + _convert(text.strip()).replace('`', '}').replace('@', '{') + ft


exText = '''
[
{
x_(1)^2 + y^2 = 3
x^(2 + 3^x) = 5
}
{
x + 2 =  y
y - 5 = x^2
}{
x / y = 0
y / (x + 1) = 1
}
  i^2 = -1
]
'''

res = convert(exText, True)
#pdfl = PDFLaTeX.from_texfile('cout.txt')
#pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
