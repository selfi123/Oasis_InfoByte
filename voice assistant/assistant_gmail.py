import speech_recognition as sr
import google.generativeai as genai
import ipaddress, requests
import os,datetime
import pyttsx3
from simplegmail import Gmail
from simplegmail.query import construct_query
from word2number import w2n
import socket,nmap,ipaddress

gmail=Gmail()
  
def reading_email(): 
  query_params={
  "unread": True,
  "labels": "important"
  }
  messages=gmail.get_messages(query=construct_query(query_params))
  for message in messages:
    print("\nTo:" +message.recipient)
    print("From: "+message.sender)
    print("Subject: "+message.subject)
    print("Date: "+ message.date)
    print("Preview: "+message.snippet)
    if message.plain:
      print("Message Body: "+ message.plain)
      with open("spams.txt","a") as f:
         if len(message.plain) < 1000:
              f.write(message.plain)

recepients=["undeadeyes12@gmail.com","abeljorlinchirayath@gmail.com","nidhinsuresh858@gmaili.com","kali123hitman@gmail.com"]

def listenemail():
  print("lisntening email contents......")
  with sr.Microphone() as source:
    audio = r.listen(source)
  try:
    text = r.recognize_google(audio)
    print(text)
    return text
     
  except sr.UnknownValueError:
    print("Sorry, I couldn't understand.")
    listenemail()

def getresponse(text):
    try:
        response = model.generate_content(f"{text}------for this make sure they look like what it is saying in it. for example if its a letter body, make sure to add newlines, paragraphs, font size, etc")
        if response and hasattr(response, 'text'):
            return response.text.replace("*", "")
        else:
            print("No valid response received from the model.")
            return "I'm sorry, I couldn't generate a response."
    except Exception as e:
        print(f"An error occurred while generating a response: {e}")
        return "I'm sorry, an error occurred while generating a response."


def send_email():
  subject,to, body="","",""
  engine.say("To whom ?")
  print("To whom ?")
  engine.runAndWait()
  
  to=listenemail()    
  if not to:
        print("No recipient recognized.")
        return
  
    
  for i in recepients:
      if to in i:
          to = i
          break
  else:
      print("\nUser not found ...\nSelect a person from the following addresses:---\n")
      for j, i in enumerate(recepients, start=1):          
          print(f"Say {i} for {j}")
          engine.say(f"Say {i} for {j}")
          engine.runAndWait()
      
      rec = listenemail()
      
      
      
      if rec == "":
          print("No recipient selected.")
          return
      rec=w2n.word_to_num(rec)
      
      try:
          rec_index=int(rec)-1
          if 0<=rec_index<len(recepients):
              to=recepients[rec_index]
          else:
              print("Invalid selection.")
              return
      except ValueError:
          print("Invalid input. Please select a valid number.")
          return
  """engine.say("who is the sender ?")
  engine.runAndWait()
  sender=listenemail()
  """
  engine.say("what should be the subject ?")
  engine.runAndWait()
  subject=listenemail()
  engine.say("give me the content sir ")
  engine.runAndWait()
  body=listenemail()
  if "generate" in body:
    body=getresponse(body)
  else:
    body=body
  print(body)  
  send_params={
    "to": to,
    "sender": "abelselfi12@gmail.com",
    "subject": subject,
    "msg_html": body,
    "signature": True
  }
  messge=gmail.send_message(**send_params)
  engine.say("email has been sent sir ")
  engine.runAndWait()  

engine = pyttsx3.init()
engine.setProperty('rate', 125)  
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  

genai.configure(api_key=os.getenv('API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

r = sr.Recognizer()

def listen():
  """Listens for user input and responds with generated text."""
  print("Listening...")
  with sr.Microphone() as source:
    audio = r.listen(source)

  try:
    text = r.recognize_google(audio)
    print("You said:", text)
    if "date" in text:
      engine.say(datetime.date.today())
      engine.runAndWait()
    elif text=="stop":
      exit()
    elif text=="get my spam mails":
      reading_email()
    elif text=="send an email":

      send_email()

    elif "current temperature" in text or "weather data" in text:
       aa=get_weather_data()
       engine.say(f"{aa} degree celcius")
       engine.runAndWait()
    elif "devices connected" in text or "machines in the same network" in text:
       ip_range=get_ip_range()
       devices=scan_network1(ip_range)
       print_devices(devices)
    else:
     speak(text)

  except sr.UnknownValueError:
    print("Sorry, I couldn't understand.")

def speak(text):
  """Generates response from the model and speaks it."""
  response = model.generate_content(text)
  print(response.text.replace("*",""))
  engine.say(response.text.replace("*",""))
  engine.runAndWait()
 

def get_location_by_ip():
    response = requests.get('https://ipinfo.io')
    data = response.json()
    return data

def get_weather_data():
    location_info = get_location_by_ip()
    ip = location_info.get('ip')
    response1 = requests.get(f'https://ipapi.co/{ip}/json/').json()
    city=response1.get('city')

    if city:
        weather_response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key=ee93cd962bca4c249f7152750240307&q={city}&days=7")
        weather_data = weather_response.json()
        temperature = weather_data['current']['temp_c']
        return temperature
    else:
        return None

def scan_network1(target_ip):
    nm=nmap.PortScanner()
    nm.scan(hosts=target_ip,arguments='-sn')

    devices = []
    for host in nm.all_hosts():
        devices.append({'ip':host,'hostname':get_hostname(host)})

    return devices

def get_hostname(ip_address):
    try:
        hostname, _, _=socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return "Unable to resolve hostname"

def get_ip_range():
    local_ip=socket.gethostbyname(socket.gethostname())
    ip_network=ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
    
    return str(ip_network.network_address)+"/24"

def print_devices(devices):
    print("IP Address        | Hostname")
    print("------------------|-----------------------------")
    for device in devices:
        print(f"{device['ip']:17}|{device['hostname']}")
while True:
  listen()


  

