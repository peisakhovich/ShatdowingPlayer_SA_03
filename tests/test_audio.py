from audio.cache import AudioCache


cache = AudioCache()


speed_1 = 0.5583333333333333
speed_2 = 0.595
speed_3 = 0.6

path_1 = cache.get_path("Hello World", "en-US-GuyNeural", speed_1)
path_2 = cache.get_path("Hello World", "en-US-GuyNeural", speed_2)
path_3 = cache.get_path("Hello World", "en-US-GuyNeural", speed_3)

print(path_1)
print(path_2)
print(path_3)

print("1 == 2:", path_1 == path_2)
print("2 == 3:", path_2 == path_3)

for speed in [
    0.1, 0.2, 0.3, 0.4,
    0.5, 0.6, 0.7, 0.8,
    0.9, 1.0, 1.1, 1.2
]:
    print(
        speed,
        cache.get_path("Hello World", "en-US-GuyNeural", speed)
    )
