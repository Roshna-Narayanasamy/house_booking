database: show tables;
+-------------------------+
| Tables_in_house_booking |
+-------------------------+
| admin                   |
| approver                |
| payment                 |
| rental_house            |
| request_for_post        |
| request_for_rent        |
| user_details            |
+-------------------------+ 

import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="roshna#2001",database="house_booking")
mycursor = mydb.cursor()
class userdetails:
    def __init__(self,username,userpwd):
        self.name=username
        self.password=userpwd
    def isAlready(self):
        mycursor.execute('select user_id,name,password from user_details where name like %s',(self.name,))
        details=mycursor.fetchall()
        if(details):
            if(details[0][1]==self.name and details[0][2]==self.password):
                return details[0][0]
        else:
            return 0
class admindetails:
    def __init__(self,adminname,adminpwd):
        self.name=adminname
        self.password=adminpwd
    def isAlready(self):
        mycursor.execute("select admin_id,name,password from admin where name like %s",(self.name,))
        details=mycursor.fetchall()
        if(details):
            if(details[0][1]==self.name and details[0][2]==self.password):
                return details[0][0]
        else:
            return 0
    def booked(self):
        mycursor.execute("select rental_house.house_id,rental_house.rent,rental_house.type,rental_house.sq_feet,rental_house.city,rental_house.locality,user_details.name,user_details.phone_no,rental_house.status from rental_house inner join user_details where rental_house.owner_id=user_details.user_id and rental_house.status=%s",("booked",))
        details = mycursor.fetchall()
        if (details):
            for i in range(len(details)):
                row = details[i]
                print("house id:", row[0], "  ", "Rent:", row[1], "  ", "Type:", row[2], "  ", "sq_feet:", row[3], "  ","city:", row[4], "  ","locality:", row[5],"  ","owner name:",row[6],"  ","owner phone_no:",row[7])
        else:
            print("no booking")
class approverdetails:
    def __init__(self,appname,apppwd):
        self.name=appname
        self.password=apppwd
    def isAlready(self):
        mycursor.execute("select approver_id,name,password from approver where name like %s",(self.name,))
        details=mycursor.fetchall()
        if(details):
            if(details[0][1]==self.name and details[0][2]==self.password):
                return details[0][0]
        else:
            return 0
    def request_for_post(self):
        mycursor.execute("select rental_house.house_id,rental_house.rent,rental_house.type,rental_house.sq_feet,rental_house.city,rental_house.locality,user_details.name,user_details.phone_no,rental_house.status from rental_house inner join user_details where rental_house.owner_id=user_details.user_id and rental_house.status=%s",("checking",))
        details = mycursor.fetchall()
        if(details):
            for i in range(len(details)):
                row = details[i]
                print("house id:", row[0], "  ", "Rent:", row[1], "  ", "Type:", row[2], "  ", "sq_feet:", row[3], "  ","city:", row[4], "  ", "locality:", row[5],"  ","owner name:",row[6],"  ","owner phone_no:",row[7])
            h=int(input("Enter house id do u want give result"))
            s=str(input("Do u want to rejected or approved"))
            if(s=="approved"):
               mycursor.execute("update rental_house set status=%s where house_id=%s",("approved",h,))
               mydb.commit()
            if(s == "rejected"):
               mycursor.execute("update  rental_house set status=%s where house_id=%s", (s,h,))
               mydb.commit()
        else:
            print("no request")


