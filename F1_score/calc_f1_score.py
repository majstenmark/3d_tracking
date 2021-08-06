import sys
label_file = sys.argv[1]
def read(l): return list(map(int, l.split()))

data = map(read, open(label_file, 'r').readlines())
labels = {k:v for (k, v) in data}

NOT_VISIBLE = 1
VISIBLE = 2
NOT_VISIBLE_INCORRECTLY = -NOT_VISIBLE
VISIBLE_INCORRECTLY = -VISIBLE

values = labels.values()
true_positives = values.count(VISIBLE)
false_positives = values.count(VISIBLE_INCORRECTLY)
true_negatives = values.count(NOT_VISIBLE)
false_negatives = values.count(NOT_VISIBLE_INCORRECTLY)

# precision = True positives divided by all positives
precision = true_positives/(true_positives + false_positives)
#recall = true positives divided by true positives plus false negatives
recall = true_positives/(true_positives + false_negatives)
#f1 
f1_score = 2 * (precision * recall)/(precision + recall)

print(f'Precision {precision}')
print(f'Recall {recall}')
print(f'F1 score {f1_score}')


    
    
