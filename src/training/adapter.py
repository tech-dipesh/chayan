import numpy as np

from src.config import root

path = root / "data" / "adapter.npy"

def load_adapter(): return np.load(path) if path.exists() else None

def mrr(w, x, d, y):
    scores = (x @ w.T) @ d.T
    rank = (scores > scores[np.arange(len(y)), y][:, None]).sum(1) + 1
    return float((1 / rank).mean())

def fit(x, d, y, steps=300, lr=1e-3, lam=1e-3, tau=0.05):
    cut = int(len(x) * 0.8)
    xt, yt, xv, yv = x[:cut], y[:cut], x[cut:], y[cut:]
    eye = np.eye(x.shape[1], dtype="float32")
    w, m, v = eye.copy(), np.zeros_like(eye), np.zeros_like(eye)
    best, top = w, mrr(w, xv, d, yv)
    print(f"val mrr before: {top:.3f}")
    for t in range(1, steps + 1):
        logits = (xt @ w.T) @ d.T / tau
        p = np.exp(logits - logits.max(1, keepdims=True))
        p /= p.sum(1, keepdims=True)
        p[np.arange(cut), yt] -= 1
        grad = ((p / cut / tau) @ d).T @ xt + 2 * lam * (w - eye)
        m = 0.9 * m + 0.1 * grad
        v = 0.999 * v + 0.001 * grad ** 2
        w = w - lr * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
        if t % 10: continue
        score = mrr(w, xv, d, yv)
        if score > top: best, top = w.copy(), score
    print(f"val mrr after:  {top:.3f}")
    return best
