
from unittest.result import failfast
import torch
from eval_score import RA_score
import datasets
import numpy as np
from sklearn.metrics import confusion_matrix

detect_null_score = torch.load("detect_null_score.torch")
rating_null_score = torch.load("rating_null_score.torch")
rating_null_score2 = torch.load("rating_null_score2.torch")

detect_prediction = detect_null_score[-1,:].type(torch.int)
detect_null_score = detect_null_score[0,:]

predictions = rating_null_score[-2,:].type(torch.int)
labels = rating_null_score[-1, :].type(torch.int)

rating_non_null_score = rating_null_score[1,:]
rating_null_score = rating_null_score[0,:]
# rating_detect_prediction = (predictions > 0).type(torch.int)
# print(rating_detect_prediction)

predictions2 = rating_null_score2[-2,:].type(torch.int)
labels2 = rating_null_score2[-1, :].type(torch.int)

rating_non_null_score2 = rating_null_score2[1,:]
rating_null_score2 = rating_null_score2[0,:]

ra_metric = RA_score()
f1_metric = datasets.load_metric("f1")

ori_ra_score = ra_metric.compute(predictions= predictions, references= labels)["ra_score"]
ori_f1_score = f1_metric.compute(predictions= predictions, references= labels, average='macro')['f1']

ori_ra_score2 = ra_metric.compute(predictions= predictions2, references= labels2)["ra_score"]
ori_f1_score2 = f1_metric.compute(predictions= predictions2, references= labels2, average='macro')['f1']



# null_score = 0.9 * rating_null_score + 0.09999999999999998 * detect_null_score
# print(detect_null_score[36:36+6])
# print(rating_null_score[36:36+6])
# print(null_score[0:6])

best_ra_score = max(ori_ra_score, ori_ra_score2)
best_f1_score = max(ori_f1_score2, ori_f1_score)
best_thresh_ra = -1e3
f1_with_ra = None
best_thresh_f1 = -1e3
ra_with_f1 = None


print("Original score: ra - {}, f1 - {}".format(best_ra_score, best_f1_score))
# mask_detect1_rating0 = detect_prediction - rating_detect_prediction
# mask_detect1_rating0 = (mask_detect1_rating0 == 1)

# rating_non_null_score = ~mask_detect1_rating0 *rating_non_null_score + mask_detect1_rating0 * 4
# print(rating_non_null_score[mask_detect1_rating0])

rating_non_null_score = np.ceil((rating_non_null_score + rating_non_null_score2)/2)

for alpha in np.arange(0.0, 1.0, 0.1):
    for beta in np.arange(0.0, 1-alpha, 0.1):
        gamma = 1 - alpha -beta
        # beta = 1 - alpha
        null_score = alpha * rating_null_score + beta * rating_null_score + gamma * detect_null_score

        for threshold in np.arange(-3, 3, 0.005):
            final_predictions = (null_score < threshold).type(torch.int)*rating_non_null_score
            ra_score = ra_metric.compute(predictions= final_predictions, references= labels)["ra_score"]
            f1_score = f1_metric.compute(predictions= final_predictions, references= labels, average='macro')['f1']
            if ra_score > best_ra_score:
                best_ra_score = ra_score
                f1_with_ra = f1_score
                best_thresh_ra = [threshold, alpha, beta, gamma]
                print("New best ra: {} thresh= {} alpha= {} beta= {} gamma= {}".format(ra_score, threshold, alpha, beta, gamma))

            if f1_score > best_f1_score:
                best_f1_score = f1_score
                ra_with_f1 = ra_score
                best_thresh_f1 = [threshold, alpha, beta, gamma]
                print("New best f1: {} thresh= {} alpha= {} beta= {} gamma= {}".format(f1_score, threshold, alpha, beta, gamma))


print("Best ra = {}, f1= {} with threshold = {} || f1= {}, ra= {} with threshhold = {}".format(best_ra_score, f1_with_ra, best_thresh_ra, best_f1_score, ra_with_f1, best_thresh_f1))