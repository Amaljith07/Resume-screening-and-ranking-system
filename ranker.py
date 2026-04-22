def rank_candidate(similarity_score, skill_match_percent):
    """
    Combines similarity and skill match into final score
    """
    final_score = (0.7 * similarity_score) + (0.3 * skill_match_percent)
    return round(final_score * 100, 2)
