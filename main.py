from conv import convert

exText = '''
[
{
x_(1)^2 + y^2 = 3
x^(2 + 3^x) = 5
}
{
x + 2 =  y
y - 5 = x^2
`Ответ: 11`
}{
x / y = 0
y / (x + 1) = 1
}
  i^2 = -1
]
'''

res = convert(exText, True, False, False)
print(res)
