def hit_rank(hits, evidence):
    return next((i + 1 for i, h in enumerate(hits) if evidence in h["text"]), None)

def summarize(ranks, ks=(1, 3, 5)):
    n = len(ranks)
    hit = {k: sum(r is not None and r <= k for r in ranks) / n for k in ks}
    mrr = sum(1 / r for r in ranks if r) / n
    return hit, mrr
