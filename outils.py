import re
from pyTelegramBotCAPTCHA import CaptchaOptions, CustomLanguage
from tweety import Twitter
from telebot.util import antiflood,user_link
import langkups

def ucaptcha():
  default_options = CaptchaOptions()
  default_options.generator = "multicolor"
  default_options.language = "en"
  default_options.timeout = 600 
  default_options.only_digits = True
  default_options.add_noise = False
  default_options.max_attempts = 3
  captcha_text = CustomLanguage()
  #captcha_text.text = "Welcome,"
  default_options.custom_language = captcha_text
  return default_options

def uhas_user(con, uid):
    q = f"SELECT id FROM user WHERE id = '{uid}'"
    res = con.cursor().execute(q).fetchall()
    if len(res) > 0:
        return True
    else:
        return False

def uis_banned(con,uid):
   q = f"SELECT isbanned FROM user WHERE id = '{uid}'"
   res = con.cursor().execute(q).fetchone()
   try:
    if res[0] == 'Y':
        return True
   except:
      return False
   return False

def ustep(con,uid):
   q = f"SELECT step FROM user WHERE id = '{uid}'"
   res = con.cursor().execute(q).fetchone()
   if res==None:
      return 0
   return res[0]

def ustep_update(con,uid,value):
   q = f"SELECT step FROM user WHERE id = '{uid}'"
   res = con.cursor().execute(q).fetchone()
   if res==None:
      return 0
   else:
      con.cursor().execute(f"UPDATE user SET step='{value}' WHERE id={uid}")
      con.commit()

def uban(con,uid): #bans user
   con.cursor().execute(f"UPDATE user SET isbanned='Y' WHERE id={uid}")
   con.commit()

def unban(con,uid):
   q = "SELECT isbanned FROM user WHERE id = {uid}"
   res = con.cursor().execute(q).fetchone()
   if res[0]=="Y":
      con.cursor().execute(f"UPDATE user SET isbanned='N' WHERE id={uid}")
      con.commit()
      return True
   else:
      return False

def urefby(msg): #check if referredby
    x = msg.split(' ')
    if len(x)>1:
        try: 
            y = int(x[1])
        except:
            y = 0
    else:
        y = 0
    return y

def urefcheck(con,refby): #checks if the referrer exist
   q = f"SELECT isbanned,step FROM user WHERE id = '{refby}'"
   res = con.cursor().execute(q).fetchone() 
   if res==None:
      return False
   if res[1]==5 and res[0]=='N': # if the referrer has completed task and not banned.
      return True
   return False

def checkbal(con,uid):
   q = f"SELECT balance FROM user WHERE id = '{uid}'"
   res = con.cursor().execute(q).fetchone()
   if not res==None:
      return res[0]
   

def uupbalance(con,uid:int,upval:int): #updates balance of an uid
   res = checkbal(con,uid)
   if not res == None:
      con.cursor().execute(f"UPDATE user SET balance='{res+upval}' WHERE id={uid}")
      con.commit()

def uupref(con,uid):
   q = f"SELECT referrals FROM user WHERE id = '{uid}'"
   r = con.cursor().execute(q).fetchone()
   q = f"UPDATE user SET referrals = {r[0]+1} WHERE id={uid}"
   res = con.cursor().execute(q)

def ustats(con,uid):
   a = f"SELECT COUNT(id) FROM user"
   tp = con.cursor().execute(a).fetchone()[0] #total_paticipants
   
   b = f"SELECT COUNT(id) FROM user WHERE referredby = {uid}"
   tr = con.cursor().execute(b).fetchone()[0] #total_referrals

   c = f"SELECT id FROM user ORDER BY referrals"
   srr = con.cursor().execute(c).fetchall()
   for i,e in enumerate(srr):
      if e[0]==uid:
         rr = i+1 #referral rank

   d = f"SELECT twitter,wallet,referrals FROM user where id={uid}"
   ui = con.cursor().execute(d).fetchone() 
   twitter = f"<a href='https://x.com/{ui[0]}'>X/{ui[0].strip('@')}</a>"
   if ui[1]=="skipped":
      wlt = "skipped"
   else:
      wlt = f"{ui[1][:5]}.....{ui[1][-5:]}"
   referrals = ui[2] #confirmed_referrals

   return tp,tr,referrals,rr,twitter,wlt

