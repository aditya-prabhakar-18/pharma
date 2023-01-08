from tkinter import *
#python 39/scripts
#pip install Pillow
#pip install Prettytable
#pip install mysql-connector-python
from PIL import ImageTk,Image
from mysql.connector import *
from tkinter import messagebox
from tkinter import ttk
from prettytable import PrettyTable
from datetime import datetime

mydb = connect(host="localhost", user="root", password="tiger")
mycursor = mydb.cursor(buffered=1)

# Checking the databese
mycursor.execute("SHOW DATABASES")
databases = mycursor.fetchall()
if ("pharmacy",) in databases:
    mycursor.execute("USE pharmacy")
    mydb.commit()
else:
    mycursor.execute("CREATE DATABASE pharmacy")
    mycursor.execute("USE pharmacy")
    mydb.commit()

# Checking the user table
mycursor.execute("SHOW TABLES")
tables = mycursor.fetchall()
if ('stocks',) in tables:
    pass
else:
    mycursor.execute("""
    CREATE TABLE stocks(
    med_id   varchar(30) PRIMARY KEY,  
    med_name varchar(200), 
    amt      int,          
    expiry   date,         
    price    float,        
    lot_no   int         
    )""")
    mydb.commit()

if ("users",) in tables:
    pass
else:
    mycursor.execute("""
    CREATE TABLE users (
    userID INTEGER PRIMARY KEY AUTO_INCREMENT,
    name varchar(50),
    username varchar(20),
    password varchar(20)
    )""")
    mydb.commit()
    mycursor.execute("insert into users values(1,'Admin','root','tiger')")
    mycursor.execute("insert into users values(2,'Aditya Prabahkar','Adi','tiger')")
    mydb.commit()
mycursor.close()
mydb.close()

allowentry=0

def LoginPage():
    global allowentry
    mydb = connect(host="localhost",database="pharmacy" ,user="root", password="tiger")
    mycursor = mydb.cursor(buffered=1)

    log=Tk()
    log.title("pharma")
    log.geometry("500x500+400+60")
    log.resizable(False,False)
    bgimg=ImageTk.PhotoImage(Image.open("pharma\\loginbg.png"))
    log.configure(background="navajowhite")
    log.iconbitmap("pharma\\sign-emergency-code-sos_24_icon-icons.com_57215.ico")

    LoginFrame = Frame(log, bg="midnightblue")
        
    limg=Label(LoginFrame,image=bgimg,borderwidth=0)
    limg.place(x=0,y=0)

    center=Frame(LoginFrame,borderwidth=0,bg="#0489A8")

    LoginHeading = Label(LoginFrame, text="Log In", bg="#0B111D",height=1,fg='white',font=("Bahnschrift Light",30,""))
    LoginHeading.pack(fill=X,side=TOP,pady=30)

    userName = Label(center, text="Username:",font=("Bahnschrift Light",17,"bold underline"),fg="white",bg="#0489A8")
    userName.grid(row=0,column=0,padx=22,pady=20,sticky="nsew")

    usernameValue = Entry(center,width=16,font=("Calibri",15,"bold"),relief="flat")
    usernameValue.grid(row=0,column=1,padx=0,pady=20,)

    Password = Label(center, text="Password:",fg="white",bg="#0489A8",font=("Bahnschrift Light",17,"bold underline"))
    Password.grid(row=2,column=0,padx=22,pady=20,sticky="nsew")

    PasswordValue = Entry(center,width=16,font=("Calibri",15,"bold"),relief="flat",show="●")
    PasswordValue.grid(row=2,column=1,padx=0,pady=20,)

    def submit():
        global allowentry
        mycursor.execute("SELECT * FROM users WHERE username='{}' AND password='{}'".format(usernameValue.get(),PasswordValue.get()))
        data = mycursor.fetchall()
        if len(data)!=0:
            allowentry=1
            mycursor.close()
            mydb.close()
            log.destroy()
        else:
            messagebox.showinfo("Log-In Error","InValid Username or Password")

    submitButton = Button(LoginFrame, text="Submit",command=submit,fg="white",height=0, bg="#0B111D",font=("Segoe UI",18,"bold"),borderwidth=0)
    submitButton.pack(side=BOTTOM,expand=True,pady=20,fill=X)

    center.pack(expand=1,fill=BOTH,padx=70,pady=50)

    LoginFrame.pack(expand=1,fill=BOTH)
    usernameValue.focus()
    def efoc(e):
        submit()
    def pfoc(e):
        PasswordValue.focus()
    usernameValue.bind("<Return>",pfoc)
    PasswordValue.bind("<Return>",efoc)
    log.mainloop()

def check_float(s):
    try:
        float(s)
        return True

    except ValueError:
        return False

def check_date(st):
    s=1
    if len(st)!=10:
        s=0
    elif st[4]!="-" or st[7]!="-":
        s=0
    elif st[:4].isdigit()==0 or st[8:].isdigit()==0 or st[5:7].isdigit()==0:
        s=0
    if s==1:
        if int(st[5:7]) in (1,3,5,7,8,10,12):
            maxdays=31
        elif int(st[5:7]) in (4,6,9,11):
            maxdays=30
        elif int(st[:4])%4==0 and int(st[:4])%100!=0 or int(st[:4])%400==0:
            maxdays=29
        else:
            maxdays=28
        if int(st[5:7]) not in range(1,13):
            s=0
        elif int(st[8:]) not in range(1,maxdays+1):
            s=0
    if s==0:
        return False
    else:
        return True

