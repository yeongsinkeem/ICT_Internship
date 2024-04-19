def levenshtein_distance(str1, str2):
    # 두 문자열 사이의 레벤슈타인 거리를 계산
    len_str1 = len(str1)
    len_str2 = len(str2)
    
    # 초기 행렬 생성
    dp = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]
    
    # 초기 값 설정
    for i in range(len_str1 + 1):
        dp[i][0] = i
    for j in range(len_str2 + 1):
        dp[0][j] = j
    
    # 레벤슈타인 거리 계산
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
    
    return dp[len_str1][len_str2]

def similarity_score(str1, str2):
    # 두 문자열의 유사성 점수 계산, 유사성 점수는 0 ~ 1
    max_len = max(len(str1), len(str2))
    distance = levenshtein_distance(str1, str2)
    similarity = 1 - (distance / max_len)
    return similarity

# 테스트
str1 = "유안 클리닉"
str2 = "유안 의원"

str1 = ''.join(str1.split())
str2 = ''.join(str2.split())
similarity = similarity_score(str1, str2)
print(f"두 문자열 '{str1}'과 '{str2}'의 유사성 점수: {similarity}")
