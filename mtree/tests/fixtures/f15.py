from mtree.tests.fixtures.generator import ADD, REMOVE, QUERY
"""
actions = '15a15r15a15r'
dimensions = 5
remove_chance = 0.1
"""

DIMENSIONS = 5

def PERFORM(callback):
	callback(ADD((68, 54, 52, 82, 34), QUERY((32, 53, 94, 73, 84), 39.37195082926823, 6)))
	callback(ADD((34, 42, 65, 58, 13), QUERY((52, 1, 61, 42, 16), 38.97509990195208, 1)))
	callback(ADD((17, 51, 60, 83, 10), QUERY((34, 19, 1, 7, 45), 37.98805885598537, 1)))
	callback(ADD((80, 73, 27, 52, 65), QUERY((3, 16, 60, 92, 74), 21.529068104382468, 5)))
	callback(ADD((3, 58, 3, 28, 53), QUERY((30, 49, 10, 36, 51), 44.96543778260048, 3)))
	callback(ADD((34, 100, 11, 92, 4), QUERY((12, 4, 68, 89, 90), 34.867852389792105, 3)))
	callback(ADD((23, 15, 10, 64, 8), QUERY((5, 96, 76, 73, 45), 69.60656895741275, 4)))
	callback(ADD((23, 14, 40, 65, 75), QUERY((98, 67, 68, 70, 23), 24.94078145225105, 7)))
	callback(ADD((93, 50, 88, 15, 67), QUERY((90, 79, 33, 93, 86), 73.18830763419675, 6)))
	callback(ADD((70, 45, 22, 85, 51), QUERY((64, 46, 89, 35, 6), 61.252484530918636, 5)))
	callback(ADD((1, 20, 53, 48, 5), QUERY((23, 17, 59, 64, 14), 4.425358588276778, 2)))
	callback(ADD((69, 56, 95, 80, 99), QUERY((45, 77, 0, 83, 95), 15.800547186006888, 18)))
	callback(ADD((93, 26, 94, 42, 16), QUERY((5, 17, 42, 64, 65), 61.920557773856004, 2)))
	callback(ADD((17, 85, 68, 21, 88), QUERY((54, 43, 92, 54, 38), 4.544013824825424, 19)))
	callback(ADD((30, 99, 43, 31, 76), QUERY((14, 17, 10, 9, 94), 67.04624733078732, 5)))
	callback(REMOVE((17, 51, 60, 83, 10), QUERY((78, 26, 55, 59, 86), 72.83777258730886, 1)))
	callback(REMOVE((30, 99, 43, 31, 76), QUERY((0, 7, 76, 32, 27), 4.784126636687347, 4)))
	callback(REMOVE((68, 54, 52, 82, 34), QUERY((28, 31, 98, 64, 79), 9.628483123632003, 8)))
	callback(REMOVE((23, 15, 10, 64, 8), QUERY((43, 65, 71, 74, 48), 23.518956606945743, 14)))
	callback(REMOVE((93, 50, 88, 15, 67), QUERY((27, 79, 38, 75, 93), 0.48157386845173455, 16)))
	callback(REMOVE((23, 14, 40, 65, 75), QUERY((35, 39, 23, 87, 6), 73.00573160288002, 7)))
	callback(REMOVE((17, 85, 68, 21, 88), QUERY((99, 24, 27, 99, 57), 18.662544867442765, 6)))
	callback(REMOVE((34, 42, 65, 58, 13), QUERY((55, 14, 68, 78, 84), 28.809831102221686, 9)))
	callback(REMOVE((3, 58, 3, 28, 53), QUERY((57, 83, 19, 47, 25), 0.6771014574632073, 9)))
	callback(REMOVE((70, 45, 22, 85, 51), QUERY((6, 87, 85, 99, 50), 34.890713067628134, 7)))
	callback(REMOVE((1, 20, 53, 48, 5), QUERY((72, 79, 68, 31, 42), 58.514537270634875, 4)))
	callback(REMOVE((34, 100, 11, 92, 4), QUERY((45, 89, 65, 76, 97), 24.575841231378064, 7)))
	callback(REMOVE((80, 73, 27, 52, 65), QUERY((60, 9, 8, 37, 90), 36.153560402480515, 3)))
	callback(REMOVE((69, 56, 95, 80, 99), QUERY((32, 44, 21, 14, 0), 77.62066187395294, 2)))
	callback(REMOVE((93, 26, 94, 42, 16), QUERY((21, 79, 97, 64, 75), 65.00450087349434, 4)))
	callback(ADD((83, 51, 78, 58, 7), QUERY((44, 76, 77, 73, 73), 51.50021364194835, 5)))
	callback(ADD((2, 60, 1, 69, 35), QUERY((76, 2, 93, 53, 90), 79.48092170029419, 5)))
	callback(ADD((83, 30, 91, 99, 98), QUERY((23, 77, 17, 32, 89), 42.828450294636234, 6)))
	callback(ADD((79, 59, 64, 18, 84), QUERY((28, 59, 88, 65, 26), 57.851615939471685, 5)))
	callback(ADD((57, 18, 20, 61, 55), QUERY((5, 24, 76, 53, 87), 27.243439614682234, 6)))
	callback(ADD((67, 29, 83, 61, 32), QUERY((39, 74, 54, 6, 54), 44.30861182468461, 5)))
	callback(ADD((87, 82, 53, 11, 75), QUERY((8, 61, 21, 85, 61), 73.53857485200393, 9)))
	callback(ADD((66, 71, 96, 82, 58), QUERY((6, 33, 69, 61, 79), 38.30408590766575, 10)))
	callback(ADD((18, 48, 84, 82, 99), QUERY((42, 46, 49, 84, 81), 15.703603824702252, 8)))
	callback(ADD((94, 90, 97, 16, 96), QUERY((26, 65, 95, 31, 51), 0.14766567361899519, 4)))
	callback(ADD((94, 48, 63, 80, 74), QUERY((25, 60, 12, 24, 30), 49.67956952329071, 6)))
	callback(ADD((1, 30, 3, 14, 0), QUERY((85, 66, 46, 1, 12), 29.306515521460046, 3)))
	callback(ADD((93, 96, 45, 24, 6), QUERY((25, 98, 37, 46, 1), 74.97136845656291, 9)))
	callback(ADD((28, 59, 88, 91, 92), QUERY((62, 37, 85, 27, 65), 2.229458940563216, 9)))
	callback(ADD((3, 59, 56, 27, 83), QUERY((35, 34, 89, 74, 68), 74.36150469469978, 8)))
	callback(REMOVE((94, 48, 63, 80, 74), QUERY((76, 69, 39, 25, 55), 31.656995821213147, 8)))
	callback(REMOVE((18, 48, 84, 82, 99), QUERY((43, 92, 51, 74, 22), 29.828284659560865, 17)))
	callback(REMOVE((79, 59, 64, 18, 84), QUERY((29, 15, 29, 88, 36), 14.836576734008933, 14)))
	callback(REMOVE((66, 71, 96, 82, 58), QUERY((12, 90, 68, 23, 64), 5.7219850853933085, 1)))
	callback(REMOVE((93, 96, 45, 24, 6), QUERY((71, 18, 36, 89, 59), 61.07687748395416, 1)))
	callback(REMOVE((87, 82, 53, 11, 75), QUERY((85, 93, 20, 82, 94), 13.397675546522194, 2)))
	callback(REMOVE((83, 30, 91, 99, 98), QUERY((19, 14, 36, 67, 79), 29.29762681633676, 6)))
	callback(REMOVE((83, 51, 78, 58, 7), QUERY((55, 44, 96, 44, 48), 49.91587506682998, 4)))
	callback(REMOVE((57, 18, 20, 61, 55), QUERY((59, 77, 61, 66, 62), 26.898135721364476, 4)))
	callback(REMOVE((28, 59, 88, 91, 92), QUERY((43, 82, 38, 62, 37), 37.93195411781549, 1)))
	callback(REMOVE((1, 30, 3, 14, 0), QUERY((49, 27, 66, 89, 57), 57.85132704542715, 6)))
	callback(REMOVE((67, 29, 83, 61, 32), QUERY((1, 62, 80, 75, 59), 64.80313160722427, 8)))
	callback(REMOVE((2, 60, 1, 69, 35), QUERY((51, 60, 39, 32, 16), 49.06784552855234, 3)))
	callback(REMOVE((94, 90, 97, 16, 96), QUERY((64, 20, 5, 21, 42), 20.714432484109302, 4)))
	callback(REMOVE((3, 59, 56, 27, 83), QUERY((38, 27, 61, 29, 20), 79.86882793701463, 3)))
