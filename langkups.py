# Dictionary of Airdemobot
from telebot.types import ReplyKeyboardMarkup
from telebot.util import quick_markup

class words:
  def __init__(self) -> None:
    self.start_text = """Hi {} , 

<blockquote>The introduction page of your airdrop. This part can describe your project in few lines. As a demo, we will put explanations of functions in quotes. All remains customizable, of course.</blockquote>

Join the Airdrop to get 10 🍪.
Cookies make the world happy as a cookie well made is a smile on a plate.

<b>Follow the below steps :</b> 

<blockquote>You can put as many tasks as you want. But it is recommended from us to restrain the tasks atmost 3 social networks. Best for user engagement.</blockquote>

🔸 Join our Telegram <a href="https://t.me/AirbotsFam">Community</a>
🔸 Join our Telegram <a href="https://t.me/AirbotsX">Channel</a>
🔸 Follow us at <a href="https://twitter.com/Airbots">Twitter</a> + Retweet 
🔸 ( Subscribe us at Youtube ) 👍

<blockquote>Referrals are the most effective system to lead an airdrop to succes. You can decide to offer some tokens for inviting or to organize a referral competition.</blockquote>

✅  Get 🍪 by inviting your friends !
"""

    self.tgtxt = """<b>Please join us on telegram :</b> 

<blockquote>The bot can auto verify if the user has joined telegram channel or group. The bot must be set admin with minimum permissions.</blockquote>

📣 <a href="https://t.me/AirbotsX">Airbots Telegram Channel</a>
💭 <a href="https://t.me/AirbotsFam">Airbots Telegram Group</a>

<blockquote>The bot frequently checks whereas the user is still in groupes. If not, it reminds the user. At the end of the airdrop, all users unsubscribed are auto banned.</blockquote>

<blockquote>Press /skiptg to skip the task. But recommended to try.</blockquote>
Please note that you must remain in our channels + groups qualify."""

    self.twitxt = """<b>Pleass follow us on Twitter ( X ):</b>

<blockquote>Twitter verifications are also possible in AirbotsX. <b>Participants must follow you at twitter to pass to next step.</b> We can also verify retweets as well ! </blockquote>

# 🐦 <a href="https://twitter.com/Airbots">Aitbots Twitter</a> + Retweet

<blockquote>The username to submit must not exist on airdrop database to be accepted. It prevents multiple-entries and exploits.</blockquote>

Please submit your X username :
<blockquote>For demo, we let you /skipt. But highly recommend to give it a try.</blockquote>"""

    self.wltxt = """<b>👛 Please submit your Cookie wallet</b>

<blockquote>The bot is uses patterns to identify all principal crypto chains. For cookies, what's better than solana?</blockquote>
<blockquote>For demo, we let you /skipw. But highly recommend to give it a try.</blockquote>"""

    self.finitxt = "<b>Congratulations on completing the airdrop. You've got 10</b>🍪\n\n<blockquote>At this step, a user has successfully completed the airdrop. If he doesn't do anything stupid in the meantime, he is good for the distribution.</blockquote>\n\n🦋 {} \n\n<blockquote><b>Only at this moment :</b>\n\n▫ The referrer if exists gets rewarded with extra tokens. If he is not banned, he is notified immediately.\n\n▫ User details are shown in airdrop spreadsheet. ( remains in database )\n\n▫ The bot menu unlocks where the user can check stats, leaderboard, make referrals and do specific tasks.</blockquote>\n\n⚠ Please remember to remain active in our chats. Please abide by the rules trying not to cheat.\n\n<blockquote>Cookies are for everyone!</blockquote>\n\n🔥 Bot menu is now unlocked ! Try it."

    self.baltxt = """<blockquote>This text shows user's balance at the moment of consultation. The balance represents the amount of token, the participant should get in their wallet adress during the distribution.</blockquote>

👛 Congrats! You currently own :

{} Cookies
<b><u>Updated</u></b> : {} ( UTC+0 )

<blockquote>Participant may increase his balance through referrals, tournaments, giveway and daily tasks.</blockquote>

/refer gets you more cookies.
🔄 Refresh to look for balance update.
"""

    self.reftext = """<blockquote>
Friends are nice, but friends with cookies are better.
</blockquote>

<b>Share this magic link  :</b>

t.me/AirDemoXbot?start={}

Joining through this link will get your friend 10 and you 2 cookies. 

<blockquote>Participants only get rewarded if their referrals complete the airdrop.</blockquote>"""

    self.podtxt = """Welcome to Podium 🏆
You can check here the top succesful referrers of this airdrop. Staying at top always gets you something.

👑 <b>Top referrers : </b> ( demo )

1. UserA - 1023 referrals 
2. Airdev - 501 referrals
3. UserB - 703 referrals 

etc.. upto 10

<b><u>Updated</u></b> : {} ( UTC+0 )

<blockquote>
Shows top 10 succesful referrers. Allocating some extra rewards to top referrers can boost the airdrop [ Referral competition ].
</blockquote>"""

    self.stattxt = """<b>Statistics :</b>

🚀 Airdrop running : {}
👾 Participants : {}

🚹 User : {}
⭐ Referrals : {}
🌟Confirmed Referrals : {}
🎖Referral rank : {}

💠Telegram : {}
🐦 Twitter : {}
👛 Waller : {}

Please contact support for assistance"""

    self.tasktxt = """<blockquote>Tasks are a feature to ensure user engagements. You ask participants to do particular one-time or regular tasks against some tokens.

1. Send a message to Telegram group
2.  Like Twitter posts or retweet
3. Add " | Project " name.
4. Do x, y, z tasks.

Of course this features remains optional. If no tasks, " No new tasks " will be shown. All telegram and some twitter actions can be auto-verified.</blockquote>"""

    self.admintxt = """🧰 <b>Welcome to Administration panel.</b>

<blockquote>The buttons are only for bot admins and should normally be used with extreme care.</blockquote>
<blockquote>Bot admins are generally predefined. You can anyhow add admins to the bot.</blockquote>
 
<b>You can :</b>

📣 Broadcast : Make announcement.
📁 Export Data : Export all user data.
🔍 User query : Check user, take action.
🛑 Stop Airdrop : Pause/stop the bot. 

Try out the buttons to learn more!
"""
    self.bcasttxt = """Broadcast gives you wings - BlueBull🦋

<blockquote>Broadcast is an effective and one of the compulsary features of airdrop bot. It let's you connect to the  airdrop participants, give them updates on the airdrop or your project. Nice way to promote, no?</blockquote>

Please don't abuse this feature.  Don't send broadcasts too frequently. User may mark the bot spam and block it. <tg-spoiler>( As spam mails,  you see )</tg-spoiler>

<blockquote>All forms of messages are supported ( Text,  image, video etc.)</blockquote>

Press /cancel to close and return or
Please send or forward the message you want to broadcast :
"""

    self.bcprog ="""<b>>>>Sending message :</b> 
 
✅ Sent : {}
❎ Blocked : {}
 
👾 Completed : {}%  
 
You can track the progression of the broadcast function."""

    self.guidetxt = """Here's some context and explanations of columns. You can do of course some basic sortings to get the table you want.


<b>id :</b> unique telegram id of participant 
<b>referredby :</b>  telegram id of participant's referrer. Blank if is not referred 
<b>username :</b>  telegram username of participant. Blank if doesn't have any 
<b>twitter :</b>  participant's submitted twitter handle. 'skipped' if was skipped.   
<b>wallet :</b>  participant's submitted wallet adresse. 'skipped' if was skipped. 
<b>balance :</b>  total balance of the participant. 
<b>isbanned :</b>  'Y' if participant is banned, blank if not 
<b>referrals :</b>  number of users referred by the participant;   
<b>step :</b>  tracks participant's status.  

    
<blockquote>🔹Step 1 - user is at telegram task 
🔹Step 2 - user has passed telegram task and now at twitter task.
🔹Step 3 means user passed telegram & twitter. Now at wallet submit. 
🔹Step 4 - user at captcha challenge 
🔹Step5 - user successfully completed the airdrop and good for distribution.</blockquote>
 
<blockquote>step >= 10 are only for admins. Doesn't concern the airdrop.</blockquote>"""

    self.sensitive_txt = """User : {}

Twitter : {}
Wallet : {}
Balance: {}

<b>Use the buttons if you want to:</b>

🛑 Ban : Ban a user permenantely.
❎ Unban : Unban a banned user.
👑 Add Admins : Give admin rights.
⛔️ Remove Admins : Revoke admin."""

    self.bantxt = """<b>Please read the details before confirming :</b>

* Bans are permement but
* You can unban user.s anytime 
* User must be a participant.
* You may indicate a motif of ban
* Press /cancel to close and return"""

    self.unbantxt = """<b>Please read the details before confirming :</b>

* User to unban must be banned. 
* User must be a participant.
* You may indicate a motif of unban
* Press /cancel to close and return"""

    self.uquerytxt = """Please send telegram id of the user :

<b>User must be a participant.</b> 

* Try forwarding a message from user. 
* Try sending user's tg username. Or,
* Try sending user's twitter handle. Or,
* Try sending user's wallet adress. Or,
* Refer to bot database for id ( export )"""


