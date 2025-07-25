import asyncio
import websockets
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import re
import sys
import threading
import random

# --- Country name mapping ---
COUNTRY_NAMES = {
    "AW": "Aruba",
    "AF": "Afghanistan",
    "AO": "Angola",
    "AI": "Anguilla",
    "AX": "Åland Islands",
    "AL": "Albania",
    "AD": "Andorra",
    "AE": "United Arab Emirates",
    "AR": "Argentina",
    "AM": "Armenia",
    "AS": "American Samoa",
    "AQ": "Antarctica",
    "TF": "French Southern Territories",
    "AG": "Antigua and Barbuda",
    "AU": "Australia",
    "AT": "Austria",
    "AZ": "Azerbaijan",
    "BI": "Burundi",
    "BE": "Belgium",
    "BJ": "Benin",
    "BQ": "Bonaire, Sint Eustatius and Saba",  
    "BF": "Burkina Faso",
    "BD": "Bangladesh",
    "BG": "Bulgaria",
    "BH": "Bahrain",
    "BS": "Bahamas",
    "BA": "Bosnia and Herzegovina",
    "BL": "Saint Barthélemy",
    "BY": "Belarus",
    "BZ": "Belize",
    "BM": "Bermuda",
    "BO": "Bolivia, Plurinational State of",
    "BR": "Brazil",
    "BB": "Barbados",
    "BN": "Brunei Darussalam",
    "BT": "Bhutan",
    "BV": "Bouvet Island",
    "BW": "Botswana",
    "CF": "Central African Republic",
    "CA": "Canada",
    "CC": "Cocos (Keeling) Islands",
    "CH": "Switzerland",
    "CL": "Chile",
    "CN": "China",
    "CI": "Côte d'Ivoire",
    "CM": "Cameroon",
    "CD": "Congo, The Democratic Republic of the",
    "CG": "Congo",
    "CK": "Cook Islands",
    "CO": "Colombia",
    "KM": "Comoros",
    "CV": "Cabo Verde",
    "CR": "Costa Rica",
    "CU": "Cuba",
    "CW": "Curaçao",
    "CX": "Christmas Island",
    "KY": "Cayman Islands",
    "CY": "Cyprus",
    "CZ": "Czechia",
    "DE": "Germany",
    "DJ": "Djibouti",
    "DM": "Dominica",
    "DK": "Denmark",
    "DO": "Dominican Republic",
    "DZ": "Algeria",
    "EC": "Ecuador",
    "EG": "Egypt",
    "ER": "Eritrea",
    "EH": "Western Sahara",
    "ES": "Spain",
    "EE": "Estonia",
    "ET": "Ethiopia",
    "FI": "Finland",
    "FJ": "Fiji",
    "FK": "Falkland Islands (Malvinas)",
    "FR": "France",
    "FO": "Faroe Islands",
    "FM": "Micronesia, Federated States of",
    "GA": "Gabon",
    "GB": "United Kingdom",
    "GE": "Georgia",
    "GG": "Guernsey",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GN": "Guinea",
    "GP": "Guadeloupe",
    "GM": "Gambia",
    "GW": "Guinea-Bissau",
    "GQ": "Equatorial Guinea",
    "GR": "Greece",
    "GD": "Grenada",
    "GL": "Greenland",
    "GT": "Guatemala",
    "GF": "French Guiana",
    "GU": "Guam",
    "GY": "Guyana",
    "HK": "Hong Kong",
    "HM": "Heard Island and McDonald Islands",
    "HN": "Honduras",
    "HR": "Croatia",
    "HT": "Haiti",
    "HU": "Hungary",
    "ID": "Indonesia",
    "IM": "Isle of Man",
    "IN": "India",
    "IO": "British Indian Ocean Territory",
    "IE": "Ireland",
    "IR": "Iran, Islamic Republic of",
    "IQ": "Iraq",
    "IS": "Iceland",
    "IL": "Israel",
    "IT": "Italy",
    "JM": "Jamaica",
    "JE": "Jersey",
    "JO": "Jordan",
    "JP": "Japan",
    "KZ": "Kazakhstan",
    "KE": "Kenya",
    "KG": "Kyrgyzstan",
    "KH": "Cambodia",
    "KI": "Kiribati",
    "KN": "Saint Kitts and Nevis",
    "KR": "Korea, Republic of",
    "KW": "Kuwait",
    "LA": "Lao People's Democratic Republic",
    "LB": "Lebanon",
    "LR": "Liberia",
    "LY": "Libya",
    "LC": "Saint Lucia",
    "LI": "Liechtenstein",
    "LK": "Sri Lanka",
    "LS": "Lesotho",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "MO": "Macao",
    "MF": "Saint Martin (French part)",
    "MA": "Morocco",
    "MC": "Monaco",
    "MD": "Moldova, Republic of",
    "MG": "Madagascar",
    "MV": "Maldives",
    "MX": "Mexico",
    "MH": "Marshall Islands",
    "MK": "North Macedonia",
    "ML": "Mali",
    "MT": "Malta",
    "MM": "Myanmar",
    "ME": "Montenegro",
    "MN": "Mongolia",
    "MP": "Northern Mariana Islands",
    "MZ": "Mozambique",
    "MR": "Mauritania",
    "MS": "Montserrat",
    "MQ": "Martinique",
    "MU": "Mauritius",
    "MW": "Malawi",
    "MY": "Malaysia",
    "YT": "Mayotte",
    "NA": "Namibia",
    "NC": "New Caledonia",
    "NE": "Niger",
    "NF": "Norfolk Island",
    "NG": "Nigeria",
    "NI": "Nicaragua",
    "NU": "Niue",
    "NL": "Netherlands",
    "NO": "Norway",
    "NP": "Nepal",
    "NR": "Nauru",
    "NZ": "New Zealand",
    "OM": "Oman",
    "PK": "Pakistan",
    "PA": "Panama",
    "PN": "Pitcairn",
    "PE": "Peru",
    "PH": "Philippines",
    "PW": "Palau",
    "PG": "Papua New Guinea",
    "PL": "Poland",
    "PR": "Puerto Rico",
    "KP": "Korea, Democratic People's Republic of",
    "PT": "Portugal",
    "PY": "Paraguay",
    "PS": "Palestine, State of",
    "PF": "French Polynesia",
    "QA": "Qatar",
    "RE": "Réunion",
    "RO": "Romania",
    "RU": "Russian Federation",
    "RW": "Rwanda",
    "SA": "Saudi Arabia",
    "SD": "Sudan",
    "SN": "Senegal",
    "SG": "Singapore",
    "GS": "South Georgia and the South Sandwich Islands",
    "SH": "Saint Helena, Ascension and Tristan da Cunha",
    "SJ": "Svalbard and Jan Mayen",
    "SB": "Solomon Islands",
    "SL": "Sierra Leone",
    "SV": "El Salvador",
    "SM": "San Marino",
    "SO": "Somalia",
    "PM": "Saint Pierre and Miquelon",
    "RS": "Serbia",
    "SS": "South Sudan",
    "ST": "Sao Tome and Principe",
    "SR": "Suriname",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "SE": "Sweden",
    "SZ": "Eswatini",
    "SX": "Sint Maarten (Dutch part)",
    "SC": "Seychelles",
    "SY": "Syrian Arab Republic",
    "TC": "Turks and Caicos Islands",
    "TD": "Chad",
    "TG": "Togo",
    "TH": "Thailand",
    "TJ": "Tajikistan",
    "TK": "Tokelau",
    "TM": "Turkmenistan",
    "TL": "Timor-Leste",
    "TO": "Tonga",
    "TT": "Trinidad and Tobago",
    "TN": "Tunisia",
    "TR": "Turkey",
    "TV": "Tuvalu",
    "TW": "Taiwan, Province of China",
    "TZ": "Tanzania, United Republic of",
    "UG": "Uganda",
    "UA": "Ukraine",
    "UM": "United States Minor Outlying Islands",
    "UY": "Uruguay",
    "US": "United States",
    "UZ": "Uzbekistan",
    "VA": "Holy See (Vatican City State)",
    "VC": "Saint Vincent and the Grenadines",
    "VE": "Venezuela, Bolivarian Republic of",
    "VG": "Virgin Islands, British",
    "VI": "Virgin Islands, U.S.",
    "VN": "Viet Nam",
    "VU": "Vanuatu",
    "WF": "Wallis and Futuna",
    "WS": "Samoa",
    "YE": "Yemen",
    "ZA": "South Africa",
    "ZM": "Zambia",
    "ZW": "Zimbabwe"
}

