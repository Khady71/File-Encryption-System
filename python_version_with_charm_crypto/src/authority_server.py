from contextlib import asynccontextmanager
from fastapi import FastAPI
from pathlib import Path
import pickle
from ibe_utils import IBEEncryption
from charm.toolbox.pairinggroup import serialize, deserialize, PairingGroup
import json
import base64


# Global variables
_ibe = None
_P = None
_P_pub = None
_s = None
SETUP_FILE = Path("ibe_state.json")
_GROUP = PairingGroup('SS512')

def initialize_ibe():
    """Initialize IBE system (runs once)"""
    global _ibe, _P, _P_pub, _s
    
    _ibe = IBEEncryption('SS512')
    
    if SETUP_FILE.exists():
        try:
            with open(SETUP_FILE, 'r') as f:
                pub_params = json.load(f)
                  
                _P = _ibe.group.deserialize(bytes.fromhex(pub_params['P']))
                _P_pub = _ibe.group.deserialize(bytes.fromhex(pub_params['P_pub']))
                _s = _ibe.group.deserialize(bytes.fromhex(pub_params['s']))

                _ibe.P = _P
                _ibe.P_pub = _P_pub
                _ibe.s = _s
                _ibe.initialized = True


                print("Existing IBE state loaded ")
                return
        except Exception as e:
            print(f"Error loading state: {e}")
            print("Will generate new parameters...")
            SETUP_FILE.unlink()
    
    print("Generating new IBE parameters...")
    _P, _P_pub, _s = _ibe.setup()
    

    # Save state for next time
    try:
        with open(SETUP_FILE, 'w') as f:
            json.dump({
                'P': _ibe.group.serialize(_P).hex(),
                'P_pub': _ibe.group.serialize(_P_pub).hex(),
                's': _ibe.group.serialize(_s).hex(),
                'version': '1.0'
            }, f, indent=2)
        print(f"IBE state saved to {SETUP_FILE}")
    except Exception as e:
        print(f"Warning: Could not save public parameters: {e}")


    

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialise ibe server
    initialize_ibe()
    yield
    # reset ibe_server


app = FastAPI(lifespan=lifespan)


@app.get("/setup")
def get_public_params():
    global _ibe,_P, _P_pub
    return {
        "P" : _ibe.group.serialize(_P).hex(), 
        "P_pub" : _ibe.group.serialize(_P_pub).hex()
    }


@app.get("/getPrivateKey/{email}")
def get_private_key(email: str):
    global _ibe
    # if not _ibe:
    #     initialize_ibe()
    try:
        d_id = _ibe.extract(email)
        return {
            "email": email,
            "d_id": _ibe.group.serialize(d_id).hex()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/reset")
def reset_system():
    # reset_ibe_server()
    return {"message": "System reset successfully"}




