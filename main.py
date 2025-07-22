import asyncio
import websockets
from datetime import datetime
import telebot
import json
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "7606577483:AAHdLrkJzvGDpt01QGRRSq4kzwURpKFYXRI"
TELEGRAM_GROUP_ID = -1002627358838  # Can be group ID or username (with @)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# WebSocket Configuration
WS_URL = "wss://ivasms.com:2087/socket.io/?token=eyJpdiI6Ild5d293UkxCeEVJK3RYeTRtUDFyT2c9PSIsInZhbHVlIjoieWZqT0d3MERVekw4ZGFTbXhaUWtpZ2hRb0xlSGUvT3kvQzJLQ2tVZVBVU211YjhuMFlmVFZXTGxaUm9UcnN3d3RPSUIrdnRLM3dVZ29lR1duelpPY3RkZUIwZk9vNXNLclFvOFBOM01wVXZWRXM2SjQvNDRNemFLWU5tL09Fa3NOR2MrY1pkYTRWbi9QOEhmU0hXd28vTFZBbTVoVzROQTF3ZS9qRVc4NzFWU2gydld5YkJQMlBCMjVEUjNhelhjUFFlc29RUjFUVjdheTUrczlxSUY0MzRlSE1XQytjMzYxUWZiaDRHVGtUK0x5elViSElLc3RCMUdMS0doV0M4MXh3SVo1MU9PR2lPeVNMelRqWU0xVDVUclR4YjdCczJEc0ZYa3BPNFNMd1M0bUFCQjl0a0JJWE8wNjBCand1aFB4NmFvRFpaemlUdFlURjhERjdzN2lFQyt6enZOVVpaSWtwZUJqekQxSlBHeXBlQmNPaExZWUxETTduOUR4KzlvVWxqYUhmWG5EWUw0RC9vQndUbU1XNXJleDNKTXdRTXJRbG04S1ZhZm0zNCtyYmp4QzUyS2VUMkNRNHpNMGkyaFppb1hyQVFPSFpzQ1ZEVTFVYXFTdi84aWJWSUN6YmF5clFhbzdiWXE2SFR4L0FoRGlZZzdDaTFGc2R1NUpVc3pLcXRiNlV0SWk5VnZXQTRPVG1sM1JBPT0iLCJtYWMiOiI0ZDI0MDEwZWVhYjM0MTQ3MjJkYzZlMjVjZTUzZTkwYjQwYjRhM2Q2MGM5MWY4YzQ3ODcyZThlMTdlZWM4ZDRkIiwidGFnIjoiIn0%3D&user=ea62eccab305a48879e7e75cbb11c033&EIO=4&transport=websocket"

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

@bot.message_handler(commands=["start"])
def handle_start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📞 Contact Admin", url="https://t.me/nextblacklist"),
        InlineKeyboardButton("📢 Join Our Channel", url="https://t.me/blaclistarea")
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=(
            "👋 Hello!\n\n"
            "This bot is built to automatically receive and forward OTP (One-Time Password) messages in real-time.\n\n"
            "If you're a developer or service provider and want a bot that can send OTPs like this one to your users, "
            "we can build a custom solution just for you.\n\n"
            "🔧 Our team specializes in building OTP sender bots for various use cases.\n\n"
            "📢 Stay updated with our latest bots, tools, and services by joining our Telegram channel.\n\n"
            "👇 Tap a button below to get started:"
        ),
        reply_markup=keyboard
    )




def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def iso_to_flag(country_iso):
    if not country_iso or len(country_iso) != 2:
        return "🏳️"
    return chr(ord(country_iso[0].upper()) + 127397) + chr(ord(country_iso[1].upper()) + 127397)

def get_country_name(iso_code):
    return COUNTRY_NAMES.get(iso_code.upper(), "Unknown Country")

def extract_otp(text):
    # First, try to match patterns with dash like 123-456 or 1234-5678
    match = re.search(r"\b\d{3,4}-\d{3,4}\b", text)
    if match:
        return match.group(0)
    
    # If not found, match plain 4 to 8 digit numbers
    match = re.search(r"\b\d{4,8}\b", text)
    if match:
        return match.group(0)
    
    return "Not Detected"

