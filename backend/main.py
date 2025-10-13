from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
from dcm_analyzer import DCMAnalyzer
import os

app = FastAPI(title='Shwedtreid Backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

DATA_CSV = os.path.join(os.path.dirname(__file__), 'sample_data', 'btc_usdt_1m.csv')
analyzer = DCMAnalyzer(window=5, min_prominence=0.0, repetition_strength=0.5)

@app.get('/api/ohlcv')
def get_ohlcv(limit: int = 500):
    if not os.path.exists(DATA_CSV):
        raise HTTPException(status_code=404, detail='Data CSV not found')
    df = pd.read_csv(DATA_CSV, parse_dates=['timestamp'])
    df = df.sort_values('timestamp').tail(limit)
    return df.to_dict(orient='records')

@app.get('/api/analyze')
def analyze(limit: int = 500):
    if not os.path.exists(DATA_CSV):
        raise HTTPException(status_code=404, detail='Data CSV not found')
    df = pd.read_csv(DATA_CSV, parse_dates=['timestamp']).sort_values('timestamp').tail(limit).reset_index(drop=True)
    results = analyzer.compute_dcm(df)
    return {'signals': results['signals'], 'marks': results['marks']}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