class post:
    def __init__(self,id):
        self.user_id=id
    def owner(self):
        while True:
            print("1.New post\n2.see posts\n3.request for rent\n4.back")
            opt=int(input("Enter your option:"))
            if(opt==1):
                rent=str(input("Enter rent of your house"))
                type=str(input("Enter type of your house(2BHK/3BHK):"))
                sq_feet=str(input("Enter square feet:"))
                city=str(input("Enter city:"))
                locality=str(input("Enter area:"))
                mycursor.execute("insert into rental_house(rent,type,sq_feet,city,locality,owner_id,status) values(%s,%s,%s,%s,%s,%s,%s)",(rent,type,sq_feet,city,locality,self.user_id,"checking",))
                mydb.commit()

                print("Your request send to approver,once he verified we will notify you")
            if(opt==2):
                mycursor.execute("select rent,type,sq_feet,city,locality,status,owner_id from rental_house where owner_id=%s",(self.user_id,))
                details=mycursor.fetchall()
                if(details):
                    for i in range(len(details)):
                        row=details[i]
                        print("Rent:",row[0],"  ","Type:",row[1],"  ","sq_feet:",row[2],"  ","city:",row[3],"  ","locality:",row[4],"  ","status:",row[5])
                else:
                    print("You didn't post anything")
            if(opt==3):
                mycursor.execute("select house_id,user_id from request_for_rent where status=%s and house_id in (select house_id from rental_house where user_id=%s)",("checking",self.user_id,))
                details=mycursor.fetchall()
                if(details):
                    for i in range(len(details)):
                        row=details[i]
                        mycursor.execute("select name,phone_no,email,aadhar,user_id from user_details where user_id=%s",(row[1],))
                        u=mycursor.fetchall()
                        print("id:",u[4],"   ","Name:",u[0],"   ","Phone_no:",u[1],"   ","email:",u[2],"   ","aadhar:",u[3])
                    tid=int(input("which tenant do u want to rent ur house enter their id"))
                    mycursor.execute("select house_id from request_for_rent where user_id=%s",(tid,))
                    house=mycursor.fetchall()
                    h_id=house[0]

                    mycursor.execute("update  request_for_rent set status=%s where house_id=%s",("rejected",h_id,))
                    mydb.commit()
                    mycursor.execute("update  request_for_rent set status=%s where user_id=%s and house_id=%s", ("selected", tid,h_id,))
                    mydb.commit()
                    mycursor.execute("update  rental_house set status=%s where house_id=%s",("booked",h_id))
                    mydb.commit()
                    print("Your confirmation will send to tenant")
                else:
                    print("No request")

            if(opt==4):
                break
class rental:
    def __init__(self,id):
        self.user_id=id
    def rent(self):
        print("Search by 1.rent\n.2.type\n3.city")
        opt=int(input("Enter your choice"))
        if opt==1:
            rent=int(input("Enter rent upto which do u want:"))
            mycursor.execute("select rental_house.house_id,rental_house.rent,rental_house.type,rental_house.sq_feet,rental_house.city,rental_house.locality,user_details.name,user_details.phone_no from rental_house inner join user_details where rental_house.owner_id=user_details.user_id and rental_house.rent<=%s",(rent,))
            details=mycursor.fetchall()
            if(details):
                for i in range(len(details)):
                    row=details[i]
                    print("house id:",row[0],"  ","Rent:",row[1],"  ","Type:",row[2],"  ","sq_feet:",row[3],"  ","city:",row[4],"  ","locality:",row[5],"  ","owner name:",row[6],"  ","owner phone_no:",row[7])
                h=int(input("Enter house to give request:"))
                mycursor.execute("insert into request_for_rent(user_id,house_id,status) values(%s,%s,%s)",(self.user_id,h,"checking",))
                mydb.commit()
            else:
                print("No house available")
        if opt==2:
            type = int(input("Enter type of house  do u want:"))
            mycursor.execute(
                "select rental_house.house_id,rental_house.rent,rental_house.type,rental_house.sq_feet,rental_house.city,rental_house.locality,user_details.name,user_details.phone_no from rental_house inner join user_details where rental_house.owner_id=user_details.user_id and rental_house.type=%s",
                (type,))
            details = mycursor.fetchall()
            if (details):
                for i in range(len(details)):
                    row = details[i]
                    print("house id:", row[0], "  ", "Rent:", row[1], "  ", "Type:", row[2], "  ", "sq_feet:", row[3],
                          "  ", "city:", row[4], "  ", "locality:", row[5], "  ", "owner name:", row[6], "  ",
                          "owner phone_no:", row[7])
                h = int(input("Enter house to give request:"))
                mycursor.execute("insert into request_for_rent(user_id,house_id,status) values(%s,%s,%s)",
                                 (self.user_id, h, "checking",))
                mydb.commit()
            else:
                print("No house available")
        if opt==3:
            city = int(input("Enter city wdo u want:"))
            mycursor.execute("select rental_house.house_id,rental_house.rent,rental_house.type,rental_house.sq_feet,rental_house.city,rental_house.locality,user_details.name,user_details.phone_no from rental_house inner join user_details where rental_house.owner_id=user_details.user_id and rental_house.city=%s",
                (city,))
            details = mycursor.fetchall()
            if (details):
                for i in range(len(details)):
                    row = details[i]
                    print("house id:", row[0], "  ", "Rent:", row[1], "  ", "Type:", row[2], "  ", "sq_feet:", row[3],
                          "  ", "city:", row[4], "  ", "locality:", row[5], "  ", "owner name:", row[6], "  ",
                          "owner phone_no:", row[7])
                h = int(input("Enter house to give request:"))
                mycursor.execute("insert into request_for_rent(user_id,house_id,status) values(%s,%s,%s)",
                                 (self.user_id, h, "checking",))
                mydb.commit()
            else:
                print("No house available")
    def rent_status(self):
        mycursor.execute("select rental_house.rent,rental_house.type,rental_house.sq_feet,rental_house.city,rental_house.locality,request_for_rent.status from rental_house inner join request_for_rental on rental_house.house_id=request_for_rent.house_id where request_for_rent.user_id=%s",(self.user_id,))
        details = mycursor.fetchall()
        if (details):
            for i in range(len(details)):
                row = details[i]
                print("Rent:", row[0], "  ", "Type:", row[1], "  ", "sq_feet:", row[2], "  ", "city:", row[3], "  ",
                      "locality:", row[4], "  ", "status:", row[5])
        else:
            print("You didn't request anything")



