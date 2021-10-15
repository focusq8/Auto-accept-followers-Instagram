import requests
import uuid
import time
import secrets


class App():
    def  __init__(self):
        
        
        self.username = input("USERNAME: ")
        self.password = input("PASSWORD: ")
        
        
        self.request = requests.Session()
        self.uid = uuid.uuid4()
        self.secret = secrets.token_hex(8)*2
        self.headers = {
            'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 480dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)',
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US",
            "X-IG-Capabilities": "3brTvw==",
            "X-IG-Connection-Type": "WIFI",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            'Host': 'i.instagram.com'
        }

        self.done = 0
        self.blacklist = 0
        self.check = 0
        self.false = 0
        self.error = 0
        self.lst = []
        try:

            for user in open("blacklist.txt",'r').read().splitlines():
                self.lst.append(str(user))
        except:
            pass
        self.Time_sleep = int( input("How Many Seconds Between Accept Followers Are: " ) )


    def login(self):

        url = "https://i.instagram.com/api/v1/accounts/login/"

        data = {
            '_uuid': self.uid,
            'username': self.username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{str(time.time()).split(".")[1]}:{self.password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'device_id': self.uid,
            'from_reg': 'false',
            '_csrftoken': 'missing',
            'login_attempt_count': '0'
        }

        request_login = self.request.post( url, headers=self.headers, data=data )
        
        if ("logged_in_user") in request_login.text:
            self.request.headers.update({'X-CSRFToken': str(request_login.cookies['csrftoken'])})
            self.csrftoken = request_login.cookies['csrftoken']
            print(" Loged in Done")
        elif ("\challenge") in request_login.text:
            print("Challenge Please accept it and Login again")
        else:
            print("Bad Logining")
            exit()
        self.ask_you = str( input("Do You Want To Follow Back? [y] if Yes [n] if No ===> " ) )
        print("")

    def run(self):
        self.login()
        while True:
            self.get_users()
            time.sleep(self.Time_sleep)

    def get_users(self):
        
        url = "https://i.instagram.com/api/v1/friendships/pending/"
        if self.ask_you == "y":
            try:
                Respones = self.request.get( url, headers=self.headers ).json()
                self.check += 1
                self.print()
                for user in Respones['users']:
                    self.user_id = user['pk']
                    self.user_name = user['username']
                    if self.user_name in self.lst:
                        self.ignore()
                    else:
                        self.accept()
                        self.follow_back()
                        with open("accepted.txt",'a') as file:
                            file.write(self.user_name+"\n")
            except:
                pass
        else:
                try:
                    Respones = self.request.get( url, headers=self.headers ).json()
                    self.check += 1
                    self.print()
                    for user in Respones['users']:
                        self.user_id = user['pk']
                        self.user_name = user['username']
                        if self.user_name in self.lst:
                            self.ignore()
                        else:
                            self.accept()
                            with open( "accepted.txt", 'a' ) as file:
                                file.write( self.user_name + "\n" )
                except:
                    pass


    def accept(self):

        url = f"https://i.instagram.com/api/v1/friendships/approve/{self.user_id}/"

        data = {
            "surface":"follow_requests",
            "_csrftoken":"missing",
            "user_id":self.user_id,
            "radio_type":"wifi-none",
            "_uid": "3502222789",
            "_uuid":self.uid,
        }

        Respones = self.request.post(url, headers=self.headers, data=data)
        
        if ('"status": "ok"') in Respones.text:
            self.done += 1
            self.print()

        else:
            print(Respones.json())
            self.false += 1
            self.print()

    def ignore(self):
        url = f"https://i.instagram.com/api/v1/friendships/ignore/{self.user_id}/"

        data = {
            "_csrftoken": "missing",
            "user_id": self.user_id,
            "radio_type": "wifi-none",
            "_uid": "3502222789",
            "_uuid": self.uid,
        }
        Respones = self.request.post( url, headers=self.headers, data=data )


        if ('"status": "ok"') in Respones.text:
            self.blacklist += 1
            self.print()
        else:
            print( Respones.json() )
            self.false += 1
            self.print()

    def follow_back(self):
        url = f"https://i.instagram.com/api/v1/friendships/create/{self.user_id}/"

        data = {
            "_csrftoken": "missing",
            "user_id": self.user_id,
            "radio_type": "wifi-none",
            "_uid": self.uid,
            "_uuid": self.uid,
        }

        Respones = self.request.post( url, headers=self.headers, data=data )

        if ('"status": "ok"') in Respones.text:
            pass
        else:
            self.false += 1

    def print(self):
        print(f"Done Accept : {self.done}\nFalse Accept :  {self.false}\nCheck List : {self.check}\nError : {self.error}\nblacklist : {self.blacklist}\nlist : {self.lst}")

if __name__=="__main__":
    app = App()
    app.run()