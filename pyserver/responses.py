BASE_RESPONSE = {
    "status": 200,
    "content": "Hello World, I'm the Backend for Livre Mon Colis"
}

### User Area
IS_USER_CONNECTED = {
    "status": 200,
    "content": ""
}

COLIS_RESPONSE = {
  "id": "6573183120d499455eedda44",
  "weight": 0,
  "dimension": {
    "height": 0,
    "width": 0,
    "length": 0
  },
  "state": {
    "wrapped": {
      "state": False,
      "timestamp": None
    },
    "storage-arrival": {
      "state": False,
      "timestamp": None
    },
    "storage-departure": {
      "state": False,
      "timestamp": None
    },
    "delivery": {
      "state": False,
      "timestamp": None
    },
    "received": {
      "state": False,
      "timestamp": None
    }
  }
}

DELIVERY_RESPONSE = {
  "id": "",
  "name": "",
  "vehicle": {
    "id": "65731bb120d499455eedda46",
    "gps": ""
  },
  "packages": [],
  "is-working": True
}

CLIENT_RESPONSE = {
  "name": "",
  "address": "",
  "packages": []
}

VENDOR_RESPONSE = {
  "name": "",
  "collection": {},
  "packages": []
}