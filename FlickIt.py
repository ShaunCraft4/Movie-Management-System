import tkinter as tk
import mysql.connector as ms
from tabulate import tabulate
import random
import datetime as dt


con=ms.connect(host='localhost',database="Movie",user='root',password="YourMySQLPassword") #Please update with your MySQL password
cur=con.cursor()

time = dt.datetime.now()
current_time = time.strftime("%H:%M:%S")
date=str(dt.date.today())


def DisplayMovies():
    BGText=tk.Text(window,width=195, height=66,bg="Red",highlightbackground="black")
    BGText.place(relx=0.18,rely=0.65,anchor="w")
    MainText=tk.Text(window,width=195, height=45,bg="White",highlightbackground="black",fg="red")
    MainText.place(relx=0.18,rely=0.65,anchor="w")
    Label=tk.Label(text="Displaying Available Movies",bg="Red",fg="White",font=('Helvetica', 50, 'bold'))
    Label.place(relx=0.35,rely=0.2,anchor="w")
    ScrollBar=tk.Scrollbar(window,orient="vertical",command=MainText.yview,cursor="heart")
    MainText["yscrollcommand"]=ScrollBar.set
    MainText.config(state="normal")
    MainText.delete("1.0","end")
    cur.execute("Select * from Movies")
    Movies=(tabulate(cur.fetchall(), headers=['Movie ID', 'Movie Name', "Available Front Seats","Available Middle Seats","Available Back Seats","Total Available Seats","Show Time","Price"],tablefmt='orgtbl'))
    MainText.insert("end",Movies)
    MainText.config(state="disabled")
    BGText.config(state="disabled")


def ViewAllReservations():
    BGText=tk.Text(window,width=195, height=66,bg="Red",highlightbackground="black")
    BGText.place(relx=0.18,rely=0.65,anchor="w")
    MainText=tk.Text(window,width=195, height=45,bg="White",highlightbackground="black",fg="red")
    MainText.place(relx=0.18,rely=0.65,anchor="w")
    Label=tk.Label(text="Displaying All Reservations",bg="Red",fg="White",font=('Helvetica', 51, 'bold'))
    Label.place(relx=0.35,rely=0.2,anchor="w")
    ScrollBar=tk.Scrollbar(window,orient="vertical",command=MainText.yview,cursor="heart")
    MainText["yscrollcommand"]=ScrollBar.set
    MainText.config(state="normal")
    MainText.delete("1.0","end")
    cur.execute("Select * from ReservationList")
    Movies=(tabulate(cur.fetchall(),headers=['Customer ID', 'Customer Name', "Movie Name","Seat Plan","Show Time","Price Paid","Food and Drinks"],tablefmt='orgtbl'))
    MainText.insert("end",Movies)
    MainText.config(state="disabled")
    BGText.config(state="disabled")


