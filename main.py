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


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def iso_to_flag(country_iso):
    if not country_iso or len(country_iso) != 2:
        return "🏳️"
    return chr(ord(country_iso[0].upper()) + 127397) + chr(ord(country_iso[1].upper()) + 127397)

def get_country_name(iso_code):
    return COUNTRY_NAMES.get(iso_code.upper(), "Unknown Country")

def extract_otp(text):
    match = re.search(r"\b\d{4,8}\b", text)
    return match.group(0) if match else "Not Detected"

def send_to_telegram(message_data):
    try:
        message = message_data.get("message", "")
        originator = message_data.get("originator", "Unknown")
        recipient = message_data.get("recipient", "Unknown")
        country_code = message_data.get("country_iso", "").upper()
        otp_code = extract_otp(message)
        flag = iso_to_flag(country_code)
        country_name = get_country_name(country_code)

        # Create inline keyboard with Join Channel button
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
        InlineKeyboardButton("📢 Join Our Channel", url="https://t.me/blaclistarea")
        )

        # Your formatted message
        formatted_msg = (
        f"🔐 <b>New OTP Received</b>\n\n"
        f"🕒 <b>Time:</b> <code>{get_current_time()}</code>\n"
        f"📱 <b>Service:</b> <code>{originator}</code>\n"
        f"📞 <b>Number:</b> <code>{recipient}</code>\n"
        f"🌍 <b>Country:</b> {flag} {country_name}\n"
        f"🔢 <b>Code:</b> <code>{otp_code}</code>\n\n"
        f"💬 <b>Full Message:</b>\n<pre>{message}</pre>\n\n"
        f"👨‍💻 <i>Developed by:</i> @nextblacklist"
        )

        # Send message with inline button
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
