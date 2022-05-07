from PIL import Image, ImageDraw
import random

def main():
    numClusters = 8
    list_for_centroids = []
    img = Image.open('test5.jpg')
    data = img.load()
    imgPix = []

    width = img.size[0]
    height = img.size[1]
    for x in range(width):
        imgPix.append([])
        for y in range(height):
            imgPix[x].append([data[x, y][0], data[x, y][1], data[x, y][2], 100])
            list_for_centroids.append([data[x, y][0], data[x, y][1], data[x, y][2]])
    list_centroids = random.sample(list_for_centroids, numClusters)

    c1 = 0
    while True:
        pixels_with_class = calculate_min_distance(list_centroids, imgPix, numClusters, width, height)
        old_centroids = list_centroids.copy()
        list_centroids = move_centroids(pixels_with_class, list_centroids, numClusters, width, height)
        flag = distance_difference(list_centroids, old_centroids)
        if not flag:
            break
        c1 += 1
        print(c1)
    convert_colors(pixels_with_class, list_centroids, width, height, img)
    print('Сжатое изображение готово!')

    return img

def convert_colors(pixels_with_class, list_centroids, width, height, img):
    draw = ImageDraw.Draw(img)
    for i in range(len(list_centroids)):
        for x in range(width):
            for y in range(height):
                if pixels_with_class[x][y][3] == i:
                    pixels_with_class[x][y][0] = list_centroids[i][0]
                    pixels_with_class[x][y][1] = list_centroids[i][1]
                    pixels_with_class[x][y][2] = list_centroids[i][2]
    for x in range(width):
        for y in range(height):
            draw.point((x, y), (pixels_with_class[x][y][0], pixels_with_class[x][y][1], pixels_with_class[x][y][2]))
    img.save("result.jpg", "JPEG")
    print(*list_centroids, sep='\n')

def distance_difference(list_centroids, old_centroids):
    distance = []
    for i in range(len(list_centroids)):
        distance.append(0)
        distance[i] = ((list_centroids[i][0] - old_centroids[i][0])**2 + \
                       (list_centroids[i][1] - old_centroids[i][1])**2 + \
                       (list_centroids[i][2] - old_centroids[i][2])**2)**(0.5)
    for i in range(len(distance)):
        if distance[i] > 2:
            return True
    return False

def move_centroids(pixels_with_class, list_centroids, numClusters, width, height):
    for i in range(numClusters):
        sum = [0, 0, 0]
        count = 0
        for x in range(width):
            for y in range(height):
                if pixels_with_class[x][y][3] == i:
                    sum[0] += pixels_with_class[x][y][0]
                    sum[1] += pixels_with_class[x][y][1]
                    sum[2] += pixels_with_class[x][y][2]
                    count += 1
        list_centroids[i] = [int(sum[0] / count), int(sum[1] / count), int(sum[2] / count)]
        print('.')
    return list_centroids

def distance(list_centroids, imgPix, numClusters):
    sum_list = []
    for i in range(numClusters):
        sum = 0
        for j in range(3):
            sum += (list_centroids[i][j] - imgPix[j])**2
        sum**(0.5)
        sum_list.append(sum)
    return sum_list.index(min(sum_list))

def calculate_min_distance(list_centroids, imgPix, numClusters, width, height):
    sum_list = []
    for x in range(width):
        for y in range(height):
            imgPix[x][y][3] = distance(list_centroids, imgPix[x][y], numClusters)
    return imgPix

if __name__ == '__main__':
    img = main()

