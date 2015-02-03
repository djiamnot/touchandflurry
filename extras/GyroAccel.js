loadedInterfaceName = "Gyroscope & Accelerator";

interfaceOrientation = "portrait";

pages = [
  [
    {
      "name": "refresh",
      "type": "Button",
      "bounds": [.6, .9, .2, .1],
      "startingValue": 0,
      "isLocal": true,
      "mode": "contact",
      "ontouchstart": "interfaceManager.refreshInterface()",
      "stroke": "#aaa",
      "label": "refrsh",
    },
    {
      "name": "tabButton",
      "type": "Button",
      "bounds": [.8, .9, .2, .1],
      "mode": "toggle",
      "stroke": "#aaa",
      "isLocal": true,
      "ontouchstart": "if(this.value == this.max) { control.showToolbar(); } else { control.hideToolbar(); }",
      "label": "menu",
    },
    {
      "name":"pitch",
      "type":"Knob",
      "x":0, "y":0,
      "width":.25, "height":.25,
      "adress", "/pitch"
    },
    {
      "name":"roll",
      "type":"Knob",
      "x":0, "y":0,
      "width":.25, "height":.25,
      "adress", "/roll"
    },
    {
      "name":"yaw",
      "type":"Knob",
      "x":0, "y":0,
      "width":.25, "height":.25,
      "adress", "/yaw"
    },
    {
      "name": "gyro",
      "type": "Gyro",
      "updateRate":50,
      "min": 0,
      "max": 1,
    },
    {
      "name": "acc",
      "type": "Accelerometer",
      "updateRate":50,
      "min": 0,
      "max": 1,
    },
  ]

];
