brazilSettings = [
    'quectel.br',     # 0
    '',               # 1
    '',               # 2
    'IPv4',           # 3
    'NONE'            # 4
]

argentinaSettings = [
    'quectel.bg.std', # 0
    'quectel',        # 1
    'quectel',        # 2
    'IPv4',           # 3
    'PAP'             # 4
]

APNSettings = 'Argentina'

if APNSettings =='Brazil':
    initialFlag = brazilSettings[0:4]
if APNSettings == 'Argentina':
    initialFlag = argentinaSettings[0:4]

print(f'{initialFlag[0]}')