def launchapp():
    #===================base window================
    root=Tk()
    root.title("pharma")
    root.geometry("1230x600+60+50")
    root.minsize(1230,600)
    #root.resizable(False,False)
    root.iconbitmap("pharma\\sign-emergency-code-sos_24_icon-icons.com_57215.ico")
    root.configure()
    #===============base window====================

    mycon=connect(host="localhost",user="root",password="tiger",database="pharmacy")
    cur=mycon.cursor(buffered=True)

    global additemcount,bill_list
    additemcount=1
    bill_list=[]
    def pay():
        t=PrettyTable(["Product","Exp. Date","Qty.","Total Price"])
        for i in bill_table.get_children():
            vv=bill_table.item(i,"values")
            med_id=vv[0]
            qty=int(vv[5])
            cur.execute("update stocks set amt=amt-%s where med_id=%s"%(qty,med_id) )
            t.add_row([vv[2],vv[3],vv[5],vv[6]])
            mycon.commit()
        t.add_row(['','','',''])
        t.add_row(['','','',''])
        t.add_row(["",'','Grand Total:',str(grandtot())])
        for j in bill_table.get_children():
            bill_table.delete(j)
        grandtot()

        t_string=t.get_string()

        bb1=0
        for i in t_string:
            if i=="\n":
                break
            bb1+=1
        
        bb=(bb1-13)//2

        p1=(bb)*"="+"|Pharma Bill|"+(bb1-bb-13)*"="+"\n\n"
        p2="Time  : "+datetime.now().strftime("%d %b, %Y   %H:%M:%S")+"\n\n"
        p3=("\n\n"+((bb1-24)//2)*" "+"Wishing You Good HEALTH."+" "*(bb1-((bb1-24)//2)))

        f=open("kk.txt","w")
        f.write(p1+p2+t_string+p3)
        f.close()
        showbill['state']='normal'
        showbill.delete("1.0","end")
        showbill.insert(INSERT,(p1+p2+t_string+p3))
        showbill['state']='disabled'
        show_frame(f_showbill)

        
        cleardbill()
        es_bill.delete(0,END)
        global additemcount,bill_list
        additemcount=1
        bill_list=[]
    
    def grandtot():
        tot=0.00
        
        for i in bill_table.get_children():

            val=bill_table.item(i,"values")
            tot+=float(val[6])
        d_e8['state']='normal'

        d_e8.delete(0,END)
        d_e8.insert(0,tot)
        d_e8['state']='readonly'
        return tot

    def del_item():
        global bill_list
        x=bill_table.selection()
        for record in x:
            v=bill_table.item(record,"values")
            bill_list.remove(v[0])
            bill_table.delete(record)
        update_bill_table()
        
    def search_bill(e):
        typed=es_bill.get()

        sbill_table.tag_configure("oddrow",background="white")
        sbill_table.tag_configure("evenrow",background="plum")
        l=["evenrow","oddrow"]

        for record in sbill_table.get_children():
            sbill_table.delete(record)

        cur.execute("select* from stocks where med_name like "+'"'+typed+"%"+'"'+"and expiry>now() and amt>0 order by med_name")
        tabledata=cur.fetchall()
        i=0
        for  row in tabledata: 
            i=i+1
            sbill_table.insert("",index=END,values=(row[0],row[1]),tags=(l[i%2],))

    def cleardbill():
        for i in [d_e0,d_e1,d_e2,d_e3,d_e4,d_e6]:
            i['state']='normal'
        d_e0.delete(0,END)
        d_e1.delete(0,END)
        d_e2.delete(0,END)
        d_e3.delete(0,END)
        d_e4.delete(0,END)
        d_e5.delete(0,END)
        d_e6.delete(0,END)
        for i in [d_e0,d_e1,d_e2,d_e3,d_e4,d_e6]:
            i['state']='readonly'

    def select_sbill(e):
        cleardbill()
        selected=sbill_table.focus()
        values=sbill_table.item(selected,"values")
        if len(values)!=0:
            cur.execute("select * from stocks where med_id="+"'"+values[0]+"'")

            d=cur.fetchone()
        
            for i in [d_e0,d_e1,d_e2,d_e3,d_e4,d_e6]:
                i['state']='normal'
            d_e0.insert(0,d[0])
            d_e1.insert(0,d[1])
            d_e2.insert(0,d[5])
            d_e3.insert(0,d[3])
            d_e4.insert(0,d[4])

            for i in [d_e0,d_e1,d_e2,d_e3,d_e4,d_e6]:
                i['state']='readonly'
            d_e5.focus()
    def d_e5check(e):
        global bill_list
        d_e6['state']='normal'

        if d_e5.get().isdigit()==True and d_e0.get().isdigit()==True:


            cur.execute("select amt,price from stocks where med_id="+"'"+d_e0.get()+"'")
            d=cur.fetchone()
            k=int(d[0])
            if int(d_e5.get())>k and d_e0.get() not in bill_list:
                messagebox.showerror("","only "+str(k)+" units available")
                d_e5.delete(0,END)
                d_e5.insert(0,k)
                d_e6.delete(0,END)
                d_e6.insert(0,int(d_e5.get())*d[1])
            else:
                
                d_e6.delete(0,END)
                d_e6.insert(0,int(d_e5.get())*d[1])
            if d_e0.get() in bill_list:
                sum=0
                for i in bill_table.get_children():
                    vv=bill_table.item(i,'values')
                    if d_e0.get()==vv[0]:
                        sum+=int(vv[5])
                if int(d_e5.get())>(k-sum):
                    messagebox.showerror("","only "+str(k-sum)+" units available")
                    d_e5.delete(0,END)
                    d_e5.insert(0,k-sum)
                    d_e6.delete(0,END)
                    d_e6.insert(0,int(d_e5.get())*d[1])
                else:
                
                    d_e6.delete(0,END)
                    d_e6.insert(0,int(d_e5.get())*d[1]) 

        else:
            if len(d_e5.get())!=0:
                 messagebox.showerror("","invalid Qty.")
                 d_e5.delete(0,END)

            else:
                d_e6.delete(0,END)
        d_e6['state']='readonly'

    def update_bill_table():
        global additemcount
        additemcount=1
        l=["evenrow","oddrow"]
        bill_table.tag_configure("oddrow",background="white")
        bill_table.tag_configure("evenrow",background="thistle")
        for i in bill_table.get_children():
            bill_table.set(i,'#2',additemcount)
            bill_table.item(i,tags=(l[additemcount%2],))
            additemcount+=1
        grandtot()

    
    def additem():
        l=["evenrow","oddrow"]
        bill_table.tag_configure("oddrow",background="white")
        bill_table.tag_configure("evenrow",background="thistle")
        global additemcount,bill_list
        if (d_e5.get()).isdigit()==True and (d_e0.get().isdigit()==True):
            if int(d_e5.get())!=0:
                bill_table.insert("",index=END,values=(d_e0.get(),additemcount,d_e1.get(),d_e3.get(),d_e4.get(),d_e5.get(),d_e6.get()),tags=(l[additemcount%2],))
                additemcount+=1
                bill_list.append(d_e0.get())
                cleardbill()
                es_bill.focus()

        grandtot()

    def de5foc(e):
        additem()

    def buttonstyle(nom):
        nom['bg']='navyblue'
        for b in [b1,b2,b3,b4]:
            if b!=nom:
                b['bg']="#2a57de"


    def search_view(e):
        search_view1()

    def search_view1():
        l=["evenrow","oddrow"]
        typed=e_search.get()
        ch_=choice_table.get()

        clearview_table()
        
        if typed=="":

            if ch_=="All":
                update_table()
            elif ch_=="Expired Medicine":
                cur.execute("select* from stocks where expiry < now() order by expiry desc")
                tabledata=cur.fetchall()
                i=0
                for  row in tabledata: 
                    i=i+1
                    table.insert("",index=END,values=(i,row[0],row[1],row[3],row[5],row[2],row[4]),tags=(l[i%2],))

            elif ch_=="Valid Medicine":
                cur.execute("select* from stocks where expiry > now() order by med_name")
                tabledata=cur.fetchall()
                i=0
                for  row in tabledata: 
                    i=i+1
                    table.insert("",index=END,values=(i,row[0],row[1],row[3],row[5],row[2],row[4]),tags=(l[i%2],))
            
        else:
            if  ch_=="All":
                cur.execute("select* from stocks where med_name like "+'"'+typed+"%"+'"'+"order by med_name")
                tabledata=cur.fetchall()
                i=0
                for  row in tabledata:
                    i=i+1
                    table.insert("",index=END,values=(str(i),row[0],row[1],row[3],row[5],row[2],row[4]),tags=(l[i%2],))
                
            elif ch_=="Expired Medicine":
                cur.execute("select* from stocks where expiry < now() and med_name like "+'"'+typed+"%"+'"'+"order by med_name")
                tabledata=cur.fetchall()
                i=0
                for  row in tabledata: 
                    i=i+1
                    table.insert("",index=END,values=(i,row[0],row[1],row[3],row[5],row[2],row[4]),tags=(l[i%2],))
                
            elif ch_=="Valid Medicine":
                cur.execute("select* from stocks where expiry > now() and med_name like "+'"'+typed+"%"+'"'+"order by med_name")
                tabledata=cur.fetchall()
                i=0
                for  row in tabledata: 
                    i=i+1
                    table.insert("",index=END,values=(i,row[0],row[1],row[3],row[5],row[2],row[4]),tags=(l[i%2],))
            

    def choice_view(event):
        ch=choice_table.get()
        l=["evenrow","oddrow"]
        clearview_table()
        
        if ch=="All":
            update_table()
        elif ch=="Expired Medicine":
            cur.execute("select* from stocks where expiry < now() order by expiry desc")
            tabledata=cur.fetchall()
            i=0
            for  row in tabledata: 
                i=i+1
                table.insert("",index=END,values=(i,row[0],row[1],row[3],row[5],row[2],row[4]),tags=(l[i%2],))
       
        elif ch=="Valid Medicine":
            cur.execute("select* from stocks where expiry > now() order by med_name")
            tabledata=cur.fetchall()
            i=0
            for  row in tabledata: 
                i=i+1
                table.insert("",index=END,values=(i,row[0],row[1],row[3],row[5],row[2],row[4]),tags=(l[i%2],))
        search_view1()

    def clearview_table():
        for record in table.get_children():
            table.delete(record)
    
    def update_table():
        
        clearview_table()
        l=("evenrow","oddrow")
        
        cur.execute("select* from stocks order by med_name")
        tabledata=cur.fetchall()
        i=0
        for  row in tabledata: 
            i=i+1
            table.insert("",index=END,values=(i,row[0],row[1],row[3],row[5],row[2],row[4]),tags=(l[i%2],))

    def table_insert_update(e):
        reset_update()
        selected=table.focus()
        values=table.item(selected,"values")
        if True and len(values)!=0:
            e1u.insert(0,values[1])
            e2u.insert(0,values[2])
            e3u.insert(0,values[5])
            e4u.insert(0,values[3])
            e5u.insert(0,values[6])
            e6u.insert(0,values[4])

    def reset_update():
        e1u.delete(0,END)
        e2u.delete(0,END)
        e3u.delete(0,END)
        e4u.delete(0,END)
        e5u.delete(0,END)
        e6u.delete(0,END)

    def search_update():
        k=e1u.get()
        if e1u.get()!=None:
            if e1u.get().isdigit()==True:
                cur.execute("select* from stocks where med_id='"+e1u.get()+"'")
                data=cur.fetchone()
                if data==None:
                    
                    bad['image']=img_
                    bad.after(800,laugh)
                    messagebox.showerror("","Data does not exist\nPlease add it first")
    
                else:
                    reset_update()
                    e1u.insert(0,k)
                    e2u.insert(0,data[1])
                    e3u.insert(0,data[2])
                    e4u.insert(0,data[3])
                    e5u.insert(0,data[4])
                    e6u.insert(0,data[5])
            else:
                messagebox.showerror("ID Error","please enter a valid numeric id")
                bad['image']=img_
                bad.after(100,laugh)

        else:
            messagebox.showerror("ID Error","please enter a valid numeric id")
    
    def reset_add():
        e1.delete(0,END)
        e2.delete(0,END)
        e3.delete(0,END)
        e4.delete(0,END)
        e5.delete(0,END)
        e6.delete(0,END)

    def laugh():
        bad['image']=img

    def update_med():
        if e1u.get()!=None:
            if e1u.get().isdigit()==True:
                cur.execute("select med_id from stocks where med_id=%s",((e1u.get()),))
        else:
            messagebox.showerror("","please enter a numeric code")
        
        if '' in (e1u.get(),e2u.get(),e3u.get(),e4u.get(),e5u.get(),e6u.get()):
            messagebox.showerror("","one or more fields empty")
            
        elif cur.fetchone()==None:
            messagebox.showerror("ID Error","Data does not exist\nPlease add it first")
            
            reset_update()
        
        elif e1u.get().isdigit()==False:
            messagebox.showerror("","please enter a numeric code")
        elif e1u.get().isdigit()==False:
            messagebox.showerror("","please enter a numeric value")
        elif e3u.get().isdigit()==False:
            messagebox.showerror("","please enter a numeric value")
        elif e6u.get().isdigit()==False:
            messagebox.showerror("","please enter a numeric value")
        elif check_float(e5u.get())==False:
            messagebox.showerror("","please enter a numeric value")
        elif check_date(e4u.get())==False:
            messagebox.showerror("","Invalid Date Format")
            
        else :
            cur.execute("delete from stocks where med_id=%s",(e1u.get().strip(),))
            cur.execute("insert into stocks values(%s,%s,%s,%s,%s,%s)",(e1u.get().strip(),
                e2u.get().lower().strip(),int(e3u.get().strip()),e4u.get().strip(),
                float(e5u.get().strip()),int(e6u.get().strip())))
            mycon.commit()
            reset_update()
            e1u.focus()

    def delete_med():
        if e1u.get()!=None:
            if e1u.get().isdigit()==True:
                cur.execute("select med_id from stocks where med_id=%s",((e1u.get()),))
        else:
            messagebox.showerror("","please enter a numeric code")
        
        if '' in (e1u.get(),e2u.get(),e3u.get(),e4u.get(),e5u.get(),e6u.get()):
            messagebox.showerror("","one or more fields empty")
            
        elif cur.fetchone()==None:
            messagebox.showerror("","Data does not exist\nPlease add it first")
            reset_update()
        
        elif e1u.get().isdigit()==False:
            messagebox.showerror("","please enter a numeric code")
        elif e1u.get().isdigit()==False:
            messagebox.showerror("","please enter a numeric value")
        elif e3u.get().isdigit()==False:
            messagebox.showerror("","please enter a numeric value")
        elif e6u.get().isdigit()==False:
            messagebox.showerror("","please enter a numeric value")
        elif check_float(e5u.get())==False:
            messagebox.showerror("","please enter a numeric value")
        elif check_date(e4u.get())==False:
            messagebox.showerror("","Invalid Date Format")
        else :
            cur.execute("delete from stocks where med_id=%s",(e1u.get().strip(),))
            mycon.commit()
            reset_update()

    def add_med():
        if e1.get()!=None:
            if e1.get().isdigit()==True:
                cur.execute("select med_id from stocks where med_id=%s",((e1.get()),))
        else:
            messagebox.showerror("","please enter a numeric code")

        if '' in (e1.get(),e2.get(),e3.get(),e4.get(),e5.get(),e6.get()):
            messagebox.showerror("","one or more fields empty")
            
        elif cur.fetchone()!=None:
            messagebox.showerror("","Data already exists,Please add new data")
            reset_add()
        
        elif e1.get().isdigit()==False:
            messagebox.showerror("ID Error","please enter a numeric code")
            e1.focus()
        elif e3.get().isdigit()==False:
            messagebox.showerror("","please enter a numeric value")
        elif e6.get().isdigit()==False:
            messagebox.showerror("","please enter a numeric value")
        elif check_float(e5.get())==False:
            messagebox.showerror("","please enter a numeric value")
        elif check_date(e4.get())==False:
            messagebox.showerror("","Invalid Date Format\n  YYYY-MM-DD")
            e4.focus()
        else :
            cur.execute("insert into stocks values(%s,%s,%s,%s,%s,%s)",(e1.get().strip(),e2.get().lower().strip(),int(e3.get().strip()),e4.get().strip(),float(e5.get().strip()),int(e6.get().strip())))
            mycon.commit()
            reset_add()
            e1.focus()        
        
    def show_frame(frame):
        hide_all_fr()
        frame.pack(fill=BOTH,expand=1)
    
    def hide_all_fr():
        f_x.pack_forget()
        f_add.pack_forget()
        f_view.pack_forget()
        f_update.pack_forget()
        f_bill.pack_forget()
        f_showbill.pack_forget()

    def DESTROY():
        mycon.close()
        root.destroy()


    frame=LabelFrame(root,borderwidth=0)
    frame.pack(fill=Y,side="left")

    #image
    img=ImageTk.PhotoImage(Image.open("pharma\\r11.png"))
    img_=ImageTk.PhotoImage(Image.open("pharma\\troll-face.png"))


    #admin button
    bad=Button(frame,borderwidth=0,image=img,bg="#2a57de",font=("Calibri",15),fg="White")
    bad.pack(fill="both",expand=True)


    #buttons        
    b1=Button(frame,borderwidth=0,text="View Stock",bg="#2a57de",font=("Calibri",16,"bold"),fg="White",command=lambda:[show_frame(f_view),search_view1(),buttonstyle(b1),e_search.focus()])
    b1.pack(fill="both",expand=True)
    b2=Button(frame,borderwidth=0,text="ADD Medicine",bg="#2a57de",font=("Calibri",16,"bold"),fg='White',command=lambda:[show_frame(f_add),buttonstyle(b2),e1.focus()])
    b2.pack(fill=BOTH,expand=True)
    b3=Button(frame,borderwidth=0,text="Update Stock",bg="#2a57de",font=("Calibri",16,"bold"),fg='White',command=lambda:[show_frame(f_update),buttonstyle(b3),e1u.focus()])
    b3.pack(fill=BOTH,expand=True)
    b4=Button(frame,borderwidth=0,text="Generate BILL",bg="#2a57de",font=("Calibri",16,"bold"),fg='White',command=lambda:[show_frame(f_bill),es_bill.focus(),buttonstyle(b4)])
    b4.pack(fill=BOTH,expand=True)
    b5=Button(frame,borderwidth=0,text="Log OUT",bg="#171010",font=("Calibri",16,"bold"),fg='White',command=DESTROY)
    b5.pack(fill=BOTH,expand=True)

    f_x=LabelFrame(root,borderwidth=0)
    Label(f_x,text="Made by  -",font=("Segoe UI",30,"italic"),fg="lightgray",anchor="s").grid(row=0,column=0,sticky="s",pady=220,ipady=10)
    Label(f_x,text="  Aditya Prabhakar",font=("Segoe UI",45,"italic"),fg="silver").grid(row=0,column=1,sticky="w",pady=170)
    f_x.pack()

    f_showbill=LabelFrame(root,borderwidth=0)
    showbill=Text(f_showbill,font=("consolas",13),state="disabled")
    showbill.pack(expand=1,fill=BOTH,pady=10,padx=10)
    
#===========f_add===========#

    f_add=LabelFrame(root,borderwidth=0,bg="navajowhite")

    #ID
    f_add1=LabelFrame(f_add,borderwidth=0,bg="navajowhite")
    l1=Label(f_add1,text="ID:                        ",font=("Calibri",15,"bold"),bg="navajowhite")
    l1.grid(row=0,column=0,padx=22,pady=20,sticky="nsew")
    
    e1=Entry(f_add1,width=20,font=("Calibri",15,"bold"))
    e1.grid(row=0,column=1,pady=20,sticky="nsew")

    f_add1.pack(expand=1,fill=BOTH,side=TOP)
    
    #med name
    f_add2=LabelFrame(f_add,borderwidth=0,bg="navajowhite")
    
    l2=Label(f_add2,text="Medicine Name:",font=("Calibri",15,"bold"),bg="navajowhite")
    l2.grid(row=0,column=0,padx=15,pady=20,sticky="nsew")

    e2=Entry(f_add2,width=20,font=("Calibri",15,"bold"))
    e2.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")

    f_add2.pack(expand=1,fill=BOTH,side=TOP)

    #units
    f_add3=LabelFrame(f_add,borderwidth=0,bg="navajowhite")

    l3=Label(f_add3,text="No. of Units:    ",font=("Calibri",15,"bold"),bg="navajowhite")
    l3.grid(row=0,column=0,padx=20,pady=20,sticky="nsew")

    e3=Entry(f_add3,width=20,font=("Calibri",15,"bold"))
    e3.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")

    f_add3.pack(expand=1,fill=BOTH,side=TOP)

    #exp date
    f_add4=LabelFrame(f_add,borderwidth=0,bg="navajowhite")
    l4=Label(f_add4,anchor=W,text="Expiry Date:     \n(YYYY-MM-DD)",font=("Calibri",15,"bold"),bg="navajowhite")
    l4.grid(row=0,sticky="w",column=0,padx=20,pady=20,)

    e4=Entry(f_add4,width=20,font=("Calibri",15,"bold"))
    e4.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")

    f_add4.pack(expand=1,fill=BOTH,side=TOP)
    #price
    f_add5=LabelFrame(f_add,borderwidth=0,bg="navajowhite")
    
    l5=Label(f_add5,text="Price per unit:  ",font=("Calibri",15,"bold"),bg="navajowhite")
    l5.grid(row=0,column=0,padx=20,pady=20,sticky="nsew")
    
    e5=Entry(f_add5,width=20,font=("Calibri",15,"bold"))
    e5.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")
    f_add5.pack(expand=1,fill=BOTH,side=TOP)
    #lot no.
    f_add6=LabelFrame(f_add,borderwidth=0,bg="navajowhite")
    l6=Label(f_add6,text="Lot No.:             ",font=("Calibri",15,"bold"),bg="navajowhite")
    l6.grid(row=0,column=0,padx=20,pady=20,sticky="nsew")
    e6=Entry(f_add6,width=20,font=("Calibri",15,"bold"))

    def e6foc(e):
        add_med()

    e6.bind("<Return>",e6foc)

    e6.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")
    f_add6.pack(expand=1,fill=BOTH,side=TOP)
    #confirm entry button
    addbutton=Button(f_add,bg="#5bc236",text="Confirm Entry",font=("Calibri",15,"bold underline"),command=add_med)
    addbutton.pack(expand=1,side=RIGHT,fill=X)
    
    #reset button
    reb=Button(f_add,bg="#5bc236",font=("Calibri",15,"bold underline"),text="RESET",command=reset_add)
    reb.pack(expand=1,side=RIGHT,fill=X)

#--------------frame view ------------#
    f_view=LabelFrame(root,borderwidth=0,bg="navajowhite")

    #style
    style=ttk.Style()
    style.theme_use("winnative")
    
    style.configure("Treeview.Heading",background="purple",font=('calibri', 12),foreground="white")
    
    style.configure("Treeview",
                    background="whitesmoke",
                    foreground="black",
                    fieldbackground="whitesmoke",
                    font=('calibri', 11)
                    )
    style.map("Treeview",
              background=[('selected','green')])

    f_view1=LabelFrame(f_view,borderwidth=0,bg="darksalmon")

    option_table=("All",
                  'Expired Medicine',
                  'Valid Medicine')                  

    choice_table=ttk.Combobox(f_view1,state="readonly",value=option_table,font=("Calibri",13))
    choice_table.current(0)
    choice_table.bind("<<ComboboxSelected>>",choice_view)
    choice_table.pack(side=RIGHT,expand=1)

    e_search=Entry(f_view1,width=40,font=("Calibri",15,"bold underline"))
    e_search.bind("<KeyRelease>",search_view)
    e_search.pack(side=RIGHT)

    view_search_label=Label(f_view1,text="Search:",font=("Calibri",13,"italic"),bg="darksalmon")
    view_search_label.pack(side=RIGHT,padx=20)

    f_view1.pack(expand=1,fill=X,side=TOP)

    table_view_frame=Frame(f_view,bg="moccasin")

    table_scroll=Scrollbar(table_view_frame)
    table_scroll.pack(side=RIGHT,fill=Y)

     # table data
    table=ttk.Treeview(table_view_frame,yscrollcommand=table_scroll.set,selectmode="browse")
    table["columns"]=("S.no.","ID",'Medicine Name','Expiry Date',"Lot No.",'No. of Units',"Price")
    table.column("#0",minwidth=0,width=0,stretch=NO)
    table.column('S.no.',anchor=W,minwidth=40,width=40)
    table.column('ID',anchor=W,minwidth=150,width=150)
    table.column('Medicine Name',anchor=CENTER,minwidth=250,width=250,)
    table.column('Expiry Date',anchor=CENTER,minwidth=160,width=160)
    table.column('Lot No.',anchor=CENTER,minwidth=100,width=100)
    table.column('No. of Units',minwidth=130,width=130,anchor=CENTER)
    table.column('Price',minwidth=150,width=150,anchor=CENTER)

    table_scroll.config(command=table.yview)

    # headings
    table.heading("#0",text="",anchor=W)
    table.heading('S.no.',text='S.no.')
    table.heading('ID',text='ID')
    table.heading('Medicine Name',anchor=CENTER,text='Medicine Name')
    table.heading('Expiry Date',anchor=CENTER,text='Expiry Date')
    table.heading('Lot No.',anchor=CENTER,text='Lot No.')
    table.heading('No. of Units',anchor=CENTER,text='No. of Units',)
    table.heading('Price',text='₹ Price')

    table.bind("<ButtonRelease-1>",table_insert_update)

    table.tag_configure("oddrow",background="white")
    table.tag_configure("evenrow",background="thistle")
        
    table.pack(expand=1,fill=BOTH,side=BOTTOM,padx=10,pady=10)

    table_view_frame.pack(expand=1,fill=BOTH,side=BOTTOM)

#=====================frame update=====================
    
    f_update=LabelFrame(root,borderwidth=0,bg="navajowhite")

    #ID
    f_u1=LabelFrame(f_update,borderwidth=0,bg="navajowhite")
    l1u=Label(f_u1,text="ID:                        ",font=("Calibri",15,"bold"),bg="navajowhite")
    l1u.grid(row=0,column=0,padx=22,pady=20,sticky="nsew")
    
    e1u=Entry(f_u1,width=20,font=("Calibri",15,"bold"))
    e1u.grid(row=0,column=1,pady=20,sticky="nsew")
    def e1ufoc(e):
        search_update()
    e1u.bind("<Return>",e1ufoc)

    #search button
    su_btn=Button(f_u1,font=("Calibri",12,"bold italic"),text="search",command=search_update,borderwidth=1,bg="#24a0ed",fg="white")
    su_btn.grid(row=0,column=2,ipady=1,padx=5)

    f_u1.pack(expand=1,fill=BOTH,side=TOP)

    #med name
    f_u2=LabelFrame(f_update,borderwidth=0,bg="navajowhite")
    
    l2u=Label(f_u2,text="Medicine Name:",font=("Calibri",15,"bold"),bg="navajowhite")
    l2u.grid(row=0,column=0,padx=15,pady=20,sticky="nsew")

    e2u=Entry(f_u2,width=20,font=("Calibri",15,"bold"))
    e2u.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")

    f_u2.pack(expand=1,fill=BOTH,side=TOP)

    #units
    f_u3=LabelFrame(f_update,borderwidth=0,bg="navajowhite")

    l3u=Label(f_u3,text="No. of Units:    ",font=("Calibri",15,"bold"),bg="navajowhite")
    l3u.grid(row=0,column=0,padx=20,pady=20,sticky="nsew")

    e3u=Entry(f_u3,width=20,font=("Calibri",15,"bold"),)
    e3u.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")

    f_u3.pack(expand=1,fill=BOTH,side=TOP)

    #exp date
    f_u4=LabelFrame(f_update,borderwidth=0,bg="navajowhite")
    l4u=Label(f_u4,anchor=W,text="Expiry Date:     \n(YYYY-MM-DD)",font=("Calibri",15,"bold"),bg="navajowhite")
    l4u.grid(row=0,sticky="w",column=0,padx=20,pady=20,)

    e4u=Entry(f_u4,width=20,font=("Calibri",15,"bold"))
    e4u.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")

    f_u4.pack(expand=1,fill=BOTH,side=TOP)
    #price
    f_u5=LabelFrame(f_update,borderwidth=0,bg="navajowhite")
    
    l5u=Label(f_u5,text="Price per unit:  ",font=("Calibri",15,"bold"),bg="navajowhite")
    l5u.grid(row=0,column=0,padx=20,pady=20,sticky="nsew")
    
    e5u=Entry(f_u5,width=20,font=("Calibri",15,"bold"))
    e5u.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")
    f_u5.pack(expand=1,fill=BOTH,side=TOP)
    #lot no.
    f_u6=LabelFrame(f_update,borderwidth=0,bg="navajowhite")
    l6u=Label(f_u6,text="Lot No.:             ",font=("Calibri",15,"bold"),bg="navajowhite")
    l6u.grid(row=0,column=0,padx=20,pady=20,sticky="nsew")
    e6u=Entry(f_u6,width=20,font=("Calibri",15,"bold"))
    e6u.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")
    f_u6.pack(expand=1,fill=BOTH,side=TOP)
    #confirm entry button
    update_button=Button(f_update,bg="#5bc236",text="Update",font=("Calibri",15,"bold underline"),command=update_med)
    update_button.pack(expand=1,side=RIGHT,fill=X)

    #delete button
    del_btn=Button(f_update,bg="red",text="DELETE",font=("Calibri",15,"bold underline"),command=delete_med)
    del_btn.pack(expand=1,side=RIGHT,fill=X)
    
    #reset button
    rebu=Button(f_update,bg="#5bc236",font=("Calibri",15,"bold underline"),text="RESET",command=reset_update)
    rebu.pack(expand=1,side=RIGHT,fill=X)


#=============BILL Frame===========

    f_bill=LabelFrame(root,borderwidth=0,bg="navajowhite")


    #search bill frame=================>
    f_bill_search=LabelFrame(f_bill,borderwidth=0,bg="darksalmon")
    


    bill_search_label=Label(f_bill_search,text="Search:",font=("Calibri",13,"italic"),bg="darksalmon")
    bill_search_label.pack(fill=X)

    es_bill=Entry(f_bill_search,width=20,font=("Calibri",13))
    es_bill.bind("<KeyRelease>",search_bill)
    es_bill.pack(padx=7,side=TOP,anchor=W)

    s_bill_frame=Frame(f_bill_search,bg="darksalmon")

    sbill_scroll=Scrollbar(s_bill_frame)
    sbill_scroll.pack(side=RIGHT,fill=Y)

     # table data
    sbill_table=ttk.Treeview(s_bill_frame,yscrollcommand=sbill_scroll.set,selectmode=BROWSE,show="tree")
    sbill_table["columns"]=("med_id",'Medicine Name')
    sbill_table.column("#0",minwidth=0,width=0,stretch=NO)
    sbill_table.column('med_id',anchor=W,minwidth=0,width=0,stretch=NO)
    sbill_table.column('Medicine Name',anchor=W,minwidth=180,width=180,)

    sbill_scroll.config(command=sbill_table.yview)

    # headings
    sbill_table.heading("#0",text="",anchor=W)
    sbill_table.heading('Medicine Name',anchor=CENTER,text='')
    sbill_table.heading('med_id',anchor=CENTER,text='')

    sbill_table.pack(expand=1,fill=BOTH,side=BOTTOM,padx=5,pady=5)

    sbill_table.bind("<ButtonRelease-1>",select_sbill)

    s_bill_frame.pack(expand=1,fill=Y,side=BOTTOM)

    f_bill_search.pack(fill=Y,side="left")


    #bill ,price , quantity frame=================

    d_bill=LabelFrame(f_bill,bg="navajowhite",borderwidth=0)


    d_e0=Entry(d_bill,font=("Calibri",13,"italic"),state='readonly')

    d_l1=Label(d_bill,text="Medicine Name:",font=("Calibri",13,"italic"),anchor=W,bg="bisque")
    d_e1=Entry(d_bill,state='readonly',font=("Calibri",13,"italic"))

    d_l1.grid(row=0,column=0,sticky="w",padx=7,pady=7)
    d_e1.grid(row=0,column=1,padx=7,pady=7)

    d_l2=Label(d_bill,text="Lot No.:",font=("Calibri",13,"italic"),bg="bisque")
    d_e2=Entry(d_bill,state='readonly',font=("Calibri",13,"italic"))

    d_l2.grid(row=1,column=0,sticky="w",padx=7,pady=7)
    d_e2.grid(row=1,column=1,padx=7,pady=7)

    d_l3=Label(d_bill,text="Exp. Date:",font=("Calibri",13,"italic"),bg="bisque")
    d_e3=Entry(d_bill,state='readonly',font=("Calibri",13,"italic"))

    d_l3.grid(row=2,column=0,sticky="w",padx=7,pady=7)
    d_e3.grid(row=2,column=1,padx=7,pady=7)

    d_l4=Label(d_bill,text="₹ Price/unit:",font=("Calibri",13,"italic"),bg="bisque")
    d_e4=Entry(d_bill,state='readonly',font=("Calibri",13,"italic"))

    d_l4.grid(row=0,column=2,sticky=W,padx=10,pady=7)
    d_e4.grid(row=0,column=3,padx=7,pady=7)

    d_l5=Label(d_bill,text="Qty:",font=("Calibri",13,"italic"),bg="bisque")
    d_e5=Entry(d_bill,font=("Calibri",13,"italic"))

    d_e5.bind("<KeyRelease>",d_e5check)
    d_e5.bind("<Return>",de5foc)

    d_l5.grid(row=1,column=2,sticky="w",padx=10,pady=7)
    d_e5.grid(row=1,column=3,padx=7,pady=7)

    d_l6=Label(d_bill,text="Total Price:",font=("Calibri",13,"italic"),bg="bisque")
    d_e6=Entry(d_bill,state='readonly',font=("Calibri",13,"bold italic"),bg="silver",fg="firebrick")

    d_l6.grid(row=2,column=2,sticky="w",padx=10,pady=7)
    d_e6.grid(row=2,column=3,padx=7,pady=7)

    #add to cart ==========================
    ab_btn=Button(d_bill,font=("Calibri",13,"italic"),text="Add to Cart",borderwidth=1,bg="#24a0ed",command=additem)
    ab_btn.grid(row=3,column=4,ipady=1,padx=5)

    #billing table=======================

    bill_table_frame=Frame(d_bill,bg="moccasin")

    bill_table_scroll=Scrollbar(bill_table_frame)
    bill_table_scroll.pack(side=RIGHT,fill=Y)
    bill_table_scrollx=Scrollbar(bill_table_frame,orient="horizontal")
    bill_table_scrollx.pack(side=BOTTOM,fill=X,padx=5,pady=5)

     # table data
    bill_table=ttk.Treeview(bill_table_frame,yscrollcommand=bill_table_scroll.set,xscrollcommand=bill_table_scrollx.set,selectmode="extended")
    bill_table["columns"]=("ID","S.no.",'Medicine Name','Expiry Date',"Price","No. of Units","Total Price")
    bill_table.column("#0",minwidth=0,width=0,stretch=NO)

    bill_table.column("ID",minwidth=0,width=0,stretch=NO)
    bill_table.column('S.no.',anchor=W,minwidth=30,width=40)

    bill_table.column('Medicine Name',anchor=CENTER,minwidth=250,width=250,)
    bill_table.column('Expiry Date',anchor=CENTER,minwidth=100,width=120)
    
    bill_table.column('Price',minwidth=100,width=100,anchor=CENTER)
    bill_table.column('No. of Units',minwidth=70,width=100,anchor=CENTER)
    bill_table.column('Total Price',minwidth=100,width=150,anchor=CENTER)

    bill_table_scroll.config(command=bill_table.yview)
    bill_table_scrollx.config(command=bill_table.xview)

    # headings
    bill_table.heading('S.no.',text='S.no.',)
    
    bill_table.heading('Medicine Name',anchor=CENTER,text='Medicine Name')
    bill_table.heading('Expiry Date',anchor=CENTER,text='Expiry Date')
    
    bill_table.heading('Price',text='₹ Price')
    bill_table.heading('No. of Units',anchor=CENTER,text='Qty.',)
    bill_table.heading('Total Price',anchor=CENTER,text='Total Price',)

    bill_table.pack(expand=1,fill=BOTH,side=BOTTOM,padx=10)

    bill_table_frame.grid(sticky="nsew",columnspan=11,pady=20,padx=5,column=0,row=4)
    Grid.rowconfigure(d_bill,4,weight=4)

    #delete bill item button

    del_btn=Button(d_bill,font=("Calibri",15,"italic"),text="Delete Item",borderwidth=1,bg="red",fg="white",command=del_item)
    del_btn.grid(row=5,column=0,padx=3,sticky="n",pady=7)

    #grand total
    d_l7=Label(d_bill,text="Grand TOTAL:",font=("Helvetica",15,"bold italic underline"),bg="yellow")
    d_l7.grid(row=5,column=1,sticky="e",padx=0,pady=7)
    
    d_e8=Entry(d_bill,font=("Segoe UI",15,"bold"),bg="bisque",relief="flat",width=12,state="readonly")
    d_e8.grid(row=5,column=2,sticky="w",padx=0,pady=7)
    
    confirm_btn=Button(d_bill,font=("Calibri",15,"italic"),text="Confirm and Pay",borderwidth=1,bg="navyblue",fg="white",command=pay)
    confirm_btn.grid(row=5,column=4,padx=5,sticky="n",pady=7)
    
    d_bill.pack(expand=1,fill=BOTH,side=TOP)
    root.mainloop()

LoginPage()
if allowentry==1:
    launchapp()