def ReserveSeats():
    def SendRS():
        Info_Text.config(state="normal")
        Info_Text.delete("1.0","end")
        try:
                Movie_ID=MovieID_Text.get(1.0, "end-1c")
                NOFS=NOFS_Text.get(1.0, "end-1c")
                NOMS=NOMS_Text.get(1.0, "end-1c")
                NOBS=NOBS_Text.get(1.0, "end-1c")
                Names=Names_Text.get(1.0, "end-1c")
                Names=Names.replace(" ","")
                MovieID_Text.delete("1.0","end")
                NOFS_Text.delete("1.0","end")
                NOMS_Text.delete("1.0","end")
                NOBS_Text.delete("1.0","end")
                Names_Text.delete("1.0","end")
                cur.execute("Select * from Movies where Movie_ID = %s",(Movie_ID,))
                data=cur.fetchmany()
                Movie_Name=data[0][1]
                dom={"Front Seat":data[0][2],"Middle Seat":data[0][3],"Back Seat":data[0][4]}
                tvs=data[0][5]
                time=str(data[0][6])
                time2=time
                time=time.replace(":","")
                price=data[0][7]
                doc={"Front Seat":int(NOFS),"Middle Seat":int(NOMS),"Back Seat":int(NOBS)}
                nor=int(NOFS)+int(NOMS)+int(NOBS)
                NameList=Names.split(",")
                sp=[]
                for i in doc:
                    for j in range(doc[i]):
                        sp.append(i)
                cv=list(doc.values())
                mv=list(dom.values())
                fl=[]
                c=0
                for i in range(len(mv)):
                    if cv[i]<=mv[i]:
                        fl.append(mv[i]-cv[i])
                    else:
                        c+=1
                        break
                custd={}
                if c==0 and len(NameList)==nor:
                    Info_Text.insert("end","Tickets reserved successfully! Please refer to the all reservations tab to find your ticket and for refreshments please refer to the food and drinks tab!"+"\n")
                    for j in range(len(NameList)):
                        while True:
                            c=0
                            cur.execute("Select * from ReservationList")
                            rl=[]
                            for i in cur:
                                  rl.append(i)
                            CID="C"
                            for i in range(3):
                                x=random.randint(0,9)
                                CID+=str(x)
                            for i in rl:
                                if i[0]==CID:
                                    c+=1
                                    break
                            if c==0:
                                    break
                        custd[str(NameList[j])]=str(CID)
                        t=(str(CID),str(NameList[j]),str(Movie_Name), str(sp[j]), str(time), str(price),"None")
                        cur.execute("Insert into ReservationList values(%s,%s,%s,%s,%s,%s,%s)",t)
                        con.commit()
                    for i in range(3):
                        t=(str(fl[i]),str(Movie_ID))
                        if i==0:
                            Query="Update Movies SET Available_Front_Seats = %s where Movie_ID = %s"
                        elif i==1:
                            Query="Update Movies SET Available_Middle_Seats = %s where Movie_ID = %s"
                        elif i==2:
                            Query="Update Movies SET Available_Back_Seats = %s where Movie_ID = %s"
                        cur.execute(Query,t)
                        con.commit()
                    t=(str(tvs-nor),str(Movie_ID))
                    cur.execute("Update Movies SET Total_Available_Seats = %s where Movie_ID = %s",t)
                    Info_Text.insert("end","Please note the following customer IDs for the Movie:"+"\n")
                    for i in custd:
                        Info_Text.insert("end",i+":"+custd[i]+"\n")
                    con.commit()
                else:
                    Info_Text.insert("end","Tickets could not be reserved, please try again!"+"\n")
        except:
                Info_Text.insert("end","Tickets could not be reserved, please try again with appropriate entries!"+"\n")
        Info_Text.config(state="disabled")
    
    MainText=tk.Text(window,width=195, height=66,bg="Red",highlightbackground="black")
    MainText.place(relx=0.18,rely=0.65,anchor="w")
    ScrollBar=tk.Scrollbar(window,orient="vertical",command=MainText.yview,cursor="heart")
    Label=tk.Label(text="Seat Reservation",bg="Red",fg="White",font=('Helvetica', 50, 'bold'))
    Label.place(relx=0.43,rely=0.2,anchor="w")
    MovieID_Label = tk.Label(text="Movie ID:",bg="Red",fg="White",font=('Helvetica', 44, 'bold'))
    MovieID_Label.place(relx=0.27,rely=0.29,anchor="center")
    MovieID_Text=tk.Text(window,width=100, height=4,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    MovieID_Text.place(relx=0.55,rely=0.29,anchor="center")
    NOFS_Label = tk.Label(text="No. of Front seat Reservations:",bg="Red",fg="White",font=('Helvetica', 30, 'bold'))
    NOFS_Label.place(relx=0.35,rely=0.38,anchor="center")
    NOFS_Text=tk.Text(window,width=100, height=5,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    NOFS_Text.place(relx=0.71,rely=0.38,anchor="center")
    NOMS_Label = tk.Label(text="No. of Middle seat Reservations:",bg="Red",fg="White",font=('Helvetica', 28, 'bold'))
    NOMS_Label.place(relx=0.35,rely=0.47,anchor="center")
    NOMS_Text=tk.Text(window,width=100, height=5,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    NOMS_Text.place(relx=0.71,rely=0.47,anchor="center")
    NOBS_Label = tk.Label(text="No. of Back seat Reservations:",bg="Red",fg="White",font=('Helvetica', 30, 'bold'))
    NOBS_Label.place(relx=0.35,rely=0.56,anchor="center")
    NOBS_Text=tk.Text(window,width=100, height=5,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    NOBS_Text.place(relx=0.71,rely=0.56,anchor="center")
    Names_Label = tk.Label(text="Names according to reservations:",bg="Red",fg="White",font=('Helvetica', 28, 'bold'))
    Names_Label.place(relx=0.357,rely=0.65,anchor="center")
    Names_Text=tk.Text(window,width=100, height=5,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    Names_Text.place(relx=0.71,rely=0.65,anchor="center")
    Note_Label = tk.Label(text="(Seperated with comma)",bg="Red",fg="White",font=('Helvetica', 10, 'bold'))
    Note_Label.place(relx=0.357,rely=0.69,anchor="center")
    Info_Text=tk.Text(window,width=215, height=8,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    Info_Text.place(relx=0.59,rely=0.79,anchor="center")
    Info_Text.config(state="disabled")
    SendButtonRS=tk.Button(text="Send",width=100,height=3,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=SendRS)
    SendButtonRS.place(relx=0.2,rely=0.88)

    
def DeleteSeats():
    def SendDS():
        Info_Text.config(state="normal")
        Info_Text.delete("1.0","end")
        CID=CID_Text.get(1.0, "end-1c")
        CID_Text.delete("1.0","end")
        cur.execute("Select * from ReservationList where Customer_ID = %s", (CID,))
        data=cur.fetchmany()
        if len(data)==0:
            Info_Text.insert("end","Customer ID could not be found")
        else:
            sp=data[0][3]
            mn=data[0][2]
            cur.execute("Select * from Movies where Movie_Name = %s",(mn,))
            data2=cur.fetchmany()
            Movie_ID=data2[0][0]
            if sp=="Front Seat":
                Query2="Update Movies set Available_Front_Seats = Available_Front_Seats + 1 where Movie_ID = %s"
            elif sp=="Middle Seat":
                Query2="Update Movies set Available_Middle_Seats = Available_Middle_Seats + 1 where Movie_ID = %s"
            elif sp=="Back Seat":
                Query2="Update Movies set Available_Back_Seats = Available_Back_Seats + 1 where Movie_ID = %s"
            cur.execute("Delete from ReservationList where Customer_ID = %s",(CID,))
            cur.execute(Query2,(Movie_ID,))
            cur.execute("Update Movies set Total_Available_Seats = Total_Available_Seats + 1 where Movie_ID = %s",(Movie_ID,))
            con.commit()
            Info_Text.insert("end","Ticket reservation has been deleted successfully")
        Info_Text.config(state="disabled")
        
    MainText=tk.Text(window,width=195, height=66,bg="Red",highlightbackground="black")
    MainText.place(relx=0.18,rely=0.65,anchor="w")
    ScrollBar=tk.Scrollbar(window,orient="vertical",command=MainText.yview,cursor="heart")
    Label=tk.Label(text="Seat Deletion",bg="Red",fg="White",font=('Helvetica', 50, 'bold'))
    Label.place(relx=0.43,rely=0.2,anchor="w")
    CID_Label = tk.Label(text="Customer ID:",bg="Red",fg="White",font=('Helvetica', 44, 'bold'))
    CID_Label.place(relx=0.29,rely=0.31,anchor="center")
    CID_Text=tk.Text(window,width=100, height=4,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    CID_Text.place(relx=0.59,rely=0.31,anchor="center")
    SendButtonDS=tk.Button(text="Send",width=100,height=3,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=SendDS)
    SendButtonDS.place(relx=0.2,rely=0.88)
    Info_Text=tk.Text(window,width=215, height=8,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    Info_Text.place(relx=0.59,rely=0.75,anchor="center")
    Info_Text.config(state="disabled")


def ViewSpecficReservation():
    def SendVSR():
        Info_Text.config(state="normal")
        Info_Text.delete("1.0","end")
        CID=CID_Text.get(1.0, "end-1c")
        CID_Text.delete("1.0","end")
        cur.execute("Select * from ReservationList where Customer_ID = %s",(CID,))
        data=cur.fetchmany()
        if len(data)==0:
            c=0
        else:
            c=1
        if c==0:
            Info_Text.insert("end","Customer ID could not be found")
        else:
            Info_Text.insert("end",tabulate(data, headers=['Customer ID', 'Customer Name', "Movie Name","Seat Plan","Show Time","Price Paid","Food and Drinks"],tablefmt='orgtbl'))
        Info_Text.config(state="disabled")
    
    MainText=tk.Text(window,width=195, height=66,bg="Red",highlightbackground="black")
    MainText.place(relx=0.18,rely=0.65,anchor="w")
    ScrollBar=tk.Scrollbar(window,orient="vertical",command=MainText.yview,cursor="heart")
    Label=tk.Label(text="View Specfic Reservation",bg="Red",fg="White",font=('Helvetica', 50, 'bold'))
    Label.place(relx=0.43,rely=0.2,anchor="w")
    CID_Label = tk.Label(text="Customer ID:",bg="Red",fg="White",font=('Helvetica', 44, 'bold'))
    CID_Label.place(relx=0.29,rely=0.31,anchor="center")
    CID_Text=tk.Text(window,width=100, height=4,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    CID_Text.place(relx=0.59,rely=0.31,anchor="center")
    SendButtonDS=tk.Button(text="Send",width=100,height=3,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=SendVSR)
    SendButtonDS.place(relx=0.2,rely=0.88)
    Info_Text=tk.Text(window,width=189, height=8,bg="White",highlightbackground="black",fg="Red")
    Info_Text.place(relx=0.59,rely=0.75,anchor="center")
    Info_Text.config(state="disabled")


def AddRefreshments():
    def SendR():
        try:
            Info_Text.config(state="normal")
            Info_Text.delete("1.0","end")
            Refreshments=Refreshments_Text.get(1.0, "end-1c")
            Refreshments_Text.delete("1.0","end")
            CID=CID_Text.get(1.0, "end-1c")
            CID_Text.delete("1.0","end")
            Refreshments=Refreshments.replace(" ","")
            rl=Refreshments.split(",")
            rp=0
            AvailableRefreshments=[]
            for i in data1:
                AvailableRefreshments.append(i[0].lower())
            for i in rl:
                if i.lower() in AvailableRefreshments:
                    cur.execute("Select Price from Refreshment_Prices where Item=%s",(i,))
                    data2=cur.fetchone()
                    rp+=int(data2[0])
                else:
                    Info_Text.insert("end","Sorry,",i,"is not available"+"\n")
            cur.execute("Select Food_And_Drinks from ReservationList where Customer_ID=%s",(CID,))
            data3=cur.fetchone()
            if "None" in data3[0]:
                cur.execute("Update ReservationList set Food_And_Drinks=%s where Customer_ID=%s",(Refreshments,CID))
            else:
                Refreshments=str(data3[0])+","+Refreshments
                cur.execute("Update ReservationList set Food_And_Drinks=%s where Customer_ID=%s",(Refreshments,CID))
            cur.execute("Update ReservationList set Price_Paid=Price_Paid+%s where Customer_ID=%s",(rp,CID))
            con.commit()
            Info_Text.insert("end","Refreshments were added!")
        except:
            Info_Text.insert("end","Refreshments couldnt be added, please try again with appropriate values!")
        Info_Text.config(state="disabled")
        
    MainText=tk.Text(window,width=195, height=66,bg="Red",highlightbackground="black")
    MainText.place(relx=0.18,rely=0.65,anchor="w")
    ScrollBar=tk.Scrollbar(window,orient="vertical",command=MainText.yview,cursor="heart")
    Label=tk.Label(text="Refreshment Tab",bg="Red",fg="White",font=('Helvetica', 50, 'bold'))
    Label.place(relx=0.43,rely=0.2,anchor="w")
    CID_Label = tk.Label(text="Customer ID:",bg="Red",fg="White",font=('Helvetica', 44, 'bold'))
    CID_Label.place(relx=0.29,rely=0.31,anchor="center")
    CID_Text=tk.Text(window,width=100, height=4,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    CID_Text.place(relx=0.59,rely=0.31,anchor="center")
    Refreshments_Label = tk.Label(text="Refreshments:",bg="Red",fg="White",font=('Helvetica', 44, 'bold'))
    Refreshments_Label.place(relx=0.29,rely=0.42,anchor="center")
    Note_Label = tk.Label(text="(Seperated with comma)",bg="Red",fg="White",font=('Helvetica', 10, 'bold'))
    Note_Label.place(relx=0.29,rely=0.47,anchor="center")
    Refreshments_Text=tk.Text(window,width=100, height=4,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    Refreshments_Text.place(relx=0.59,rely=0.42,anchor="center")
    SendButtonDS=tk.Button(text="Send",width=100,height=3,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=SendR)
    SendButtonDS.place(relx=0.2,rely=0.88)
    RefreshmentInfo=tk.Text(window,width=40, height=30,bg="White",highlightbackground="black",fg="Red")
    RefreshmentInfo.place(relx=0.9,rely=0.40,anchor="center")
    cur.execute("Select * from Refreshment_Prices")
    data1=cur.fetchall()
    RefreshmentInfo.insert("end",tabulate(data1, headers=["Items","Prices"],tablefmt='orgtbl'))
    RefreshmentInfo.config(state="disabled")
    Info_Text=tk.Text(window,width=189, height=8,bg="White",highlightbackground="black",fg="Red")
    Info_Text.place(relx=0.59,rely=0.75,anchor="center")
    Info_Text.config(state="disabled")


def DeleteRefreshments():
    def SendDR():
        try:
            Info_Text.config(state="normal")
            Info_Text.delete("1.0","end")
            CID=CID_Text.get(1.0, "end-1c")
            CID_Text.delete("1.0","end")
            DF=Refreshments_Text.get(1.0, "end-1c")
            Refreshments_Text.delete("1.0","end")
            dfl=DF.split(",")
            cur.execute("Select Food_And_Drinks from ReservationList where Customer_ID=%s",(CID,))
            data1=cur.fetchone()
            rl=data1[0].split(",")
            dl=[]
            for i in dfl:
                if i.title() in rl:
                    rl.remove(i.title())
                    dl.append(i.title())
                else:
                    Info_Text.insert("end",i.title()+" was not bought"+"\n")
            s=""
            if len(rl)==0:
                s+="None"
            else:   
                for i in rl:
                    if i==rl[-1]:
                        s+=i
                    else:
                        s+=i+","
            rp=0
            for i in dl:
                cur.execute("Select Price from Refreshment_Prices where Item=%s",(i.title(),))
                data2=cur.fetchone()
                rp+=int(data2[0])
            cur.execute("Update ReservationList set Price_Paid=Price_Paid-%s where Customer_ID=%s",(rp,CID))
            cur.execute("Update ReservationList set Food_And_Drinks=%s where Customer_ID=%s",(s,CID))
            con.commit()
            Info_Text.insert("end","Appropriate Refreshments were removed")
        except:
            Info_Text.insert("end","Incorrect values given, please try again with appropriate values")
        Info_Text.config(state="disabled")
            
    MainText=tk.Text(window,width=195, height=66,bg="Red",highlightbackground="black")
    MainText.place(relx=0.18,rely=0.65,anchor="w")
    ScrollBar=tk.Scrollbar(window,orient="vertical",command=MainText.yview,cursor="heart")
    Label=tk.Label(text="Delete Refreshment",bg="Red",fg="White",font=('Helvetica', 50, 'bold'))
    Label.place(relx=0.43,rely=0.2,anchor="w")
    CID_Label = tk.Label(text="Customer ID:",bg="Red",fg="White",font=('Helvetica', 44, 'bold'))
    CID_Label.place(relx=0.29,rely=0.31,anchor="center")
    CID_Text=tk.Text(window,width=100, height=4,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    CID_Text.place(relx=0.59,rely=0.31,anchor="center")
    Refreshments_Label = tk.Label(text="Refreshments to be Removed:",bg="Red",fg="White",font=('Helvetica', 25, 'bold'))
    Refreshments_Label.place(relx=0.31,rely=0.42,anchor="center")
    Note_Label = tk.Label(text="(Seperated with comma)",bg="Red",fg="White",font=('Helvetica', 10, 'bold'))
    Note_Label.place(relx=0.29,rely=0.47,anchor="center")
    Refreshments_Text=tk.Text(window,width=100, height=4,bg="White",highlightbackground="black",fg="Red",font=("Helvetica",10,"bold"))
    Refreshments_Text.place(relx=0.62,rely=0.42,anchor="center")
    SendButtonDS=tk.Button(text="Send",width=100,height=3,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=SendDR)
    SendButtonDS.place(relx=0.2,rely=0.88)
    RefreshmentInfo=tk.Text(window,width=40, height=30,bg="White",highlightbackground="black",fg="Red")
    RefreshmentInfo.place(relx=0.9,rely=0.40,anchor="center")
    cur.execute("Select * from Refreshment_Prices")
    data1=cur.fetchall()
    RefreshmentInfo.insert("end",tabulate(data1, headers=["Items","Prices"],tablefmt='orgtbl'))
    RefreshmentInfo.config(state="disabled")
    Info_Text=tk.Text(window,width=189, height=8,bg="White",highlightbackground="black",fg="Red")
    Info_Text.place(relx=0.59,rely=0.75,anchor="center")
    Info_Text.config(state="disabled")


def CloseWindow():
    window.destroy()


window = tk.Tk()
window.geometry("1920x1080")
window.configure(bg="Red")
window.resizable(False,False)

FlickIt = tk.Label(text="FlickIt",bg="Red",fg="White",font=('Ravie', 80, 'bold'))
FlickIt.place(relx=0.5,rely=0.5,anchor="center")
FlickIt.pack() 

MainText=tk.Text(window,width=195, height=66,bg="Red",highlightbackground="black")
MainText.place(relx=0.18,rely=0.65,anchor="w")
MainText.config(state="disabled")
Label=tk.Label(text="Please select a tab to start!",bg="Red",fg="White",font=('Helvetica', 50, 'bold'))
Label.place(relx=0.57,rely=0.54,anchor="center")
DateLabel=tk.Label(text=current_time+"\n"+date,bg="Red",fg="White",font=('Helvetica', 30, 'bold'))
DateLabel.place(relx=0.08,rely=0.07,anchor="center")

DAM=tk.Button(text="Available Movies",width=19,height=2,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=DisplayMovies)
DAM.place(relx=0.08,rely=0.22,anchor="center")
RS=tk.Button(text="Reserve Seats",width=19,height=2,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=ReserveSeats)
RS.place(relx=0.08,rely=0.34,anchor="center")
VSR=tk.Button(text="View Specific Reservation",width=20,height=2,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=ViewSpecficReservation)
VSR.place(relx=0.085,rely=0.46,anchor="center")
VAR=tk.Button(text="View All Reservations",width=19,height=2,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=ViewAllReservations)
VAR.place(relx=0.08,rely=0.58,anchor="center")
DR=tk.Button(text="Delete Reservation",width=19,height=2,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=DeleteSeats)
DR.place(relx=0.08,rely=0.7,anchor="center")
ARe=tk.Button(text="Add Refreshments",width=19,height=2,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=AddRefreshments)
ARe.place(relx=0.08,rely=0.82,anchor="center")
DRe=tk.Button(text="Delete Refreshments",width=19,height=2,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=DeleteRefreshments)
DRe.place(relx=0.08,rely=0.94,anchor="center")
XButton=tk.Button(text="X",width=3,height=1,bg="White",fg="Red",font=("Helvetica",18,"bold"),command=CloseWindow)
XButton.place(relx=0.981, rely=0.03,anchor="center")

CanvasLine1=tk.Canvas(window, width=15000, height=10,bg="Black",highlightbackground="Red",highlightthickness  = 1)
CanvasLine1.place(relx=0.5,rely=0.15,anchor="center")
CanvasLine1.create_line(0, 25, 1000, 25, width=5)
CanvasLine2=tk.Canvas(window, width=10, height=10200,bg="Black",highlightbackground="Red",highlightthickness  = 1)
CanvasLine2.place(relx=0.17,rely=0.15,anchor="center")
CanvasLine2.create_line(0, 50, 1000, 50, width=5)

window.mainloop()
