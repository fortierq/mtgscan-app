# MTGScan app

```mermaid
  flowchart LR;
  subgraph "Browser"
    C1[Client];
    C2[Client];
    C3[Client];
  end
  subgraph "Frontend"
    F((Flask Server));
  end
  subgraph "Backend"
    W1[Celery Worker<br>using mtgscan];
    W2[Celery Worker<br>using mtgscan];
  end
  subgraph "Cloud"
    A[Azure Read OCR];
  end
  C1 <-->|Socket.IO| F;
  C2 <-->|Socket.IO| F;
  C3 <-->|Socket.IO| F;
  F <-->|RedisMQ| W1;
  F <-->|RedisMQ| W2;
  W1 <-->|API| A;
  W2 <-->|API| A;
```

---

This is a web application for [mtgscan](https://github.com/fortierq/mtgscan), to recognize Magic cards on an image.

# Installation

```
pip install -r requirements.txt  
source launch.sh
```

# Usage

Load an image or select an URL to get the decklist and an image displaying recognized cards.

# RESTful API

## Request

`GET /api/<url>`  
Get cards (JSON format) on the image given by url

<br>

Example:
```
curl -G 127.0.0.1:5000/api/https://user-images.githubusercontent.com/49362475/105632710-fa07a180-5e54-11eb-91bb-c4710ef8168f.jpeg
```

```
{
  "maindeck": {
    "Ancient Tomb": 4, 
    "Arcbound Ravager": 4, 
    "Black Lotus": 1, 
    "Chalice of the Void": 1, 
    "Chief of the Foundry": 3, 
    "Fleetwheel Cruiser": 2, 
    "Foundry Inspector": 4, 
    "Lodestone Golem": 1, 
    "Mana Crypt": 1, 
    "Mishra's Factory": 4, 
    "Mishra's Workshop": 4, 
    "Mox Emerald": 1, 
    "Mox Jet": 1, 
    "Mox Pearl": 1, 
    "Mox Ruby": 1, 
    "Mox Sapphire": 1, 
    "Mystic Forge": 1, 
    "Phyrexian Revoker": 4, 
    "Sacrifice": 1, 
    "Sol Ring": 1, 
    "Sphere of Resistance": 4, 
    "Stonecoil Serpent": 3, 
    "Strip Mine": 1, 
    "Thorn of Amethyst": 1, 
    "Tolarian Academy": 1, 
    "Traxos, Scourge of Kroog": 1, 
    "Trinisphere": 1, 
    "Walking Ballista": 5, 
    "Wasteland": 4
  }, 
  "sideboard": {
    "Crucible of Worlds": 2, 
    "Leyline of the Void": 4, 
    "Mindbreak Trap": 3, 
    "Pithing Needle": 4, 
    "Wurmcoil Engine": 2
  }
}
```