if __name__ == '__main__':
    print("1.user\n2.Approver\n3.Admin")
    op=int(input("Enter your options:"))
    if(op==1):
        username=str(input("Enter your name"))
        userpwd = str(input("Enter password"))
        user = userdetails(username, userpwd)
        isal = user.isAlready()
        if isal:
            while True:
                print("1.post\n2.search for rental\n3.rent request status\n4.logout")
                opt=int(input("Enter your option:"))
                if(opt==1):
                        p=post(isal)
                        p.owner()
                if(opt==2):
                    r=rental(isal)
                    r.rent()
                if(opt==3):
                    r=rental(isal)
                    r.rent_status()
                if(opt==4):
                    exit()
        else:
            email = str(input("Enter your email:"))
            phone = str(input("Enter your phone number:"))
            aadhar = str(input("Enter your Aadhaar number"))
            mycursor.execute("insert into user_details(name,password,email,phone_no,aadhar) values(%s,%s,%s,%s,%s)",
                         (username, userpwd, email, phone,aadhar))
            mydb.commit()
            print("you are successfully signed in")
    if(op==2):
        appname = str(input("Enter your name"))
        apppwd = str(input("Enter password"))
        appr = approverdetails(appname, apppwd)
        isal = appr.isAlready()
        if isal:
            while True:
                print("1.Request for post\n.2.logout")
                opt = int(input("Enter your option:"))
                if (opt == 1):

                    appr.request_for_post()
                if(opt==2):
                    exit()
        else:
            email = str(input("Enter your email:"))
            phone = str(input("Enter your phone number:"))
            mycursor.execute("insert into approver(name,password,email,phone_no) values(%s,%s,%s,%s)",
                             (appname, apppwd, email, phone, ))
            mydb.commit()
            print("you are successfully signed in")
    if(op == 3):
        adminname = str(input("Enter your name"))
        adminpwd = str(input("Enter password"))
        adm = admindetails(adminname, adminpwd)
        isal = adm.isAlready()
        if isal:
            while True:
                print("1.house booked\n.2.logout")
                opt = int(input("Enter your option:"))
                if (opt == 1):
                    adm.booked()
                if (opt == 2):
                    exit()
        else:
            email = str(input("Enter your email:"))
            phone = str(input("Enter your phone number:"))

            mycursor.execute("insert into admin(name,password,email,phone_no) values(%s,%s,%s,%s)",
                             (adminname, adminpwd, email, phone,))
            mydb.commit()
            print("you are successfully signed in")







