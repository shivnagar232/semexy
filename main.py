import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
import threading
import json

with open('config.json', 'r') as f: DATA = json.load(f)
def getenv(var): return os.environ.get(var) or DATA.get(var, None)

bot_token = getenv("TOKEN") 
api_hash = getenv("HASH") 
api_id = getenv("ID")
gagan = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ss = getenv("STRING")
if ss is not None:
	acc = Client("myacc" ,api_id=api_id, api_hash=api_hash, session_string=ss)
	acc.start()
else: acc = None

# download status
def downstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as downread:
			txt = downread.read()
		try:
			gagan.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**\n\nBot Made with ❤️ by __**[Team SPY](https://t.me/+8UDNP64FhAU4ZTg1)**__")
			time.sleep(10)
		except:
			time.sleep(5)


# upload status
def upstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as upread:
			txt = upread.read()
		try:
			gagan.edit_message_text(message.chat.id, message.id, f"__Unrestricted__ : **{txt}**\n\nBot Made with ❤️ by __**[Team SPY](https://t.me/+8UDNP64FhAU4ZTg1)**__")
			time.sleep(10)
		except:
			time.sleep(5)


# progress writter
def progress(current, total, message, type):
	with open(f'{message.id}{type}status.txt',"w") as fileup:
		fileup.write(f"{current * 100 / total:.1f}%")


#help command

@gagan.on_message(filters.command(["help"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	gagan.send_message(message.chat.id, f"__Here is the help guide by **Team SPY**__\n{USAGE}",
	reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("Try V1 Bot", url="https://t.me/bdysplbot")]]), reply_to_message_id=message.id)



# start command
@gagan.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    caption = "👋 Hi, I am **Save Restricted Content V2** bot Made with ❤️ by __**Team SPY**__. Send **/help** to know how to use this gagan."

    inline_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Join Channel", url="https://t.me/dev_gagan"),
            InlineKeyboardButton("Try V1 Bot", url="https://t.me/bdysplbot")
        ],
        [
            InlineKeyboardButton("Visit GitHub", url="https://github.com/devgaganin")
        ]
    ])

    gagan.send_photo(
        chat_id=message.chat.id,
        photo="https://graph.org/file/5947a7392ead84d7207ce.jpg",  # Replace with the actual image URL
        caption=caption,
        reply_markup=inline_keyboard,
        reply_to_message_id=message.id
    )


@gagan.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	print(message.text)

	# joining chats
	if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:

		if acc is None:
			gagan.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
			return

		try:
			try: acc.join_chat(message.text)
			except Exception as e: 
				gagan.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
				return
			gagan.send_message(message.chat.id,"**Chat Joined**", reply_to_message_id=message.id)
		except UserAlreadyParticipant:
			gagan.send_message(message.chat.id,"**Chat alredy Joined**", reply_to_message_id=message.id)
		except InviteHashExpired:
			gagan.send_message(message.chat.id,"**Invalid Link**", reply_to_message_id=message.id)

	# getting message
	elif "https://t.me/" in message.text:

		datas = message.text.split("/")
		temp = datas[-1].replace("?single","").split("-")
		fromID = int(temp[0].strip())
		try: toID = int(temp[1].strip())
		except: toID = fromID

		for msgid in range(fromID, toID+1):

			# private
			if "https://t.me/c/" in message.text:
				chatid = int("-100" + datas[4])
				
				if acc is None:
					gagan.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
					return
				
				handle_private(message,chatid,msgid)
				# try: handle_private(message,chatid,msgid)
				# except Exception as e: gagan.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
			
			# bot
			elif "https://t.me/b/" in message.text:
				username = datas[4]
				
				if acc is None:
					gagan.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
					return
				try: handle_private(message,username,msgid)
				except Exception as e: gagan.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)

			# public
			else:
				username = datas[3]

				try: msg  = gagan.get_messages(username,msgid)
				except UsernameNotOccupied: 
					gagan.send_message(message.chat.id,f"**The username is not occupied by anyone**", reply_to_message_id=message.id)
					return

				try: gagan.copy_message(message.chat.id, msg.chat.id, msg.id,reply_to_message_id=message.id)
				except:
					if acc is None:
						gagan.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
						return
					try: handle_private(message,username,msgid)
					except Exception as e: gagan.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)

			# wait time
			time.sleep(3)


# handle private
def handle_private(message: pyrogram.types.messages_and_media.message.Message, chatid: int, msgid: int):
		msg: pyrogram.types.messages_and_media.message.Message = acc.get_messages(chatid,msgid)
		msg_type = get_message_type(msg)
	
		thumb = 'thumb.jpg'
		caption = f"{msg.caption}\n\n__Unrestricted by **[Team SPY](https://t.me/+8UDNP64FhAU4ZTg1)**__" if msg.caption else "__Unrestricted by **[Team SPY](https://t.me/+8UDNP64FhAU4ZTg1)**__"
		

		if "Text" == msg_type:
			gagan.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
			return

		smsg = gagan.send_message(message.chat.id, '__Unrestricting(D)__', reply_to_message_id=message.id)
		dosta = threading.Thread(target=lambda:downstatus(f'{message.id}downstatus.txt',smsg),daemon=True)
		dosta.start()
		file = acc.download_media(msg, progress=progress, progress_args=[message,"down"])
		os.remove(f'{message.id}downstatus.txt')

		upsta = threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',smsg),daemon=True)
		upsta.start()
		
		if "Document" == msg_type:
			gagan.send_document(message.chat.id, file, thumb=thumb, caption=caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
			

		elif "Video" == msg_type:
			gagan.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
		

		elif "Animation" == msg_type:
			gagan.send_animation(message.chat.id, file, reply_to_message_id=message.id)
			   
		elif "Sticker" == msg_type:
			gagan.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

		elif "Voice" == msg_type:
			gagan.send_voice(message.chat.id, file, caption=caption, thumb=thumb, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])

		elif "Audio" == msg_type:
			gagan.send_audio(message.chat.id, file, caption=caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])   
			

		elif "Photo" == msg_type:
			gagan.send_photo(message.chat.id, file, caption=caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)

		os.remove(file)
		if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
		gagan.delete_messages(message.chat.id,[smsg.id])


# get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
	try:
		msg.document.file_id
		return "Document"
	except: pass

	try:
		msg.video.file_id
		return "Video"
	except: pass

	try:
		msg.animation.file_id
		return "Animation"
	except: pass

	try:
		msg.sticker.file_id
		return "Sticker"
	except: pass

	try:
		msg.voice.file_id
		return "Voice"
	except: pass

	try:
		msg.audio.file_id
		return "Audio"
	except: pass

	try:
		msg.photo.file_id
		return "Photo"
	except: pass

	try:
		msg.text
		return "Text"
	except: pass

USAGE = """
**FOR PUBLIC CHATS**

__just send post/s link__

**FOR PRIVATE CHATS**

__first send invite link of the chat (unnecessary if the account of string session already member of the chat)
then send post/s link__

**FOR BOT CHATS**

__send link with '/b/', bot's username and message id, you might want to install some unofficial client to get the id like below__

```
Team SPY
https://t.me/b/botusername/4321
```

**MULTI POSTS 🔥**

__send public/private posts link as explained above with formate "from - to" to send multiple messages like below__

```
Team SPY 
Public : https://t.me/abcdef123/1001-1010
Private: https://t.me/c/123456.../101-120
```
"""



# infinty polling
gagan.run()