def uquery(con,bot,msg):
   uid = msg.chat.id
   if msg.forward_origin != None:
      if msg.forward_origin.type!='hidden_user':
         quid = msg.forward_origin.sender_user.id
      else:
         bot.send_message(uid,"Forwarder's profile is hidden. Please try other methods if possible.")
   else:
      q = f"SELECT id FROM user WHERE id={msg.text} OR twitter='{msg.text}' OR wallet='{msg.text}' OR username='{msg.text}'"
      try:
         r = con.cursor().execute(q).fetchone()
      except:
         q = f"SELECT id FROM user WHERE twitter='{msg.text}' OR wallet='{msg.text}' OR username='{msg.text}'"
         r = con.cursor().execute(q).fetchone()
      if r is not None:
         qid = r[0]
         a = ustats(con,qid)
         mention = f"<a href='tg://user?id={r[0]}'>{r[0]}</a>"
         
         bot.send_message(uid,langkups.words().sensitive_txt.format(mention,a[4],a[-1],checkbal(con,uid)),parse_mode="html",reply_markup=langkups.sensitives())
         ustep_update(con,uid,10)

      else:
         bot.send_message(uid,"User not found in bot database. User must start the bot.")
         ustep_update(con,uid,10)
         bot.send_message(uid,"🧰",parse_mode='html',reply_markup=langkups.adminkm())



## Admin helpers 

def ubroadcast(con,bot,message,uid,words,cancelkey): # a completer
   q = f"SELECT id FROM user WHERE step=5"
   r = con.cursor().execute(q).fetchall()
   x = bot.send_message(uid,words().bcprog.format(0,0,0),parse_mode='html',reply_markup=cancelkey())
   f =0
   for i,e in enumerate(r):
      try:
         antiflood(bot.copy_message,e[0],message.chat.id,message.message_id)
      except Exception as e:
         print(e)
         f+=1
      if i%10==0:
         bot.edit_message_text(words().bcprog.format(i,f,((i+f)//len(r)*100)),x.chat.id,x.message_id,parse_mode='html',reply_markup=cancelkey())


import pandas as pd
def uexport(con,uid):
   a = f"SELECT * FROM user WHERE id={uid}"
   read = pd.read_sql(a,con)
   df = pd.DataFrame(read)
   
   df.loc[df["isbanned"] == "N", "isbanned"] = "" 
   df.loc[df["referredby"] == 0, "referredby"] = ""
   df.loc[df["username"] == 'None', "username"] = ""
   
      
   read.to_excel('AirDemoXbot.xlsx',columns=['id','referredby','username','twitter','wallet','balance','isbanned','referrals','step'],index=False)
   




   
from tweety import Twitter,exceptions_
def utwitter_check(con,bot,msg): # message.text (step twitter)
   twitter = msg.text.strip('@')
   q = f"SELECT * FROM user WHERE twitter='@{twitter}'"
   r = con.cursor().execute(q).fetchall()
   if len(r)==0: # if twitter not already used for airdrop
      bot.send_chat_action(chat_id=msg.chat.id,action='typing')
      try:
         app = Twitter("session")
         app.start()
         tuser = app.get_user_info(twitter)
         for u,followings in app.iter_user_followings(twitter):   # tweety.exceptions_.UserNotFound
            lenf=15 if len(followings)>15 else len(followings)
            l = [followings[i].username for i in range(lenf)]     
         if 'AirbotsX' in l:
            return True
         else: 
            bot.reply_to(msg,f"<a href='https://x.com/{tuser.username}'>{tuser.name}</a> is not following <a href='https://x.com/@AirbotsX'>@AirbotsX</a>. \nFollow then try resending your handle :",parse_mode="html",disable_web_page_preview=True)
      except exceptions_.UserNotFound:
         bot.reply_to(msg,"Please send a valid twitter handle :")
      except:
         bot.reply_to(msg,"Please send a valid twitter handle :")

   else:
      bot.reply_to(msg,"⚠ Account already in use for airdrop.\n Please try with a different account or contact support.")


## source : https://gist.github.com/etherx-dev/76559d9e6d916917a960e33ceea91481
def uwmatch(wallet,ticker):
  if ticker == "eth" or ticker=="bnb":
    s = r"^(0x)[0-9A-Fa-f]{40}$" # eth,bnb pattern
    if re.match(s,wallet):
      return True 
    return False
  elif ticker == "sol":
    s = r"^[1-9A-HJ-NP-Za-km-z]{32,44}$" # sol pattern
    if re.match(s,wallet):
      return True 
    return False
  elif ticker == "bnb1":
    s = r"(bnb1)[0-9a-z]{38}$" # bnb1 pattern
    if re.match(s,wallet):
      return True 
    return False
#print(uwmatch("0x694698D30A5CE3988e65Lke99BD9014d60Cb9246","eth"))

from datetime import datetime,timezone

def utimenow():
   x = datetime.now(timezone.utc)
   day = x.day
   month = x.strftime("%b")
   year = x.year
   hour = x.hour 
   min = x.minute

   return (f"{day} {month}, {year} {hour}:{min}")

def utimesince():
   start = datetime(2024,1,16,tzinfo=timezone.utc)
   newtime = (datetime.now(timezone.utc))-start
   ts = newtime.total_seconds()
   n  = datetime.fromtimestamp(ts)
   return f"{n.day} days {n.hour} hours"
   