valves = ['/ThePipeL/valve/x',
          '/ThePipeR/valve/x',
          '/C1V1/valve/x',
          '/C1V2/valve/x',
          '/C1V3/valve/x',
          '/C1V4/valve/x',
          '/C1V5/valve/x',
          '/C1V6/valve/x',
          '/C1V7/valve/x',
          '/C1V8/valve/x',
          '/C1V9/valve/x',
          '/C1V10/valve/x',
          '/C2V1/valve/x',
          '/C2V2/valve/x',
          '/C2V3/valve/x',
          '/C2V4/valve/x',
          '/C2V5/valve/x',
          '/C2V6/valve/x',
          '/C2V7/valve/x',
          '/C2V8/valve/x',
          #'/C2V9/valve/x',
          #'/C2V10/valve/x',
          '/C3V1/valve/x',
          '/C3V2/valve/x',
          '/C3V3/valve/x',
          '/C3V4/valve/x',
          '/C3V5/valve/x',
          '/C3V6/valve/x',
          '/C3V7/valve/x',
          '/C3V8/valve/x',
          '/C3V9/valve/x',
          '/C3V10/valve/x',
          '/A/L/valve/x', 
          '/A/R/valve/x',
          '/B/L/valve/x', 
          '/B/R/valve/x', 
          '/C/L/valve/x', 
          '/C/R/valve/x', 
          '/D/L/valve/x', 
          '/D/R/valve/x', 
]

ThePipe = {
    'instruments': ['ThePipeL', 'ThePipeR'],
    'controls': ['valve/x', 'roller/x', 'mute/x', 'tirapVert/x', 'tirapHoriz/x']
}

Tele = {
    'instruments': ['A/L', 'A/R', 'B/L', 'B/R', 'C/L', 'C/R','D/L', 'D/R'],
    'controls': ['valve/x', 'length/x', 'speed/x']
}

Choir = {
    'instruments': ['C1V1','C1V2','C1V3','C1V4','C1V5','C1V6','C1V7','C1V8','C1V9','C1V10','C2V1','C2V2','C2V3','C2V4','C2V5','C2V6','C2V7','C2V8','C3V1','C3V3','C3V3','C3V4','C3V5','C3V6','C3V7','C3V8','C3V9','C2V10'],
    'controls': ['valve/x', 'speed/x', 'dur/x', 'onoff/x', 'open/x']
}

groups =  {'ThePipe': ThePipe, 'Tele': Tele, 'Choir': Choir}

