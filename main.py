
# Written in December,  2023. 
# Made public 31 march, 2024.

import sqlite3,os
from outils import *
from langkups import *
from telebot import TeleBot,types
from telebot.util import antiflood
from pyTelegramBotCAPTCHA import CaptchaManager
from tweety import Twitter

#os.remove("database.db")
db_exists=os.path.exists("database.db")
con=sqlite3.connect("database.db", check_same_thread=False)
if not db_exists:
    con.cursor().execute("CREATE TABLE user (id INT,referredby INT, username VARCHAR(30), twitter VARCHAR(50),wallet VARCHAR(200),balance INT,isbanned VARCHAR(1),step INT,referrals INT)")
    con.commit()
    
bot = TeleBot("") # Yout bot token @BotFather
captcha_manager = CaptchaManager(bot.get_me().id, default_options=ucaptcha())
app = Twitter("session") # Gotta login with your twitter credentials in terminal. 
app.start()

""" Steps guide :
0 - fresh user. Taping /start for the first time
1 - At Telegram task
2 - At twitter task
3 - At wallet submit
4 - At captcha 
5 - Airdrop complete

Admin steps

10: Broadcast
11:

"""

## Todo : Blacklist
@bot.message_handler(chat_types=['private']) 
def all(message): 
  user = message.from_user
  uid = user.id
  try: 
    tname = user.first_name+" "+user.last_name
  except:
    tname = user.first_name
  mention = f"<a href='tg://user?id={user.id}'>{tname}</a>"
  try:
    username = '@'+str(user.username)
  except:
    username = 'None'
  
  if not uis_banned(con,uid):
    if message.text.startswith("/start"):
      bot.send_sticker(uid,"CAACAgIAAxkBAAEpBtdlrU11m5SWww9O_Fs9Hrc5O9qVtwACRAADO2AkFDPkfcK-cjUHNAQ") # cookie hey sticker
      referredby = urefby(message.text)
      if ustep(con,uid)==0:
        if not uhas_user(con,uid): # checks if the user already exist.
          con.cursor().execute(f"INSERT INTO user VALUES ({uid},{referredby},'{username}','None','None',0,'N',0,0)")
          con.commit()
        bot.reply_to(message,words().start_text.format(mention),parse_mode='html',disable_web_page_preview=True,reply_markup=mstart())
      elif ustep(con,uid)==10:
        bot.send_message(uid,words().admintxt,parse_mode='html',reply_markup=adminkm())
      elif ustep(con,uid)==5:
        bot.reply_to(message,f"Hey {mention},\nUse the menu buttons to explore ...",parse_mode='html',reply_markup=mainrkm())
      elif ustep(con,uid)==4:
        captcha_manager.send_new_captcha(bot, message.chat, message.from_user)
      elif ustep(con,uid)==3:
        bot.send_message(uid,words().wltxt,parse_mode='html',reply_markup=types.ForceReply(input_field_placeholder="Enter your sol wallet adresse:"))
      elif ustep(con,uid)==2:
        bot.send_message(uid,words().twitxt,disable_web_page_preview=True,parse_mode='html',reply_markup=types.ForceReply(input_field_placeholder="Enter your twitter username:"))
      elif ustep(con,uid)==1:
        bot.send_message(uid,words().tgtxt,reply_markup=mtg(),disable_web_page_preview=True,parse_mode='html')
      else:
        bot.delete_message(message.chat.id,message.id)


        pass
        #step_manager(ustep(con,uid))
    elif ustep(con,uid)==1: # telegram task
      if message.text == "/skiptg":
        bot.send_message(uid,words().twitxt,disable_web_page_preview=True,parse_mode='html',reply_markup=types.ForceReply(input_field_placeholder="Enter your twitter username:"))
        ustep_update(con,uid,2)

    elif ustep(con,uid)==2: # twitter task
      if message.text == "/skipt": #if skipped
        bot.send_message(uid,words().wltxt,parse_mode='html')
        con.cursor().execute(f"UPDATE user SET twitter='skipped' WHERE id={uid}")
        con.commit()
        ustep_update(con,uid,3)
      else:
        try:
          if utwitter_check(con,bot,message):
            bot.send_message(uid,words().wltxt,parse_mode='html',reply_markup=types.ForceReply(input_field_placeholder="Enter your sol wallet adresse:"))
            con.cursor().execute(f"UPDATE user SET twitter='@{message.text.strip('@')}' WHERE id={uid}")
            con.commit()
            ustep_update(con,uid,3)
          else:
            pass
        except Exception as e:
          print(e)
          bot.send_message(uid,words().wltxt,parse_mode='html',reply_markup=types.ForceReply(input_field_placeholder="Enter your sol wallet adresse:"))
          con.cursor().execute(f"UPDATE user SET twitter='@{message.text.strip('@')}' WHERE id={uid}")
          con.commit()
          ustep_update(con,uid,3)
    
    elif ustep(con,uid)==3: #wallet_task
      if message.text =="/skipw": #if skipped
        captcha_manager.send_new_captcha(bot, message.chat, message.from_user)
        con.cursor().execute(f"UPDATE user SET wallet='skipped' WHERE id={uid}")
        con.commit()
        
        ustep_update(con,uid,4)
      elif uwmatch(message.text,'sol'):
        captcha_manager.send_new_captcha(bot, message.chat, message.from_user)
        con.cursor().execute(f"UPDATE user SET wallet='{message.text}' WHERE id={uid}")
        con.commit()
        ustep_update(con,uid,4)
      else:
        bot.reply_to(message,"Please enter a valid <b>Solana Adresse</b> :",parse_mode='html')

    ## here starts the post airdrop things
    elif ustep(con,uid)==5:
      if message.text == "🍪 My Cookies":
        balance = checkbal(con,uid)
        bot.reply_to(message,words().baltxt.format(balance,utimenow()),parse_mode='html',reply_markup=balkey())
      if (message.text == "🌟 Referrals") or message.text =="/refer":
        bot.send_message(uid,words().reftext.format(uid),parse_mode='html',disable_web_page_preview=True,reply_markup=refkey(uid))
      if message.text == "🏆 Podium":
        bot.send_message(uid,words().podtxt.format(utimenow()),parse_mode='html',reply_markup=podkey())
      if message.text == "📊 Statistics" :
        u = ustats(con,uid)
        bot.send_message(uid,words().stattxt.format(utimesince(),u[0],mention,u[1],u[2],u[3],mention,u[4],u[5]),parse_mode='html',disable_web_page_preview=True)
      if message.text == "🔥 Tasks" :
        bot.send_message(uid,words().tasktxt,parse_mode='html')
      
      if message.text == "㊙️ Admin Panel ( Demo only )":
        bot.send_message(uid,words().admintxt,parse_mode='html',reply_markup=adminkm())
        bot.send_message(message.chat.id,"🎈 Some options are demo-only to protect privacy of demobot users.")

        ustep_update(con,uid,10)
      

    elif ustep(con,uid)==10:
      if message.text == "📣  Broadcast":
        bot.send_message(uid,words().bcasttxt,parse_mode='html',reply_markup=types.ReplyKeyboardRemove())
        ustep_update(con,uid,11)
      elif message.text == "📁 Export Data":
        uexport(con,uid)
        bot.send_message(uid,words().guidetxt,parse_mode='html',reply_markup=adminkm())
        bot.send_document(uid,open('AirDemoXbot.xlsx','rb'),caption=f"Generated at :\n {utimenow()} ")
        os.remove("AirDemoXbot.xlsx")
      elif message.text == "🔍 User query":
        bot.send_message(uid,words().uquerytxt,parse_mode='html')
        ustep_update(con,uid,14)
      elif message.text == "🛑 Stop Airdrop":
        bot.send_message(uid,"<blockquote>As a demo bot, we don't allow this feature, of course. But how about discovering an ester egg?</blockquote>\n\n/cancel to close and go back or,\n <b>Please send the password :</b>",parse_mode='html')
        ustep_update(con,uid,15)
      elif message.text == "🚹 User Mode":
        bot.reply_to(message,f"Hey {mention},\nUse my menu buttons to explore ...",parse_mode='html',reply_markup=mainrkm())
        ustep_update(con,uid,5)
   
    elif ustep(con,uid)==14:
      if message.text == "/cancel":
        bot.send_message(uid,"🧰",parse_mode='html',reply_markup=adminkm())
        ustep_update(con,uid,10)
      else:
        uquery(con,bot,message)
    
    elif ustep(con,uid)==15:
      if message.text == "/cancel":
        bot.send_message(uid,"🧰",parse_mode='html',reply_markup=adminkm())
        ustep_update(con,uid,10)

      elif message.text.lower() == "cookie":
        bot.send_message(uid,"So close yet 2o far")
      elif message.text.lower() == "ckie":
        bot.send_sticker(uid,"CAACAgIAAxkBAAEpCDhlra3BEc1DzpLLWzuA189MCawUbAACJwAD9wLID0vZJXq0bnAbNAQ") # no sticker
        bot.send_message(uid,"Bingo. C kie ic eikoo!")
      else:
        bot.send_sticker(uid,"CAACAgIAAxkBAAEpCD5lra7gMZlltVXHGEwRFSuJI7NwoAACVQADO2AkFOPuvbUhzLeRNAQ")
        bot.send_message(uid,"🧰",parse_mode='html',reply_markup=adminkm())
        ustep_update(con,uid,10)
    
    elif ustep(con,uid)==11: #incoming broadcast message to copy
      if message.text == "/cancel":
        bot.send_message(uid,"🧰",parse_mode='html',reply_markup=adminkm())
        ustep_update(con,uid,10) 
      else:
        ustep_update(con,uid,10)
        x = bot.send_message(uid,words().bcprog.format(0,0,0),parse_mode='html')
        f =0
        s = 0
        for i in range(247):
          if i%10==0:
            s+=1
            antiflood(bot.edit_message_text,words().bcprog.format(s,f,int((i/247)*100)),chat_id=x.chat.id,message_id=x.message_id,parse_mode='html',number_retries=100)
          elif i%11==0:
            f+=1
          else:
            s+=1
          
        bot.edit_message_text(words().bcprog.format(s,f,100),chat_id=x.chat.id,message_id=x.message_id,parse_mode='html')
        bot.send_message(x.chat.id,f"🔔 <b>Broadcast concluded  !</b>\n\n✅ Sent : {s}\n❎ Blocked : {f}",parse_mode="html",reply_markup=adminkm())
        

    elif ustep(con,uid) == 12:
      if message.text == '/cancel':
        ustep_update(con,uid,10)
        bot.send_message(uid,"🧰",reply_markup=adminkm())
      elif message.text.startswith('@'):
        q = f"SELECT id FROM user WHERE username = '{message.text}'"
        res = con.cursor().execute(q).fetchone()
        if res == None:
          bot.send_message(uid,"Username not found in database.\n\n- Check if user is a participant.\n-Verify the username sent.")
        else:
          bid = res[0] #banid
          if bid != uid:
            bot.send_message("User found but not banned (demo).")
          else:
            bot.send_message("You shouldn't ban yourself.")
      elif not message.text == uid:
        try:
          bid = int(message.text)
          q = f"SELECT isbanned FROM user WHERE username = '{message.text}'"
          res = con.cursor().execute(q).fetchone()
          if res!=None:
            #uban(con,bid)
            bot.send_message("User found but not banned (demo).")
        except:
          bot.send_message(uid,"An error occured.\n\n-Verify the username/uid submitted.\n- Check if user is a participant.\n")
      else:
        bot.send_message(uid,"An error occured.\n\n-Verify the username/uid submitted.\n- Check if user is a participant.\n-Check the id is not yours.")
      bot.send_message(uid,"🧰 Admin menu",parse_mode='html',reply_markup=adminkm())
      ustep_update(con,uid,10)

    elif ustep(con,uid) == 13:
      if message.text == '/cancel':
        ustep_update(con,uid,10)
        bot.send_message(uid,"🧰",reply_markup=adminkm())
      else:
        try:
          if unban(con,message.text):
            bot.send_message(uid,"User found and unbanned.")
          else:
            bot.send_message(uid,"User not found in database.\n\n- Check if user is a participant.\n-Verify the username sent.\n-The user was previousely banned.")
        except:
          bot.send_message(uid,"Verify the username/uid submitted.")

        bot.send_message(uid,"🧰",parse_mode='html',reply_markup=adminkm())
        ustep_update(con,uid,10)
    
    else:
      bot.delete_message(message.chat.id,message.message_id)
  else:
    bot.delete_message(message.chat.id,message.message_id)



