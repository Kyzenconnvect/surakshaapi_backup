from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from deps import get_current_user
import google.generativeai as genai
import var
import models

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

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def detect_fraud(msg: str):
    prompt_parts = [
  f"Detect if this sms is possible fraud message and categorize it in any following three category. OK, Suspicious, Fraud. Message: {msg}",
]
    response = model.generate_content(prompt_parts)
    return response.text

@router.get("/sms")
async def get_all_smses():
    query = "SELECT * FROM sms ORDER BY timestamp DESC;"
    var.cur.execute(query)
    rows = var.cur.fetchall()
    return JSONResponse(jsonable_encoder(rows))

@router.post("/sms/create")
async def create_sms(userdata: models.Sms):
    tag = detect_fraud(userdata.text)
    query = "INSERT INTO sms (uid, text, smsTag, timestamp, senderNumber, senderName) VALUES (%s, %s, %s, %s, %s, %s)"
    var.cur.execute(query, (userdata.uid,
                            userdata.text,
                            tag,
                            userdata.timestamp,
                            userdata.senderNumber,
                            userdata.senderName))
    var.conn.commit()
    return "Success"


@router.put("sms/update")
async def update_sms(userdata: models.SmsUpdate, smsid: int):
    query = "UPDATE sms SET text = %s, smsTag = %s WHERE sid = %s;"
    var.cur.execute(query, (userdata.text,
                            userdata.smsTag,
                            smsid))
    var.conn.commit()
    return "Success"


@router.delete("sms/delete")
async def delete_sms(smsid: int):
    query = "DELETE FROM sms WHERE sid = %s;"
    var.cur.execute(query, (smsid,))
    var.conn.commit()
    return "Success"