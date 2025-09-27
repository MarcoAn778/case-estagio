from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    origins = [
        "http://localhost:5173",  # frontend local
        "https://meusite.com",    # domínio de produção
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,         # quem pode acessar
        allow_credentials=True,        # cookies e credenciais
        allow_methods=["*"],           # GET, POST, PUT, DELETE, OPTIONS...
        allow_headers=["*"],           # Headers customizados
    )
