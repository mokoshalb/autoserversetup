#!/usr/bin/env python3

import paramiko
from paramiko_expect import SSHClientInteraction
from time import sleep

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def main():
    try:
        print("Starting Ops")
        ip, username, password = "", " ", ""
        file = open('serverlist.txt', 'r')
        lines = file.readlines()
        count = 1
        # Strips the newline character
        for line in lines:
            if count == 1:
                ip = line.strip()
            if count == 2:
                username = line.strip()
            if count == 3:
                password = line.strip()
                PROMPT = ".*\$\s+"
                ROOT_PROMPT = ".*\#\s+"
                print("Processing for IP: {} - Username: {} - Password: {}".format(ip, username, password))
                client.connect(ip, port=22, username=username, password=password, timeout=30)
                t = paramiko.Transport((ip, 22)) 
                t.connect(username=username, password=password)
                sftp = paramiko.SFTPClient.from_transport(t)
                sftp.put("sshd_config", "/home/ubuntu/sshd_config")
                sftp.close()
                t.close()
                with SSHClientInteraction(client, display=True) as interact:
                    interact.expect(PROMPT)
                    interact.send("sudo su")
                    interact.expect(ROOT_PROMPT)
                    interact.send("whoami")
                    interact.expect(ROOT_PROMPT)
                    interact.send("sudo passwd root")
                    interact.expect([PROMPT, 'Enter new UNIX password: '])
                    interact.send("AMudar321")
                    interact.expect([PROMPT, 'Retype new UNIX password: '])
                    interact.send("AMudar321")
                    interact.expect(ROOT_PROMPT)
                    interact.send("mv /home/ubuntu/sshd_config /etc/ssh/")
                    interact.expect(ROOT_PROMPT)
                    interact.send("sudo reboot")
                    interact.expect()
                    print("Root configuration done, rebooting server...")
                    sleep(30)
                print("Restarting server...")
                client.close()
                sleep(5)
                print("Getting server hostname...")
                client.connect(ip, port=22, username="root", password="AMudar321", timeout=30)
                stdin, stdout, stderr = client.exec_command("sudo hostname")
                hostname = str(stdout.read().decode('utf-8')).strip()
                print("Server hostname is", hostname)
                print("Installing dependencies...")
                with SSHClientInteraction(client, display=True) as interact:
                    interact.expect(ROOT_PROMPT)
                    interact.send("apt-get update")
                    interact.expect(ROOT_PROMPT)
                    interact.send("dpkg --configure -a")
                    interact.expect(ROOT_PROMPT)
                    interact.send("apt-get dist-upgrade -y")
                    interact.expect(ROOT_PROMPT)
                    interact.send("echo "+hostname+".vps.ovh.net > /etc/hostname")
                    interact.expect(ROOT_PROMPT)
                    interact.send("echo "+hostname+".vps.ovh.net > /proc/sys/kernel/hostname")
                    interact.expect(ROOT_PROMPT)
                    interact.send("apt-get install -y software-properties-common")
                    interact.expect(ROOT_PROMPT)
                    interact.send("add-apt-repository ppa:ondrej/php -y")
                    interact.expect(ROOT_PROMPT)
                    interact.send("apt-get update -y")
                    interact.expect(ROOT_PROMPT)
                    interact.send("echo 'postfix postfix/mailname string "+hostname+".vps.ovh.net' | debconf-set-selections")
                    interact.expect(ROOT_PROMPT)
                    interact.send("echo 'postfix postfix/main_mailer_type string \"Internet Site\"' | debconf-set-selections")
                    interact.expect(ROOT_PROMPT)
                    interact.send("apt-get install -y nano apache2 php7.2 libapache2-mod-php7.2 php7.2-cli php7.2-mysql php7.2-gd php7.2-imagick php7.2-tidy php7.2-xmlrpc php7.2-common php7.2-xml php7.2-curl php7.2-dev php7.2-imap php7.2-mbstring php7.2-opcache php7.2-soap php7.2-zip php7.2-intl toilet unzip curl postfix --allow-unauthenticated --assume-yes")
                    interact.expect(ROOT_PROMPT)
                    interact.send("toilet --filter metal 'Banco New' > /etc/motd")
                    interact.expect(ROOT_PROMPT)
                    interact.send("ufw disable")
                    interact.expect(ROOT_PROMPT)
                    interact.send("apt-get install sendmail -y")
                    interact.expect(ROOT_PROMPT)
                    interact.send("sudo reboot")
                    interact.expect()
                client.close()
                print("Install complete, final reboot")
                count = 0
                print("Completed "+ip+" server configuration.\n")
            count += 1
    finally:
        print("\n\nEOF")

if __name__ == "__main__":
    main()