def mstart():
  markup = quick_markup({
      #'Twitter': {'url': 'https://twitter.com'},
      "Let's go 🚀": {'callback_data': 'start1'}
  }, row_width=1)
  return markup

def mtg():
  markup = quick_markup({
      #'Twitter': {'url': 'https://twitter.com'},
      "✅ Validate": {'callback_data': 'tgvalid'},
      "Skip ⏩( Demo Only )": {'callback_data': 'skiptg'}
  }, row_width=1)
  return markup

def balkey():
  markup = quick_markup({
      "🔄 Refresh": {'callback_data': 'refreshbal'}
  }, row_width=1)
  return markup

def podkey():
  markup = quick_markup({
      "☘ Refresh": {'callback_data': 'refreshpod'}
  }, row_width=1)
  return markup

def refkey(uid):
  markup = quick_markup({
      'Click to share!❣': {'url': f'tg://msg?text=%0AJoin+this+airdrop+to+win+10+Cookies+🍪%0A&url=http://t.me/AirDemoXbot?start={uid}'},
  }, row_width=1)
  return markup

def sensitives():
    markup = quick_markup({
        "🛑 Ban": {'callback_data': 'ban'},
        "❎ Unban":{'callback_data': 'unban'},
        "👑 Add Admin": {'callback_data': 'addadmins'},
        "⛔️ Remove Admin": {'callback_data': 'rmadmins'},
    }, row_width=2)
    return markup

