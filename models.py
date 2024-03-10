from pydantic import BaseModel

class SystemUser(BaseModel):
    id: int = None
    username: str = None
    email: str = None

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

class User(BaseModel):
    # addressId: int = None
    name: str
    phonenumber: str
    email: str
    gender: str
    occupation: str = None
    dob: str = None
    pwd: str


class Call(BaseModel):
    uid: int = None
    callerName: str
    callerNumber: str
    callTime: str
    callTag: str


class Sms(BaseModel):
    uid: int = None
    text: str
    smsTag: str = 'OK'
    timestamp: str = None
    senderNumber: str = None
    senderName: str = None


class Transaction(BaseModel):
    uid: int = None
    senderName: str
    senderUpi: str
    paymentApp: str
    transactionTag: str


class Address(BaseModel):
    addressline1: str
    addressline2: str
    pincode: int
    city: str
    state: str
    country: str


class Url(BaseModel):
    uid: int = None
    tag: str
    score: int


class UserUpdate(BaseModel):
    name: str
    phonenumber: str
    email: str
    gender: str
    occupation: str
    dob: str
    pwd: str


class CallUpdate(BaseModel):
    callerName: str
    callerNumber: str
    callTime: str
    callTag: str    


class SmsUpdate(BaseModel):
    text: str
    smsTag: str
    

class TransactionUpdate(BaseModel):
    senderName: str
    senderUpi: str
    paymentApp: str
    transactionTag: str


class AddressUpdate(BaseModel):
    addressline1: str
    addressline2: str
    pincode: int
    city: str
    state: str
    country: str


class UrlUpdate(BaseModel):
    tag: str
    score: int

class QrRequest(BaseModel):
    qr_data: str