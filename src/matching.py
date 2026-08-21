def calculate_match_score(
    name_match=False,
    email_match=False,
    phone_match=False,
    city_match=False
):
    score = 0

    if email_match:
        score += 50

    if phone_match:
        score += 50

    if name_match:
        score += 20

    if city_match:
        score += 10

    return score

score = calculate_match_score(
    name_match=True,
    email_match=True,
    phone_match=False,
    city_match=True
)

print("Match score:", score)