# Callback query handler
@bot.callback_query_handler(func=lambda callback:True)
def on_callback(callback):
  uid = callback.from_user.id
  if not uis_banned(con,uid):
    if ustep(con,uid)==4:
      captcha_manager.update_captcha(bot, callback) # manages captcha callbacks
    elif callback.data == "start1" and ustep(con,uid)==0:
      try:
        if bot.get_chat_member("@airbotsx",uid).status=="left" and bot.get_chat_member("@airbotsfam",uid).status=="left":
          bot.send_message(uid,words().tgtxt,reply_markup=mtg(),disable_web_page_preview=True,parse_mode='html')
          ustep_update(con,uid,1)
        else:
          bot.send_message(uid,words().twitxt,disable_web_page_preview=True,parse_mode='html',reply_markup=types.ForceReply(input_field_placeholder="Enter your twitter username:"))
          bot.answer_callback_query(callback.id, "Telegram validated. Please make sure to remain in our chats to qualify.",show_alert=True)
          ustep_update(con,uid,2)
      except:
        bot.send_message(uid,words().tgtxt,reply_markup=mtg(),disable_web_page_preview=True,parse_mode='html')
        ustep_update(con,uid,1)
    elif callback.data == "tgvalid" and ustep(con,uid)==1:
      try:
        if bot.get_chat_member("@airbotsx",uid).status=="left" and bot.get_chat_member("@airbotsfam",uid).status=="left":
          bot.answer_callback_query(callback.id, "We can't find you in our channels. Please make sure you've joined all of our telegram chats mentioned.", show_alert=True)
        else:
          bot.send_message(uid,words().twitxt,disable_web_page_preview=True,parse_mode='html',reply_markup=types.ForceReply(input_field_placeholder="Enter your twitter username:"))
          ustep_update(con,uid,2)
      except:
        bot.send_message(uid,words().twitxt,disable_web_page_preview=True,parse_mode='html',reply_markup=types.ForceReply(input_field_placeholder="Enter your twitter username:"))
        ustep_update(con,uid,2)

    elif callback.data == "refreshbal" and ustep(con,uid)==5:
      try:
        bot.edit_message_text(words().baltxt.format(checkbal(con,uid),utimenow()),callback.message.chat.id,callback.message.message_id,reply_markup=balkey(),parse_mode='html')
      except Exception as e:
        bot.answer_callback_query(callback.id,"Balance remained unchanged..", show_alert=True)
    elif callback.data == "refreshpod" and ustep(con,uid)==5:
      bot.answer_callback_query(callback.id, "Demo only. Thus not updated...")
    
    elif callback.data == "ban" and ustep(con,uid)==10:
      bot.send_message(uid,words().bantxt,parse_mode='html',reply_markup=querykey())
      ustep_update(con,uid,12)
    
    elif callback.data == "unban" and ustep(con,uid)==10:
      if uis_banned(con,uid):
        bot.send_message(uid,words().unbantxt,parse_mode='html',reply_markup=querykey1())
      else:
        bot.answer_callback_query(callback.id,"User is not banned  !",show_alert=True)
      ustep_update(con,uid,13)
    
    elif callback.data == "addadmins" and ustep(con,uid)==10:
      bot.answer_callback_query(callback.id,"Not available as demo yet. ")
    
    elif callback.data == "rmadmins" and ustep(con,uid)==10:
      bot.answer_callback_query(callback.id,"Not available as demo yet. ")
    
    elif callback.data == "confirmb" and ustep(con,uid)==10:
      bot.answer_callback_query(callback.id,"Not available as demo yet. ")
    
    elif callback.data == "cancel" and ustep(con,uid)==10:
      bot.delete_message(callback.message.chat.id,callback.message.message_id)
      ustep_update(con,uid,10)
      bot.send_message(uid,"🧰",reply_markup=adminkm())
    
    else: 
      bot.delete_message(callback.from_user.id,callback.message.message_id)
  else: # if banned
    bot.delete_message(callback.from_user.id,callback.message.message_id)

      





