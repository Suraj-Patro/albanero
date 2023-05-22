# importing module
from dataclasses import dataclass

@dataclass
class A:
	a: int
	b: str

@dataclass
class B:
	c: str
	d: A


# Method 1
data = {'c':'hello', 'd':{'a':4, 'b':'bye'}}
b = B(**data)
print (b)

# Method 2
data = {'c':'hello', 'd': A(**{'a':4, 'b':'bye'})}
c = B(**data)
print(c)


