class Categories:
    def __init__(self):
        self._categories=['expense',['food',['meal','snack','drink'],'transportation',['bus','railway']],'income',['salary','bonus']]

    def view(self):
        def innerview(L,level=0):
            if L==None:
                return
            if type(L) in {list,tuple}:
                for i in L:
                    innerview(i,level+1)
            else:
                print(f'{"  "*(level-1)}{L}')
        L=self._categories
        innerview(L,)


    def is_category_valid(self,category):
        """This function is used for checking if the category is valid"""
        L=self._categories
        L=set(self.flatten(L))
        if category in L:
            return True
        else:
            return False


    def find_subcategories(self,target):
        def find_subcategories_gen(target, categories,found=False):
            if type(categories) == list :
                for index,child in enumerate(categories):
                    yield from find_subcategories_gen(target,child,found)
                    if child == target and index + 1 < len(categories) and type(categories[index + 1]) == list:
                        yield from find_subcategories_gen(target,categories[index+1],True)
            else:
                if categories==target or found:
                    yield categories
        categories=self._categories
        l=[i for i in find_subcategories_gen(target,categories)]
        return l