# Handler for correct solved CAPTCHAs
@captcha_manager.on_captcha_correct
def on_correct(captcha):
  ustep_update(con,captcha.user.id,5)
  mention = f"<a href='tg://user?id={captcha.user.id}'>{captcha.user.first_name}</a>"
  q = f"SELECT referredby FROM user WHERE id = {captcha.user.id}"
  res = con.cursor().execute(q).fetchone() # referrer id
  if urefcheck(con,res[0]):
    mention_txt = mention+" got 2 extra cookies thanks to your participation."
    uupbalance(con,res[0],2)
    uupref(con,res[0]) 
    try:
      bot.send_message(res[0],f"🦋 {mention} just completed the airdrop and gave you 2🍪 as thank you.",parse_mode='html')
    except:
      pass
  else:
    mention_txt = " No one referred you. How about referring someone for extra cookies?"
  
  bot.send_sticker(captcha.chat.id,"CAACAgIAAxkBAAEpBstlrUsNoUaKeKUZHSO6SMMpcphV-wACQgADO2AkFLjp0so8nIjNNAQ") # cookie done sticker
  bot.send_message(captcha.chat.id, words().finitxt.format(mention_txt),reply_markup=mainrkm(),parse_mode='html')
  bot.send_message(captcha.chat.id,"🎈 Some options are demo-only to protect privacy of demo users.")
  
  uupbalance(con,captcha.chat.id,10)
  captcha_manager.delete_captcha(bot, captcha)

# Handler for wrong solved CAPTCHAs
@captcha_manager.on_captcha_not_correct
def on_not_correct(captcha):
  mention = f"<a href='tg://user?id={captcha.user.id}'>{captcha.user.first_name}</a>"
  if captcha.previous_tries < 3:
    captcha_manager.refresh_captcha(bot, captcha)
  else:
    bot.send_message(captcha.chat.id, f"{mention} failed solving the CAPTCHA and was banned!\nSorry to see you go bot.",parse_mode='html')
    uban(con,captcha.user.id) # ban the user
    captcha_manager.delete_captcha(bot, captcha)

@captcha_manager.on_captcha_timeout
def on_timeout(captcha):
  bot.send_message(captcha.chat.id, "You didn't complete the captcha on time. Press /start to retry. ")
  captcha_manager.delete_captcha(bot, captcha)


print("Started..")
bot.infinity_polling(timeout=10, long_polling_timeout = 5,restart_on_change=True,path_to_watch=r'./dd.py') # doesn't stop the bot if error