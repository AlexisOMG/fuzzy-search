def jaro_distance(s, t):
    s_len, t_len = len(s), len(t)
    match_distance = max(s_len, t_len) // 2 - 1

    s_matches, t_matches = [False] * s_len, [False] * t_len
    matches, transpositions = 0, 0

    for i in range(s_len):
        start, end = max(0, i - match_distance), min(i + match_distance + 1, t_len)
        for j in range(start, end):
            if t_matches[j]:
                continue
            if s[i] != t[j]:
                continue
            s_matches[i] = t_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(s_len):
        if not s_matches[i]:
            continue
        while not t_matches[k]:
            k += 1
        if s[i] != t[k]:
            transpositions += 1
        k += 1

    return (matches / s_len + matches / t_len + (matches - transpositions // 2) / matches) / 3


def jaro_winkler_distance(s, t, p=0.1):
    jaro_dist = jaro_distance(s, t)

    if jaro_dist > 0.0:
        prefix = 0
        for i in range(min(len(s), len(t))):
            if s[i] == t[i]:
                prefix += 1
            else:
                break
        jaro_dist += (p * prefix * (1 - jaro_dist))

    return jaro_dist


# Example usage:
s = "Алексей"
t = "Алкесей"

distance = jaro_winkler_distance(s, t)
print(f"Jaro-Winkler distance: {distance}")
