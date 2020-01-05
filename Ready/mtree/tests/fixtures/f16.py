from mtree.tests.fixtures.generator import ADD, REMOVE, QUERY
"""
actions = '16a16r16a16r'
dimensions = 2
remove_chance = 0.1
"""

DIMENSIONS = 2

def PERFORM(callback):
	callback(ADD((56, 1), QUERY((64, 81), 51.97930568373785, 1)))
	callback(ADD((87, 41), QUERY((52, 7), 30.190749870740614, 5)))
	callback(ADD((88, 28), QUERY((17, 35), 67.08029578831348, 8)))
	callback(ADD((96, 12), QUERY((68, 33), 74.63129337618862, 7)))
	callback(ADD((77, 28), QUERY((69, 19), 71.44090699195228, 2)))
	callback(ADD((85, 13), QUERY((13, 68), 49.40532609344623, 9)))
	callback(ADD((89, 19), QUERY((16, 45), 8.029243653157412, 1)))
	callback(ADD((46, 36), QUERY((53, 7), 63.75551369709334, 13)))
	callback(ADD((28, 79), QUERY((34, 21), 26.456815885225716, 7)))
	callback(ADD((17, 5), QUERY((70, 7), 54.46473535481833, 7)))
	callback(ADD((11, 46), QUERY((64, 73), 68.97573608900954, 9)))
	callback(ADD((68, 17), QUERY((14, 92), 25.839497640736255, 14)))
	callback(ADD((95, 76), QUERY((65, 2), 60.34034160799483, 8)))
	callback(ADD((51, 19), QUERY((50, 21), 60.21071456061972, 6)))
	callback(ADD((81, 11), QUERY((72, 64), 21.04820410609335, 17)))
	callback(ADD((60, 16), QUERY((78, 22), 34.206961896855105, 17)))
	callback(REMOVE((11, 46), QUERY((78, 45), 31.252374030599206, 22)))
	callback(REMOVE((28, 79), QUERY((45, 58), 68.43253328646372, 3)))
	callback(REMOVE((89, 19), QUERY((47, 63), 14.99964801938054, 9)))
	callback(REMOVE((87, 41), QUERY((67, 36), 62.19227908413332, 7)))
	callback(REMOVE((56, 1), QUERY((14, 57), 4.440807680148424, 8)))
	callback(REMOVE((51, 19), QUERY((25, 27), 7.651374923350458, 3)))
	callback(REMOVE((96, 12), QUERY((51, 3), 67.32194556967877, 15)))
	callback(REMOVE((60, 16), QUERY((54, 14), 3.837232462603879, 4)))
	callback(REMOVE((77, 28), QUERY((1, 91), 34.38605910436729, 1)))
	callback(REMOVE((68, 17), QUERY((47, 62), 18.341821615576404, 8)))
	callback(REMOVE((95, 76), QUERY((59, 74), 24.077321729856862, 11)))
	callback(REMOVE((88, 28), QUERY((92, 20), 56.955622608836656, 4)))
	callback(REMOVE((46, 36), QUERY((39, 29), 62.89158647814607, 2)))
	callback(REMOVE((81, 11), QUERY((98, 83), 18.288322424781704, 5)))
	callback(REMOVE((17, 5), QUERY((42, 92), 56.769437012179324, 2)))
	callback(REMOVE((85, 13), QUERY((26, 76), 48.28027186168586, 3)))
	callback(ADD((91, 73), QUERY((76, 40), 34.020714910648344, 5)))
	callback(ADD((39, 81), QUERY((30, 40), 29.155255079371738, 3)))
	callback(ADD((48, 58), QUERY((79, 46), 13.066598526112276, 6)))
	callback(ADD((56, 9), QUERY((37, 73), 43.30235362029393, 3)))
	callback(ADD((62, 86), QUERY((100, 53), 52.66463458846595, 4)))
	callback(ADD((68, 72), QUERY((36, 62), 49.45151195189656, 5)))
	callback(ADD((24, 35), QUERY((43, 51), 13.339453943524173, 9)))
	callback(ADD((88, 33), QUERY((63, 30), 76.58326004110971, 8)))
	callback(ADD((75, 64), QUERY((25, 3), 1.1680470754746342, 2)))
	callback(ADD((69, 56), QUERY((59, 87), 42.15278911997811, 9)))
	callback(ADD((69, 57), QUERY((92, 30), 39.627621965620534, 4)))
	callback(ADD((27, 65), QUERY((33, 88), 34.795324676392674, 4)))
	callback(ADD((45, 40), QUERY((52, 54), 65.54197829034334, 14)))
	callback(ADD((36, 57), QUERY((19, 76), 4.61911404860988, 13)))
	callback(ADD((81, 52), QUERY((83, 38), 1.2237590444023105, 15)))
	callback(ADD((83, 55), QUERY((98, 68), 74.0099200692048, 2)))
	callback(REMOVE((68, 72), QUERY((0, 97), 69.99925382725154, 22)))
	callback(REMOVE((69, 57), QUERY((33, 18), 37.627376098986545, 4)))
	callback(REMOVE((24, 35), QUERY((9, 48), 20.959028967258604, 5)))
	callback(REMOVE((75, 64), QUERY((46, 89), 5.3143035769238, 2)))
	callback(REMOVE((56, 9), QUERY((88, 52), 28.372717502810147, 13)))
	callback(REMOVE((81, 52), QUERY((79, 10), 76.63738416013686, 11)))
	callback(REMOVE((27, 65), QUERY((50, 13), 47.384165011926896, 12)))
	callback(REMOVE((62, 86), QUERY((57, 88), 39.67711841067303, 5)))
	callback(REMOVE((36, 57), QUERY((2, 58), 25.435201121891573, 2)))
	callback(REMOVE((91, 73), QUERY((83, 68), 27.478308852931708, 10)))
	callback(REMOVE((45, 40), QUERY((47, 43), 26.549629815241815, 11)))
	callback(REMOVE((88, 33), QUERY((53, 8), 27.959641649919114, 2)))
	callback(REMOVE((39, 81), QUERY((93, 49), 20.972481057234063, 4)))
	callback(REMOVE((83, 55), QUERY((100, 92), 36.24177843446844, 5)))
	callback(REMOVE((69, 56), QUERY((14, 56), 14.701304755915015, 5)))
	callback(REMOVE((48, 58), QUERY((60, 78), 40.380192469613306, 0)))