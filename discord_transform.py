import sys
import json
import os
import requests
import xml.etree.ElementTree as ET

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"discord_token": ""}

CONFIG = load_config()
DISCORD_TOKEN = CONFIG.get("discord_token", "")

class DiscordAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": token, "Content-Type": "application/json"}
        self.base_url = "https://discord.com/api/v9"
    
    def get_user(self, user_id):
        url = f"{self.base_url}/users/{user_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

def create_entity(entity_type, value, properties=None):
    entity = ET.Element("Entity", {"Type": entity_type})
    value_elem = ET.SubElement(entity, "Value")
    value_elem.text = str(value)
    
    if properties:
        for key, val in properties.items():
            if val:
                prop = ET.SubElement(entity, "AdditionalFields")
                prop.set("Name", key)
                prop.set("DisplayName", key.replace("_", " ").title())
                prop.text = str(val)
    return entity

def return_results(entities):
    root = ET.Element("MaltegoMessage")
    root.set("xmlns", "https://maltego.com/schema/3.0/")
    response = ET.SubElement(root, "MaltegoTransformResponse")
    response.set("ResponseType", "Complete")
    
    message = ET.SubElement(response, "UIMessage")
    message.set("MessageType", "Inform")
    message.text = f"Найдено {len(entities)} объектов"
    
    entities_elem = ET.SubElement(response, "Entities")
    for entity in entities:
        entities_elem.append(entity)
    
    print('<?xml version="1.0" encoding="UTF-8"?>')
    print(ET.tostring(root, encoding="unicode"))

def main():
    if len(sys.argv) < 2:
        root = ET.Element("MaltegoMessage")
        response = ET.SubElement(root, "MaltegoTransformResponse")
        response.set("ResponseType", "Complete")
        message = ET.SubElement(response, "UIMessage")
        message.set("MessageType", "FatalError")
        message.text = "Не указан ID пользователя Discord"
        print(ET.tostring(root, encoding="unicode"))
        return
    
    input_value = sys.argv[1].strip()
    
    if not input_value:
        root = ET.Element("MaltegoMessage")
        response = ET.SubElement(root, "MaltegoTransformResponse")
        response.set("ResponseType", "Complete")
        message = ET.SubElement(response, "UIMessage")
        message.set("MessageType", "FatalError")
        message.text = "ID пользователя не может быть пустым"
        print(ET.tostring(root, encoding="unicode"))
        return
    
    if not DISCORD_TOKEN:
        root = ET.Element("MaltegoMessage")
        response = ET.SubElement(root, "MaltegoTransformResponse")
        response.set("ResponseType", "Complete")
        message = ET.SubElement(response, "UIMessage")
        message.set("MessageType", "FatalError")
        message.text = "Не указан Discord токен. Создайте config.json с полем discord_token"
        print(ET.tostring(root, encoding="unicode"))
        return
    
    api = DiscordAPI(DISCORD_TOKEN)
    user_data = api.get_user(input_value)
    
    if not user_data:
        root = ET.Element("MaltegoMessage")
        response = ET.SubElement(root, "MaltegoTransformResponse")
        response.set("ResponseType", "Complete")
        message = ET.SubElement(response, "UIMessage")
        message.set("MessageType", "Inform")
        message.text = f"Пользователь {input_value} не найден"
        print(ET.tostring(root, encoding="unicode"))
        return
    
    entities = []
    full_name = f"{user_data.get('username')}#{user_data.get('discriminator')}"
    
    props = {
        "discord_id": user_data.get("id"),
        "discord_username": user_data.get("username"),
        "discord_discriminator": user_data.get("discriminator"),
        "avatar_hash": user_data.get("avatar"),
        "is_bot": str(user_data.get("bot", False)),
        "profile_url": f"https://discord.com/users/{user_data.get('id')}"
    }
    
    entities.append(create_entity("maltego.Person", full_name, props))
    entities.append(create_entity("maltego.Identifier", 
        f"https://cdn.discordapp.com/avatars/{user_data.get('id')}/{user_data.get('avatar')}.png" if user_data.get("avatar") else "",
        {"type": "Avatar URL"}))
    
    return_results(entities)

if __name__ == "__main__":
    main()
