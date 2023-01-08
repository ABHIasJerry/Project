# supports 55 languages

import langdetect
from langdetect import detect
from langdetect import detect_langs

# Detect languages
result_1 = detect("hello there")
print(result_1)

result_2 = detect("مرحبًا بكم")
print(result_2)

result_3 = detect("吁 汝可安好")
print(result_3)

result_4 = detect("Hallo jij daar")
print(result_4)

# Detect Confidence (0.99.... = 99 % sure)
result = detect_langs("Hallo jij daar")
print(result)


