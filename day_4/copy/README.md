Shallow Copy
------------
import copy
li1 = [1, 2, [3,5], 4]
li2 = copy.copy(li1)
li2     ->      [1, 2, [3,5], 4]


Deep Copy
---------
import copy
li1 = [1, 2, [3,5], 4]
li2 = copy.deepcopy(li1)
li2     ->      [1, 2, [3,5], 4]
