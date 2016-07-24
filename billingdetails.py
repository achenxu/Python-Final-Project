from Tkinter import *
from sqlite3 import dbapi2 as sqlite
import win32api
import win32print
import random
import time


columns=('Item_No', 'Item_Name', 'Item_Type', 'Quantity_Remain', 'Item_Cost', 'Expiry_Date','Manufactured_By')

c=sqlite.connect("grocery.sqlite")
cur=c.cursor()

def billingitems():
    global c, cur, flag, t, name, name1, add, billingsto, names, qty, sl, qtys,n, namee, lb1
    t=0
    
    names=[]
    qty=[]
    sl=[]
    n=[]
    qtys=['']*10
    cur.execute("select * from grocerylist")
    for i in cur:
        n.append(i[1])
    c.commit()
    # apt.destroy()
    flag='billingsto'
    billingsto=Tk()
    billingsto.title('BILLING')
    Label(billingsto,text='-'*48+'Billing'+'-'*49).grid(row=0,column=0,columnspan=7,sticky='W')
    Label(billingsto,text='Enter Name: ').grid(row=1,column=0)
    name1=Entry(billingsto)
    name1.grid(row=1, column=1)
    Label(billingsto,text='Enter Address: ').grid(row=2,column=0)
    add=Entry(billingsto)
    add.grid(row=2, column=1)
    
    Label(billingsto,text='-'*115).grid(row=6, column=0,columnspan=7,sticky='W')
    Label(billingsto,text='Select Item',relief='ridge',width=15).grid(row=7,column=0)
    Label(billingsto,text='Qty_Remain',relief='ridge',width=10).grid(row=7,column=1)
    Label(billingsto,text='Cost',relief='ridge',width=4).grid(row=7,column=2)
    Label(billingsto,text='Expiry Date',width=10,relief='ridge').grid(row=7,column=3)
   
    Button(billingsto,text='Add to bill',width=15,command=addtothebill).grid(row=8, column=6)
    Label(billingsto,text='QUANTITY',width=20,relief='ridge').grid(row=7, column=5)
    qtys=Entry(billingsto)
    qtys.grid(row=8,column=5)
    refresh()
    Button(billingsto,width=15,text='Main Menu', command= mainmenu).grid(row=1,column=6)
    Button(billingsto,width=15,text='Refresh Stock',command=refresh).grid(row=3,column=6)
    Button(billingsto,width=15,text='Reset Bill',command=resetbill).grid(row=4,column=6)
    Button(billingsto,width=15,text='Print Bill',command=printbill).grid(row=5,column=6)
    Button(billingsto,width=15,text='Save Bill',command=savebill).grid(row=7,column=6)
    
    billingsto.mainloop()

def refresh():
    global cur, c, billingsto, lb1, lb2, vsb
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)

    def onmousewheel():
        lb1.ywiew=('scroll',event.delta,'units')
        lb2.ywiew=('scroll',event.delta,'units')
        return 'break'
    index=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    lb1=Listbox(billingsto,width=25, yscrollcommand=vsb.set)
    lb2=Listbox(billingsto ,width=7,yscrollcommand=vsb.set)
    lb3=Listbox(billingsto,yscrollcommand=vsb.set,width=7)
    lb4=Listbox(billingsto,yscrollcommand=vsb.set,width=20)
    
    
    vsb.grid(row=8,column=2,sticky=N+S)
    lb1.grid(row=8,column=0)
    lb2.grid(row=8,column=1)
    lb3.grid(row=8,column=2)
    lb4.grid(row=8,column=3)
    
    
    lb1.bind('<MouseWheel>',onmousewheel)
    lb2.bind('<MouseWheel>',onmousewheel)
    cur.execute("select * from grocerylist")
    for i in cur:
        index+=1
        lb1.insert(index,str(i[0])+' '+i[1])
        lb2.insert(index,i[3])
        lb3.insert(index,i[4])
        lb4.insert(index,i[5])
        
        
    c.commit()
    lb1.bind('<<ListboxSelect>>', select_mn)    

