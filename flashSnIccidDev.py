from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime
from serial import Serial
from tqdm import tqdm
import time

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1FLPs1bO2exvXxIQzh7-y-g0N5ZuyAUcJ5MXFrJLGYAw'

SPREADSHEET_COLUMN_SN = 'B'
SPREADSHEET_COLUMN_ICCID = 'N'

PORT = 'COM15'
BAUDRATE = 115200

ser = Serial(port= PORT, baudrate= BAUDRATE, timeout= 1)
    
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('sheets', 'v4', credentials=creds)

date = datetime.now()

dateYear = date.year
dateMonth = date.month
dateDay = date.day

formatedYear = str(dateYear)[-2:]
formatedMonth = str(dateMonth).zfill(2)
formatedDay = str(dateDay).zfill(2)

#-------------------------------- Getting the last four number ---------------------------------#
def getSequenceNumber():

    getData = (service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='{}!{}2:{}99999'.format(getProductModel(ser), SPREADSHEET_COLUMN_SN, SPREADSHEET_COLUMN_SN)).execute())
    values = getData.get('values', [])
            
    lastNumber = [item[0][-4:] for item in values] # Getting the last four numbers of each data in the list
    max_number = max([int(number) for number in lastNumber]) # Converting the last string number for an int
    nextNumber = max_number + 1
    nextNumberStr = str(nextNumber).zfill(4) # Converting the last created int number for a string again

    return nextNumberStr
#-----------------------------------------------------------------------------------------------#

#------------------------------- Create the New serial Numbers ---------------------------------#
def createNewSerialNumber(serial: Serial, formatedProductModel, sequenceNumber):

    checkSerial = f'$INFO PRODUCT SERIAL_NUM\r\n'
    serial.write(checkSerial.encode(encoding='ascii', errors='ignore'))

    time.sleep(500e-10)

    checkSerialAnswer = serial.readline().decode('utf8').strip()

    if checkSerialAnswer[2:4] != 'PX':

        serialNumber = [[f"{formatedYear}"+ formatedProductModel + f"{formatedMonth}{formatedDay}{sequenceNumber}"]]
        serialNumberFormated = ', '.join([str(item[0]) for item in serialNumber])

        commandUnlock = f'$INTERNAL CONFIGS UNLOCK A4B3C2D1\r\n'
        serial.write(commandUnlock.encode(encoding='ascii', errors='ignore'))

        time.sleep(1)

        commandSerial = f'$INTERNAL MANUFACTURING SET_SERIAL_NUM {serialNumberFormated} {serialNumberFormated}\r\n'
        serial.write(commandSerial.encode(encoding= 'ascii', errors='ignore'))

        time.sleep(1)
        serial.read_all()

        spreadsheetsSerialNumber = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                                       range='{}!{}1:{}99999'.format(getProductModel(ser), SPREADSHEET_COLUMN_SN, SPREADSHEET_COLUMN_SN)).execute()['values']

        service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                                   range= '{}!{}{}'.format(getProductModel(ser), SPREADSHEET_COLUMN_SN, len(spreadsheetsSerialNumber) + 1),
                                                   valueInputOption= 'USER_ENTERED', 
                                                   body={"values": serialNumber}).execute()
        
        print(f'The Serial Number {serialNumberFormated} was successfully flashed.')
    else:
        return print(f'The product already has a serial number flashed: {checkSerialAnswer}')
#-----------------------------------------------------------------------------------------------#

#------------------------------------ Get the product model ------------------------------------#
def getProductModel(serial: Serial):
    turnOffNmeaMessages = f'$NMEA0183 SERIAL1 DISABLE ALL\r\n'
    serial.write(turnOffNmeaMessages.encode(encoding= 'ascii', errors= 'ignore'))

    time.sleep(1)

    serial.readline().decode('utf8').strip()

    time.sleep(500e-10)

    command = f'$INFO PRODUCT MODEL\r\n'
    serial.write(command.encode(encoding='ascii', errors= 'ignore'))

    time.sleep(500e-10)

    answer = serial.readline().decode('utf8').strip()

    return answer
#-----------------------------------------------------------------------------------------------#

#--------------------------------- Product Model serial codes ----------------------------------#
def formatedProductModel(productModel):
    if productModel == 'PXOEM':
        return 'PXO'
    if productModel == 'PXULT':
        return 'PXU'
    if productModel == 'PXSTD':
        return 'PXP'
    if productModel == 'PXRTK':
        return 'PXR'
#-----------------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------------#

#--------------------------------- Getting SIM Card ICCID ----------------------------------#
def getICCID(serial: Serial, timeout):
    command = f'$INFO PRODUCT SERIAL_NUM\r\n'
    serial.write(command.encode(encoding='ascii', errors='ignore'))

    time.sleep(1)
    answerSerial = serial.readline().decode('utf8').strip()
    if answerSerial[2:4] != 'PX':
        print('Fail writing the ICCID')
        return

    valid_SN_flag = False
    spreadsheetsSerialNumber = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                                                   range='{}!{}1:{}99999'.format(getProductModel(ser), SPREADSHEET_COLUMN_SN, SPREADSHEET_COLUMN_SN)).execute()['values']
    
    for ICCID_Index in range(len(spreadsheetsSerialNumber)):
        if spreadsheetsSerialNumber[ICCID_Index][0] == answerSerial:
            valid_SN_flag = True
            break
    if valid_SN_flag == False:
        print('Fail writing the ICCID')
        return

    answerICCID = 'ICCID: UNKNOWN'
    delay_s = 0
    while answerICCID == 'ICCID: UNKNOWN':
        checkICCID = f'$CELLULAR DIAGNOSTIC ICCID\r\n'
        serial.write(checkICCID.encode(encoding= 'ascii', errors= 'ignore'))

        time.sleep(1)
        answerICCID = serial.readline().decode('utf8').strip()

        if answerICCID != 'ICCID: UNKNOWN':
            formatedICCIDAnswer = [[answerICCID.split(": ")[1][:20]]]
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                                   range= '{}!{}{}'.format(getProductModel(ser), SPREADSHEET_COLUMN_ICCID, ICCID_Index + 1),
                                                   valueInputOption= 'USER_ENTERED', 
                                                   body={"values": formatedICCIDAnswer}).execute()
            print('The ICCID number {} was flashed successfuly'.format(formatedICCIDAnswer[0][0]))
            return
        delay_s += 1

        if delay_s > timeout:
            return print('FAIL')
#-----------------------------------------------------------------------------------------------#
#--------------------------------- Turn on the internet Module ----------------------------------#        
def EnableInternetModule(serial: Serial):
    turnOnBG95 = f'$CORRECTION STATE ENABLE\r\n'
    serial.write(turnOnBG95.encode(encoding= 'ascii', errors= 'ignore'))

    time.sleep(1)
    serial.readline().decode('utf8').strip()

    turnOnLBAND = f'$CORRECTION SOURCE SET LBAND\r\n'
    serial.write(turnOnLBAND.encode(encoding= 'ascii', errors= 'ignore'))

    time.sleep(3)
    serial.readline().decode('utf8').strip()
#-----------------------------------------------------------------------------------------------#

EnableInternetModule(ser)

createNewSerialNumber(ser, formatedProductModel(getProductModel(ser)), getSequenceNumber(), )

getICCID(ser, 20)

ser.close()
