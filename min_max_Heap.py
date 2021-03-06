'''
My implementation of a MinHeap.

MaxHeap would just have the comparisons
in heapifyUp() and heapifyDown() reversed.
'''
class Heap(object):
	def __init__(self, maxHeap=False):
		self.size_ = 0
		self.heap_ = []
		self.maxHeap_ = maxHeap
	def swap(self, firstIndex, secondIndex):
		'''
		If there is an IndexError, great!
		But hopefully all those conditions are already checked.
		'''
		temp = self.heap_[firstIndex]
		self.heap_[firstIndex] = self.heap_[secondIndex]
		self.heap_[secondIndex] = temp

	'''
	These functions act as all three:-
		-> has[Right/LeftChild/Parent]
		-> get[Right/LeftChild/Parent]Index
		-> get[Right/Left/Parent]Of
	'''	
	def getLeftChildOf(self, index):
		'''
		(index*2)+1 is the left child
		'''
		if self.size_ > (index*2)+1:
			return self.heap_[int(index*2+1)], int(index*2+1)
		return None, None

	def getRightChildOf(self, index):
		'''
		(index*2)+2 is the right child
		'''
		if self.size_ > (index*2)+2:
			return self.heap_[int(index*2+2)], int(index*2+2)
		return None, None

	def getParentOf(self, index):
		'''
		(index-1)/2 is the parent 
		'''
		if self.size_ > (index-1)/2 and (index-1)/2 >= 0:
			return self.heap_[int((index-1)/2)], int((index-1) / 2)
		return None, None

	def peek(self):
		'''
		Just return the top element
		'''
		if self.size_ == 0:
			return None
		return self.heap_[self.size_ - 1]

	def poll(self):
		'''
		Remove the top element,
		bring the last element here,
		decrease the size,
		heapifyDown to adjust this
		'''
		if self.size_ == 0:
			return None
		heapTop = self.heap_[0]
		self.heap_[0] = self.heap_[self.size_ - 1]
		self.heap_.pop(self.size_ - 1) # n00b mistake
		self.size_ -= 1
		self.heapifyDown()
		return heapTop

	def addElement(self, element):
		'''
		Add new element to the end,
		increase size,
		heapifyUp to adjust this new element
		'''
		self.heap_.append(element)
		self.size_ += 1
		self.heapifyUp()

	def heapifyDown(self, current=0):
		'''
		Largest element is at the top,
		compare with both children,
		while element is larger than left child,
		swap the smaller (or larger with max heap)
		of right & left child with current
		'''
		if self.size_ == 0:
			return
		currentIndex = current
		left, _ = self.getLeftChildOf(currentIndex)
		if left is None:
			return
		while left is not None:
			right, right_index = self.getRightChildOf(currentIndex)
			left, left_index = self.getLeftChildOf(currentIndex)
			if left is not None:
				if right is not None:
					if self.maxHeap_: # swap the larger element in a max heap
						child_index = right_index if right > left else left_index
					else: # swap the smaller element in a min heap
						child_index = right_index if right < left else left_index
				else:
					child_index = left_index
			else:
				break
			if self.maxHeap_:
				if self.heap_[child_index] < self.heap_[currentIndex]:
					break
				else:
					self.swap(child_index, currentIndex)
			else:
				if self.heap_[child_index] > self.heap_[currentIndex]:
					break
				else:
					self.swap(child_index, currentIndex)
			currentIndex = child_index

	def heapifyUp(self):
		'''
		Largest element is at the very end,
		so starting at the bottom, 
		while element has parent node, 
		compare element with it's parent,
		if parent is larger, then swap
		'''
		if self.size_ <= 1:
			return
		currentIndex = self.size_ - 1
		while True:
			parent, parent_index = self.getParentOf(currentIndex)
			if parent is None:
				break
			if self.maxHeap_:
				if self.heap_[parent_index] <= self.heap_[currentIndex]:
					self.swap(parent_index, currentIndex)
				else:
					break
			else:
				if self.heap_[parent_index] >= self.heap_[currentIndex]:
					self.swap(parent_index, currentIndex)
				else:
					break
			currentIndex = parent_index

	def removeElement(self, element):
		'''
		Find if element exists in the list, 
		pop it out and replace it with the bottom element,
		and then heapifyDown from that index
		'''
		try:
			index = self.heap_.index(element)
		except ValueError as e:
			# print(e) # prints "element is not in list"
			return
		elementToRemove = self.heap_[index]
		self.heap_[index] = self.heap_[self.size_ - 1]
		self.heap_.pop(self.size_ - 1) # or remove()
		self.size_ -= 1
		self.heapifyDown(index)

	def printHeap(self):
		print(self.heap_[:self.size_])


heap = Heap(maxHeap=True)
heap.addElement(10)
heap.addElement(15)
heap.addElement(20)
heap.addElement(17)
heap.printHeap()
heap.addElement(8)
heap.printHeap()
print(heap.poll())
heap.printHeap()
heap.addElement(25)
heap.printHeap()
print(heap.poll())
heap.printHeap()
heap.addElement(1)
heap.addElement(2)
heap.addElement(3)
heap.printHeap()
heap.addElement(40)
heap.addElement(45)
heap.removeElement(8)
heap.printHeap()
print(heap.poll())
heap.printHeap()
heap.addElement(18)
heap.addElement(8)
heap.printHeap()
print(heap.poll())
print(heap.poll())
heap.addElement(30)
heap.addElement(9)
print(heap.poll())
heap.printHeap()
heap.addElement(35)
heap.printHeap()
heap.addElement(32)
heap.printHeap()
heap.addElement(23)
heap.printHeap()
heap.printHeap()
heap.removeElement(90)
heap.removeElement(32)
heap.printHeap()
print(heap.poll())
print(heap.poll())
print(heap.poll())
print(heap.poll())
print(heap.poll())
print(heap.poll())
print(heap.poll())
print(heap.poll())
print(heap.poll())
heap.printHeap()
print(heap.poll())
heap.printHeap()
print(heap.poll())