def querykey():
    markup = quick_markup({
        "✅ Confirm": {'callback_data': 'confirmb'},
        "⭕ Cancel":{'callback_data': 'cancel'},
    }, row_width=2)
    return markup

def querykey1():
    markup = quick_markup({
        "✅ Confirm": {'callback_data': 'confirmub'},
        "⭕ Cancel":{'callback_data': 'cancel'},
    }, row_width=2)
    return markup

def mainrkm():
    markup = ReplyKeyboardMarkup(resize_keyboard=True,input_field_placeholder="Cookies, cookies and cookies...") #is_persistent=True
    markup.add('🍪 My Cookies',row_width=1)
    markup.add('🌟 Referrals','🏆 Podium',row_width=2)
    markup.add('📊 Statistics','🔥 Tasks',row_width=2)
    markup.add('㊙️ Admin Panel ( Demo only )',row_width=1)
    return markup

def adminkm():
    markup = ReplyKeyboardMarkup(resize_keyboard=True,input_field_placeholder="Admin mode active..t()",one_time_keyboard=True)
    markup.add('📁 Export Data','📣  Broadcast',row_width=2)
    markup.add('🔍 User query','🛑 Stop Airdrop',row_width=2)
    markup.add('🚹 User Mode',row_width=1)
    return markup 
