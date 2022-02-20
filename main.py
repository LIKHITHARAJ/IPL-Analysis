from ast import For
from datetime import datetime
from turtle import st
from fastapi import FastAPI, Request, Cookie
from fastapi.params import Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import starlette.status as status
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
# creating a FastAPI object
app = FastAPI()
security = HTTPBasic()

# configuring the static, which serve static
app.mount("/static", StaticFiles(directory="static"), name="static")


# adding the Session Middleware
app.add_middleware(SessionMiddleware, secret_key='MyApp')

# configuring the HTML pages
templates = Jinja2Templates(directory="templates")


# declaring urls


@app.get("/register",response_class=HTMLResponse)
def register(request:Request):
 return templates.TemplateResponse("register.html",{"request":request})

@app.post("/register",response_class=HTMLResponse)
def do_register(request:Request,username: str=Form(...), email: str =Form(...),password:str=Form(...),phone:str=Form(...),address:str=Form(...)):

  with sqlite3.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into users(username, email, password,phone, address) values(?,?,?,?,?)",
                    (username, email, password, phone,address))
        con.commit()  
  return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

@app.get("/login",response_class=HTMLResponse)
def login(request:Request):
 return templates.TemplateResponse("login.html",{"request":request})

@app.post("/login",response_class=HTMLResponse)
def do_login(request:Request,response:Response,username: str=Form(...),password:str=Form(...)):
  con = sqlite3.connect("app.db")
  con.row_factory = sqlite3.Row
  cur = con.cursor()
  cur.execute("select * from users where username=? and password=?" ,[username,password])
  users = cur.fetchone()
  if not users:
    return templates.TemplateResponse("/login",{"request":request,"msg":"Invalid Username or Password"})
  else:
    request.session.setdefault("isLogin",True)
    request.session.setdefault('username',users['username'])
    request.session.setdefault('uid',users['id'])
    return RedirectResponse("/index",status_code=status.HTTP_302_FOUND)

@app.get("/index",response_class=HTMLResponse)
def index(request:Request):
 return templates.TemplateResponse("index.html",{"request":request}) 

@app.get("/home",response_class=HTMLResponse)
def home(request:Request):
 return templates.TemplateResponse("home.html",{"request":request}) 

@app.get("/teams",response_class=HTMLResponse)
def teams(request:Request):
 return templates.TemplateResponse("teams.html",{"request":request}) 

@app.get("/table",response_class=HTMLResponse)
def table(request:Request):
 return templates.TemplateResponse("table.html",{"request":request}) 

@app.get("/records",response_class=HTMLResponse)
def records(request:Request):
  con = sqlite3.connect("app.db")
  con.row_factory = sqlite3.Row
  cur = con.cursor()
  cur.execute("select * from records")
  records = cur.fetchall() 
  con.close()
  return templates.TemplateResponse("/records.html",{"request":request,"records":records})
 

@app.get("/detail1",response_class=HTMLResponse)
def detail1(request:Request):
  return templates.TemplateResponse("detail1.html",{"request":request}) 


@app.get("/booking",response_class=HTMLResponse)
def booking(request: Request):
  return templates.TemplateResponse("booking.html", {"request": request}) 

      
@app.post("/booking",response_class=HTMLResponse)
def do_booking(request:Request,name: str=Form(...),phone: str=Form(...),email: str=Form(...),place: str=Form(...),stadium:str=Form(...),datetime:str=Form(...),seat:str=Form(...),ticket:str=Form(...),amount:str=Form(...)):

  with sqlite3.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into book(name,phone,email,place,stadium,datetime,seat,ticket,amount) values(?,?,?,?,?,?,?,?,?)",
                    (name, phone, email, place, stadium, datetime, seat, ticket, amount))
        con.commit()  
  return RedirectResponse("/payment", status_code=status.HTTP_302_FOUND)


@app.get("/payment", response_class=HTMLResponse)
def payment(request: Request):
  return templates.TemplateResponse("payment.html", {"request": request})    


@app.get("/admin/",response_class=HTMLResponse)
def admin_login(request:Request):
  return templates.TemplateResponse("/admin/login.html",{"request":request}) 

