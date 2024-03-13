from fastapi import FastAPI, UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import QrRequest
import google.generativeai as genai
import json

router = APIRouter()

genai.configure(api_key="AIzaSyCh_oxhhxHfcdkc0zStwaAAOMdXZWpDL9o")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["I am giving you extracted data from a qr code. It may contains urls or payment codes and links. You perform regex and keyword based analysis and using ML techniques according to your own database to detect if this is possible fraud and categorize it in any following two category. OK, Fraud. Your will return only a json containing a key tag with proper category tag and a key message with details of your detection. Qr data: upi://pay?pa=9163619700@paytm&pn=PaytmUser&mc=0000&mode=02&purpose=00&orgid=159761&cust=1153763655. Strictly follow the format and don't return the text saying json before the actual data. Format: {\\\"tag\\\": \\\"fraud\\\", \\\"message\\\": \\\"details\\\"}. Don't flag any gpay, paytm or phonepay payment qr as fraud."]
  },
  {
    "role": "model",
    "parts": ["{\"tag\": \"OK\", \"message\": \"No fraud detected\"}"]
  },
  {
    "role": "user",
    "parts": ["qr_data: https://payment-gatemal.way.org"]
  },
  {
    "role": "model",
    "parts": ["{\"tag\": \"fraud\", \"message\": \"Suspicious URL detected\"}"]
  },
])

@router.post("/detect_qr")
async def detect_qr(qr: QrRequest):
    data = qr.qr_data
#     prompt_parts = [
#   f"I am giving you extracted data from a qr code. It may contains urls or payment codes and links. You perform regex and keyword based analysis and using ML techniques according to your own database to detect if this is possible fraud and categorize it in any following two category. OK, Fraud. Your will return only a json containing a key tag with proper category tag and a key message with details of your detection. Qr data: {data}. Strictly follow the format and don't return the text saying json before the actual data. Format: \"tag\": \"OK\", \"message\": \"detailed message\""
# ]
    user_data = f"qr data: {data}"
    convo.send_message(user_data)
    response = convo.last.text
    json_data = json.loads(response)
    return json_data