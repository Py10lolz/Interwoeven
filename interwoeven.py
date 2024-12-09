import itertools


INC = 14
DEC = 31
LFT = 43
RGT = 47
INP = 53
OUT = 56
LOAD = 61
HLT = 62


class Interwoeven_Interpreter:

	def __init__(self, program, inp = "", mem_size = 30000):
		self.nodes = []
		self.node_values = []
		self.num_of_nodes = 0
		self.inp = list(inp)
		self.mem = [0 for _ in range(mem_size)]
		self.mem_ptr = 0
		self.mem_size = mem_size
		self.halt = False
		self.build_graph(program)


	def run(self):
		while self.halt != True: self.forward()


	def forward(self):
		ins = self.node_values[0]
		if ins == INC:
			self.mem[self.mem_ptr] += 1
			self.mem[self.mem_ptr] %= 256

		elif ins == DEC:
			self.mem[self.mem_ptr] -= 1
			self.mem[self.mem_ptr] %= 256

		elif ins == LFT:
			self.mem_ptr -= 1
			self.mem_ptr %= self.mem_size

		elif ins == RGT:
			self.mem_ptr += 1
			self.mem_ptr %= self.mem_size

		elif ins == INP:
			if self.inp == []: self.mem[self.mem_ptr] = 0
			else: self.mem[self.mem_ptr] = self.inp.pop(0)

		elif ins == OUT:
			print(chr(self.mem[self.mem_ptr]), end = '')

		elif ins == LOAD:
			self.node_values[0] = self.mem[self.mem_ptr]

		elif ins == HLT:
			self.halt = True

		new_node_values = [0 for _ in range(self.node_num)]
		for i in range(len(self.node_num)):
			P = sum(self.node_values[j] for j in self.partially_contained[i])
			F = sum(self.node_values[j] for j in self.fully_contained[i])
			new_node_values[i] = pow(self.node_values[i]+F, P, 101)
		self.node_values = new_node_values


	def build_graph(self, program):

		paren = []
		brac = []
		i = 0

		for ch in program:
			if ch == '(':
				paren.append(i)
			elif ch == ')':
				self.nodes.append((paren.pop(), i))
				self.node_values.append(1)
			if ch == '{':
				brac.append(i)
			elif ch == '}':
				self.nodes.append((brac.pop(), i))
				self.node_values.append(1)
			i += 1
		
		self.partially_contained = [[] for _ in range(len(self.nodes))]
		self.fully_contained = [[] for _ in range(len(self.nodes))]
		self.node_num = len(self.nodes)
		for i in range(self.node_num):
			for j in itertools.chain(range(i), range(i+1, len(self.nodes))):
				n1 = self.nodes[i]
				n2 = self.nodes[j]
				s = (n1[0] > n2[0] and n1[0] < n2[1]) + (n1[1] > n2[0] and n1[1] < n2[1])
				if s == 1: self.partially_contained[i].append(j)
				elif s == 2: self.fully_contained[i].append(j)