def send_to_telegram(message_data):
    try:
        message = message_data.get("message", "")
        originator = message_data.get("originator", "Unknown")
        recipient = message_data.get("recipient", "Unknown")
        country_code = message_data.get("country_iso", "").upper()
        otp_code = extract_otp(message)
        flag = iso_to_flag(country_code)
        country_name = get_country_name(country_code)

        # Remove "<#>" from beginning if present
        if message.startswith("<#>"):
            message = message.replace("<#>", "", 1).lstrip()

        # Create inline keyboard with two buttons
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            # InlineKeyboardButton("📢 Join Our Channel", url="https://t.me/blacklistarea"),
            InlineKeyboardButton("👨‍💻 Bot Developer", url="https://t.me/nextblacklist")
        )


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



        # choice random islamic quotes
        random_quote = random.choice(islamic_quotes)


        # Build the formatted message
        formatted_msg = (  
            f"🔐 <b>New OTP Received</b>\n\n"
            f"🕒 <b>Time:</b> <code>{get_current_time()}</code>\n"
            f"📱 <b>Service:</b> <code>{originator}</code>\n"
            f"📞 <b>Number:</b> <code>{recipient}</code>\n"
            f"🌍 <b>Country:</b> {flag} {country_name}\n"
            f"🔢 <b>Code:</b> <code>{otp_code}</code>\n\n"
            f"💬 <b>Full Message:</b>\n<pre>{message}</pre>\n\n"
            f"🕋 <b>Islamic Quotes:</b>\n<pre>{random_quote}</pre>\n\n"
            f"👨‍💻 <i>Developed by:</i> @nextblacklist"
        )

        # Send to Telegram
        bot.send_message(
            chat_id=TELEGRAM_GROUP_ID,
            text=formatted_msg,
            parse_mode="HTML",
            reply_markup=keyboard
        )

        print(f"[{get_current_time()}] ✅ Message sent to Telegram group")
    except Exception as e:
        print(f"[{get_current_time()}] ⚠️ Error sending to Telegram: {str(e)}")

async def handle_socket_protocol():
    while True:
        try:
            print(f"[{get_current_time()}] 🔄 Connecting to WebSocket...")
            async with websockets.connect(WS_URL) as websocket:
                print(f"[{get_current_time()}] ✅ Connected successfully!")
                
                # Step 1: Send initial handshake
                init_msg = "40/livesms,"
                print(f"[{get_current_time()}] ⬆️ Sending: {init_msg}")
                await websocket.send(init_msg)
                
                # Step 2: Wait for first response
                first_response = await websocket.recv()
                print(f"[{get_current_time()}] 📥 First response: {first_response}")
                
                # Step 3: Enter ping-pong loop
                while True:
                    try:
                        # Send ping
                        ping_msg = "3"
                        print(f"[{get_current_time()}] ⬆️ Sending ping: {ping_msg}")
                        await websocket.send(ping_msg)
                        
                        # Receive response
                        response = await websocket.recv()
                        print(f"[{get_current_time()}] 📥 Raw response: {response}")

                        # Process livesms responses
                        if response.startswith("42/livesms,"):
                            print(f"[{get_current_time()}] 🎯 Relevant response: {response}")
                            try:
                                # Extract the JSON part
                                json_part = response[len("42/livesms,"):]
                                data = json.loads(json_part)
                                
                                # The message data is the second element in the array
                                if len(data) >= 2 and isinstance(data[1], dict):
                                    message_data = data[1]
                                    send_to_telegram(message_data)
                            except Exception as e:
                                print(f"[{get_current_time()}] ⚠️ Error processing message: {str(e)}")
                        
                        await asyncio.sleep(1)

                    except websockets.exceptions.ConnectionClosed:
                        print(f"[{get_current_time()}] ❌ Connection closed during ping-pong. Reconnecting...")
                        break
                        
        except Exception as e:
            print(f"[{get_current_time()}] ⚠️ Error: {str(e)}. Retrying in 1 second...")
            await asyncio.sleep(1)

if __name__ == "__main__":
    print("Starting Socket.IO protocol handler with Telegram integration...")
    
    # Start the Telegram bot in a separate thread
    import threading
    telegram_thread = threading.Thread(target=bot.infinity_polling)
    telegram_thread.start()
    
    # Start the WebSocket client
    asyncio.get_event_loop().run_until_complete(handle_socket_protocol())
