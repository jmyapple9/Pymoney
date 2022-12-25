from datetime import *
class Records:
    def __init__(self):
        import ast
        try:
            fh=open('records.txt','r')
            s=fh.readline()
            if s=='':
                s='[]'
            s=ast.literal_eval(s)
            self._records=s
            assert s==[]
            try:
                origin=int(input('How much money do you have?'))
                self._inital_money=origin
            except ValueError:
                origin=0
                print('Invalid Value for money. Set to 0 by default.')
                self._inital_money=origin
        except AssertionError:
            print('Welcome!\n')
            origin=int(s[1])
            s.pop(1)
            s.pop(0)
            self._records=s
            self._inital_money=origin
        finally:
            fh.close()
    
	
    def add(self,record):
        """Add is used for addition"""
        record=record.split()
        if len(record)!=3 and len(record)!=4:
            record=''
            print('The format of a record should be like this:meal breakfast -50.\
\nFail to add a record.')
            self._records.extend('')
            return None
        '''暫時不判斷categories是否存在，等等回來修（問題在is categories valid 裡的flatten）
        if not categories.is_category_valid(record[0]):
            print("The specified category is not in the category list.\
\nYou can check the category list by command \"view categories\".")
            print("Fail to add a record.")
            self._records.extend('')
            return None
        '''
        try:
            if len(record)==3 :
                int(record[2])
            elif len(record)==4:
                int(record[3])
        except ValueError:
            record=''
            print('Invalid value for money.\nFail to add a record.')
            self._records.extend('')
            return None


        d=record[0]
        d=d.split('-')
        if len(record)==4:
            try:
                assert len(d[0])==4 and len(d[1])==2 and len(d[2])==2 and len(d)==3
            except AssertionError:
                print('The format of date should be YYYY-MM-DD.\nFail to add a record.')
                return None
        if len(record)==3:
            today=str(date.today())
            record.insert(0,today)

        self._records.extend(record)

    def view(self):
        """View is used for checking the records"""
        sum=0
        length=len(self._records)
        date=[self._records[i] for i in range(0,length) if i%4==0]
        category=[self._records[i] for i in range(1,length) if i%4==1]
        food=[self._records[i] for i in range(2,length) if i%4==2]
        price=[int(self._records[i]) for i in range(3,length) if i%4==3]
        for i in range(int(length/4)):
            sum=sum+price[i]
        print('num    Date       Categories       Description    Amount')
        print('=== ========== ================ ================= ======')
        for i in range(int(length/4)):
            print(f'{i+1:2}  {date[i]} {category[i]:14}   {food[i]:18}{price[i]:d}')
        print('=== ========== ================ ================= ======')
        if self._inital_money!=0:
            print(f'Originally you have:{self._inital_money} dollars')
            print(f'Now you have {sum+self._inital_money} dollars!!!')
        else:
            print(f'The total amount above is {sum} dollars.')

    def delete(self,de):
        """Delete is used for deleting the record"""
        if len(self._records)==0:
            print(f'The records is empty.')
            return None
        else:
            try:
                de=int(de)
            except:
                print('Invalid format. Fail to delete a record.')
                return None
        if de<1 or de>int(len(self._records)/4):
            print('There\'s no record with %d. Fail to delete a record.'%de)
            return None
        self._records.pop(-1+4*de)
        self._records.pop(-2+4*de)
        self._records.pop(-3+4*de)
        self._records.pop(-4+4*de)


    def save(self):
        """Save is used for saving record"""
        import sys
        if self._records==[] or self._records[0]!='origin':
            ori=['origin',self._inital_money]
            self._records=ori+self._records
        fh=open('records.txt','w')
        fh.write(str(self._records))
        fh.close()




    def find(self,sub):
        """Find is used for searching records"""
        if sub!=[]:
            x=sub[0]
        SUB=set(sub)
        S=[]
        sum=0
        for i in range(1,int(len(self._records)),4):
            if self._records[i] in SUB:
                S.append(self._records[i-1])
                S.append(self._records[i])
                S.append(self._records[i+1])
                S.append(self._records[i+2])
        if SUB==set():
            print('''The category you searhed isn't exist!''')
        else:
            print(f'Here\'s your expense and income records under category \"{x}\":')
            length=len(S)
            date=[self._records[i] for i in range(0,length) if i%4==0]
            category=[S[i] for i in range(1,length) if i%4==1]
            food=[S[i] for i in range(2,length) if i%4==2]
            price=[int(S[i]) for i in range(3,length) if i%4==3]
            for i in range(int(length/4)):
                sum=sum+price[i]
            print('num    Date       Categories       Description    Amount')
            print('=== ========== ================ ================= ======')
            for i in range(int(length/4)):
                print(f'{i+1:2}  {date[i]} {category[i]:14}   {food[i]:18}{price[i]:d}')
            print('=== ========== ================ ================= ======')
            print(f'The total amount above is {sum} dollars.')
        return S
        
    def ad(self,r):
        self._records.extend(r)
	
    def sumup(self,L):
        price=[int(self._records[i]) for i in range(3,len(self._records)) if i%4==3]
        return sum(price)

