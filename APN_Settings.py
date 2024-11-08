from serial import Serial
import time

BAUDRATE = '115200'
PORT = 'COM15'

argentinaSettings = [
    'quectel.bg.std', # 0
    'quectel',        # 1
    'quectel',        # 2
    'IPv4',           # 3
    'PAP'             # 4
]

brazilSettings = [
    'quectel.br',     # 0
    '',               # 1
    '',               # 2
    'IPv4',           # 3
    'NONE'            # 4
]

ser = Serial(port = PORT, baudrate = BAUDRATE, timeout = 1)

def getICCID(serial: Serial, timeout):

    turnOffNmea = f'$NMEA0183 SERIAL1 DISABLE ALL\r\n'
    print(f'Turnig off NMEA0183 \n {turnOffNmea}')
    serial.write(turnOffNmea.encode(encoding='ascii', errors='ignore'))

    time.sleep(1.5)

    serial.readline().decode('utf8').strip()

    turnOnBG = f'$CORRECTION STATE ENABLE\r\n'
    print(f'Turning on the BG95 \n {turnOnBG}')
    serial.write(turnOnBG.encode(encoding='ascii', errors='ignore'))

    time.sleep(1.5)

    serial.readline().decode('utf8').strip()

    setLband = f'$CORRECTION SOURCE SET LBAND\r\n'
    print(f'Setting the LBand \n {setLband}')
    serial.write(setLband.encode(encoding='ascii', errors='ignore'))

    time.sleep(1.5)

    serial.readline().decode('utf8').strip()

    answerICCID = 'ICCID: UNKNOWN'
    delay_s = 0

    while answerICCID == 'ICCID: UNKNOWN':
        getIccid = f'$CELLULAR DIAGNOSTIC ICCID\r\n'
        serial.write(getIccid.encode(encoding='ascii', errors='ignore'))

        time.sleep(1)

        answerICCID = serial.readline().decode('utf8').strip()

        print(answerICCID)

        if answerICCID != 'ICCID: UNKNOWN': # Switch the '=' signal to '!'
            formatedICCIDAnswer = answerICCID.split(": ")[1][:20] # For tests, this variable is commented because the formated ICCID is forced
            #formatedICCIDAnswer = "8933201122037502443F"
            print(f'The ICCID verification was successful, value retorned -> {formatedICCIDAnswer}')
            return formatedICCIDAnswer
        delay_s += 1

        if delay_s > timeout:
            return print("Time excepted.")
        
def selectICCID(ICCIDNumber):

    fiveNumbersICCID = ICCIDNumber[:4]
    
    if fiveNumbersICCID == '8933':
        return 'Argentina'
    if fiveNumbersICCID == '8955':
        return 'Brazil'
    
def APNSettings(serial: Serial, APNSettings):

    if APNSettings == 'Argentina':
        initialFlag = argentinaSettings[0:4]
    if APNSettings =='Brazil':
        initialFlag = brazilSettings[0:4] 




    configsDefault = f'$ALL CONFIGS DEFAULT\r\n'
    serial.write(configsDefault.encode(encoding='ascii', errors='ignore'))

    time.sleep(1)

    serial.readline().decode('utf8').strip()

    nameAPN = f'$CELLULAR APN NAME 0\r\n'
    serial.write(nameAPN.encode(encoding='ascii', errors='ignore'))

    time.sleep(1)

    serial.readline().decode('utf8').strip()

    userAPN = f'$CELLULAR APN USER 0 quectel\r\n'
    serial.write(userAPN.encode(encoding='ascii', errors='ignore'))

    time.sleep(1)

    serial.readline().decode('utf8').strip()

    passwordAPN = f'$CELLULAR APN PASSWORD 0 quectel\r\n'
    serial.write(passwordAPN.encode(encoding='ascii', errors='ignore'))

    time.sleep(1)

    serial.readline().decode('utf8').strip()

    contextTypeAPN = f'$CELLULAR APN CONTEXT_TYPE 0 IPv4\r\n'
    serial.write(contextTypeAPN.encode(encoding='ascii', errors='ignore'))

    time.sleep(1)

    serial.readline().decode('utf8').strip()

    authMethodAPN = f'$CELLULAR APN AUTH_METHOD 0 PAP\r\n'
    serial.write(authMethodAPN.encode(encoding='ascii', errors='ignore'))

    time.sleep(1)

    serial.readline().decode('utf8').strip()

    configsSave = f'$CELLULAR CONFIGS SAVE\r\n'
    serial.write(configsSave.encode(encoding='ascii', errors='ignore'))

    time.sleep(1)

    serial.readline().decode('utf8').strip()

    allConfigsSave = f'$ALL CONFIGS SAVE\r\n'
    serial.write(allConfigsSave.encode(encoding='ascii', errors='ignore'))

    time.sleep(1)

    serial.readline().decode('utf8').strip()

    
def settingsAPNCountry(serial: Serial, returnCountry):

    if returnCountry == 'Argentina':
        
    

selectICCID(getICCID(ser, 15))
        




