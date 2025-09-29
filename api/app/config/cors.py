from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    origins = [
        "http://localhost:5173", 
        "https://case-monks.com",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,    
        allow_credentials=True,
        allow_methods=["*"],   
        allow_headers=["*"],           
    )
