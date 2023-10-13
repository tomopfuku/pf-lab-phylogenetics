class Node:
    def __init__(self):
        self.label = ""
        self.length = 0.0
        self.time_length = 0.0
        self.parent = None
        self.children = []
        self.data = {}
        self.istip = False
        self.height = 0
        self.note = ""

    def get_sib(self):
        assert len(self.parent.children)==2
        for ch in self.parent.children:
            if ch != self:
                return ch

    def add_child(self,child):
        #make sure that the child is not already in there
        assert child not in self.children
        self.children.append(child)
        child.parent = self

    def remove_child(self,child):
        #make sure that the child is in there
        assert child in self.children
        self.children.remove(child)
        child.parent = None

    def leaves(self,v=None):
        if v == None:
            v = []
        if len(self.children) == 0:
            v.append(self)
        else:
            for child in self.children:
                child.leaves(v)
        return v

    def leaves_fancy(self):
        return [n for n in self.iternodes() if n.istip ]

    def lvsnms(self):
        return [n.label for n in self.iternodes() if n.istip ]

    def iternodes(self,order="preorder"):
        if order.lower() == "preorder":
            yield self
        for child in self.children:
            for d in child.iternodes(order):
                yield d
        if order.lower() == "postorder":
            yield self

    def inorder(self):
        if len(self.children)>0:
            for i,child in enumerate(self.children):
                if i == 0:
                    for d in child.inorder():
                        yield d
                    yield self
                else:
                    for d in child.inorder():
                        yield d
        else:
            yield self
        #for child in self.children[0].inorder():
        #    yield child
        #yield from self.children[0].inorder()
        #yield self
        #for child in self.children[1:]:
        #    yield from child.inorder()
        #    for d in child.inorder():
        #        yield d


    def prune(self):
        p = self.parent
        if p != None:
            p.remove_child(self)
        return p
    
    def get_newick_repr_paint(self,showbl=False):
        ret = ""
        painted_children = []
        for i in self.children:
            if "paint" in i.data:
                painted_children.append(i)
        for i in range(len(painted_children)):
            if i == 0:
                ret += "("
            ret += painted_children[i].get_newick_repr_paint(showbl)
            if i == len(painted_children)-1:
                ret += ")"
            else:
                ret += ","
        if self.label != None and "paint" in self.data:
            ret += self.label
        if showbl == True:
            ret += ":" + str(self.length)
        return ret

    def get_newick_repr(self,showbl=False):
        ret = ""
        for i in range(len(self.children)):
            if i == 0:
                ret += "("
            ret += self.children[i].get_newick_repr(showbl)
            if i == len(self.children)-1:
                ret += ")"
            else:
                ret += ","
        if self.label != None:
            ret += self.label
        if showbl == True:
            ret += ":" + str(self.length)
        return ret

    def get_ext_newick_repr(self):
        ret = ""
        for i in range(len(self.children)):
            if i == 0:
                ret += "("
            ret += self.children[i].get_ext_newick_repr()
            if i == len(self.children)-1:
                ret += ")"
            else:
                ret += ","
        if self.label != None:
            ret += self.label
        ret += ":" + str(self.length)+self.note
        return ret

    """def get_newick_repr_note(self,showbl=False):
        ret = ""
        for i in range(len(self.children)):
            if i == 0:
                ret += "("
            ret += self.children[i].get_newick_repr(showbl)
            if i == len(self.children)-1:
                ret += ")"
            else:
                ret += ","
        if self.label != None:
            ret += self.label+self.note
        if showbl == True:
            ret += ":" + str(self.length)
        return ret"""

    def get_newick_repr_note(self,showbl=False):
        ret = ""
        for i in range(len(self.children)):
            if i == 0:
                ret += "("
            ret += self.children[i].get_newick_repr_note(showbl)
            if i == len(self.children)-1:
                ret += ")"
            else:
                ret += ","
        if self.label != None:
            ret += self.label
        #if len(self.note) > 0:
            #ret += "["+self.note+"]"
        if showbl == True:
            ret += ":" + str(self.length)+self.note
        else:
            ret += ":" + str(1.0)+self.note
        return ret

    def get_nexus_repr(self,notes=True):
        if notes==False:
            newick=self.get_newick_repr(True)
        else:
            newick=self.get_newick_repr_note(True)
        ret="#NEXUS\nbegin trees;\ntree tree1 = [&R] "
        ret+=newick+";\n"
        ret+="end;"
        return ret

    def len_to_root(self):
        path=0.0
        curnode = self
        while True:
            if curnode.parent == None:
                break
            path+=curnode.length
            curnode=curnode.parent
        return path

    def set_heights_fossil(self):
        tipps={}
        for tip in self.leaves_fancy():
            pl = tip.len_to_root()
            tipps[tip] = pl
        zerotip = max(tipps,key=tipps.get)            
        treeh = tipps[zerotip]
        for tip in tipps:
            tip.height = treeh-tipps[tip]            
        for n in self.iternodes(order="postorder"):
            if n.istip == False:
                n.height = n.children[0].height+n.children[0].length

    def set_height(self):
        if len(self.children) == 0:
            self.height = 0
        else:
            tnode = self
            h = 0
            while len(tnode.children) > 0:
                if tnode.children[1].length < tnode.children[0].length:
                    tnode = tnode.children[1]
                else:
                    tnode = tnode.children[0]
                h += tnode.length
            self.height = h

