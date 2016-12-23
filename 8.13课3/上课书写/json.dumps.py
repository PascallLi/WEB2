import json

data = {'b': 789}
print('DATA:', repr(data))
print('repr(data)             :'), print(repr(data))
print('dumps(data)            :'), print(len(json.dumps(data)))
print('dumps(data)            :'), print(len(json.dumps(data, indent=1)))
print('dumps(data, separators):'), print(len(json.dumps(data, separators=(',', ':'))))


print(json.dumps(data, indent=1))

