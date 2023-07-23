# Python code to demonstrate naive method
# to compute factorial
'''
n = int(input())

fact = 1

if n < 0:
	print("There is no factorial of a negative number.")
elif n == 0:
	print("1")
else:
	for i in range(1, n+1):
		fact = fact * i
	print(f'Factorial of {n} = {fact}.')
'''
num = int(input())

res = num ** 2

print(res)