def select_mn(e): #store the selected item from listbox
    global billingsto, lb1, n ,p, sl1, nm
    p=lb1.curselection()
    x=0
    sl1=''
    cur.execute("select * from grocerylist")
    for i in cur:
        if x==int(p[0]):
            sl1=int(i[0])
            break
        x+=1
    c.commit()
    print sl1
    nm=n[x]
    print nm
    
def addtothebill(): # append to the bill
    global st, names, nm , qty, sl,cur, c, sl1
    sl.append(sl1)
    names.append(nm)
    qty.append(qtys.get())
    print qty
    print sl[len(sl)-1],names[len(names)-1],qty[len(qty)-1]
    
def printbill():
    win32api.ShellExecute (0,"print",'bill.txt','/d:"%s"' % win32print.GetDefaultPrinter (),".",0)
    ShellExecute
    
def resetbill():
    global sl, names, qty
    sl=[]
    names=[]
    qty=[]
    
def savebill():
    global t, c, cur, st, names, qty, sl , named, addd, name1, add,det, vc_id
    price=[0.0]*10
    q=0
    det=['','','','','','','','']
    det[2]=str(sl)
    for i in range(len(sl)):
        print sl[i],' ',qty[i],' ',names[i]
    for k in range(len(sl)):
        cur.execute("select * from grocerylist where Item_No=?",(sl[k],))
        for i in cur:
            price[k]=int(qty[k])*float(i[4])
            print qty[k],price[k]
            cur.execute("update grocerylist set Quantity_Remain=? where Item_No=?",(int(i[3])-int(qty[k]),sl[k]))
        c.commit()
    det[5]=str(random.randint(100,999))
    total=0.00
    for i in range(10):
        if price[i] != '':
            total+=price[i] #totalling
    m='\n\n\n'
    m+="===============================================\n"
    m+="                                  No :%s\n\n" % det[5]
    m+="          INDIAN GROCERY STORE\n"
    m+="  1602 ,Chatham Hills, Springfield-62704, Illinois\n\n"
    m+="-----------------------------------------------\n"
    if t==1:
        m+="Name: %s\n" % named
        m+="Address: %s\n" % addd
        det[0]=named.lower()
        det[1]=addd.lower()
        cur.execute('select * from customer')
        for i in cur:
            if i[0]==named:
                det[7]=i[3]
    else:
        m+="Name: %s\n" % name1.get()
        m+="Address: %s\n" % add.get()
        det[0]=name1.get()
        det[1]=add.get()
        cur.execute('insert into customer values(?,?)',(det[0].lower(),det[1].lower()))
    m+="-----------------------------------------------\n"
    m+="Product                      Qty.       Price\n"
    m+="-----------------------------------------------\n"
    for i in range(len(sl)):
        if names[i] != 'nil':
            s1=' '
            s1=(names[i]) + (s1 * (27-len(names[i]))) + s1*(3-len(qty[i])) +qty[i]+ s1*(15-len(str(price[i])))+str(price[i]) + '\n'
            m+=s1
    m+="\n-----------------------------------------------\n"
    m+='Total'+(' '*25)+(' '*(12-len(str(total)))) +'Rs '+ str(total)+'\n'
    det[3]=str(total)
        
    m+="-----------------------------------------------\n\n"
    m+="Dealer 's signature:___________________________\n"
    m+="===============================================\n"
    print m
    p=time.localtime()
    det[4]=str(p[2])+'/'+str(p[1])+'/'+str(p[0])
    det[6]=m
    bill=open('bill.txt','w')
    bill.write(m)
    bill.close()
    cb=('cus_name','cus_add','items','Total_cost','bill_dt','bill_no','bill')
    cur.execute('insert into bill values(?,?,?,?,?,?,?)',(det[0],det[1],det[2],det[3],det[4],det[5],det[6]))
    c.commit()

    
    
def mainmenu():
    if flag=='sto':
        sto.destroy()
    elif flag=='billingsto':
        billingsto.destroy()  
        
billingitems()