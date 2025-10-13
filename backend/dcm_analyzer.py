import pandas as pd

class DCMAnalyzer:
    def __init__(self, window=5, min_prominence=0.0, repetition_strength=0.5):
        self.window = window
        self.min_prominence = min_prominence
        self.repetition_strength = repetition_strength

    def compute_repetition_weight(self, df, idx):
        price = df.loc[idx, 'close']
        window = self.window
        count = 0
        for i in range(window, min(len(df)-window, idx)):
            local = df['close'].iloc[i-window:i+window+1].values
            if df['close'].iloc[i] == local.max() and price == df['close'].iloc[i]:
                count += 1
        return 1.0 + self.repetition_strength * (count / (len(df) / 100 + 1))

    def mark_points(self, df):
        marks = []
        w = self.window
        for i in range(w, len(df)-w):
            local = df['close'].iloc[i-w:i+w+1].values
            center = df['close'].iloc[i]
            ts = df['timestamp'].iloc[i].isoformat()
            if center == local.max():
                prom = center - local.min()
                if prom >= self.min_prominence:
                    weight = self.compute_repetition_weight(df, i)
                    marks.append({'ts': ts, 'type': 'peak', 'price': float(center), 'weight': float(weight)})
            if center == local.min():
                prom = local.max() - center
                if prom >= self.min_prominence:
                    weight = self.compute_repetition_weight(df, i)
                    marks.append({'ts': ts, 'type': 'trough', 'price': float(center), 'weight': float(weight)})
        return marks

    def compute_dcm(self, df):
        marks = self.mark_points(df)
        signals = []
        if marks:
            last = marks[-1]
            sig = 'buy' if last['type'] == 'trough' else 'sell'
            signals.append({'timestamp': last['ts'], 'signal': sig, 'price': last['price'], 'weight': last['weight']})
        return {'marks': marks, 'signals': signals}
