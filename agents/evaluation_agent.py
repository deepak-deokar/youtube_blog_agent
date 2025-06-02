# agents/evaluation_agent.py

from rouge_score import rouge_scorer

# IMPROVEMENT: Evaluation agent → computes ROUGE scores

def evaluate_summary(generated_summary: str, reference_summary: str) -> dict:
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_summary, generated_summary)

    # Convert to dict for easy logging
    results = {
        "rouge1_f": scores['rouge1'].fmeasure,
        "rouge2_f": scores['rouge2'].fmeasure,
        "rougeL_f": scores['rougeL'].fmeasure
    }

    print(f"[EVAL] ROUGE scores: {results}")
    return results