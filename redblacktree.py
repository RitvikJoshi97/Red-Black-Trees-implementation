class Node:
    def __init__(self, val= None):
        self.val = val
        self.parent = None
        self.left = None
        self.right = None
        self.red = False

class Tree:
    def __init__(self):
        self.nil = Node()
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil

## INSERT
    def insert(self, val):
        node = Node(val)
        node.parent = None
        node.left = self.nil
        node.right = self.nil
        node.red = True

        y = None
        x = self.root

        while x != self.nil:
            y = x
            if node.val < x.val:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.val < y.val:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.red = False
            return

        if node.parent.parent == None:
            return

        self.checkViolation(node)

    def checkViolation(self, node):
        while node.parent.red == True:
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left
                if uncle.red == True:
                    uncle.red = False
                    node.parent.red = False
                    node.parent.parent.red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rightRotation(node)
                    node.parent.red = False
                    node.parent.parent.red = True
                    self.leftRotation(node.parent.parent)
            else:
                uncle = node.parent.parent.right

                if uncle.red == True:
                    uncle.red = False
                    node.parent.red = False
                    node.parent.parent.red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.leftRotation(node)
                    node.parent.red = False
                    node.parent.parent.red = True
                    self.rightRotation(node.parent.parent)
            if node == self.root:
                break
        self.root.red = False
    
    def leftRotation(self, node):
        y = node.right
        node.right = y.left
        if y.left != self.nil:
            y.left.parent = node

        y.parent = node.parent
        if node.parent == None:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y

    def rightRotation(self, node):
        y = node.left
        node.left = y.right
        if y.right != self.nil:
            y.right.parent = node

        y.parent = node.parent
        if node.parent == None:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y

    def traverseInOrder(self):
        self.inOrderTraversal(self.root)

    def inOrderTraversal(self, curNode):
        if curNode.left != None:
            self.inOrderTraversal(curNode.left)
        if curNode.val != None:
            print(curNode.val)
        if curNode.right != None:
            self.inOrderTraversal(curNode.right)

    
    def asIsTraversal(self, start, curNode):
        if start:
            curNode += ("val: " + str(start.val))
            if start.parent != None:
                curNode += ", parent: " 
                curNode +=  str(start.parent.val)
            if start.red == True:
                curNode += ", colour: red |" 
            else:
                curNode += ", colour: black |"
            curNode = self.asIsTraversal(start.left, curNode)
            curNode = self.asIsTraversal(start.right, curNode)
        return curNode


## SEARCH
    def search(self, val):
        node = self.searchFunc(val, self.root)
        return node


    def searchFunc(self, val, node):
        print(f"searching for {val} at {node.val}")
        if val == node.val:
            print(f"{node.val} found with the parent: {node.parent.val}")
            return node.val
        elif node.val < val:
            self.searchFunc(val, node.right)
        elif node.val > val:
            self.searchFunc(val, node.left)
        else:
            print(f"{val} not found")


# MAX and MIN
    def max(self, node):
        while node.right != self.nil:
            node = node.right
        print(node.val)
        return node

    def min(self, node):
        while node.left != self.nil:
            node = node.left
        print(node.val)
        return node