class UserBot:
    def __init__(self, bot_id, telegram_token, ws_url, group_id):
        self.bot_id = bot_id
        self.telegram_token = telegram_token
        self.ws_url = ws_url
        self.group_id = group_id
        self.bot = telebot.TeleBot(self.telegram_token)
        self.running = False
        self.start_time = None

        # Register /start handler
        self.bot.message_handler(commands=["start"])(self.handle_start)

    def handle_start(self, message):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("📞 Contact Admin", url="https://t.me/nextblacklist"),
            InlineKeyboardButton("📢 Join Our Channel", url="https://t.me/blaclistarea")
        )
        welcome_text = (
            "👋 Hello!\n\n"
            "This bot automatically receives and forwards OTP (One-Time Password) messages in real-time.\n\n"
            "If you're a developer or service provider and want a bot that can send OTPs like this one to your users, "
            "we can build a custom solution just for you.\n\n"
            "🔧 Our team specializes in building OTP sender bots for various use cases.\n\n"
            "📢 Stay updated with our latest bots, tools, and services by joining our Telegram channel.\n\n"
            "👇 Tap a button below to get started:"
        )
        self.bot.send_message(
            chat_id=message.chat.id,
            text=welcome_text,
            reply_markup=keyboard
        )

    def get_current_time(self):
        # Returns local system time as string
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def extract_otp(self, text):
        # Match OTP patterns like 123-456 or 1234-5678 first
        match = re.search(r"\b\d{3,4}-\d{3,4}\b", text)
        if match:
            return match.group(0)
        # Then match plain 4 to 8 digit numbers
        match = re.search(r"\b\d{4,8}\b", text)
        if match:
            return match.group(0)
        return "Not Detected"

    def iso_to_flag(self, country_iso):
        if not country_iso or len(country_iso) != 2:
            return "🏳️"
        return chr(ord(country_iso[0].upper()) + 127397) + chr(ord(country_iso[1].upper()) + 127397)

    def get_country_name(self, iso_code):
        return COUNTRY_NAMES.get(iso_code.upper(), "Unknown Country")

    def send_to_telegram(self, message_data):
        try:
            message = message_data.get("message", "")
            originator = message_data.get("originator", "Unknown")
            recipient = message_data.get("recipient", "Unknown")
            country_code = message_data.get("country_iso", "").upper()
            otp_code = self.extract_otp(message)
            flag = self.iso_to_flag(country_code)
            country_name = self.get_country_name(country_code)

            # Remove "<#>" tag if present
            if message.startswith("<#>"):
                message = message.replace("<#>", "", 1).lstrip()

            keyboard = InlineKeyboardMarkup()
            keyboard.add(
                InlineKeyboardButton("👨‍💻 Bot Developer", url="https://t.me/nextblacklist")
            )

            # ✅ Islamic Quotes List
            islamic_quotes = [
                "📖 اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ — *Allah is the Light of the heavens and the earth.* (24:35)",
                "📖 فَإِنَّ مَعَ الْعُسْرِ يُسْرًا — *Indeed, with hardship [will be] ease.* (94:6)",
                "📖 إِنَّ اللَّهَ مَعَ الصَّابِرِينَ — *Indeed, Allah is with the patient.* (2:153)",
                "📖 وَمَا تَوْفِيقِي إِلَّا بِاللَّهِ — *My success is only by Allah.* (11:88)",
                "📖 وَاللَّهُ يُحِبُّ الْمُحْسِنِينَ — *And Allah loves the doers of good.* (3:134)",
                "📖 وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ — *Perhaps you hate a thing and it is good for you.* (2:216)",
                "📖 إِنَّ رَبِّي لَسَمِيعُ الدُّعَاءِ — *Indeed, my Lord is the Hearer of supplication.* (14:39)",
                "📖 وَاللَّهُ غَالِبٌ عَلَىٰ أَمْرِهِ — *And Allah is predominant over His affair.* (12:21)",
                "📖 إِنَّ رَحْمَتَ اللَّهِ قَرِيبٌ مِّنَ الْمُحْسِنِينَ — *Indeed, the mercy of Allah is near to the doers of good.* (7:56)",
                "📖 إِنَّ اللَّهَ لَا يُضِيعُ أَجْرَ الْمُحْسِنِينَ — *Indeed, Allah does not allow to be lost the reward of the doers of good.* (9:120)",
                "📖 لَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ — *Do not despair of the mercy of Allah.* (39:53)",
                "📖 إِنَّ اللَّهَ غَفُورٌ رَّحِيمٌ — *Indeed, Allah is Forgiving and Merciful.* (2:173)",
                "📖 إِنَّ رَبِّي قَرِيبٌ مُّجِيبٌ — *Indeed, my Lord is near and responsive.* (11:61)",
                "📖 وَقُل رَّبِّ زِدْنِي عِلْمًا — *And say: My Lord, increase me in knowledge.* (20:114)",
                "📖 حَسْبِيَ اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ — *Allah is sufficient for me; there is no deity except Him.* (9:129)",
                "📖 إِنَّ اللَّهَ يُحِبُّ الْمُتَوَكِّلِينَ — *Indeed, Allah loves those who rely upon Him.* (3:159)",
                "📖 أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ — *Verily, in the remembrance of Allah do hearts find rest.* (13:28)",
                "📖 وَإِذَا مَرِضْتُ فَهُوَ يَشْفِينِ — *And when I am ill, it is He who cures me.* (26:80)",
                "📖 إِنَّ مَعِيَ رَبِّي سَيَهْدِينِ — *Indeed, with me is my Lord; He will guide me.* (26:62)",
                "📖 وَهُوَ مَعَكُمْ أَيْنَ مَا كُنتُمْ — *And He is with you wherever you are.* (57:4)",
                "📖 مَا ظَنَّكُم بِرَبِّ الْعَالَمِينَ — *What do you think about the Lord of the worlds?* (37:87)",
                "📖 وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا — *Whoever fears Allah – He will make for him a way out.* (65:2)",
                "📖 وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ — *And whoever relies upon Allah – then He is sufficient for him.* (65:3)",
                "📖 وَرَحْمَتِي وَسِعَتْ كُلَّ شَيْءٍ — *And My Mercy encompasses all things.* (7:156)",
                "📖 إِنَّ اللَّهَ لَا يُخْلِفُ الْمِيعَادَ — *Indeed, Allah does not fail in His promise.* (3:9)",
                "📖 وَاصْبِرْ وَمَا صَبْرُكَ إِلَّا بِاللَّهِ — *And be patient, and your patience is not but through Allah.* (16:127)",
                "📖 إِنَّ رَبَّكَ وَاسِعُ الْمَغْفِرَةِ — *Indeed, your Lord is vast in forgiveness.* (53:32)",
                "📖 نَحْنُ أَقْرَبُ إِلَيْهِ مِنْ حَبْلِ الْوَرِيدِ — *We are closer to him than [his] jugular vein.* (50:16)",
                "📖 قُلْ إِنَّ الْهُدَىٰ هُدَى اللَّهِ — *Say: Indeed, the guidance is Allah’s guidance.* (2:120)",
                "📖 وَقُلْ جَاءَ الْحَقُّ وَزَهَقَ الْبَاطِلُ — *And say: Truth has come, and falsehood has departed.* (17:81)",
                "📖 قُلْ يَا عِبَادِيَ الَّذِينَ أَسْرَفُوا عَلَىٰ أَنفُسِهِمْ لَا تَقْنَطُوا — *Say: O My servants who have transgressed against themselves, do not despair.* (39:53)",
                "📖 إِنَّ اللَّهَ سَرِيعُ الْحِسَابِ — *Indeed, Allah is swift in account.* (3:199)",
                "📖 إِنَّمَا يُوَفَّى الصَّابِرُونَ أَجْرَهُم — *Indeed, the patient will be given their reward.* (39:10)",
                "📖 وَلَا تَهِنُوا وَلَا تَحْزَنُوا — *Do not weaken and do not grieve.* (3:139)",
                "📖 فَصَبْرٌ جَمِيلٌ — *So patience is most fitting.* (12:18)",
                "📖 فَاذْكُرُونِي أَذْكُرْكُمْ — *So remember Me; I will remember you.* (2:152)",
                "📖 وَقِيلَ لِلَّذِينَ اتَّقَوْا مَاذَا أَنزَلَ رَبُّكُمْ — *It will be said to those who feared Allah, “What has your Lord sent down?”* (16:30)",
                "📖 سَيَجْعَلُ اللَّهُ بَعْدَ عُسْرٍ يُسْرًا — *Allah will bring about ease after hardship.* (65:7)",
                "📖 وَاللَّهُ خَيْرُ الرَّازِقِينَ — *And Allah is the best of providers.* (62:11)",
                "📖 فَإِنَّكَ بِأَعْيُنِنَا — *Indeed, you are under Our watchful sight.* (52:48)",
                "📖 وَاللَّهُ عَلِيمٌ حَكِيمٌ — *And Allah is Knowing and Wise.* (9:60)",
                "📖 إِنَّ رَبَّكَ لَبِالْمِرْصَادِ — *Indeed, your Lord is in observation.* (89:14)",
                "📖 وَاللَّهُ غَنِيٌّ حَلِيمٌ — *And Allah is Free of need and Forbearing.* (2:263)",
                "📖 مَن جَاءَ بِالْحَسَنَةِ فَلَهُ خَيْرٌ مِّنْهَا — *Whoever brings a good deed will have better than it.* (27:89)",
                "📖 كُلُّ نَفْسٍ ذَائِقَةُ الْمَوْتِ — *Every soul will taste death.* (3:185)",
                "📖 إِنَّ الْآخِرَةَ هِيَ دَارُ الْقَرَارِ — *Indeed, the Hereafter is the [final] home.* (40:39)",
                "📖 لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا — *Allah does not burden a soul beyond that it can bear.* (2:286)",
                "📖 وَمَن يُؤْمِن بِاللَّهِ يَهْدِ قَلْبَهُ — *And whoever believes in Allah – He will guide his heart.* (64:11)",
                "📖 وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِّلْعَالَمِينَ — *And We have not sent you, [O Muhammad], except as a mercy to the worlds.* (21:107)",
                "📖 إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ وَالإِحْسَانِ — *Indeed, Allah commands justice and the doing of good.* (16:90)",
                "📖 وَإِذَا حُيِّيْتُم بِتَحِيَّةٍ فَحَيُّوا بِأَحْسَنَ مِنْهَا — *And when you are greeted with a greeting, greet in return with what is better.* (4:86)",
                "📖 إِنَّ اللَّهَ كَانَ عَلَيْكُمْ رَقِيبًا — *Indeed, Allah is ever, over you, an Observer.* (4:1)",
                "📖 إِنَّ اللَّهَ لَا يُغَيِّرُ مَا بِقَوْمٍ حَتَّى يُغَيِّرُوا مَا بِأَنْفُسِهِمْ — *Indeed, Allah will not change the condition of a people until they change what is in themselves.* (13:11)",
                # ... You can continue adding more in this format.
            ]

            random_quote = random.choice(islamic_quotes)

            formatted_msg = (
                f"🔐 <b>New OTP Received</b>\n\n"
                f"🕒 <b>Time:</b> <code>{self.get_current_time()}</code>\n"
                f"📱 <b>Service:</b> <code>{originator}</code>\n"
                f"📞 <b>Number:</b> <code>{recipient}</code>\n"
                f"🌍 <b>Country:</b> {flag} {country_name}\n"
                f"🔢 <b>Code:</b> <code>{otp_code}</code>\n\n"
                f"💬 <b>Full Message:</b>\n<pre>{message}</pre>\n\n"
                f"🕋 <b>Islamic Quote:</b>\n<pre>{random_quote}</pre>\n\n"
                f"👨‍💻 <i>Developed by:</i> @nextblacklist"
            )

            self.bot.send_message(
                chat_id=self.group_id,
                text=formatted_msg,
                parse_mode="HTML",
                reply_markup=keyboard
            )
            print(f"[{self.get_current_time()}] [{self.bot_id}] ✅ Message sent to Telegram group")

        except Exception as e:
            print(f"[{self.get_current_time()}] [{self.bot_id}] ⚠️ Error sending to Telegram: {str(e)}")

    async def handle_socket_protocol(self):
        while self.running:
            try:
                print(f"[{self.get_current_time()}] [{self.bot_id}] Connecting to WebSocket...")
                async with websockets.connect(self.ws_url) as websocket:
                    print(f"[{self.get_current_time()}] [{self.bot_id}] Connected successfully!")
                    init_msg = "40/livesms,"
                    await websocket.send(init_msg)
                    first_response = await websocket.recv()
                    print(f"[{self.get_current_time()}] [{self.bot_id}] First response: {first_response}")

                    while self.running:
                        try:
                            ping_msg = "3"
                            await websocket.send(ping_msg)
                            response = await websocket.recv()

                            if response.startswith("42/livesms,"):
                                json_part = response[len("42/livesms,"):]
                                data = json.loads(json_part)
                                if len(data) >= 2 and isinstance(data[1], dict):
                                    self.send_to_telegram(data[1])

                            await asyncio.sleep(1)
                        except websockets.exceptions.ConnectionClosed:
                            print(f"[{self.get_current_time()}] [{self.bot_id}] Connection closed, reconnecting...")
                            break
            except Exception as e:
                print(f"[{self.get_current_time()}] [{self.bot_id}] Error: {str(e)}. Retrying in 1 second...")
                await asyncio.sleep(1)

    def start(self):
        if self.running:
            print(f"[{self.get_current_time()}] [{self.bot_id}] Already running!")
            return
        self.running = True
        self.start_time = datetime.now()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"[{self.get_current_time()}] [{self.bot_id}] Bot started.")
        threading.Thread(target=self.bot.infinity_polling, daemon=True).start()

    def _run_loop(self):
        asyncio.run(self.handle_socket_protocol())

    def stop(self):
        if not self.running:
            print(f"[{self.get_current_time()}] [{self.bot_id}] Bot not running!")
            return
        self.running = False
        print(f"[{self.get_current_time()}] [{self.bot_id}] Bot stopped.")

    def uptime(self):
        if not self.start_time:
            return "Not running"
        delta = datetime.now() - self.start_time
        return str(delta).split('.')[0]  # HH:MM:SS

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python user_bot_template.py <bot_id> <telegram_token> <ws_url> <group_id>")
        sys.exit(1)

    bot_id = sys.argv[1]
    telegram_token = sys.argv[2]
    ws_url = sys.argv[3]
    group_id = int(sys.argv[4])

    user_bot = UserBot(bot_id, telegram_token, ws_url, group_id)
    user_bot.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
        user_bot.stop()
