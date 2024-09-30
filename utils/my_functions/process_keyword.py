def process_keyword(splited_sentence, pos_result):
    keyword = []
    # 키워드 배열 생성 위해 특정 부분 후처리
    for test_word in splited_sentence:
        temp_word = ''
        temp_word_arr = []
        temp_pos_arr = []
        while temp_word != test_word:
            pop_word, pop_pos = pos_result.pop(0)
            temp_word += pop_word
            temp_word_arr.append(pop_word)
            temp_pos_arr.append(pop_pos)

        result_words = []
        i = 0
        while i < len(temp_pos_arr):
            # 1. Determiner + Noun 패턴 결합
            if temp_pos_arr[i] == 'Determiner' and i < len(temp_pos_arr) - 1 and temp_pos_arr[i + 1] == 'Noun':
                combined_word = temp_word_arr[i] + temp_word_arr[i + 1]  # Determiner와 Noun 결합
                result_words.append(combined_word)
                i += 2  # 결합 후 다음 인덱스로 넘어감
            # 2. Adverb + Noun 패턴 결합
            elif temp_pos_arr[i] == 'Adverb' and i < len(temp_pos_arr) - 1 and temp_pos_arr[i + 1] == 'Noun':
                combined_word = temp_word_arr[i] + temp_word_arr[i + 1]  # Adverb와 Noun 결합
                result_words.append(combined_word)
                i += 2  # 결합 후 다음 인덱스로 넘어감
            # 3. Noun + Any POS + Noun 패턴 결합
            elif i < len(temp_pos_arr) - 2 and temp_pos_arr[i] == 'Noun' and temp_pos_arr[i + 2] == 'Noun':
                combined_word = temp_word_arr[i] + temp_word_arr[i + 1] + temp_word_arr[i + 2]  # Noun, Unknown, Noun 결합
                result_words.append(combined_word)
                i += 3  # 결합 후 다음 인덱스로 넘어감
            # 4. 붙어있는 Noun 결합
            elif temp_pos_arr[i] == 'Noun':
                combined_word = temp_word_arr[i]
                i += 1
                while i < len(temp_pos_arr) and temp_pos_arr[i] == 'Noun':
                    combined_word += temp_word_arr[i]  # 붙어있는 Noun 결합
                    i += 1
                result_words.append(combined_word)
            # 5. 그 외 (Josa, Adverb 등)는 그냥 건너뛰기
            else:
                i += 1
        # keyword 배열 확장
        keyword.extend(result_words)

    return keyword