# DELETE
    def deleteFix(self, node):
        while node != self.root and node.red == False:
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.red == True:
                    sibling.red = False
                    node.parent.red = True
                    self.leftRotation(node.parent)
                    sibling = node.parent.right

                if sibling.left.red == False and sibling.right.red == False:
                    sibling.red = True
                    node = node.parent
                else:
                    if sibling.right.red == False:
                        sibling.left.red = False
                        sibling.red = True
                        self.rightRotation(sibling)
                        sibling = node.parent.right

                    sibling.red = node.parent.red
                    node.parent.red = False
                    sibling.right.red = False
                    self.leftRotation(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling.red == True:
                    sibling.red = False
                    node.parent.red = True
                    self.rightRotation(node.parent)
                    sibling = node.parent.left

                if sibling.right.red == False and sibling.right.red == False:
                    sibling.red = True
                    node = node.parent
                else:
                    if sibling.left.red == False:
                        sibling.right.red = False
                        sibling.red = True
                        self.leftRotation(sibling)
                        sibling = node.parent.left

                    sibling.red = node.parent.red
                    node.parent.red = False
                    sibling.left.red = False
                    self.rightRotation(node.parent)
                    node = self.root
        node.red = False
        

    def transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, node, val):
        z = self.nil
        while node != self.nil:
            if node.val == val:
                z = node

            if node.val <= val:
                node = node.right
            else:
                node = node.left

        if z == self.nil:
            print("Cannot find val in the tree")
            return

        y = z
        y_original_red = y.red
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif (z.right == self.nil):
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.min(z.right)
            y_original_red = y.red
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.red = z.red
        if y_original_red == 0:
            self.deleteFix(x)


    def listAllNodes(self,curNode,listofallnodes):
        if curNode.left != None:
            listofallnodes.append(curNode.val)
            self.listAllNodes(curNode.left, listofallnodes)
        if curNode.val != None:
            listofallnodes.append(curNode.val)
        if curNode.right != None:
            listofallnodes.append(curNode.val)
            self.listAllNodes(curNode.right, listofallnodes)
        return listofallnodes

    def median(self):
        listofallnodes = []
        listofallnodes = self.listAllNodes(self.root, listofallnodes)
        # print(listofallnodes[len(listofallnodes)//2])
        return listofallnodes[len(listofallnodes)//2]


def intersection(root1, root2):
    l1 = []
    l2 = []
    l1 = tree1.listAllNodes(root1, l1)
    l2 = tree2.listAllNodes(root2, l2)
    l3 = list(set(l1) & set(l2))
    return l3
    

##############################

tree1 = Tree()
tree1.insert(8)
tree1.insert(14)
tree1.insert(5)
tree1.insert(6)
tree1.insert(7)
tree1.insert(9)



tree2 = Tree()
tree2.insert(8)
tree2.insert(14)
tree2.insert(16)
tree2.insert(18)
tree2.insert(1)
tree2.insert(2)
tree2.insert(3)
tree2.insert(4)
tree2.insert(5)
tree2.insert(6)

# print("intersect here: ", intersection(tree1.root, tree2.root))

##############################


tree = Tree()
tree.insert(8)
tree.insert(14)
tree.insert(16)
tree.insert(18)
tree.insert(1)
tree.insert(2)
tree.insert(3)
tree.insert(4)
tree.insert(5)
tree.insert(6)
tree.insert(7)
tree.insert(9)
tree.insert(10)
tree.insert(11)
tree.insert(13)
tree.insert(15)
tree.insert(19)
tree.insert(21)
tree.insert(24)

tree.delete(tree.root, 6)
tree.delete(tree.root, 18)
tree.delete(tree.root, 1)
tree.delete(tree.root, 4)
tree.delete(tree.root, 7)
tree.delete(tree.root, 9)
tree.delete(tree.root, 13)
tree.delete(tree.root, 15)

# print("____________")
# print("traverse: ")
# tree.traverseInOrder()
# print("____________")
# print("min: ", tree.min(tree.root).val)
# print("max: ", tree.max(tree.root).val)



# print("____________")
# print(tree.asIsTraversal(tree.root, ""))
# print("____________")


# print("median", tree.median())
# tree.search(3)


print("____________")
print("____________")
done = False
while not done:
    print("1. insert")
    print("2. delete")
    print("3. search")
    print("4. traverse")
    print("5. min")
    print("6. max")
    print("7. median")
    print("8. intersection")
    print("0. exit")
    getInput = int(input("enter an integer from one of the above: "))
    if getInput == 1:
        getVal = int(input("enter integer to insert: "))
        tree.insert(getVal)
    elif getInput == 2:
        getVal = int(input("enter integer to delete: "))
        tree.delete(getVal)
    elif getInput == 3:
        getVal = int(input("enter integer to search: "))
        print(tree.search(getVal))
    elif getInput == 4:
        print("traverse in order: ")
        tree.traverseInOrder()
        print("____________")
        print("traverse as is: ")
        print(tree.asIsTraversal(tree.root, ""))
    elif getInput == 5:
        print("min: ")
        tree.min(tree.root)
    elif getInput == 6:
        print("max: ")
        tree.max(tree.root)
    elif getInput == 7:
        print("median: ")
        print(tree.median())
    elif getInput == 8:
        print("itersection: ")
        print(intersection(tree1.root, tree2.root))
    elif getInput == 0:
        done = True
    else: 
        print("incorrect value entered")
    