@app.post("/admin/",response_class=HTMLResponse)
def admin_login(request:Request,response:Response,username: str=Form(...),password:str=Form(...)):
  con = sqlite3.connect("app.db")
  con.row_factory = sqlite3.Row
  cur = con.cursor()
  cur.execute("select * from admin where username=? and password=?" ,[username,password])
  admin = cur.fetchone()
  if not admin:
    return templates.TemplateResponse("/admin/login.html",{"request":request,"msg":"Invalid Username or Password"})
  else:
    request.session.setdefault("isLogin",True)
    request.session.setdefault('username',admin['username'])
    request.session.setdefault('uid',admin['id'])
    request.session.setdefault('role',admin['role'])
    return RedirectResponse("admin/dashboard/",status_code=status.HTTP_302_FOUND)

@app.get("/admin/book",response_class=HTMLResponse)
def admin_book(request:Request):
  con = sqlite3.connect("app.db")
  con.row_factory = sqlite3.Row
  cur = con.cursor()
  cur.execute("select * from book")
  book= cur.fetchall()
  con.close
  return templates.TemplateResponse("/admin/book.html",{"request":request,"book":book})

@app.get("/admin/records",response_class=HTMLResponse)
def admin_records(request:Request):
  con = sqlite3.connect("app.db")
  con.row_factory = sqlite3.Row
  cur = con.cursor()
  cur.execute("select * from records")
  records = cur.fetchall() 
  con.close()
  return templates.TemplateResponse("/admin/records.html",{"request":request,"records":records})


@app.get("/admin/records/create",response_class=HTMLResponse)
def admin_records_create(request:Request):
 return templates.TemplateResponse("/admin/records_create.html",{"request":request}) 


@app.post("/admin/records/create",response_class=HTMLResponse)
def do_records_create(request:Request,rtitle: str=Form(...),tags: str=Form(...),image: str=Form(...),category: str=Form(...)):

  with sqlite3.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into records(rtitle,tags,image,category) values(?,?,?,?)",
                    (rtitle,tags,image,category))
        con.commit()  
  return RedirectResponse("/admin/records", status_code=status.HTTP_302_FOUND)




@app.get("/admin/winners",response_class=HTMLResponse)
def admin_winners(request:Request):
  return templates.TemplateResponse("/admin/winners.html",{"request":request}) 


@app.post("/admin/winners",response_class=HTMLResponse)
def do_admin_winners(request:Request,season: str=Form(...),date: str=Form(...),teams: str=Form(...),umpire: str=Form(...),runs: str=Form(...),won: str=Form(...),lost: str=Form(...),venue: str=Form(...)):

  with sqlite3.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into winners(season,date,teams,umpire,runs,won,lost,venue) values(?,?,?,?,?,?,?,?)",
                    (season,date,teams,umpire,runs,won,lost,venue))
        con.commit()  
  return RedirectResponse("/winners", status_code=status.HTTP_302_FOUND)

@app.get("/winners",response_class=HTMLResponse)
def winners(request:Request):
  con = sqlite3.connect("app.db")
  con.row_factory = sqlite3.Row
  cur = con.cursor()
  cur.execute("select * from winners")
  winners= cur.fetchall()
  con.close
  return templates.TemplateResponse("/winners.html",{"request":request,"winners":winners})

@app.get("/teamrecord", response_class=HTMLResponse)
def teamrecord(request: Request):
  return templates.TemplateResponse("/teamrecord.html", {"request": request})    

@app.get("/admin/bowlers",response_class=HTMLResponse)
def admin_bowlers(request:Request):
  return templates.TemplateResponse("/admin/bowlers.html",{"request":request}) 


@app.post("/admin/bowlers",response_class=HTMLResponse)
def do_admin_winners(request:Request,season: str=Form(...),player: str=Form(...),match: str=Form(...),over: str=Form(...),eco: str=Form(...),runs: str=Form(...),wic: str=Form(...)):

  with sqlite3.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into bowlers(season,player,match,over,eco,runs,wic) values(?,?,?,?,?,?,?)",
                    (season,player,match,over,eco,runs,wic))
        con.commit()  
  return RedirectResponse("/bowlers", status_code=status.HTTP_302_FOUND)

@app.get("/bowlers",response_class=HTMLResponse)
def bowlers(request:Request):
  con = sqlite3.connect("app.db")
  con.row_factory = sqlite3.Row
  cur = con.cursor()
  cur.execute("select * from bowlers")
  bowlers= cur.fetchall()
  con.close
  return templates.TemplateResponse("/bowlers.html",{"request":request,"bowlers":bowlers})

