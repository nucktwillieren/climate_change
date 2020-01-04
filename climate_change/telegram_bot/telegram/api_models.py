import json

class TelegramObject(object):
    def __init__(self):
        pass
    
    @classmethod
    def json_deserializer(cls,json_data):
        if not json_data and json_data == None:
            return None
        
        return cls(**json_data)

class Update(TelegramObject):
    def __init__(self, update_id=None, message=None, callback_query=None, *args, **kwargs):
        self.update_id = update_id
        if message != None:
            message['from_user'] = message.get('from') 
        self.message = Message.json_deserializer(message)  
        if callback_query != None:     
            callback_query['q_id'] = callback_query.get('id') 
            callback_query['from_user'] = callback_query.get('from')  
        self.callback_query = CallbackQuery.json_deserializer(callback_query)   

    def __str__(self):
        return str(self.__dict__)

class Message(TelegramObject):
    def __init__(self, message_id=None, from_user=None, date=None, chat=None, forward_from=None, 
    forward_from_chat=None, reply_to_message=None, text=None, forward_from_message_id=None, forward_date=None, *args, **kwargs):
        self.message_id = message_id 
        if from_user !=None:
            from_user['u_id'] = from_user.get('id')
            from_user['u_type'] = from_user.get('type')
        self.from_user = User.json_deserializer(from_user)
        self.date = int(date)
        chat['c_id'] = chat.get('id')
        chat['c_type'] = chat.get('type')
        self.chat_belong_to = Chat.json_deserializer(chat)
        if forward_from != None:
            forward_from['u_id'] = forward_from.get('id')
            forward_from['u_type'] = forward_from.get('type')
        self.forward_from_who = User.json_deserializer(forward_from)
        self.forward_from_chat = Chat.json_deserializer(forward_from_chat)
        self.forward_from_message_id = forward_from_message_id
        self.forward_date = forward_date
        self.reply_to_message = Message.json_deserializer(reply_to_message)
        #self.edit_date = int(json_data.get('edit_date'))
        self.text = text    

class Chat(TelegramObject):
    def __init__(self,c_id=None,c_type=None,title=None,username=None,first_name=None,last_name=None,deserializer=None, *args, **kwargs):
        self.id = int(c_id)
        self.type = c_type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

class User(TelegramObject):
    def __init__(self,u_id=None,is_bot=None,language_code=None,u_type=None,title=None,username=None,first_name=None,last_name=None,*args, **kwargs):
        self.id = int(u_id)
        self.is_bot = is_bot
        self.language_code = language_code
        self.type = u_type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        
class CallbackQuery(TelegramObject):
    def __init__(self, q_id=None, from_user=None, message=None, 
    inline_message_id=None, chat_instance=None, data=None, game_short_name=None, *args, **kwargs):
        self.q_id = q_id
        if from_user !=None:
            from_user['u_id'] = from_user.get('id')
            from_user['u_type'] = from_user.get('type')
        self.from_user = User.json_deserializer(from_user)
        if message != None:
            message['from_user'] = message.get('from') 
        self.message = Message.json_deserializer(message)  
        self.data = data
        self.inline_message_id = inline_message_id
        self.chat_instance = chat_instance
        self.game_short_name = game_short_name
        