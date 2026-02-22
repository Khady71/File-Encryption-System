from fastapi import FastAPI
from ibe_utils import IBEEncryption

app = FastAPI()

# Global variables
_ibe = None
_P = None
_P_pub = None
_s = None
SETUP_FILE = Path("ibe_state.pkl")

def initialize_ibe():
    """Initialize IBE system (runs once)"""
    global _ibe, _P, _P_pub, _s
    
    
    if SETUP_FILE.exists():
        with open(SETUP_FILE, 'rb') as f:
            state = pickle.load(f)
            _ibe = state['ibe']
            _P = state['P']
            _P_pub = state['P_pub']
            _s = state['s']
        print("Loaded existing IBE state")
        return
    
    _ibe = IBEEncryption('SS512')
    _P, _P_pub, _s = _ibe.setup()
    
    # Save state for next time
    with open(SETUP_FILE, 'wb') as f:
        pickle.dump({
            'ibe': _ibe,
            'P': _P,
            'P_pub': _P_pub,
            's': _s
        }, f)
    
def extract(email):
    d_id = ibe.extract(email)


@app.get("/setup")
def setup_system():
    ibe, P, P_pub, s = setup()
    return {"ibe" : ibe, "P" : P, "P_pub" : P_pub, "s" : s}


@app.get("/getPrivateKey/{email}")
def get(email: str):
    d_id = extract(email)
    return {"d_id": d_id}

